# CookieCutter 使用指南

## 一、什么是 CookieCutter？

### 1.1 基本概念

**CookieCutter** 是一个命令行工具，用于从模板快速生成项目。它的核心思想是：

- **模板化**：将项目结构、配置文件、代码等作为模板保存
- **变量替换**：通过交互式问答或配置文件，替换模板中的变量
- **快速生成**：一键生成完整的项目结构，无需手动复制粘贴

### 1.2 为什么使用 CookieCutter？

#### 传统方式的问题

在使用脚手架时，传统的方式是：

```bash
# 1. 克隆脚手架仓库
git clone https://github.com/your-org/gd25-arch-backend-python my-project

# 2. 删除 .git，重新初始化
cd my-project
rm -rf .git
git init

# 3. 手动修改项目名称、描述等
# 需要修改 pyproject.toml、README.md 等多个文件
# 容易遗漏，容易出错
```

**问题：**
- ❌ 需要手动修改多个文件
- ❌ 容易遗漏某些文件
- ❌ 无法灵活选择包含哪些模块
- ❌ 容易出错（如忘记修改某个文件）

#### CookieCutter 的优势

```bash
# 1. 使用 CookieCutter 生成项目
cookiecutter cookiecutter-gd25-arch-backend-python

# 2. 按提示输入项目信息
project_name [my-project]: my-awesome-api
project_description [FastAPI 后端项目]: 我的第一个 API 项目
include_celery [y]: y
include_websocket [n]: n

# 3. 完成！项目已生成，所有文件都已正确替换
```

**优势：**
- ✅ 自动替换所有文件中的变量
- ✅ 交互式问答，不会遗漏
- ✅ 可以选择包含哪些模块（Celery、WebSocket 等）
- ✅ 一键生成，快速启动

### 1.3 CookieCutter 的工作原理

```
模板文件（包含变量）                   用户输入                生成的项目
─────────────────                    ────────              ──────────
{{ cookiecutter.project_name }}   →   my-project    →      my-project
{{ cookiecutter.author_name }}    →   John Doe      →      John Doe
{% if include_celery %}           →   y             →      包含 Celery 模块
{% endif %}
```

**核心机制：**
1. **变量替换**：`{{ cookiecutter.variable }}` 会被替换为用户输入的值
2. **条件包含**：`{% if %}` 可以根据用户选择包含或排除某些文件/代码
3. **目录名替换**：目录名也可以使用变量，如 `{{ cookiecutter.project_name }}/`

---

## 二、安装 CookieCutter

### 2.1 使用 pip 安装（推荐）

```bash
# 安装 CookieCutter
pip install cookiecutter

# 验证安装
cookiecutter --version
```

### 2.2 使用 conda 安装

```bash
# 使用 conda 安装
conda install -c conda-forge cookiecutter

# 验证安装
cookiecutter --version
```

### 2.3 系统要求

- Python 3.7+
- pip 或 conda

---

## 三、CookieCutter 基本使用

### 3.1 使用本地模板

```bash
# 使用本地模板目录
cookiecutter /path/to/cookiecutter-template

# 使用当前目录的模板
cookiecutter ./cookiecutter-gd25-arch-backend-python
```

#### 3.1.1 实际案例：在另一个项目中使用本模板

**场景：** 在项目 `/Users/m684620/work/github_GD25/gd25-biz-his-python` 中使用本模板生成新项目。

**⚠️ 重要说明：** 如果目标项目目录已存在（如已创建的 GitHub 空项目），CookieCutter 会因目录冲突而无法直接生成。需要使用临时目录方案。

**操作步骤（适用于已存在的项目目录）：**

1. **确保 CookieCutter 已安装**
   ```bash
   # 检查是否已安装
   cookiecutter --version
   
   # 如果未安装，使用 pip 安装
   pip install cookiecutter
   
   # 或使用 conda 安装
   conda install -c conda-forge cookiecutter
   ```

