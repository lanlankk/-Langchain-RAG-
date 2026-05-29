# 项目运行错误总结文档

## 一、数据库连接错误

### 1.1 Unknown database 'user_service' / 'chat_history'

**错误描述：**
```
django.db.utils.OperationalError: (1049, "Unknown database 'user_service'")
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1049, "Unknown database 'chat_history'")
```

**原因分析：**
数据库尚未创建，应用程序无法连接到不存在的数据库。

**解决方案：**
```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE user_service CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE chat_history CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
exit;
```

### 1.2 Table 'user_service.user_service' doesn't exist

**错误描述：**
```
django.db.utils.ProgrammingError: (1146, "Table 'user_service.user_service' doesn't exist")
```

**原因分析：**
数据库已创建，但 Django 迁移未执行，表结构不存在。

**解决方案：**
```bash
cd DjangoUserService
.venv\Scripts\python.exe manage.py migrate
```

---

## 二、Python 版本兼容性问题

### 2.1 类型提示语法错误

**错误描述：**
```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

**原因分析：**
`str | None` 联合类型语法是 Python 3.10+ 引入的新特性，当前环境为 Python 3.9.x。

**解决方案：**
```python
# 旧语法（兼容所有 Python 3.x）
from typing import Optional

async def get_redis_cache_str(key: str) -> Optional[str]:  # 替代 str | None
async def get_redis_cache_json(key: str) -> Optional[dict]:  # 替代 dict | None
```

### 2.2 安装 langchain_classic 失败

**错误描述：**
```
ERROR: Could not find a version that satisfies the requirement langchain_classic
```

**原因分析：**
当前环境 Python 版本为 3.9.25，而 `langchain_classic` 需要 Python 3.10+。

**解决方案：**
```bash
# 创建新的 Conda 环境
conda create -n myenv_name python=3.10
conda activate myenv_name
pip install langchain_classic
```

---

## 三、依赖安装错误

### 3.1 sqlalchemy 安装失败

**错误描述：**
```
error: Microsoft Visual C++ 14.0 or greater is required.
ERROR: Failed building wheel for greenlet
```

**原因分析：**
`greenlet` 依赖需要编译环境，缺少 Visual C++ Build Tools。

**解决方案：**
```bash
# 安装预编译版本
pip install greenlet --only-binary :all:
pip install sqlalchemy
```

---

## 四、配置文件错误

### 4.1 .env 文件注释语法错误

**错误描述：**
```
python-dotenv could not parse statement starting at line 34
```

**原因分析：**
`.env` 文件中使用了 `;` 作为注释符号，正确的注释符号应为 `#`。

**解决方案：**
```env
# 错误写法
; ALIYUN_EMBED_MODEL_NAME=qwen3-vl-rerank

# 正确写法  
# ALIYUN_EMBED_MODEL_NAME=qwen3-vl-rerank
```

---

## 五、应用启动错误

### 5.1 FastAPI 模块导入失败

**错误描述：**
```
ERROR: Error loading ASGI app. Could not import module "main".
```

**原因分析：**
`main.py` 位于 `backend` 目录下，但在项目根目录运行命令。

**解决方案：**
```bash
# 方法一：进入正确目录
cd backend
uvicorn main:app --reload

# 方法二：指定完整路径
uvicorn backend.main:app --reload
```

---

## 六、环境配置建议

### 6.1 开发环境准备清单

| 序号 | 检查项 | 说明 |
| :--- | :--- | :--- |
| 1 | Python 版本 | 确保 >= 3.10 |
| 2 | MySQL 服务 | 确保已启动，可正常连接 |
| 3 | Redis 服务 | 确保已启动，端口 6379 |
| 4 | 数据库创建 | 创建 `user_service` 和 `chat_history` 数据库 |
| 5 | Django 迁移 | 运行 `python manage.py migrate` |
| 6 | 环境变量 | 检查 `.env` 文件配置正确 |

### 6.2 服务启动顺序

```bash
# 1. 启动 MySQL（确保已启动）

# 2. 启动 Redis（确保已启动）

# 3. 启动 Django 用户服务
cd DjangoUserService
.venv\Scripts\python.exe manage.py runserver 8001

# 4. 启动 FastAPI 后端服务（新终端）
cd backend
uvicorn main:app --reload
```

### 6.3 Conda 环境迁移步骤

```bash
# 1. 导出旧环境包列表
conda run -n old_env pip freeze > requirements.txt

# 2. 创建新环境（Python 3.10）
conda create -n new_env python=3.10
conda activate new_env

# 3. 安装依赖
pip install -r requirements.txt
```

---

## 七、常见问题排查流程

```
启动失败
    ↓
检查错误信息关键词
    ↓
├─ "Unknown database" → 创建对应数据库
├─ "Table doesn't exist" → 运行数据库迁移
├─ "Module not found" → 检查文件路径/安装依赖
├─ "TypeError: unsupported operand type" → 检查 Python 版本/类型提示语法
├─ "Could not parse statement" → 检查 .env 文件格式
└─ 其他错误 → 检查服务状态（MySQL/Redis）
```

---

## 八、预防措施

1. **版本管理**：使用 `pyproject.toml` 或 `requirements.txt` 记录依赖版本
2. **配置检查**：启动前验证 `.env` 文件格式
3. **环境隔离**：使用 Conda 虚拟环境避免版本冲突
4. **迁移脚本**：编写数据库初始化脚本（如 `init_db.sql`）
5. **文档记录**：更新 README 记录环境要求和启动步骤