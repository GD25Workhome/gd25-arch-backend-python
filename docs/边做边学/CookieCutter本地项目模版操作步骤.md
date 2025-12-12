# CookieCutter 本地项目模版操作步骤

## 场景说明

在已存在的 GitHub 空项目目录中使用 CookieCutter 模板生成项目内容。

**问题：** 如果先创建了 GitHub 空项目（如 `gd25-biz-his-python`），再使用 CookieCutter 生成同名项目时，会因为目录已存在而报错。

**解决方案：** 使用临时目录生成项目，然后将内容复制到目标项目目录。

---

## 操作步骤

### 方案一：在项目目录内生成（推荐）

适用于：已克隆 GitHub 空项目到本地的情况。

#### 步骤 1：克隆 GitHub 空项目（如果还未克隆）

```bash
# 克隆 GitHub 空项目
cd /Users/m684620/work/github_GD25
git clone https://github.com/your-org/gd25-biz-his-python.git
cd gd25-biz-his-python
```

#### 步骤 2：确保 CookieCutter 已安装

```bash
# 检查是否已安装
cookiecutter --version

# 如果未安装，使用 pip 安装
pip install cookiecutter

# 或使用 conda 安装
conda install -c conda-forge cookiecutter
```

#### 步骤 3：在项目目录的父目录生成临时项目

```bash
# 进入项目目录的父目录
cd /Users/m684620/work/github_GD25

# 使用 CookieCutter 生成到临时目录（使用不同的项目名称）
cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
  --output-dir . \
  --no-input \
  project_name=_temp_gd25_biz_his
```

**交互式方式：**

```bash
cd /Users/m684620/work/github_GD25

cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
  --output-dir .

# 当提示输入项目名称时，输入临时名称：
# project_name [my-project]: _temp_gd25_biz_his
# 其他选项按需输入或使用默认值
```

#### 步骤 4：将生成的内容复制到项目目录

```bash
# 进入项目目录
cd /Users/m684620/work/github_GD25/gd25-biz-his-python

# 将临时目录中的所有内容复制到当前目录（排除 .git）
rsync -av --exclude='.git' ../_temp_gd25_biz_his/ .

# 或者使用 cp 命令（如果 rsync 不可用）
# 注意：需要排除 .git 目录
cp -r ../_temp_gd25_biz_his/* .
cp -r ../_temp_gd25_biz_his/.[!.]* . 2>/dev/null || true  # 复制隐藏文件（排除 .git）
```

#### 步骤 5：清理临时目录

```bash
# 返回父目录
cd /Users/m684620/work/github_GD25

# 删除临时目录
rm -rf _temp_gd25_biz_his
```

#### 步骤 6：验证项目内容

```bash
# 进入项目目录
cd /Users/m684620/work/github_GD25/gd25-biz-his-python

# 查看项目结构
ls -la

# 应该看到完整的项目结构：
# app/, tests/, alembic/, requirements.txt, pyproject.toml 等
# 同时保留原有的 .git 目录
```

---

### 方案二：使用配置文件（非交互式，推荐）

适用于：需要重复使用相同配置的情况。

#### 步骤 1：创建配置文件

```bash
# 在项目目录的父目录创建配置文件
cd /Users/m684620/work/github_GD25

cat > gd25-biz-his-config.json << EOF
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
```

#### 步骤 2：使用配置文件生成临时项目

```bash
# 在项目目录的父目录执行
cd /Users/m684620/work/github_GD25

cookiecutter /Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python \
  --config-file gd25-biz-his-config.json \
  --no-input \
  --output-dir .
```

#### 步骤 3：复制内容到项目目录

```bash
# 进入项目目录
cd /Users/m684620/work/github_GD25/gd25-biz-his-python

# 复制临时目录内容（排除 .git）
rsync -av --exclude='.git' ../_temp_gd25_biz_his/ .

# 清理临时目录和配置文件
cd ..
rm -rf _temp_gd25_biz_his
rm -f gd25-biz-his-config.json
```

---

### 方案三：一键脚本（最便捷）

创建一个脚本自动化整个过程：