2. **进入目标项目的父目录**
   ```bash
   # 进入目标项目的父目录
   cd /Users/m684620/work/github_GD25
   ```

3. **使用临时名称生成项目**
   ```bash
   # 使用模板的绝对路径，生成到临时目录
   cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
     --output-dir . \
     --no-input \
     project_name=_temp_gd25_biz_his \
     project_description="业务历史记录服务" \
     author_name="你的名字" \
     author_email="your-email@example.com" \
     python_version="3.11" \
     include_celery="y" \
     include_websocket="n" \
     database_type="postgresql" \
     install_pgvector="n"
   ```

   **交互式方式：**
   ```bash
   cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
     --output-dir .
   
   # 当提示输入项目名称时，输入临时名称：
   # project_name [my-project]: _temp_gd25_biz_his
   # 其他选项按需输入或使用默认值
   ```

4. **将生成的内容复制到项目目录**
   ```bash
   # 进入项目目录
   cd /Users/m684620/work/github_GD25/gd25-biz-his-python
   
   # 复制临时目录内容（排除 .git，保留原有的 Git 仓库）
   rsync -av --exclude='.git' ../_temp_gd25_biz_his/ .
   
   # 如果 rsync 不可用，使用 cp 命令：
   # cp -r ../_temp_gd25_biz_his/* .
   ```

5. **清理临时目录**
   ```bash
   # 返回父目录
   cd /Users/m684620/work/github_GD25
   
   # 删除临时目录
   rm -rf _temp_gd25_biz_his
   ```

6. **验证生成的项目**
   ```bash
   # 进入项目目录
   cd /Users/m684620/work/github_GD25/gd25-biz-his-python
   
   # 查看项目结构
   ls -la
   
   # 应该看到完整的项目结构：
   # app/, tests/, alembic/, requirements.txt, pyproject.toml 等
   # 同时保留原有的 .git 目录
   ```

7. **初始化生成的项目**
   ```bash
   # 1. 添加文件到 Git（保留原有的 Git 仓库）
   git add .
   git commit -m "Initial commit: Add project structure from CookieCutter template"
   
   # 2. 创建 conda 虚拟环境（推荐）
   conda create -n gd25-biz-his-python python=3.11
   conda activate gd25-biz-his-python
   
   # 3. 安装依赖
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # 4. 创建环境变量文件
   cp env.example .env
   # 编辑 .env 文件，配置数据库连接等信息
   
   # 5. 初始化数据库（如果使用数据库）
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   
   # 6. 运行测试
   pytest
   
   # 7. 启动服务
   uvicorn app.main:app --reload
   ```

**非交互式方式（使用配置文件）：**

```bash
# 1. 创建配置文件（使用临时项目名称）
cat > /Users/m684620/work/github_GD25/gd25-biz-his-config.json << EOF
{
  "project_name": "_temp_gd25_biz_his",
  "project_description": "业务历史记录服务",
  "author_name": "你的名字",
  "author_email": "your-email@example.com",
  "python_version": "3.11",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql",
  "install_pgvector": "n"
}
EOF

# 2. 使用配置文件生成临时项目
cd /Users/m684620/work/github_GD25
cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
  --config-file gd25-biz-his-config.json \
  --no-input \
  --output-dir .

# 3. 复制内容到项目目录
cd gd25-biz-his-python
rsync -av --exclude='.git' ../_temp_gd25_biz_his/ .

# 4. 清理临时目录和配置文件
cd ..
rm -rf _temp_gd25_biz_his
rm -f gd25-biz-his-config.json
```

**注意事项：**
- ✅ **保留 .git 目录**：复制内容时务必排除 `.git` 目录，避免覆盖原有的 Git 仓库
- ✅ **临时项目名称**：可以使用任何临时名称，只要不与目标项目目录冲突即可
- ✅ **使用绝对路径**：模板路径使用绝对路径最可靠，避免路径错误
- ✅ **确保模板路径正确**：模板目录应包含 `cookiecutter.json` 文件

