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
cp .env.example .env
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

## 七、常见问题和注意事项

### 7.1 常见问题

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

