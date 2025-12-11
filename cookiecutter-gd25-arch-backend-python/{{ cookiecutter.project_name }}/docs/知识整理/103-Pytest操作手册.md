# 103-Pytest 操作手册

Pytest 是项目的测试框架，用于编写和运行单元测试、集成测试。

## 一、基本操作

### 1.1 运行测试

```bash
# 运行所有测试（推荐）
pytest

# 运行特定测试文件
pytest tests/test_main.py

# 运行特定测试函数
pytest tests/test_main.py::test_health_check

# 显示详细输出
pytest -v

# 显示详细输出和打印语句
pytest -v -s
```

### 1.2 常用参数

```bash
# -v, --verbose：详细输出
pytest -v

# -s, --capture=no：显示打印语句
pytest -s

# -k：运行匹配名称的测试
pytest -k "health"

# -m：运行标记的测试
pytest -m unit

# -x：在第一个失败时停止
pytest -x

# --pdb：失败时进入调试器
pytest --pdb
```

## 二、测试文件结构

### 2.1 测试文件命名

- 测试文件：`test_*.py`
- 测试类：`Test*`
- 测试函数：`test_*`

**示例：**
```
tests/
├── test_main.py          # 主应用测试
├── test_config.py        # 配置测试
├── test_repository.py    # Repository 测试
└── conftest.py          # 测试配置和 fixtures
```

### 2.2 测试函数示例

```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## 三、常用工作流程

### 3.1 开发时快速测试

```bash
# 运行当前正在开发的测试
pytest tests/test_main.py::test_health_check -v -s
```

### 3.2 运行所有测试

```bash
# 运行所有测试
pytest

# 或指定目录
pytest tests/
```

### 3.3 运行特定类型的测试

```bash
# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration

# 排除慢速测试
pytest -m "not slow"
```

### 3.4 查看测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 查看 HTML 报告
open htmlcov/index.html

# 终端显示覆盖率
pytest --cov=app --cov-report=term-missing
```

## 四、测试标记（Markers）

### 4.1 使用标记

在 `pytest.ini` 中已定义以下标记：

```ini
markers =
    unit: 单元测试
    integration: 集成测试
    slow: 慢速测试
```

### 4.2 标记测试

```python
import pytest

@pytest.mark.unit
def test_calculate():
    """单元测试"""
    assert 1 + 1 == 2

@pytest.mark.integration
def test_api_integration(client):
    """集成测试"""
    response = client.get("/api/users")
    assert response.status_code == 200

@pytest.mark.slow
def test_long_running():
    """慢速测试"""
    # 长时间运行的测试
    pass
```

### 4.3 运行标记的测试

```bash
# 只运行单元测试
pytest -m unit

# 只运行集成测试
pytest -m integration

# 排除慢速测试
pytest -m "not slow"
```

## 五、Fixtures（测试夹具）

### 5.1 使用项目提供的 Fixtures

项目在 `tests/conftest.py` 中提供了常用 fixtures：

```python
# client: FastAPI 测试客户端
def test_api(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200

# db_session: 数据库会话
def test_database(db_session):
    # 使用数据库会话进行测试
    pass
```

### 5.2 创建自定义 Fixture

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    """示例数据 fixture"""
    return {"name": "test", "value": 123}

# 使用
def test_with_data(sample_data):
    assert sample_data["name"] == "test"
```

## 六、异步测试

### 6.1 异步测试函数

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """异步测试"""
    result = await some_async_function()
    assert result is not None
```

### 6.2 运行异步测试

```bash
# pytest 会自动检测异步测试（pytest.ini 中已配置 asyncio_mode = auto）
pytest tests/test_async.py
```

## 七、配置文件说明

### 7.1 pytest.ini

项目配置文件位置：`pytest.ini`

**主要配置：**
- `testpaths = tests`：测试文件目录
- `python_files = test_*.py`：测试文件匹配模式
- `addopts`：默认命令行选项（包含覆盖率配置）
- `asyncio_mode = auto`：自动处理异步测试

### 7.2 覆盖配置

```bash
# 忽略 pytest.ini 中的 addopts 配置
pytest -o addopts=

# 临时禁用覆盖率
pytest --no-cov
```

## 八、常见问题

### 8.1 测试文件无法直接执行

**问题：** `python tests/test_main.py` 没有输出

**原因：** 测试文件需要使用 pytest 运行

**解决：**
```bash
# 使用 pytest 运行
pytest tests/test_main.py -v
```

**注意：** 项目中的测试文件已支持直接执行（文件末尾有 `if __name__ == "__main__"` 块），但推荐使用 `pytest` 命令。

### 8.2 Coverage 相关错误

**问题：** 运行 pytest 时提示 `pytest-cov` 未安装

**解决：**
```bash
# 安装 pytest-cov
pip install pytest-cov

# 或临时禁用覆盖率
pytest -o addopts=
```

### 8.3 测试找不到模块

**问题：** `ImportError: No module named 'app'`

**解决：**
1. 确认在项目根目录运行 pytest
2. 确认虚拟环境已激活
3. 确认已安装依赖：`pip install -r requirements-dev.txt`

### 8.4 数据库测试问题

**问题：** 测试需要数据库但连接失败

**解决：**
1. 检查 `.env` 文件中的 `DATABASE_URL` 配置
2. 确认测试使用测试数据库（不是生产数据库）
3. 检查 `tests/conftest.py` 中的数据库配置

## 九、最佳实践

### 9.1 测试组织

- ✅ **按功能模块组织**：`test_user.py`、`test_order.py` 等
- ✅ **使用描述性名称**：`test_create_user_with_valid_data()`
- ✅ **一个测试一个断言**：每个测试只验证一个功能点

### 9.2 测试编写

- ✅ **使用 fixtures**：复用测试数据和设置
- ✅ **测试边界情况**：正常情况、异常情况、边界值
- ✅ **保持测试独立**：每个测试应该可以独立运行

### 9.3 测试执行

- ✅ **开发时快速测试**：`pytest tests/test_xxx.py::test_function -v -s`
- ✅ **提交前完整测试**：`pytest` 运行所有测试
- ✅ **CI/CD 中运行**：`pytest --cov=app --cov-report=xml`

## 十、快速参考

| 操作 | 命令 |
|------|------|
| 运行所有测试 | `pytest` |
| 运行特定文件 | `pytest tests/test_main.py` |
| 运行特定函数 | `pytest tests/test_main.py::test_name` |
| 详细输出 | `pytest -v` |
| 显示打印 | `pytest -s` |
| 运行标记测试 | `pytest -m unit` |
| 覆盖率报告 | `pytest --cov=app --cov-report=html` |
| 第一个失败停止 | `pytest -x` |

---

**提示：** 
- 开发时使用 `pytest -v -s` 查看详细输出
- 提交代码前运行 `pytest` 确保所有测试通过
- 使用 `pytest --cov=app` 检查测试覆盖率