**📖 详细操作步骤请参考：** [CookieCutter本地项目模版操作步骤.md](./CookieCutter本地项目模版操作步骤.md)

### 3.2 使用 GitHub 模板

```bash
# 使用 GitHub 仓库（会自动克隆）
cookiecutter https://github.com/your-org/cookiecutter-gd25-arch-backend-python

# 使用 GitHub 仓库的特定分支
cookiecutter https://github.com/your-org/cookiecutter-gd25-arch-backend-python --checkout develop
```

### 3.3 交互式问答

运行 `cookiecutter` 命令后，会提示你输入各个变量的值：

```bash
$ cookiecutter cookiecutter-gd25-arch-backend-python

project_name [my-project]: my-awesome-api
project_description [FastAPI 后端项目]: 我的第一个 API 项目
author_name [GD25 Team]: 张三
author_email [team@gd25.com]: zhangsan@example.com
python_version [3.10]: 3.11
include_celery [y]: y
include_websocket [n]: n
database_type [postgresql]: postgresql
```

**说明：**
- `[默认值]`：括号内是默认值，直接按回车使用默认值
- 输入值后按回车确认
- 所有变量输入完成后，会自动生成项目

### 3.4 非交互式使用（使用配置文件）

如果不想每次输入，可以创建配置文件：

```bash
# 创建配置文件 cookiecutter.json
cat > cookiecutter.json << EOF
{
  "project_name": "my-awesome-api",
  "project_description": "我的第一个 API 项目",
  "author_name": "张三",
  "author_email": "zhangsan@example.com",
  "python_version": "3.11",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql"
}
EOF

# 使用配置文件（非交互式）
cookiecutter cookiecutter-gd25-arch-backend-python --no-input
```

### 3.5 覆盖已存在的目录

如果目标目录已存在，CookieCutter 会提示是否覆盖：

```bash
# 如果目录已存在，会提示：
# The directory my-project already exists. Overwrite it? [y/N]:

# 强制覆盖（不提示）
cookiecutter cookiecutter-gd25-arch-backend-python --overwrite-if-exists
```

---

## 四、CookieCutter 模板结构

### 4.1 模板目录结构

```
cookiecutter-gd25-arch-backend-python/     # 模板根目录
├── cookiecutter.json                        # 模板配置文件（定义变量）
└── {{ cookiecutter.project_name }}/        # 模板文件目录（使用变量作为目录名）
    ├── app/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── main.py
    │   └── ...
    ├── tests/
    ├── requirements.txt
    ├── README.md
    ├── pyproject.toml
    └── ...
```

### 4.2 cookiecutter.json 配置文件

`cookiecutter.json` 定义了模板的所有变量和默认值：

```json
{
  "project_name": "my-project",
  "project_description": "FastAPI 后端项目",
  "author_name": "GD25 Team",
  "author_email": "team@gd25.com",
  "python_version": "3.10",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql"
}
```

**变量类型：**
- **字符串**：`"project_name": "my-project"`
- **布尔值**：使用 `"y"` 或 `"n"` 字符串：`"include_celery": "y"`

### 4.3 模板文件中的变量替换

在模板文件中，使用 `{{ cookiecutter.variable }}` 来引用变量：

**pyproject.toml 示例：**
```toml
[project]
name = "{{ cookiecutter.project_name }}"
version = "1.0.0"
description = "{{ cookiecutter.project_description }}"

authors = [
    {name = "{{ cookiecutter.author_name }}", email = "{{ cookiecutter.author_email }}"}
]
```

**README.md 示例：**
```markdown
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 作者

- {{ cookiecutter.author_name }} ({{ cookiecutter.author_email }})
```

### 4.4 条件包含

使用 `{% if %}` 标签实现条件包含：