```bash
# 创建脚本文件
cat > /Users/m684620/work/github_GD25/init_project_from_template.sh << 'SCRIPT'
#!/bin/bash

# 配置变量
PROJECT_DIR="/Users/m684620/work/github_GD25/gd25-biz-his-python"
TEMPLATE_PATH="/Users/m684620/work/github_GD25/gd25-arch-backend-python/cookiecutter-gd25-arch-backend-python"
TEMP_NAME="_temp_$(basename $PROJECT_DIR)"
PARENT_DIR=$(dirname $PROJECT_DIR)

# 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "错误：项目目录不存在: $PROJECT_DIR"
    exit 1
fi

# 检查模板路径是否存在
if [ ! -d "$TEMPLATE_PATH" ]; then
    echo "错误：模板路径不存在: $TEMPLATE_PATH"
    exit 1
fi

# 进入父目录
cd "$PARENT_DIR"

# 生成临时项目
echo "正在生成临时项目..."
cookiecutter "$TEMPLATE_PATH" \
  --output-dir . \
  --no-input \
  project_name="$TEMP_NAME" \
  project_description="业务历史记录服务" \
  author_name="你的名字" \
  author_email="your-email@example.com" \
  python_version="3.11" \
  include_celery="y" \
  include_websocket="n" \
  database_type="postgresql" \
  install_pgvector="n"

# 复制内容到项目目录
echo "正在复制内容到项目目录..."
cd "$PROJECT_DIR"
rsync -av --exclude='.git' "../$TEMP_NAME/" .

# 清理临时目录
echo "正在清理临时文件..."
cd "$PARENT_DIR"
rm -rf "$TEMP_NAME"

echo "完成！项目已初始化。"
SCRIPT

# 赋予执行权限
chmod +x /Users/m684620/work/github_GD25/init_project_from_template.sh

# 执行脚本
/Users/m684620/work/github_GD25/init_project_from_template.sh
```

---

## 初始化生成的项目

生成项目内容后，需要初始化项目：

```bash
# 进入项目目录
cd /Users/m684620/work/github_GD25/gd25-biz-his-python

# 1. 检查 Git 状态（应该保留原有的 Git 仓库）
git status

# 2. 添加所有文件到 Git
git add .
git commit -m "Initial commit: Add project structure from CookieCutter template"

# 3. 创建 conda 虚拟环境（推荐）
conda create -n gd25-biz-his-python python=3.11
conda activate gd25-biz-his-python

# 4. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. 创建环境变量文件
cp env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 6. 初始化数据库（如果使用数据库）
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 7. 运行测试
pytest

# 8. 启动服务
uvicorn app.main:app --reload
```

---

## 注意事项

### ✅ 重要提示

1. **保留 .git 目录**：复制内容时务必排除 `.git` 目录，避免覆盖原有的 Git 仓库
2. **项目名称**：临时项目名称可以使用任何名称，只要不与目标项目目录冲突即可
3. **路径检查**：执行前确保模板路径和目标项目路径正确
4. **备份**：如果项目目录中已有重要文件，建议先备份

### ⚠️ 常见问题

#### Q1: 复制时提示权限错误

**解决：** 确保对项目目录有写权限，或使用 `sudo`（不推荐）

#### Q2: rsync 命令不存在

**解决：** 使用 `cp` 命令替代：
```bash
cp -r ../_temp_gd25_biz_his/* .
# 手动排除 .git 目录
```

#### Q3: 复制后 .git 目录丢失

**解决：** 确保使用 `--exclude='.git'` 参数，或手动排除 `.git` 目录

#### Q4: 文件权限问题

**解决：** 复制后检查文件权限，必要时使用 `chmod` 调整

---

## 完整示例

以下是一个完整的操作示例：

```bash
# ============================================
# 完整操作流程示例
# ============================================

# 1. 克隆 GitHub 空项目（如果还未克隆）
cd /Users/m684620/work/github_GD25
git clone https://github.com/your-org/gd25-biz-his-python.git
cd gd25-biz-his-python

# 2. 检查 CookieCutter 是否安装
cookiecutter --version || pip install cookiecutter

# 3. 返回父目录，生成临时项目
cd ..
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

# 4. 复制内容到项目目录
cd gd25-biz-his-python
rsync -av --exclude='.git' ../_temp_gd25_biz_his/ .

# 5. 清理临时目录
cd ..
rm -rf _temp_gd25_biz_his

# 6. 返回项目目录，初始化项目
cd gd25-biz-his-python
git add .
git commit -m "Initial commit: Add project structure from CookieCutter template"

# 7. 创建虚拟环境并安装依赖
conda create -n gd25-biz-his-python python=3.11
conda activate gd25-biz-his-python
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 8. 配置环境变量
cp env.example .env
# 编辑 .env 文件

# 9. 初始化数据库
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 10. 运行测试
pytest

# 11. 启动服务
uvicorn app.main:app --reload
```

---

## 总结

使用 CookieCutter 在已存在的项目目录中生成项目内容的步骤：

1. ✅ 在项目目录的父目录使用临时名称生成项目
2. ✅ 将生成的内容复制到项目目录（排除 .git）
3. ✅ 清理临时目录
4. ✅ 初始化项目（Git、虚拟环境、依赖等）

这样可以避免目录冲突问题，同时保留原有的 Git 仓库。

---

**文档版本**：v1.0  
**创建时间**：2025-01-27  
**最后更新**：2025-01-27
