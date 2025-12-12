# 104-CookieCutter 操作手册

CookieCutter 用于从模板快速生成新项目，自动替换项目名称、描述等变量。

## 一、基本概念

### 1.1 什么是 CookieCutter？

CookieCutter 是一个命令行工具，用于从模板生成项目：
- **模板化**：项目结构、配置文件作为模板保存
- **变量替换**：通过交互式问答替换模板中的变量
- **快速生成**：一键生成完整的项目结构

### 1.2 模板位置

项目模板位于：`cookiecutter-gd25-arch-backend-python/`

## 二、安装 CookieCutter

### 2.1 使用 pip 安装（推荐）

```bash
pip install cookiecutter
```

### 2.2 使用 conda 安装

```bash
conda install -c conda-forge cookiecutter
```

### 2.3 验证安装

```bash
cookiecutter --version
```

## 三、使用模板生成项目

### 3.1 使用本地模板

```bash
# 使用当前项目的模板
cookiecutter ./cookiecutter-gd25-arch-backend-python

# 或使用绝对路径
cookiecutter /path/to/cookiecutter-gd25-arch-backend-python
```

### 3.2 使用 GitHub 模板

```bash
# 从 GitHub 仓库使用（会自动克隆）
cookiecutter https://github.com/your-org/cookiecutter-gd25-arch-backend-python

# 使用特定分支
cookiecutter https://github.com/your-org/cookiecutter-gd25-arch-backend-python --checkout develop
```

### 3.3 交互式问答

运行命令后会提示输入变量值：

```bash
$ cookiecutter ./cookiecutter-gd25-arch-backend-python

project_name [my-project]: my-awesome-api
project_description [FastAPI 后端项目]: 我的第一个 API 项目
author_name [xiaolong.shu]: 张三
author_email [985776854@qq.com]: zhangsan@example.com
python_version [3.11]: 3.10
include_celery [y]: y
include_websocket [n]: n
database_type [postgresql]: postgresql
install_pgvector [n]: n
```

**说明：**
- `[默认值]`：括号内是默认值，直接按回车使用
- 输入值后按回车确认
- 所有变量输入完成后自动生成项目

## 四、非交互式使用

### 4.1 使用配置文件

**步骤：**

1. **创建配置文件**
```json
{
  "project_name": "my-awesome-api",
  "project_description": "我的第一个 API 项目",
  "author_name": "张三",
  "author_email": "zhangsan@example.com",
  "python_version": "3.10",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql",
  "install_pgvector": "n"
}
```

2. **使用配置文件生成**
```bash
cookiecutter ./cookiecutter-gd25-arch-backend-python \
  --config-file my-config.json \
  --no-input
```

### 4.2 使用默认值

```bash
# 使用所有默认值，不进行交互
cookiecutter ./cookiecutter-gd25-arch-backend-python --no-input
```

## 五、模板变量说明

### 5.1 必需变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `project_name` | 项目名称（也是目录名） | `my-project` |
| `project_description` | 项目描述 | `FastAPI 后端项目` |

### 5.2 可选变量

| 变量 | 说明 | 默认值 | 选项 |
|------|------|--------|------|
| `author_name` | 作者名称 | `xiaolong.shu` | - |
| `author_email` | 作者邮箱 | `985776854@qq.com` | - |
| `python_version` | Python 版本 | `3.11` | `3.10`, `3.11`, `3.12` |
| `include_celery` | 是否包含 Celery | `y` | `y`, `n` |
| `include_websocket` | 是否包含 WebSocket | `n` | `y`, `n` |
| `database_type` | 数据库类型 | `postgresql` | `postgresql`, `mysql` |
| `install_pgvector` | 是否安装 pgvector | `n` | `y`, `n` |

### 5.3 变量影响

- **`include_celery`**：
  - `y`：生成 `app/tasks/` 目录和 Celery 相关代码
  - `n`：不生成 Celery 相关代码