**requirements.txt 示例：**
```txt
fastapi>=0.104.0,<1.0.0
sqlalchemy>=2.0.0,<3.0.0
{% if cookiecutter.include_celery == 'y' %}
celery>=5.3.0,<6.0.0
{% endif %}
```

**app/main.py 示例：**
```python
from fastapi import FastAPI

{% if cookiecutter.include_websocket == 'y' %}
from app.websocket.manager import ConnectionManager
{% endif %}

app = FastAPI(title="{{ cookiecutter.project_name }}")

{% if cookiecutter.include_websocket == 'y' %}
# WebSocket 相关代码
manager = ConnectionManager()
{% endif %}
```

### 4.5 目录名变量

目录名也可以使用变量：

```
{{ cookiecutter.project_name }}/
├── app/
└── tests/
```

生成后：
```
my-awesome-api/
├── app/
└── tests/
```

---

## 五、使用本脚手架生成新项目

### 5.1 准备工作

1. **确保 CookieCutter 已安装**
   ```bash
   cookiecutter --version
   ```

2. **获取模板**
   - 方式一：使用本地模板（如果已转换为 CookieCutter 模板）
   - 方式二：从 GitHub 克隆模板仓库

### 5.2 生成项目

#### 方式一：交互式生成（推荐）

```bash
# 使用模板生成项目
cookiecutter cookiecutter-gd25-arch-backend-python

# 按提示输入项目信息
project_name [my-project]: my-awesome-api
project_description [FastAPI 后端项目]: 我的第一个 API 项目
author_name [GD25 Team]: 张三
author_email [team@gd25.com]: zhangsan@example.com
python_version [3.10]: 3.11
include_celery [y]: y          # 是否包含 Celery 模块
include_websocket [n]: n       # 是否包含 WebSocket 模块
database_type [postgresql]: postgresql
```

#### 方式二：非交互式生成

```bash
# 创建配置文件
cat > my-config.json << EOF
{
  "project_name": "my-awesome-api",
  "project_description": "我的第一个 API 项目",
  "author_name": "张三",
  "author_email": "zhangsan@example.com",
  "python_version": "3.11",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql"
}
EOF

# 使用配置文件生成
cookiecutter cookiecutter-gd25-arch-backend-python --config-file my-config.json --no-input
```

### 5.3 生成后的项目结构

生成的项目结构如下：

```
my-awesome-api/
├── app/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── db/
│   ├── utils/
│   ├── config.py
│   └── main.py
├── tests/
├── alembic/
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── pyproject.toml
└── ...
```

**注意：**
- 所有文件中的 `{{ cookiecutter.project_name }}` 等变量都已被替换
- 如果选择了不包含 Celery，则 `app/tasks/` 目录和相关代码不会生成
- 如果选择了不包含 WebSocket，则 `app/websocket/` 目录和相关代码不会生成

### 5.4 初始化生成的项目

```bash
# 1. 进入项目目录
cd my-awesome-api

# 2. 初始化 Git 仓库（可选）
git init
git add .
git commit -m "Initial commit from CookieCutter template"

# 3. 创建虚拟环境（推荐）
conda create -n my-awesome-api python=3.11
conda activate my-awesome-api

# 4. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. 创建环境变量文件
cp env.example .env
# 编辑 .env 文件，配置数据库等

# 6. 初始化数据库
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 7. 运行测试
pytest

# 8. 启动服务
uvicorn app.main:app --reload
```

---

## 六、将当前脚手架转换为 CookieCutter 模板

### 6.1 创建模板目录结构

```bash
# 1. 创建模板根目录
mkdir -p cookiecutter-gd25-arch-backend-python

# 2. 创建模板文件目录（使用变量作为目录名）
mkdir -p cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}
```

### 6.2 创建 cookiecutter.json

