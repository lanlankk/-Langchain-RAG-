# 📄 RAG对话系统 - 代码文件说明文档

---

## 📋 目录

1. [前端层 (`front/`)](#1-前端层-front)
2. [后端层 (`backend/`)](#2-后端层-backend)
3. [用户服务层 (`DjangoUserService/`)](#3-用户服务层-djangouserservice)
4. [配置与工具文件](#4-配置与工具文件)

---

## 1. 前端层 (`front/`)

### 1.1 入口文件

#### `front/main.js`
- **作用**：Vue 应用入口文件，初始化应用配置
- **核心功能**：
  - 创建 Vue 实例
  - 配置路由、状态管理
  - 导入全局样式和工具函数
- **关键技术点**：
  - 使用 `createApp` 创建应用
  - 配置 Pinia 状态管理
  - 挂载应用到 DOM

#### `front/index.html`
- **作用**：HTML 模板文件
- **核心功能**：提供应用入口的 HTML 结构
- **关键技术点**：
  - 定义根元素 `<div id="app">`
  - 引入 Vue 应用脚本

### 1.2 配置文件

#### `front/vite.config.js`
- **作用**：Vite 构建工具配置
- **核心功能**：
  - 配置开发服务器端口
  - 配置代理转发（解决跨域）
  - 配置构建输出
- **关键技术点**：
  - 代理 `/api` 请求到后端
  - 支持 Vue 单文件组件

#### `front/package.json`
- **作用**：前端依赖配置
- **核心功能**：管理项目依赖包和脚本命令
- **关键脚本**：
  - `npm run dev`：启动开发服务器
  - `npm run build`：构建生产版本

### 1.3 视图组件

#### `front/src/views/Chat.vue`
- **作用**：AI 聊天页面
- **核心功能**：
  - 展示聊天消息列表
  - 发送用户消息
  - 显示流式响应
- **关键技术点**：
  - 使用 SSE 接收流式响应
  - 管理聊天历史状态

#### `front/src/views/KnowledgeBase.vue`
- **作用**：知识库管理页面
- **核心功能**：
  - 上传文档到知识库
  - 展示已上传文档列表
  - 删除文档
- **关键技术点**：
  - 文件上传（FormData）
  - SSE 进度更新

#### `front/src/views/Login.vue`
- **作用**：用户登录页面
- **核心功能**：
  - 用户登录表单
  - 表单验证
  - Token 存储
- **关键技术点**：
  - JWT Token 管理
  - localStorage 存储

#### `front/src/views/Register.vue`
- **作用**：用户注册页面
- **核心功能**：
  - 用户注册表单
  - 表单验证
- **关键技术点**：
  - 密码强度验证
  - 重复密码验证

### 1.4 公共组件

#### `front/src/components/ChatPanel.vue`
- **作用**：聊天面板组件
- **核心功能**：
  - 消息气泡展示
  - 头像显示
  - 时间戳显示
- **关键技术点**：
  - 区分用户和 AI 消息
  - 支持 Markdown 渲染

#### `front/src/components/FileUpload.vue`
- **作用**：文件上传组件
- **核心功能**：
  - 文件选择
  - 上传进度显示
  - 文件类型校验
- **关键技术点**：
  - 拖拽上传支持
  - 大小限制

#### `front/src/components/SessionList.vue`
- **作用**：会话列表组件
- **核心功能**：
  - 展示会话列表
  - 切换会话
  - 删除会话
- **关键技术点**：
  - 会话状态管理
  - 最新消息预览

### 1.5 工具函数

#### `front/src/utils/axios.js`
- **作用**：HTTP 请求封装
- **核心功能**：
  - 全局请求拦截器（自动添加 Token）
  - 全局响应拦截器（处理 Token 过期）
  - 统一错误处理
- **关键技术点**：
  - JWT Token 自动注入
  - 401 错误自动跳转登录

### 1.6 路由配置

#### `front/src/router/index.js`
- **作用**：路由配置
- **核心功能**：
  - 定义页面路由
  - 路由守卫（登录验证）
- **关键技术点**：
  - 路由懒加载
  - 全局前置守卫

### 1.7 状态管理

#### `front/src/stores/userStore.js`
- **作用**：用户状态管理
- **核心功能**：
  - 用户信息存储
  - Token 管理
  - 登录状态判断
- **关键技术点**：
  - Pinia store
  - localStorage 持久化

---

## 2. 后端层 (`backend/`)

### 2.1 入口文件

#### `backend/main.py`
- **作用**：FastAPI 应用入口
- **核心功能**：
  - 创建 FastAPI 实例
  - 配置中间件（CORS、认证）
  - 注册路由
- **关键技术点**：
  - CORS 配置
  - 路由分组

### 2.2 Agent 模块

#### `backend/app/agent/agent.py`
- **作用**：Agent 核心实现
- **核心功能**：
  - 创建 AgentExecutor 实例
  - 执行 ReAct 推理循环
  - 流式响应输出
- **关键技术点**：
  - 工厂模式创建 Agent
  - SSE 流式响应
  - ReAct 范式实现

#### `backend/app/agent/agent_tools.py`
- **作用**：工具注册与定义
- **核心功能**：
  - 定义可调用工具（RAG检索、天气查询等）
  - 工具参数验证
- **关键技术点**：
  - `@tool` 装饰器
  - 工具描述自动生成

#### `backend/app/agent/agent_middleware.py`
- **作用**：Agent 生命周期钩子
- **核心功能**：
  - Agent 执行前后的钩子函数
  - 工具调用钩子
- **关键技术点**：
  - `before_agent`、`after_agent` 钩子
  - 日志记录

### 2.3 RAG 模块

#### `backend/app/rag/rag_service.py`
- **作用**：RAG 检索服务
- **核心功能**：
  - HyDE 假设文档生成
  - 混合检索（BM25 + 向量）
  - 文档摘要生成
- **关键技术点**：
  - HyDE 技术实现
  - 异步检索

#### `backend/app/rag/vector_store.py`
- **作用**：向量数据库服务
- **核心功能**：
  - ChromaDB 初始化
  - 文档向量化存储
  - 用户级隔离
- **关键技术点**：
  - 持久化存储
  - user_id 过滤

#### `backend/app/rag/retrievers/hybrid_retriever.py`
- **作用**：混合检索器
- **核心功能**：
  - BM25 关键词检索
  - 向量相似度检索
  - 动态权重混合
- **关键技术点**：
  - EnsembleRetriever
  - 动态权重调整

#### `backend/app/rag/reorder_service.py`
- **作用**：文档重排序服务
- **核心功能**：
  - 使用 Qwen3-Reranker 精排
  - 文档相似度计算
- **关键技术点**：
  - CrossEncoder 模型
  - 批量推理优化

### 2.4 路由模块

#### `backend/app/router/chat_router.py`
- **作用**：聊天路由
- **核心功能**：
  - 会话管理（创建、查询、删除）
  - 消息发送（流式响应）
- **关键技术点**：
  - SSE 端点
  - 异步处理

#### `backend/app/router/knowledge_router.py`
- **作用**：知识库路由
- **核心功能**：
  - 文档上传（流式进度）
  - 文档列表查询
  - 文档删除
- **关键技术点**：
  - 文件上传处理
  - SSE 进度反馈

#### `backend/app/router/knowledge_service.py`
- **作用**：知识库服务
- **核心功能**：
  - 文件处理逻辑
  - 向量存储操作
  - MD5 去重
- **关键技术点**：
  - 异步文件处理
  - 错误处理

### 2.5 工具函数

#### `backend/app/utils/auth_utils.py`
- **作用**：认证工具
- **核心功能**：
  - JWT Token 解析
  - 用户身份验证
  - Token 黑名单检查
- **关键技术点**：
  - 多种用户 ID 字段支持
  - Redis 黑名单

#### `backend/app/utils/factory.py`
- **作用**：模型工厂
- **核心功能**：
  - LLM 模型实例化（Ollama/阿里云）
  - 嵌入模型实例化
- **关键技术点**：
  - 工厂模式
  - 环境变量配置

#### `backend/app/utils/rate_limit.py`
- **作用**：限流工具
- **核心功能**：
  - 基于 Redis 的限流
  - 请求频率控制
- **关键技术点**：
  - 滑动窗口算法
  - 自定义限流阈值

### 2.6 数据库配置

#### `backend/app/db/db_config.py`
- **作用**：数据库配置
- **核心功能**：
  - MySQL 连接配置
  - 异步会话创建
- **关键技术点**：
  - SQLAlchemy 异步引擎
  - 连接池配置

#### `backend/app/db/redis_config.py`
- **作用**：Redis 配置
- **核心功能**：
  - Redis 连接配置
  - 缓存操作封装
- **关键技术点**：
  - 异步 Redis 客户端
  - 连接池

### 2.7 配置文件

#### `backend/app/config/settings.py`
- **作用**：应用配置
- **核心功能**：
  - 读取环境变量
  - 配置验证
- **关键技术点**：
  - Pydantic Settings
  - 类型安全

#### `backend/.env`
- **作用**：环境变量配置
- **核心配置项**：
  - LLM 类型（Ollama/阿里云）
  - 数据库连接信息
  - Redis 配置
  - JWT 密钥

---

## 3. 用户服务层 (`DjangoUserService/`)

### 3.1 入口文件

#### `DjangoUserService/manage.py`
- **作用**：Django 命令行入口
- **核心功能**：
  - 运行 Django 开发服务器
  - 执行数据库迁移
- **关键技术点**：
  - Django 管理命令

### 3.2 配置文件

#### `DjangoUserService/settings.py`
- **作用**：Django 配置
- **核心功能**：
  - 数据库配置
  - 中间件配置
  - 应用注册
- **关键技术点**：
  - JWT 认证配置
  - CORS 配置

#### `DjangoUserService/celery.py`
- **作用**：Celery 配置
- **核心功能**：
  - 异步任务队列配置
  - Redis 作为消息代理
- **关键技术点**：
  - 任务时间限制
  - 结果过期配置

#### `DjangoUserService/.env`
- **作用**：环境变量配置
- **核心配置项**：
  - 数据库连接信息
  - JWT 密钥
  - Celery 配置

### 3.3 用户模块

#### `DjangoUserService/apps/user/models.py`
- **作用**：用户模型
- **核心功能**：
  - 用户数据结构定义
  - 用户信息存储
- **关键技术点**：
  - Django ORM
  - 密码加密

#### `DjangoUserService/apps/user/views.py`
- **作用**：用户视图
- **核心功能**：
  - 用户注册
  - 用户登录
  - 用户信息查询
- **关键技术点**：
  - JWT Token 生成
  - 密码验证

#### `DjangoUserService/apps/user/urls.py`
- **作用**：用户路由
- **核心功能**：
  - 定义用户相关 API 端点
- **关键技术点**：
  - URL 路由配置

### 3.4 文件模块

#### `DjangoUserService/apps/file/models.py`
- **作用**：文件模型
- **核心功能**：
  - 文件数据结构定义
  - 文件元数据存储
- **关键技术点**：
  - 文件路径管理
  - 关联用户

#### `DjangoUserService/apps/file/views.py`
- **作用**：文件视图
- **核心功能**：
  - 文件上传
  - 文件列表查询
  - 文件删除
- **关键技术点**：
  - 文件存储
  - 权限验证

#### `DjangoUserService/apps/file/urls.py`
- **作用**：文件路由
- **核心功能**：
  - 定义文件相关 API 端点

---

## 4. 配置与工具文件

### 4.1 提示词模板

#### `backend/app/prompt/main_prompt.txt`
- **作用**：ReAct 提示词模板
- **核心功能**：
  - 定义 Agent 行为准则
  - 工具使用规则
- **关键技术点**：
  - 系统提示词
  - 工具调用格式

### 4.2 依赖配置

#### `backend/pyproject.toml`
- **作用**：Python 依赖配置
- **核心功能**：
  - 管理项目依赖包
  - 指定包版本
- **关键依赖**：
  - FastAPI
  - LangChain
  - ChromaDB
  - SQLAlchemy

---

## 📊 文件职责总结

### 前端文件职责

| 文件路径 | 职责 | 层级 |
|----------|------|------|
| `main.js` | 应用入口 | 入口层 |
| `router/index.js` | 路由管理 | 控制层 |
| `stores/userStore.js` | 状态管理 | 数据层 |
| `utils/axios.js` | HTTP 请求 | 工具层 |
| `views/*.vue` | 页面展示 | 视图层 |
| `components/*.vue` | UI 组件 | 组件层 |

### 后端文件职责

| 文件路径 | 职责 | 层级 |
|----------|------|------|
| `main.py` | 应用入口 | 入口层 |
| `agent/*.py` | Agent 推理 | 业务层 |
| `rag/*.py` | RAG 检索 | 业务层 |
| `router/*.py` | API 路由 | 控制层 |
| `utils/*.py` | 工具函数 | 工具层 |
| `db/*.py` | 数据库连接 | 数据层 |

### 用户服务文件职责

| 文件路径 | 职责 | 层级 |
|----------|------|------|
| `manage.py` | 命令入口 | 入口层 |
| `settings.py` | 应用配置 | 配置层 |
| `apps/user/*.py` | 用户管理 | 业务层 |
| `apps/file/*.py` | 文件管理 | 业务层 |

---

**文档版本**: v1.0  
**创建日期**: 2026-05-22  
**适用项目**: RAGAgent - 基于LangChain和RAG的Agent智能问答系统