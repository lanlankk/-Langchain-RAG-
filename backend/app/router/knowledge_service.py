import asyncio
import time
import json
from typing import List, Optional, Dict, Any, AsyncGenerator
import uuid
import magic
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

from fastapi import HTTPException, UploadFile

from app.core.logger_handler import logger
from app.rag.vector_store import VectorStoreService
from app.rag.task_queue import TaskQueue, SliceResult
from app.utils.file_handler import get_file_md5_hex


class KnowledgeService:
    """知识库管理服务"""

    async def handle_add_vector_single(self, file: UploadFile, user_id: str) -> str:
        """处理单个文件上传"""
        vector_store = VectorStoreService()
        filename = file.filename
        temp_file_path = None

        try:
            # 保存上传的文件到临时目录
            temp_file_path = await asyncio.to_thread(
                tempfile.NamedTemporaryFile,
                delete=False,
                suffix=os.path.splitext(file.filename)[1]
            )
            content = await file.read()
            await asyncio.to_thread(temp_file_path.write, content)
            temp_file_path.close()

            # 处理文档
            await vector_store.document_processor.get_document(
                files=[temp_file_path.name],
                user_id=user_id
            )

            return filename
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path.name):
                try:
                    os.unlink(temp_file_path.name)
                except:
                    pass

    async def handle_add_vector_multiple(self, files: List[UploadFile], user_id: str) -> List[str]:
        """处理多个文件上传"""
        vector_store = VectorStoreService()
        filenames = []
        temp_file_paths = []

        try:
            # 保存上传的文件到临时目录
            for file in files:
                temp_file_path = await asyncio.to_thread(
                    tempfile.NamedTemporaryFile,
                    delete=False,
                    suffix=os.path.splitext(file.filename)[1]
                )
                content = await file.read()
                await asyncio.to_thread(temp_file_path.write, content)
                temp_file_path.close()
                temp_file_paths.append(temp_file_path.name)
                filenames.append(file.filename)

            # 处理文档
            await vector_store.document_processor.get_document(
                files=temp_file_paths,
                user_id=user_id
            )

            return filenames
        finally:
            # 清理临时文件
            for temp_file_path in temp_file_paths:
                if os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass

    async def handle_add_vector_multiple_stream(
            self,
            files: List[UploadFile],
            user_id: str
    ) -> AsyncGenerator[str, None]:

        total_files = len(files)
        success_count = 0
        failed_count = 0

        logger.info(f"【SSE上传】开始处理文件上传，文件数量: {total_files}，用户ID: {user_id}")

        # ===== start event =====
        start_data = {
            "event_type": "start",
            "total_files": total_files,
            "message": "开始处理文件...",
            "progress": 0
        }

        yield f"event: progress\ndata: {json.dumps(start_data, ensure_ascii=False)}\n\n"

        max_file_folder_size = 200 * 1024 * 1024
        total_size = 0
        files_content = []

        for file in files:
            content = await file.read()
            files_content.append({'file': file, 'content': content})
            total_size += len(content)
            await file.seek(0)

        if total_size > max_file_folder_size:
            error_data = {
                "event_type": "error",
                "message": "文件总大小不能超过200MB",
                "error_message": "文件总大小不能超过200MB"
            }

            yield f"event: progress\ndata: {json.dumps(error_data, ensure_ascii=False)}\n\n"
            return

        allowed_mime_types = {
            'application/pdf',
            'text/plain',
            'text/markdown',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        mime = magic.Magic(mime=True)

        valid_files_info = []
        current_index = 1

        for file_info in files_content:
            file = file_info['file']
            content = file_info['content']

            file_type = mime.from_buffer(content)
            file_extension = os.path.splitext(file.filename)[1].lower()
            allowed_extensions = {'.pdf', '.txt', '.md', '.pptx', '.docx'}

            if file_type not in allowed_mime_types and file_extension not in allowed_extensions:
                failed_count += 1

                error_data = {
                    "event_type": "error",
                    "file_index": current_index,
                    "total_files": total_files,
                    "filename": file.filename,
                    "step": "validation",
                    "message": f"文件 {file.filename} 类型不支持",
                    "error_message": f"文件类型: {file_type}，扩展名: {file_extension}",
                    "progress": int(current_index / total_files * 100),
                    "success_count": success_count,
                    "failed_count": failed_count
                }

                yield f"event: progress\ndata: {json.dumps(error_data, ensure_ascii=False)}\n\n"

            else:
                valid_files_info.append({
                    'content': content,
                    'filename': file.filename,
                    'file_index': current_index,
                    'file_obj': file
                })

            current_index += 1

        # ===== 实际处理文件并保存到向量数据库 =====
        vector_store = VectorStoreService()

        # 保存文件到临时目录
        temp_file_paths = []
        file_name_map = {}
        for file_info in valid_files_info:
            temp_file_path = await asyncio.to_thread(
                tempfile.NamedTemporaryFile,
                delete=False,
                suffix=os.path.splitext(file_info['filename'])[1]
            )
            await asyncio.to_thread(temp_file_path.write, file_info['content'])
            temp_file_path.close()
            temp_file_paths.append(temp_file_path.name)
            file_name_map[temp_file_path.name] = file_info['filename']

        # 处理文档（直接处理文件路径列表）
        try:
            # 遍历处理每个文件
            for idx, file_path in enumerate(temp_file_paths):
                filename = file_name_map.get(file_path, os.path.basename(file_path))

                # 检查MD5是否已存在
                md5_hex = await get_file_md5_hex(file_path)
                if await vector_store.document_processor.md5_store.check_md5_hex(md5_hex, user_id):
                    logger.info(f"【SSE上传】文件 {filename} 已存在，跳过")
                    continue

                # 加载文档
                document = await vector_store.document_processor.get_file_document(file_path)
                if not document:
                    logger.error(f"【SSE上传】文件 {filename} 加载内容为空")
                    continue

                # 分割文档
                docs = await vector_store.document_processor.spliter.split_documents(document)

                # 向量化并存储（添加用户ID到metadata）
                for doc in docs:
                    doc.metadata['user_id'] = user_id
                    doc.metadata['original_filename'] = filename
                    doc.metadata['md5'] = md5_hex

                await asyncio.to_thread(vector_store.vectors_store.add_documents, docs)

                # 保存MD5记录
                await vector_store.document_processor.md5_store.save_md5_hex(md5_hex, filename, filename, user_id)

                # 发送成功事件
                success_count += 1
                completed_data = {
                    "event_type": "completed",
                    "filename": filename,
                    "step": "completed",
                    "message": f"文件 {filename} 上传成功",
                    "progress": 100,
                    "success_count": success_count,
                    "failed_count": failed_count
                }
                yield f"event: progress\ndata: {json.dumps(completed_data, ensure_ascii=False)}\n\n"

        except Exception as e:
            logger.error(f"【SSE上传】处理文件时出错: {e}")
            # 处理失败，标记错误
            for file_path in temp_file_paths:
                filename = file_name_map.get(file_path, os.path.basename(file_path))
                failed_count += 1
                error_data = {
                    "event_type": "error",
                    "filename": filename,
                    "step": "uploading",
                    "message": f"文件 {filename} 处理失败: {str(e)}",
                    "error_message": str(e),
                    "progress": 100,
                    "success_count": success_count,
                    "failed_count": failed_count
                }
                yield f"event: progress\ndata: {json.dumps(error_data, ensure_ascii=False)}\n\n"
        finally:
            # 清理临时文件
            for temp_file_path in temp_file_paths:
                if os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass

        # ===== 完成事件 =====
        finish_data = {
            "event_type": "finish",
            "total_files": total_files,
            "success_count": success_count,
            "failed_count": failed_count,
            "message": "处理完成",
            "progress": 100
        }

        yield f"event: progress\ndata: {json.dumps(finish_data, ensure_ascii=False)}\n\n"

    async def handle_get_all_md5_records(self, user_id: str) -> List[Dict]:
        """获取用户的所有MD5记录"""
        vector_store = VectorStoreService()
        records = await vector_store.get_all_md5_records(user_id)
        return records

    async def handle_get_md5_info(self, user_id: str, md5_value: str) -> Optional[Dict]:
        """获取MD5对应的文档信息"""
        vector_store = VectorStoreService()
        info = await vector_store.get_md5_info(user_id, md5_value)
        return info

    async def handle_clear_user_md5(self, user_id: str, delete_documents: bool = True):
        """清空用户的MD5记录"""
        vector_store = VectorStoreService()
        await vector_store.clear_user_md5(user_id, delete_documents)

    async def handle_delete_single_md5(self, user_id: str, md5_value: str, delete_documents: bool = True) -> bool:
        """删除单个MD5记录"""
        vector_store = VectorStoreService()
        success = await vector_store.delete_single_md5(user_id, md5_value, delete_documents)
        return success

    async def handle_delete_by_filename(self, user_id: str, filename: str, delete_documents: bool = True) -> bool:
        """通过文件名删除"""
        vector_store = VectorStoreService()
        success = await vector_store.delete_by_filename(user_id, filename, delete_documents)
        return success

    async def handle_get_user_knowledge(self, user_id: str) -> List[Dict]:
        """获取用户的知识库文档列表"""
        vector_store = VectorStoreService()
        documents = await vector_store.get_user_documents(user_id)
        return documents

    async def handle_get_document_detail(self, user_id: str, filename: str) -> Optional[Dict]:
        """获取文档详情"""
        vector_store = VectorStoreService()
        detail = await vector_store.get_document_detail(user_id, filename)
        return detail

    async def handle_get_document_chunks(self, user_id: str, filename: str) -> List[Dict]:
        """获取文档切片"""
        vector_store = VectorStoreService()
        chunks = await vector_store.get_document_chunks(user_id, filename)
        return chunks

    async def clean_user_upload(self, user_id: str):
        """清除用户上传的所有向量"""
        vector_store = VectorStoreService()
        await vector_store.clear_user_vectors(user_id)

    def _calculate_progress(self, sliced_count: int, written_count: int, total: int) -> int:
        if total == 0:
            return 0

        slice_progress = (sliced_count / total) * 60
        write_progress = (written_count / total) * 40

        return int(min(99, slice_progress + write_progress))


def get_knowledge_service() -> KnowledgeService:
    return KnowledgeService()