```json
{
  "project_name": "my-project",
  "project_description": "FastAPI 后端项目",
  "author_name": "GD25 Team",
  "author_email": "team@gd25.com",
  "python_version": "3.10",
  "include_celery": "y",
  "include_websocket": "n",
  "database_type": "postgresql"
}
```

### 6.3 复制项目文件到模板目录

```bash
# 复制项目文件到模板目录
cp -r app cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp -r tests cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp -r alembic cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp requirements.txt cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp requirements-dev.txt cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp README.md cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
cp pyproject.toml cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/
# ... 复制其他文件
```

### 6.4 替换文件中的变量

在模板文件中，将硬编码的值替换为变量：

**pyproject.toml：**
```toml
[project]
name = "{{ cookiecutter.project_name }}"
version = "1.0.0"
description = "{{ cookiecutter.project_description }}"

authors = [
    {name = "{{ cookiecutter.author_name }}", email = "{{ cookiecutter.author_email }}"}
]
```

**README.md：**
```markdown
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}
```

### 6.5 处理可选模块

对于可选模块（Celery、WebSocket），使用条件包含：

**requirements.txt：**
```txt
fastapi>=0.104.0,<1.0.0
sqlalchemy>=2.0.0,<3.0.0
{% if cookiecutter.include_celery == 'y' %}
celery>=5.3.0,<6.0.0
{% endif %}
```

**app/main.py：**
```python
{% if cookiecutter.include_websocket == 'y' %}
from app.websocket.manager import ConnectionManager
{% endif %}
```

### 6.6 测试模板

```bash
# 1. 测试模板生成
cookiecutter cookiecutter-gd25-arch-backend-python --no-input

# 2. 验证生成的项目
cd my-project
ls -la  # 检查文件结构

# 3. 检查变量替换
grep -r "my-project" .  # 应该找不到未替换的变量

# 4. 测试项目是否可以正常运行
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

---

## 七、将文档添加到 CookieCutter 模板

### 7.1 为什么需要将文档添加到模板？

当你在项目中创建了操作手册、使用指南等文档后，希望这些文档也能包含在通过模板生成的新项目中，这样：

- ✅ 新项目自动包含完整的操作文档
- ✅ 团队成员可以快速了解如何使用各个模块
- ✅ 减少重复编写文档的工作

### 7.2 操作步骤概述

将文档添加到 CookieCutter 模板的完整流程：

```
1. 准备文档 → 2. 配置同步脚本 → 3. 试运行验证 → 4. 执行同步 
   → 5. 验证结果 → 6. 测试模板生成 → 7. 提交更改
```

**快速操作（如果同步脚本已配置）：**

```bash
# 如果同步脚本中已包含 "docs/知识整理/"，直接执行：
python scripts/sync_template.py --dry-run  # 先预览
python scripts/sync_template.py            # 实际同步
```

**详细步骤请参考下面的章节。**

### 7.3 添加文档到模板的详细步骤

#### 步骤 1：准备文档

确保文档已经创建并放在合适的位置，例如：

```
docs/
└── 知识整理/
    ├── 101-Alembic操作手册.md
    ├── 102-Requirements操作手册.md
    ├── 103-Pytest操作手册.md
    └── 104-CookieCutter操作手册.md