- **`include_websocket`**：
  - `y`：生成 `app/websocket/` 目录和 WebSocket 相关代码
  - `n`：不生成 WebSocket 相关代码

- **`database_type`**：
  - `postgresql`：使用 PostgreSQL 驱动和配置
  - `mysql`：使用 MySQL 驱动和配置

## 六、生成后的操作

### 6.1 进入项目目录

```bash
cd <project_name>
# 例如：cd my-awesome-api
```

### 6.2 初始化 Git（可选）

```bash
git init
git add .
git commit -m "Initial commit from CookieCutter template"
```

### 6.3 创建虚拟环境

```bash
# 使用 conda（推荐）
conda create -n <project_name> python=<python_version>
conda activate <project_name>

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 6.4 安装依赖

```bash
# 安装开发依赖（包含生产依赖）
pip install -r requirements-dev.txt
```

### 6.5 配置环境变量

```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，至少配置 DATABASE_URL
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 6.6 初始化数据库

```bash
# 创建数据库（如果不存在）
python scripts/init_db.py

# 运行数据库迁移
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6.7 运行测试

```bash
# 运行所有测试
pytest
```

### 6.8 启动服务

```bash
# 启动开发服务器
uvicorn app.main:app --reload
```

## 七、完整工作流程示例

### 7.1 从模板生成新项目

```bash
# 1. 安装 CookieCutter（如果未安装）
pip install cookiecutter

# 2. 使用模板生成项目
cookiecutter ./cookiecutter-gd25-arch-backend-python

# 3. 按提示输入项目信息
# project_name: my-api
# project_description: 我的 API 项目
# ...

# 4. 进入项目目录
cd my-api

# 5. 创建虚拟环境
conda create -n my-api python=3.10
conda activate my-api

# 6. 安装依赖
pip install -r requirements-dev.txt

# 7. 配置环境变量
cp env.example .env
# 编辑 .env，配置 DATABASE_URL

# 8. 初始化数据库
python scripts/init_db.py
alembic upgrade head

# 9. 运行测试
pytest

# 10. 启动服务
uvicorn app.main:app --reload
```

## 八、常见问题

### 8.1 模板变量未替换

**问题：** 生成的项目中仍有 `{{ "{{" }} cookiecutter.xxx {{ "}}" }}` 变量

**原因：** 模板文件格式错误或变量名不匹配

**解决：** 检查模板文件，确保变量格式正确

### 8.2 生成的项目结构不完整

**问题：** 某些目录或文件未生成

**原因：** 可能是条件判断导致（如 `include_celery=n` 时不生成 Celery 相关文件）

**解决：** 检查 `cookiecutter.json` 中的变量值，确认是否需要这些模块

### 8.3 无法找到模板

**问题：** `cookiecutter: error: could not find template`

**解决：**
1. 确认模板路径正确
2. 使用绝对路径：`cookiecutter /absolute/path/to/template`
3. 确认模板目录包含 `cookiecutter.json` 文件

## 九、高级用法

### 9.1 覆盖特定文件

```bash
# 生成项目后，可以手动覆盖某些文件
# 例如：使用自定义的 README.md
cp custom-readme.md my-project/README.md
```

### 9.2 使用模板钩子

模板可能包含 `hooks/` 目录，在生成项目后自动执行：
- `pre_gen_project.py`：生成前执行
- `post_gen_project.py`：生成后执行

这些脚本会自动运行，无需手动执行。

## 十、快速参考

| 操作 | 命令 |
|------|------|
| 安装 CookieCutter | `pip install cookiecutter` |
| 使用本地模板 | `cookiecutter ./cookiecutter-gd25-arch-backend-python` |
| 使用 GitHub 模板 | `cookiecutter https://github.com/...` |
| 非交互式生成 | `cookiecutter ... --no-input` |
| 使用配置文件 | `cookiecutter ... --config-file config.json --no-input` |

---

**提示：** 
- 首次使用建议交互式生成，了解所有变量
- 后续可以使用配置文件批量生成项目
- 生成后记得检查 `.env` 配置和数据库初始化
