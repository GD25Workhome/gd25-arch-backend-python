# gd25-arch-backend-python

FastAPI 后端脚手架 - 通用的项目基础框架

## 项目简介

这是一个通用的 FastAPI 后端脚手架，为团队提供标准化的项目基础框架，包含：

- ✅ 标准化的项目结构
- ✅ 通用的基础设施代码
- ✅ 最佳实践和约定
- ✅ 可复用的工具类

## 核心价值

- **快速启动新项目**：避免重复搭建基础框架
- **统一代码风格**：团队使用相同的项目结构
- **减少重复工作**：基础设施代码一次编写，多次使用
- **提高开发效率**：专注于业务逻辑，而不是基础设施

## 技术栈

- **FastAPI** - Web 框架
- **SQLAlchemy** - ORM 框架
- **Alembic** - 数据库迁移
- **Pydantic** - 数据验证
- **Celery** - 异步任务队列（可选）
- **Redis** - 缓存和消息队列（可选）
- **PostgreSQL/MySQL** - 数据库支持

## 快速开始

### 1. 环境要求

- Python 3.10+
- PostgreSQL 14+ 或 MySQL 8.0+（用于测试）
- Redis 6.0+（如果使用 Celery 模块）

### 2. 安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填写实际配置值
# 至少需要配置 DATABASE_URL
```

### 4. 运行项目

#### 方式一：使用 uvicorn 命令（推荐）

```bash
# 启动开发服务器（带自动重载）
uvicorn app.main:app --reload

# 指定主机和端口
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问 API 文档
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

**命令说明：**
- `uvicorn`：ASGI 服务器（处理 HTTP 请求）
- `app.main:app`：应用路径（从 `app/main.py` 导入 `app` 应用实例）
- `--reload`：开发模式，代码变化时自动重启

#### 方式二：使用启动脚本

```bash
# 开发环境
./scripts/start_dev.sh

# 生产环境（需要先安装 gunicorn）
./scripts/start_prod.sh
```

#### 详细说明

关于启动方式的详细说明，请参考：[启动方式说明.md](./docs/启动方式说明.md)

## 项目结构

```
gd25-arch-backend-python/
├── app/                    # 应用主目录
│   ├── api/               # API 路由
│   ├── services/          # 业务逻辑层
│   ├── models/            # 数据模型
│   ├── schemas/           # Pydantic 模式
│   ├── repositories/      # 数据访问层
│   ├── db/                # 数据库相关
│   ├── utils/             # 工具类
│   ├── tasks/             # Celery 任务（可选）
│   ├── websocket/         # WebSocket 处理（可选）
│   ├── config.py          # 配置管理
│   └── main.py            # 应用入口
├── tests/                 # 测试文件
├── alembic/               # 数据库迁移脚本
├── requirements.txt       # 核心依赖
├── requirements-dev.txt   # 开发依赖
├── .env.example           # 环境变量示例
├── pytest.ini            # 测试配置
├── alembic.ini            # 数据库迁移配置
└── pyproject.toml         # 项目元数据
```

## 配置说明

### 环境变量

主要配置项（详细说明见 `.env.example`）：

- `APP_NAME` - 应用名称
- `APP_VERSION` - 应用版本
- `DEBUG` - 调试模式
- `ENVIRONMENT` - 运行环境（development/testing/production）
- `DATABASE_URL` - 数据库连接 URL
- `REDIS_URL` - Redis 连接 URL（可选）
- `LOG_LEVEL` - 日志级别
- `LOG_FORMAT` - 日志格式（json/text）
- `CORS_ORIGINS` - CORS 允许的源列表

### 配置扩展

如果需要添加自定义配置项，可以继承 `Settings` 类：

```python
from app.config import Settings
from pydantic import Field

class ProjectSettings(Settings):
    """项目自定义配置"""
    api_key: str = Field(..., description="API 密钥")
    max_retries: int = Field(default=3, ge=1, le=10)

project_settings = ProjectSettings()
```

## 开发指南

### 代码规范

- 使用详细的简体中文注释和文档字符串
- 函数和类必须有完整的类型提示
- 异常处理要完善，提供有用的错误信息
- 遵循 PEP 8 代码风格

### 测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/test_config.py
```

## 使用方式

### 方式一：Git Clone + 自定义

```bash
# 1. Clone 脚手架仓库
git clone https://github.com/your-org/gd25-arch-backend-python my-project

# 2. 删除 .git，重新初始化
cd my-project
rm -rf .git
git init

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 5. 开始开发
```

## 开发计划

详细的开发计划请参考 [开发计划.md](./开发计划.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