```

#### 步骤 2：修改同步脚本

编辑 `scripts/sync_template.py`，在 `SYNC_PATHS` 列表中添加文档路径：

```python
# 需要同步的目录和文件
SYNC_PATHS = [
    "app/",
    "alembic/",
    "tests/",
    "scripts/",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements.lock",
    "pyproject.toml",
    "pytest.ini",
    "alembic.ini",
    "env.example",
    "LICENSE",
    "docs/知识整理/",  # 添加文档目录
]
```

**注意：**
- 如果 `EXCLUDE_PATTERNS` 中有 `"docs/"`，需要确保不会排除你要同步的文档目录
- 可以添加更具体的路径，如 `"docs/知识整理/"` 而不是整个 `"docs/"`

#### 步骤 3：检查排除规则

检查 `EXCLUDE_PATTERNS` 列表，确保不会排除你要同步的文档：

```python
EXCLUDE_PATTERNS = [
    # ... 其他排除规则
    "docs/",  # 如果整个 docs/ 被排除，需要修改为更具体的排除规则
    # 或者改为：
    # "docs/边做边学/",  # 只排除特定子目录
    # "docs/开发计划.md",  # 只排除特定文件
]
```

**建议：**
- 如果只需要同步 `docs/知识整理/`，可以保持 `"docs/"` 在排除列表中
- 在 `SYNC_PATHS` 中使用具体路径 `"docs/知识整理/"` 来覆盖排除规则

#### 步骤 4：执行同步（试运行）

先使用 `--dry-run` 参数预览将要执行的操作：

```bash
python scripts/sync_template.py --dry-run
```

**检查输出：**
- 确认会同步 `docs/知识整理/` 目录
- 确认不会同步其他不需要的文档
- 确认不会删除模板中已有的文档

#### 步骤 5：执行同步

确认无误后，执行实际同步：

```bash
python scripts/sync_template.py
```

#### 步骤 6：验证同步结果

检查模板目录中是否包含文档：

```bash
# 检查文档是否已同步到模板
ls -la "cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/docs/知识整理/"

# 或使用转义
ls -la cookiecutter-gd25-arch-backend-python/\{\{\ cookiecutter.project_name\ \}\}/docs/知识整理/
```

#### 步骤 7：测试模板生成

使用模板生成测试项目，验证文档是否正确包含：

```bash
# 生成测试项目
cookiecutter cookiecutter-gd25-arch-backend-python --no-input \
  --overwrite-if-exists

# 进入生成的项目
cd my-project

# 检查文档是否存在
ls -la docs/知识整理/

# 验证文档内容
cat docs/知识整理/101-Alembic操作手册.md | head -20

# 清理测试项目
cd ..
rm -rf my-project
```

### 7.4 注意事项

#### 7.3.1 文档中的变量替换

如果文档中包含项目特定的信息，可以使用 CookieCutter 变量：

**文档示例：**
```markdown
# {{ cookiecutter.project_name }} - Alembic 操作手册

本项目使用 Alembic 进行数据库迁移管理。
```

**注意：**
- 文档中的变量会在生成项目时自动替换
- 确保变量名与 `cookiecutter.json` 中的变量名一致

#### 7.3.2 文档路径和结构

- ✅ **保持路径一致**：模板中的文档路径应与项目中的路径一致
- ✅ **目录结构**：如果文档在子目录中，确保目录结构正确
- ✅ **文件命名**：使用清晰的命名规范，便于查找

#### 7.3.3 文档更新流程

当文档更新后：

1. **更新项目文档**：在项目的 `docs/` 目录中更新文档
2. **同步到模板**：运行 `python scripts/sync_template.py` 同步到模板
3. **验证模板**：测试模板生成，确认文档正确
4. **提交更改**：提交模板目录的更改

### 7.5 完整示例：添加操作手册到模板

**场景：** 将 `docs/知识整理/` 目录添加到模板

**操作步骤：**

```bash
# 1. 编辑同步脚本
# 在 scripts/sync_template.py 的 SYNC_PATHS 中添加：
# "docs/知识整理/",

# 2. 试运行查看预览
python scripts/sync_template.py --dry-run

# 3. 确认无误后执行同步
python scripts/sync_template.py

# 4. 验证同步结果
ls -la "cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/docs/知识整理/"

# 5. 测试模板生成
cookiecutter cookiecutter-gd25-arch-backend-python --no-input \
  --overwrite-if-exists project_name=test-project
cd test-project
ls -la docs/知识整理/
cd ..
rm -rf test-project

