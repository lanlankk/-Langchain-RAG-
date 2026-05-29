# 📖 RAG 对话系统 - 错误排查与解决方案手册

---

## 📋 目录

1. [环境依赖安装](#1-环境依赖安装)
2. [数据库配置与连接问题](#2-数据库配置与连接问题)
3. [后端服务启动问题](#3-后端服务启动问题)
4. [文件上传功能问题](#4-文件上传功能问题)
5. [认证与权限问题](#5-认证与权限问题)
6. [限流与性能问题](#6-限流与性能问题)
7. [嵌入模型配置问题](#7-嵌入模型配置问题)
8. [前端交互问题](#8-前端交互问题)
9. [完整启动流程](#9-完整启动流程)
10. [服务验证清单](#10-服务验证清单)

---

## 1. 环境依赖安装

### 1.1 Python 包安装

#### 问题描述
启动后端服务时提示缺少依赖包

#### 解决方案

```powershell
# 进入项目根目录
cd D:\Agent-proj\LangChain-RAG-FastAPI-Service-master\LangChain-RAG-FastAPI-Service-master

# 安装后端依赖
cd backend
uv sync

# 安装前端依赖
cd ../front
npm install

# 安装 Django 用户服务依赖
cd ../DjangoUserService
uv sync

# 额外需要安装的包（如果缺失）
pip install python-magic-bin  # 文件类型检测
pip install chromadb  # 向量数据库
pip install langchain-core langchain-chroma  # LangChain 核心库
pip install fastapi uvicorn  # FastAPI 框架
pip install pymysql  # MySQL 驱动
pip install redis  # Redis 客户端
```

### 1.2 Ollama 安装与配置

#### 问题描述
`ollama` 命令无法识别

#### 解决方案

```powershell
# 1. 下载并安装 Ollama（Windows）
# 访问：https://ollama.com/download

# 2. 添加到系统 PATH（如果安装后无法识别命令）
$ollamaPath = "C:\Program Files\Ollama"
$env:Path += ";$ollamaPath"

# 3. 启动 Ollama 服务
ollama serve

# 4. 拉取所需模型
ollama pull qwen3.5:0.8b      # 聊天模型
ollama pull qwen3-embedding:0.6b  # 嵌入模型
```

---

## 2. 数据库配置与连接问题

### 2.1 MySQL 服务未启动

#### 问题描述
```
net start mysql
服务名无效。
```

#### 解决方案

```powershell
# 方法1：查找并启动 MySQL 服务
Get-Service | Where-Object { $_.DisplayName -match 'MySQL' }
Start-Service MySQL80  # 根据实际服务名修改

# 方法2：手动启动（修改路径）
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" --console

# 方法3：使用 Docker（推荐）
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123123 mysql:8.0
```

### 2.2 Redis 服务未启动

#### 问题描述
```
redis-cli ping
Could not connect to Redis at 127.0.0.1:6379: Connection refused
```

#### 解决方案

```powershell
# 方法1：启动 Redis 服务
Start-Service Redis

# 方法2：手动启动（修改路径）
& "C:\Program Files\Redis\redis-server.exe" "C:\Program Files\Redis\redis.windows.conf"

# 方法3：使用 Docker
docker run -d -p 6379:6379 redis:7
```

### 2.3 数据库迁移失败

#### 问题描述
```
django.db.utils.OperationalError: (1824, "Failed to open the referenced table 'user_service'")
```

#### 解决方案

```powershell
# 1. 删除并重新创建数据库
mysql -u root -p123123 -e "DROP DATABASE IF EXISTS user_service; CREATE DATABASE user_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 运行迁移
cd DjangoUserService
uv run python manage.py migrate
```

### 2.4 环境变量配置错误

#### 问题描述
数据库连接失败，提示密码错误或主机不可达

#### 解决方案

**`DjangoUserService/.env` 配置示例：**
```env
JWT_SECRET_KEY=your_jwt_secret_key_here
DB_PORT=3306
DB_NAME=user_service
DB_USER=root
DB_PASSWORD=123123
DB_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_TASK_TIME_LIMIT=300
CELERY_TASK_SOFT_TIME_LIMIT=250
CELERY_RESULT_EXPIRES=3600
REDIS_CACHE_URL=redis://localhost:6379/1
```

**`backend/.env` 配置示例：**
```env
LLM_TYPE=OLLAMA
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=qwen3.5:0.8b
EMBED_MODEL_TYPE=OLLAMA
TEXT_EMBEDDING_MODEL_NAME=qwen3-embedding:0.6b
MYSQL_USER=root
MYSQL_PASSWORD=123123
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=chat_history
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DJANGO_API_URL=http://127.0.0.1:8001
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
```

---

## 3. 后端服务启动问题

### 3.1 uv 命令无法识别

#### 问题描述
```
uv : 无法将“uv”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。
```

#### 解决方案

```powershell
# 方法1：使用 python -m 方式
python -m uv run python manage.py migrate

# 方法2：激活虚拟环境后运行
& "DjangoUserService\.venv\Scripts\Activate.ps1"
uv run python manage.py migrate

# 方法3：直接使用虚拟环境的 Python
"DjangoUserService\.venv\Scripts\python.exe" manage.py migrate
```

### 3.2 libmagic 缺失

#### 问题描述
```
ImportError: failed to find libmagic. Check your installation
```

#### 解决方案

```powershell
# 安装 python-magic-bin（Windows 预编译版本）
pip install python-magic-bin==0.4.27
```

### 3.3 端口被占用

#### 问题描述
```
ERROR:    [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000):
```

#### 解决方案

```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000

# 终止进程（替换 PID）
taskkill /F /PID 12345
```

---

## 4. 文件上传功能问题

### 4.1 上传失败（401 错误）

#### 问题描述
```
HTTP异常: 401 - 请先登录或确保您的token有效
```

#### 解决方案

**前端修改**：创建全局 axios 拦截器

```javascript
// front/src/utils/axios.js
import axios from 'axios';

const instance = axios.create({
baseURL: '',
timeout: 30000,
});

instance.interceptors.request.use(
(config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
},
(error) => Promise.reject(error)
);

export default instance;
```

**后端修改**：支持多种用户ID字段

```python
# backend/app/utils/auth_utils.py
user_id: str = payload.get("user_id") or payload.get("sub") or payload.get("id")
```

### 4.2 上传失败（429 错误）

#### 问题描述
```
HTTP异常: 429 - 请求过于频繁，请稍后再试
```

#### 解决方案

```python
# backend/app/router/knowledge_router.py
@knowledge_router.post("/add/multiple/stream")
async def add_vector_multiple_stream(
    files: List[UploadFile] = File(...),
    user_id: str = Depends(get_current_user_id),
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
    _: None = Depends(rate_limit(limit=10, window=60))  # 提高限流阈值
):
```

### 4.3 文件处理错误

#### 问题描述
```
【SSE上传】处理文件时出错: 'VectorStoreService' object has no attribute 'add_vectors'
```

#### 解决方案

```python
# backend/app/router/knowledge_service.py
# 修复文件处理逻辑
for doc in docs:
    doc.metadata['user_id'] = user_id
    doc.metadata['original_filename'] = filename
    doc.metadata['md5'] = md5_hex

await asyncio.to_thread(vector_store.vectors_store.add_documents, docs)
```

---

## 5. 认证与权限问题

### 5.1 JWT Token 不匹配

#### 问题描述
前后端 `SECRET_KEY` 不一致导致 token 验证失败

#### 解决方案

确保 `backend/.env` 和 `DjangoUserService/.env` 中的密钥一致：

```env
# backend/.env
SECRET_KEY=my_secure_jwt_secret_key_12345

# DjangoUserService/.env
JWT_SECRET_KEY=my_secure_jwt_secret_key_12345
```

### 5.2 Token 过期

#### 问题描述
用户操作时提示 token 过期

#### 解决方案

```javascript
// 前端响应拦截器
instance.interceptors.response.use(
(response) => response,
(error) => {
    if (error.response?.status === 401) {
    localStorage.removeItem('jwt_token');
    window.location.href = '/login';
    }
    return Promise.reject(error);
}
);
```

---

## 6. 限流与性能问题

### 6.1 清除限流计数器

#### 问题描述
被限流后无法继续操作

#### 解决方案

```powershell
# 清除 Redis 中的限流计数器
redis-cli
127.0.0.1:6379> FLUSHDB
OK
```

---

## 7. 嵌入模型配置问题

### 7.1 阿里云模型不存在

#### 问题描述
```
阿里云嵌入调用失败: Model not exist.
```

#### 解决方案

**方案1：使用 Ollama（推荐）**

```env
# backend/.env
EMBED_MODEL_TYPE=OLLAMA
OLLAMA_BASE_URL=http://localhost:11434
TEXT_EMBEDDING_MODEL_NAME=qwen3-embedding:0.6b
```

**方案2：使用正确的阿里云模型名称**

```env
# backend/.env
EMBED_MODEL_TYPE=ALIYUN
ALIYUN_ACCESS_KEY_SECRET=your_api_key
ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
ALIYUN_EMBED_MODEL_NAME=qwen3-embedding
```

### 7.2 嵌入模型返回空结果

#### 问题描述
```
Expected Embeddings to be non-empty list or numpy array, got [] in upsert.
```

#### 解决方案

```powershell
# 确保 Ollama 服务正在运行
ollama serve

# 确保嵌入模型已下载
ollama list  # 查看已下载的模型
ollama pull qwen3-embedding:0.6b  # 如果未下载
```

---

## 8. 前端交互问题

### 8.1 登录请求失败

#### 问题描述
```
登录请求失败，请稍后再试
```

#### 解决方案

确保 Django 用户服务正在运行：

```powershell
cd DjangoUserService
uv run python manage.py runserver 8001
```

### 8.2 跨域问题

#### 问题描述
浏览器控制台显示 CORS 错误

#### 解决方案

**后端配置**：

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 9. 完整启动流程

```powershell
# 1. 启动数据库服务
Start-Service MySQL80
Start-Service Redis

# 2. 启动 Ollama（如果使用本地模型）
ollama serve

# 3. 启动 Django 用户服务
cd DjangoUserService
& ".venv\Scripts\Activate.ps1"
uv run python manage.py runserver 8001

# 4. 启动 FastAPI 后端
cd ../backend
uvicorn main:app --reload

# 5. 启动前端
cd ../front
npm run dev
```

---

## 10. 服务验证清单

| 服务 | 地址 | 状态 |
|------|------|------|
| MySQL | localhost:3306 | ✅ 运行中 |
| Redis | localhost:6379 | ✅ 运行中 |
| Ollama | localhost:11434 | ✅ 运行中（可选） |
| Django 用户服务 | http://localhost:8001 | ✅ 可访问 |
| FastAPI 后端 | http://localhost:8000/docs | ✅ 可访问 |
| 前端 | http://localhost:3000 | ✅ 可访问 |

---

## 💡 常见问题排查顺序

1. **检查数据库连接** → MySQL 和 Redis 是否启动
2. **检查服务状态** → Django 和 FastAPI 是否运行
3. **检查配置文件** → `.env` 文件是否正确配置
4. **检查日志** → 后端日志中的错误信息
5. **检查网络** → 前端请求是否到达后端
6. **检查模型** → Ollama 或阿里云 API 是否可用

---

**文档版本**: v1.0  
**创建日期**: 2026-05-22  
**适用项目**: RAGAgent - 基于LangChain和RAG的Agent智能问答系统