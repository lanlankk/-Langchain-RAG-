# 📐 RAG对话系统 - 项目架构图文档

---

## 📋 目录

1. [图例说明](#1-图例说明)
2. [整体架构](#2-整体架构)
3. [目录结构详解](#3-目录结构详解)
4. [核心调用流程](#4-核心调用流程)
5. [服务依赖关系](#5-服务依赖关系)
6. [数据流向图](#6-数据流向图)
7. [架构特点总结](#7-架构特点总结)

---

## 1. 图例说明

| 符号 | 含义 | 颜色标识 |
|------|------|----------|
| 📁 | 目录/模块 | 蓝色 |
| 📄 | Python 源代码文件 | 绿色 |
| ⚙️ | 配置文件 | 橙色 |
| 📊 | 数据库/存储 | 紫色 |
| 🔗 | 依赖/调用关系 | 灰色箭头 |
| 🚀 | 服务/进程 | 红色 |

---

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RAGAgent 项目架构                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐         HTTP请求          ┌──────────────────┐        │
│  │    前端层        │ ─────────────────────────→ │    后端层        │        │
│  │    (Vue 3)       │ ←───────────────────────── │   (FastAPI)      │        │
│  └────────┬─────────┘           响应            └────────┬─────────┘        │
│           │                                              │                  │
│           ▼                                              ▼                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          服务层                                     │  │
│  ├────────────┬────────────┬────────────┬────────────┬───────────────┐  │  │
│  │  UserService│ ChatService│ RagService│ AgentService│ VectorStore  │  │  │
│  │  (Django)   │            │           │            │  (ChromaDB)  │  │  │
│  └─────┬──────┴──────┬─────┴─────┬──────┴─────┬──────┴───────┬───────┘  │  │
│        │             │            │            │              │            │  │
│        ▼             ▼            ▼            ▼              ▼            │  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │  │
│  │                          数据存储层                                  │  │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │  │  │
│  │  │  MySQL   │    │ ChromaDB │    │   Redis  │    │ 文件系统 │     │  │  │
│  │  │(用户/会话)│    │(向量库)  │    │(缓存/限流)│    │(文档存储)│     │  │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │  │  │
│  └──────────────────────────────────────────────────────────────┘  │  │  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │  │
│  │                          AI模型层                                    │   │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │   │  │
│  │  │ Qwen3-Max│    │Qwen3-Emb │    │Qwen3-Rerank│                     │   │  │
│  │  │ (LLM)   │    │(嵌入模型)│    │ (重排序)  │                       │   │  │
│  │  └──────────┘    └──────────┘    └──────────┘                       │   │  │
│  └──────────────────────────────────────────────────────────────────────┘   │  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 目录结构详解

### 3.1 前端层 (`front/`)

```
front/
├── 📁 src/
│   ├── 📁 components/          # 公共组件
│   │   ├── 📄 ChatPanel.vue    # 聊天面板组件
│   │   ├── 📄 FileUpload.vue   # 文件上传组件
│   │   └── 📄 SessionList.vue  # 会话列表组件
│   ├── 📁 views/               # 页面组件
│   │   ├── 📄 Chat.vue         # AI聊天页面
│   │   ├── 📄 KnowledgeBase.vue # 知识库管理页面
│   │   ├── 📄 Login.vue        # 登录页面
│   │   └── 📄 Register.vue     # 注册页面
│   ├── 📁 utils/               # 工具函数
│   │   └── 📄 axios.js         # 全局HTTP拦截器
│   ├── 📁 router/              # 路由配置
│   │   └── 📄 index.js         # 路由定义
│   ├── 📁 stores/              # 状态管理
│   │   └── 📄 userStore.js     # 用户状态
│   └── 📄 main.js              # 入口文件
├── ⚙️ vite.config.js           # Vite配置
├── ⚙️ package.json             # 依赖配置
└── 📄 index.html               # HTML模板
```

### 3.2 后端层 (`backend/`)

```
backend/
├── 📁 app/
│   ├── 📁 agent/               # Agent模块
│   │   ├── 📄 agent.py         # Agent核心实现
│   │   ├── 📄 agent_tools.py   # 工具注册
│   │   └── 📄 agent_middleware.py # 生命周期钩子
│   ├── 📁 config/              # 配置文件
│   │   └── 📄 settings.py      # 应用配置
│   ├── 📁 db/                  # 数据库模块
│   │   ├── 📄 db_config.py     # 数据库配置
│   │   └── 📄 redis_config.py  # Redis配置
│   ├── 📁 rag/                 # RAG模块
│   │   ├── 📄 rag_service.py   # RAG服务
│   │   ├── 📄 vector_store.py  # 向量存储
│   │   ├── 📁 retrievers/      # 检索器
│   │   │   └── 📄 hybrid_retriever.py
│   │   └── 📄 reorder_service.py # 重排序服务
│   ├── 📁 router/              # 路由定义
│   │   ├── 📄 chat_router.py   # 聊天路由
│   │   ├── 📄 knowledge_router.py # 知识库路由
│   │   └── 📄 knowledge_service.py # 知识库服务
│   ├── 📁 utils/               # 工具函数
│   │   ├── 📄 auth_utils.py    # 认证工具
│   │   ├── 📄 factory.py       # 模型工厂
│   │   └── 📄 rate_limit.py    # 限流工具
│   └── 📁 prompt/              # 提示词模板
│       └── 📄 main_prompt.txt  # ReAct提示词
├── ⚙️ .env                     # 环境变量
├── ⚙️ pyproject.toml           # Python依赖配置
└── 📄 main.py                  # FastAPI入口
```

### 3.3 用户服务层 (`DjangoUserService/`)

```
DjangoUserService/
├── 📁 apps/
│   ├── 📁 user/                # 用户模块
│   │   ├── 📄 models.py        # 用户模型
│   │   ├── 📄 views.py         # 用户视图
│   │   └── 📄 urls.py          # 用户路由
│   └── 📁 file/                # 文件模块
│       ├── 📄 models.py        # 文件模型
│       ├── 📄 views.py         # 文件视图
│       └── 📄 urls.py          # 文件路由
├── ⚙️ .env                     # 环境变量
├── ⚙️ settings.py              # Django配置
├── ⚙️ celery.py                # Celery配置
└── 📄 manage.py                # Django入口
```

---

## 4. 核心调用流程

### 4.1 用户登录流程

```
前端 Login.vue
    │
    ▼ POST /user/login/
    │
    ▼ DjangoUserService/apps/user/views.py
    │
    ▼ MySQL (user_service数据库)
    │
    ▼ 返回 JWT Token
    │
    ▼ 前端 localStorage 存储 token
```

**涉及文件**：
- `front/src/views/Login.vue` - 登录页面组件
- `DjangoUserService/apps/user/views.py` - 用户登录视图
- `DjangoUserService/apps/user/models.py` - 用户模型

### 4.2 文件上传到知识库流程

```
前端 KnowledgeBase.vue
    │
    ▼ POST /knowledge/add/multiple/stream
    │
    ▼ backend/app/router/knowledge_service.py
    │
    ├─→ 验证 Token (auth_utils.py)
    │
    ├─→ 文件处理 (python-magic)
    │
    ├─→ backend/app/rag/vector_store.py
    │
    ├─→ ChromaDB (向量存储)
    │
    └─→ MD5Store (去重记录)
```

**涉及文件**：
- `front/src/views/KnowledgeBase.vue` - 知识库页面组件
- `backend/app/router/knowledge_service.py` - 知识库服务
- `backend/app/utils/auth_utils.py` - 认证工具
- `backend/app/rag/vector_store.py` - 向量存储服务

### 4.3 AI 问答流程

```
前端 Chat.vue
    │
    ▼ POST /chat/agent/query/stream
    │
    ▼ backend/app/router/chat_router.py
    │
    ├─→ backend/app/utils/auth_utils.py (认证)
    │
    ├─→ backend/app/agent/agent.py (创建Agent)
    │
    ├─→ backend/app/rag/rag_service.py (RAG检索)
    │
    │   ├─→ HyDE生成假设文档
    │   ├─→ HybridRetriever检索 (BM25 + 向量)
    │   └─→ Qwen3-Reranker重排序
    │
    ├─→ Qwen3-Max (LLM生成)
    │
    └─→ MySQL (保存会话历史)
```

**涉及文件**：
- `front/src/views/Chat.vue` - 聊天页面组件
- `backend/app/router/chat_router.py` - 聊天路由
- `backend/app/utils/auth_utils.py` - 认证工具
- `backend/app/agent/agent.py` - Agent核心实现
- `backend/app/rag/rag_service.py` - RAG服务
- `backend/app/rag/retrievers/hybrid_retriever.py` - 混合检索器

---

## 5. 服务依赖关系

### 5.1 服务启动顺序

```
┌─────────────────────────────────────────────────────────────┐
│                    服务启动顺序                            │
├─────────────────────────────────────────────────────────────┤
│  1. MySQL        → 2. Redis       → 3. Ollama              │
│       │                │                │                  │
│       ▼                ▼                ▼                  │
│  4. DjangoUserService → 5. FastAPI → 6. Vue Frontend       │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 服务配置表

| 服务名称 | 端口 | 依赖服务 | 主要职责 |
|----------|------|----------|----------|
| MySQL | 3306 | 无 | 用户数据、会话历史存储 |
| Redis | 6379 | 无 | 缓存、限流计数器 |
| Ollama | 11434 | 无 | 本地大语言模型服务 |
| DjangoUserService | 8001 | MySQL, Redis | 用户认证、文件管理 |
| FastAPI | 8000 | MySQL, Redis, Ollama | 核心业务逻辑、RAG服务 |
| Vue Frontend | 3000 | FastAPI, DjangoUserService | 用户界面、交互 |

---

## 6. 数据流向图

### 6.1 文档上传数据流程

```
用户上传文档
    │
    ▼
文档切片 (chunk_size=200, chunk_overlap=20)
    │
    ▼
Qwen3-Embedding (向量化)
    │
    ▼
ChromaDB (持久化存储)
    │
    ▼
MD5Store (记录文件指纹)
```

### 6.2 问答数据流程

```
用户提问
    │
    ▼
HyDE生成假设文档
    │
    ▼
HybridRetriever (BM25 + 向量检索)
    │
    ▼
Qwen3-Reranker (文档重排序)
    │
    ▼
Qwen3-Max (生成回答)
    │
    ▼
MySQL (保存会话)
    │
    ▼
前端展示 (SSE流式输出)
```

---

## 7. 架构特点总结

### 7.1 架构优势

| 特点 | 说明 | 技术实现 |
|------|------|----------|
| **微服务架构** | 分离用户服务和对话服务 | Django + FastAPI |
| **模块化设计** | 独立模块，低耦合 | Agent、RAG、向量存储分离 |
| **异步处理** | 高并发支持 | FastAPI异步视图 |
| **可扩展性** | 多种LLM支持 | Ollama/阿里云切换 |
| **用户隔离** | 数据安全 | user_id过滤 |
| **流式响应** | 实时交互 | SSE协议 |

### 7.2 核心技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue 3 | 3.x |
| 后端框架 | FastAPI | 0.100+ |
| 用户服务 | Django | 5.x |
| 向量数据库 | ChromaDB | 0.4+ |
| 大语言模型 | Qwen3 | - |
| 数据库 | MySQL | 8.0+ |
| 缓存 | Redis | 7.0+ |

---

**文档版本**: v1.0  
**创建日期**: 2026-05-22  
**适用项目**: RAGAgent - 基于LangChain和RAG的Agent智能问答系统