# 6. 提交更改
git add cookiecutter-gd25-arch-backend-python/
git add scripts/sync_template.py
git commit -m "添加操作手册文档到 CookieCutter 模板"
```

### 7.6 常见问题

#### Q1: 同步脚本提示文档被排除

**问题：** 运行同步脚本时，文档没有被同步

**原因：** `EXCLUDE_PATTERNS` 中可能包含了 `"docs/"`，导致整个 docs 目录被排除

**解决：**
1. 检查 `EXCLUDE_PATTERNS` 列表
2. 如果使用 `"docs/知识整理/"` 作为同步路径，确保路径正确
3. 或者修改排除规则，只排除不需要的文档目录

#### Q2: 模板生成后文档路径不正确

**问题：** 生成的项目中，文档不在预期位置

**原因：** 同步时的路径与模板中的路径不一致

**解决：**
1. 检查同步脚本中的路径是否正确
2. 检查模板目录结构
3. 确保路径使用相对路径（相对于项目根目录）

#### Q3: 文档中的变量没有被替换

**问题：** 生成的项目中，文档仍包含 `{{ cookiecutter.xxx }}` 变量

**原因：** 文档文件可能被当作二进制文件处理，或者变量语法错误

**解决：**
1. 确保文档是文本文件（.md, .txt 等）
2. 检查变量语法：`{{ cookiecutter.variable_name }}`
3. 确保变量名与 `cookiecutter.json` 中的变量名一致

### 7.7 操作步骤总结

**将 `docs/知识整理/` 添加到 CookieCutter 模板的完整操作步骤：**

#### 步骤 1：确认同步脚本配置

检查 `scripts/sync_template.py` 中的 `SYNC_PATHS` 是否包含：

```python
SYNC_PATHS = [
    # ... 其他路径
    "docs/知识整理/",  # 操作手册文档
]
```

**如果已包含，直接跳到步骤 3。**

#### 步骤 2：添加同步路径（如未配置）

编辑 `scripts/sync_template.py`，在 `SYNC_PATHS` 列表中添加：

```python
"docs/知识整理/",
```

#### 步骤 3：执行同步

```bash
# 1. 先试运行查看预览
python scripts/sync_template.py --dry-run

# 2. 确认无误后执行实际同步
python scripts/sync_template.py
```

#### 步骤 4：验证同步结果

```bash
# 检查模板中的文档
ls -la "cookiecutter-gd25-arch-backend-python/{{ cookiecutter.project_name }}/docs/知识整理/"
```

应该看到 4 个操作手册文件：
- `101-Alembic操作手册.md`
- `102-Requirements操作手册.md`
- `103-Pytest操作手册.md`
- `104-CookieCutter操作手册.md`

#### 步骤 5：测试模板生成（可选但推荐）

```bash
# 生成测试项目
cookiecutter cookiecutter-gd25-arch-backend-python --no-input \
  --overwrite-if-exists

# 进入生成的项目
cd my-project

# 验证文档是否存在
ls -la docs/知识整理/

