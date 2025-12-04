# CookieCutter 模板 - FastAPI 后端脚手架

这是一个 CookieCutter 模板，用于快速生成 FastAPI 后端项目。

## 使用方法

### 1. 安装 CookieCutter

```bash
pip install cookiecutter
```

### 2. 使用模板生成项目

```bash
# 使用本地模板
cookiecutter cookiecutter-gd25-arch-backend-python

# 或使用 GitHub 模板（如果已发布）
cookiecutter https://github.com/your-org/cookiecutter-gd25-arch-backend-python
```

### 3. 按提示输入项目信息

- `project_name`: 项目名称（默认：my-project）
- `project_description`: 项目描述（默认：FastAPI 后端项目）
- `author_name`: 作者名称（默认：GD25 Team）
- `author_email`: 作者邮箱（默认：team@gd25.com）
- `python_version`: Python 版本（默认：3.10）
- `include_celery`: 是否包含 Celery 模块（默认：y）
- `include_websocket`: 是否包含 WebSocket 模块（默认：n）
- `database_type`: 数据库类型（默认：postgresql）

### 4. 初始化生成的项目

```bash
cd <project_name>

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 初始化数据库
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

## 模板变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `project_name` | 项目名称 | my-project |
| `project_description` | 项目描述 | FastAPI 后端项目 |
| `author_name` | 作者名称 | GD25 Team |
| `author_email` | 作者邮箱 | team@gd25.com |
| `python_version` | Python 版本 | 3.10 |
| `include_celery` | 是否包含 Celery 模块 | y |
| `include_websocket` | 是否包含 WebSocket 模块 | n |
| `database_type` | 数据库类型 | postgresql |

## 可选模块

### Celery 模块

如果选择包含 Celery 模块（`include_celery: y`），模板会包含：
- `app/tasks/` 目录（Celery 任务定义）
- `tests/test_celery.py`（Celery 测试）
- `scripts/start_worker.sh`（Worker 启动脚本）
- `scripts/start_flower.sh`（Flower 监控启动脚本）

### WebSocket 模块

如果选择包含 WebSocket 模块（`include_websocket: y`），模板会包含：
- `app/websocket/` 目录（WebSocket 处理）
- `tests/test_websocket.py`（WebSocket 测试）
- `tests/websocket_test.html`（WebSocket 测试页面）

## 后处理脚本

模板包含一个后处理脚本（`hooks/post_gen_project.py`），用于：
- 根据用户选择删除不需要的可选模块文件
- 清理不需要的测试文件

## 详细文档

更多使用说明请参考：
- [CookieCutter 使用指南](../docs/边做边学/CookieCutter使用指南.md)
- [快速开始指南](../docs/边做边学/快速开始指南.md)

