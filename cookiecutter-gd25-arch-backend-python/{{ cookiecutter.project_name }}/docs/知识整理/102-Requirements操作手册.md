# 102-Requirements 操作手册

项目使用 `requirements.txt` 和 `requirements-dev.txt` 管理 Python 依赖包。

## 一、文件说明

### 1.1 requirements.txt

**用途：** 生产环境核心依赖

**包含：**
- Web 框架（FastAPI、Uvicorn）
- 数据库相关（SQLAlchemy、Alembic、数据库驱动）
- 数据验证（Pydantic）
- 可选依赖（Celery、Redis 等）

### 1.2 requirements-dev.txt

**用途：** 开发环境依赖

**包含：**
- 包含所有 `requirements.txt` 的依赖（通过 `-r requirements.txt`）
- 代码质量工具（Black、Flake8、isort、mypy）
- 测试工具（pytest、pytest-asyncio、pytest-cov）
- 开发工具（python-dotenv）

## 二、基本操作

### 2.1 安装依赖

```bash
# 安装生产环境依赖
pip install -r requirements.txt

# 安装开发环境依赖（包含生产依赖）
pip install -r requirements-dev.txt
```

**推荐流程：**
```bash
# 1. 创建虚拟环境（推荐使用 conda）
conda create -n project-name python=3.10
conda activate project-name

# 2. 安装开发依赖
pip install -r requirements-dev.txt
```

### 2.2 检查依赖冲突

```bash
# 检查已安装包的依赖冲突
pip check
```

**如果发现冲突：**
- 查看冲突的包和版本
- 更新 `requirements.txt` 中的版本约束
- 重新安装依赖

### 2.3 更新依赖

```bash
# 更新所有包到最新兼容版本
pip install --upgrade -r requirements.txt

# 更新特定包
pip install --upgrade package-name
```

## 三、添加新依赖

### 3.1 添加生产依赖

**步骤：**

1. **安装并测试**
```bash
pip install package-name
# 测试功能是否正常
```

2. **添加到 requirements.txt**
```bash
# 编辑 requirements.txt，添加：
package-name>=1.0.0,<2.0.0
```

3. **验证安装**
```bash
pip install -r requirements.txt
pip check
```

### 3.2 添加开发依赖

**步骤：**

1. **安装并测试**
```bash
pip install package-name
```

2. **添加到 requirements-dev.txt**
```bash
# 编辑 requirements-dev.txt，添加：
package-name>=1.0.0,<2.0.0
```

3. **验证安装**
```bash
pip install -r requirements-dev.txt
pip check
```

### 3.3 版本约束规范

**推荐格式：**
```txt
# 主版本约束（推荐）
package-name>=1.0.0,<2.0.0

# 精确版本（不推荐，除非必要）
package-name==1.2.3

# 最低版本（谨慎使用）
package-name>=1.0.0
```

**说明：**
- `>=1.0.0,<2.0.0`：允许 1.x 版本，不允许 2.x（推荐）
- `==1.2.3`：固定版本（仅用于解决特定问题）
- `>=1.0.0`：最低版本（可能导致意外升级）

## 四、依赖锁定（可选）

### 4.1 生成锁定文件

```bash
# 生成精确版本锁定文件
pip freeze > requirements.lock
```

**用途：**
- 生产环境部署时使用精确版本
- 确保不同环境版本一致

### 4.2 使用锁定文件

```bash
# 安装锁定版本
pip install -r requirements.lock
```

## 五、常见操作场景

### 5.1 新项目初始化

```bash
# 1. 创建虚拟环境
conda create -n project-name python=3.10
conda activate project-name

# 2. 安装开发依赖
pip install -r requirements-dev.txt

# 3. 验证安装
pip check
```

### 5.2 添加可选功能依赖

**示例：添加文件上传支持**

1. **取消注释 requirements.txt 中的依赖**
```txt
# 取消注释
python-multipart>=0.0.6,<1.0.0  # 文件上传支持
```

2. **安装**
```bash
pip install -r requirements.txt
```

### 5.3 更新依赖版本

**场景：** 需要升级 FastAPI 到新版本

1. **修改 requirements.txt**
```txt
# 从
fastapi>=0.104.0,<1.0.0
# 改为
fastapi>=0.110.0,<1.0.0
```

2. **安装并测试**
```bash
pip install --upgrade -r requirements.txt
pip check
# 运行测试确保兼容性
pytest
```

### 5.4 移除依赖

**步骤：**

1. **从 requirements.txt 中删除对应行**
2. **卸载包（可选）**
```bash
pip uninstall package-name
```
3. **验证**
```bash
pip check
```

## 六、依赖管理最佳实践

### 6.1 版本管理

- ✅ **使用版本范围**：`>=1.0.0,<2.0.0` 而不是 `==1.2.3`
- ✅ **定期更新**：定期检查并更新依赖版本
- ✅ **测试兼容性**：更新后运行测试确保兼容

### 6.2 依赖分类

- ✅ **生产依赖**：`requirements.txt`（应用运行必需）
- ✅ **开发依赖**：`requirements-dev.txt`（开发、测试工具）
- ✅ **可选依赖**：在 `requirements.txt` 中注释，需要时取消注释

### 6.3 环境一致性

- ✅ **使用虚拟环境**：每个项目独立的虚拟环境
- ✅ **锁定生产版本**：生产环境使用 `requirements.lock`
- ✅ **定期检查冲突**：使用 `pip check` 检查依赖冲突

## 七、故障排查

### 7.1 安装失败

**问题：** `pip install -r requirements.txt` 失败

**排查步骤：**
1. 检查 Python 版本是否符合要求（Python 3.10+）
2. 检查网络连接（某些包需要从 PyPI 下载）
3. 检查编译环境（某些包需要编译，如 psycopg2-binary）
4. 查看详细错误信息：`pip install -r requirements.txt -v`

### 7.2 版本冲突

**问题：** `pip check` 显示版本冲突

**解决方案：**
1. 查看冲突详情
2. 更新冲突包的版本约束
3. 如果无法解决，考虑使用 `pip-tools` 工具

### 7.3 导入错误

**问题：** 运行时 `ImportError: No module named 'xxx'`

**解决方案：**
1. 确认包已安装：`pip list | grep package-name`
2. 确认虚拟环境已激活
3. 重新安装：`pip install -r requirements.txt`

## 八、快速参考

| 操作 | 命令 |
|------|------|
| 安装生产依赖 | `pip install -r requirements.txt` |
| 安装开发依赖 | `pip install -r requirements-dev.txt` |
| 检查冲突 | `pip check` |
| 更新依赖 | `pip install --upgrade -r requirements.txt` |
| 生成锁定文件 | `pip freeze > requirements.lock` |
| 查看已安装包 | `pip list` |
| 查看包信息 | `pip show package-name` |

---

**提示：** 
- 修改依赖后记得运行 `pip check` 检查冲突
- 生产环境建议使用 `requirements.lock` 锁定版本
- 定期更新依赖以获取安全补丁和新功能