# 清理测试项目
cd ..
rm -rf my-project
```

#### 步骤 6：提交更改

```bash
git add cookiecutter-gd25-arch-backend-python/
git add scripts/sync_template.py  # 如果修改了同步脚本
git commit -m "同步操作手册文档到 CookieCutter 模板"
```

**完成！** 现在通过模板生成的新项目将自动包含这些操作手册文档。

---

## 八、常见问题和注意事项

### 8.1 常见问题

#### Q1: CookieCutter 提示找不到模板

**问题：**
```bash
$ cookiecutter cookiecutter-gd25-arch-backend-python
Error: A valid repository for "cookiecutter-gd25-arch-backend-python" could not be found.
```

**解决方案：**
- 确保模板目录存在
- 使用绝对路径：`cookiecutter /absolute/path/to/cookiecutter-gd25-arch-backend-python`
- 或使用相对路径：`cookiecutter ./cookiecutter-gd25-arch-backend-python`

#### Q2: 变量没有被替换

**问题：** 生成的项目中仍然包含 `{{ cookiecutter.project_name }}` 等变量

**解决方案：**
- 检查模板文件中的变量语法是否正确：`{{ cookiecutter.variable }}`
- 确保变量名与 `cookiecutter.json` 中的变量名一致
- 检查文件编码（确保是 UTF-8）

#### Q3: 条件包含不工作

**问题：** 即使选择了不包含某个模块，相关文件仍然生成了

**解决方案：**
- 检查条件语法：`{% if cookiecutter.include_celery == 'y' %}`
- 确保变量值是 `'y'` 或 `'n'`（字符串）
- 检查 Jinja2 语法是否正确

#### Q4: 目录名包含特殊字符

**问题：** 项目名称包含空格或特殊字符，导致目录名异常

**解决方案：**
- 在 `cookiecutter.json` 中添加验证规则
- 或使用 `project_slug` 变量（自动转换项目名称为合法的目录名）

### 7.2 注意事项

1. **变量命名规范**
   - 使用小写字母和下划线：`project_name`、`author_name`
   - 避免使用 Python 关键字作为变量名

2. **布尔值处理**
   - CookieCutter 使用字符串 `'y'` 和 `'n'` 表示布尔值
   - 条件判断时使用：`{% if cookiecutter.include_celery == 'y' %}`

3. **文件编码**
   - 确保所有模板文件使用 UTF-8 编码
   - 特别是包含中文的文件

4. **Git 忽略**
   - 模板目录中不应该包含 `.git` 目录
   - 生成的项目会自动初始化新的 Git 仓库

5. **测试模板**
   - 每次修改模板后，都应该测试生成的项目
   - 确保所有变量都被正确替换
   - 确保项目可以正常启动和运行

---

## 八、高级用法

### 8.1 使用 Hook 脚本

CookieCutter 支持在生成项目前后执行脚本：

**post_gen_project.sh（生成后执行）：**
```bash
#!/bin/bash
# 生成项目后执行的脚本

# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit from CookieCutter template"

# 创建虚拟环境
conda create -n {{ cookiecutter.project_name }} python={{ cookiecutter.python_version }} -y
```

**pre_gen_project.sh（生成前执行）：**
```bash
#!/bin/bash
# 生成项目前执行的脚本

# 验证项目名称
if [[ "{{ cookiecutter.project_name }}" =~ [^a-zA-Z0-9_-] ]]; then
    echo "错误：项目名称只能包含字母、数字、下划线和连字符"
    exit 1
fi
```

### 8.2 使用自定义函数

在模板文件中可以使用 Jinja2 函数：

```python
# 自动生成项目 slug（将项目名转换为合法的目录名）
{{ cookiecutter.project_name|lower|replace(' ', '-') }}
```

### 8.3 使用循环

```jinja2
{% for module in cookiecutter.optional_modules %}
# {{ module }} 相关代码
{% endfor %}
```

---

## 九、总结

### 9.1 CookieCutter 的优势

- ✅ **快速生成**：一键生成完整的项目结构
- ✅ **自动替换**：所有变量自动替换，不会遗漏
- ✅ **灵活配置**：可以选择包含哪些模块
- ✅ **标准化**：确保所有项目使用相同的结构

### 9.2 使用场景

- **新项目启动**：快速创建新项目，无需手动配置
- **团队协作**：统一项目结构，提高团队效率
- **模板复用**：一次创建模板，多次使用

### 9.3 下一步

1. **学习更多**：查看 [CookieCutter 官方文档](https://cookiecutter.readthedocs.io/)
2. **实践**：使用本脚手架的 CookieCutter 模板生成新项目
3. **定制**：根据团队需求，定制自己的 CookieCutter 模板

---

**文档版本**：v1.0  
**创建时间**：2025-01-27  
**最后更新**：2025-01-27

