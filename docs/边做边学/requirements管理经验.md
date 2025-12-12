# Requirements 管理经验总结

本文档总结本项目在 Python 依赖管理方面的实践经验，包括文件结构、管理策略、常见问题和最佳实践。

## 一、文件结构

### 1.1 文件说明

项目使用三个文件管理 Python 依赖：

- **`requirements.txt`**：核心生产依赖，包含版本范围约束
- **`requirements-dev.txt`**：开发依赖，通过 `-r requirements.txt` 包含核心依赖
- **`requirements.lock`**：依赖锁定文件，包含所有直接和间接依赖的精确版本

### 1.2 文件关系

```
requirements.txt (核心依赖)
    ↑
    │ (通过 -r requirements.txt 引用)
    │
requirements-dev.txt (开发依赖 = 核心依赖 + 开发工具)
    ↑
    │ (安装时自动解析)
    │
requirements.lock (精确版本锁定)
```

## 二、依赖管理策略

### 2.1 版本约束原则

**核心原则：使用版本范围约束，避免过于严格的版本锁定**

```python
# ✅ 正确：使用版本范围
fastapi>=0.104.0,<1.0.0
uvicorn[standard]>=0.24.0,<1.0.0

# ❌ 错误：过于严格的版本锁定
fastapi==0.104.0  # 不允许小版本更新
```

**原因：**
- 允许安全的小版本更新（bug 修复、安全补丁）
- 避免大版本更新带来的破坏性变更
- 保持依赖的灵活性和可维护性

### 2.2 依赖分类

#### 核心依赖（requirements.txt）

```python
# Web 框架
fastapi>=0.104.0,<1.0.0
uvicorn[standard]>=0.24.0,<1.0.0  # [standard] 包含 websockets、httptools、uvloop 等

# 数据库
sqlalchemy>=2.0.0,<3.0.0
alembic>=1.12.0,<2.0.0
psycopg2-binary>=2.9.0,<3.0.0  # PostgreSQL 驱动
pymysql>=1.1.0,<2.0.0  # MySQL 驱动

# 数据验证
pydantic>=2.5.0,<3.0.0
pydantic-settings>=2.1.0,<3.0.0
email-validator>=2.0.0,<3.0.0
```

#### 可选依赖

```python
# 可选依赖（根据需要取消注释）
celery>=5.3.0,<6.0.0  # 异步任务队列
redis>=5.0.0,<6.0.0  # Redis 客户端
flower>=2.0.0,<3.0.0  # Celery 监控工具
```

**注意：** 可选依赖在代码中已使用，但可以根据项目需求决定是否安装。

#### 开发依赖（requirements-dev.txt）

```python
# 代码质量
black>=23.11.0,<24.0.0
flake8>=6.1.0,<7.0.0
isort>=5.12.0,<6.0.0
mypy>=1.7.0,<2.0.0

# 测试
pytest>=7.4.0,<8.0.0
pytest-asyncio>=0.21.0,<1.0.0
pytest-cov>=4.1.0,<5.0.0
httpx>=0.25.0,<1.0.0  # 用于测试 HTTP 请求

# 开发工具
python-dotenv>=1.0.0,<2.0.0  # 环境变量管理
```

### 2.3 依赖锁定文件（requirements.lock）

**用途：**
- 生产环境部署时使用，确保版本一致性
- 包含所有直接和间接依赖的精确版本
- 用于 CI/CD 环境，保证构建的可重复性

**生成方法：**

```bash
# 1. 安装所有依赖
pip install -r requirements-dev.txt

# 2. 生成锁定文件
pip freeze > requirements.lock

# 3. 清理不需要的包（只保留项目相关的）
pip freeze | grep -E "(fastapi|uvicorn|sqlalchemy|...)" > requirements.lock
```

**注意事项：**
- Lock 文件应定期更新，特别是在更新 requirements.txt 后
- 生产环境可以使用 lock 文件确保版本一致性
- 开发环境建议使用 requirements.txt，允许版本更新

## 三、常见依赖说明

### 3.1 uvicorn[standard]

**说明：** `uvicorn[standard]` 是 uvicorn 的完整版本，包含以下额外依赖：

- `websockets`：WebSocket 支持（FastAPI WebSocket 功能需要）
- `httptools`：高性能 HTTP 解析器
- `uvloop`：高性能事件循环（Linux/macOS）
- `watchfiles`：文件监控（用于 --reload 功能）

**为什么使用 [standard]：**
- 项目使用了 WebSocket 功能，需要 `websockets` 包
- 提供更好的性能和开发体验
- 避免手动管理这些依赖

### 3.2 数据库驱动

项目支持两种数据库：

- **PostgreSQL**：`psycopg2-binary`（二进制版本，无需编译）
- **MySQL**：`pymysql`（纯 Python 实现）

**注意：** 根据实际使用的数据库，可以只安装需要的驱动。

### 3.3 可选依赖

以下依赖是可选的，根据项目需求决定是否安装：

- **Celery**：异步任务队列（如果使用异步任务功能）
- **Redis**：缓存和消息队列（Celery 的 Result Backend）
- **Flower**：Celery 监控工具（开发/运维使用）

## 四、依赖管理流程

### 4.1 添加新依赖

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
   pip check  # 检查依赖冲突
   ```

4. **更新 lock 文件**
   ```bash
   pip freeze | grep -E "(package-name|...)" >> requirements.lock
   ```

### 4.2 更新依赖

**步骤：**

1. **更新 requirements.txt 中的版本约束**
   ```python
   # 从
   fastapi>=0.104.0,<1.0.0
   # 更新到
   fastapi>=0.110.0,<1.0.0
   ```

2. **安装新版本**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **测试功能**
   ```bash
   pytest  # 运行测试确保功能正常
   ```

4. **更新 lock 文件**
   ```bash
   pip freeze > requirements.lock
   ```

### 4.3 处理依赖冲突

**检查冲突：**

```bash
pip check
```

**常见冲突原因：**

1. **版本范围不兼容**
   - 解决：调整版本约束，找到兼容的版本范围

2. **间接依赖冲突**
   - 解决：更新直接依赖的版本，或使用 `pip install --upgrade` 更新冲突的包

3. **Python 版本不兼容**
   - 解决：检查包的 Python 版本要求，升级 Python 或降级包版本

## 五、最佳实践

### 5.1 版本约束策略

1. **使用版本范围，避免精确锁定**
   - ✅ `package>=1.0.0,<2.0.0`
   - ❌ `package==1.0.0`

2. **定期更新依赖**
   - 每月检查一次依赖更新
   - 关注安全公告，及时更新有安全漏洞的包

3. **测试后再更新**
   - 更新依赖后运行完整测试
   - 在开发环境验证后再部署到生产

### 5.2 环境管理

1. **使用虚拟环境**
   ```bash
   # 推荐使用 conda
   conda create -n project-name python=3.10
   conda activate project-name
   ```

2. **环境隔离**
   - 开发环境：使用 `requirements-dev.txt`
   - 生产环境：使用 `requirements.txt` 或 `requirements.lock`

3. **环境一致性**
   - 使用 `requirements.lock` 确保生产环境版本一致
   - CI/CD 环境使用 lock 文件

### 5.3 依赖审查

1. **定期审查依赖**
   - 检查是否有未使用的依赖
   - 检查是否有安全漏洞（使用 `pip-audit` 或 `safety`）

2. **最小化依赖**
   - 只安装项目实际需要的包
   - 避免安装不必要的可选依赖

3. **文档化依赖选择**
   - 在 requirements.txt 中添加注释说明依赖用途
   - 记录可选依赖的使用场景

## 六、常见问题

### Q1: 为什么 requirements-dev.txt 中不需要多环境配置？

**A:** 项目使用单一开发环境，通过 `-r requirements.txt` 引用核心依赖即可。如果需要多环境（如测试环境、预发布环境），可以创建额外的 requirements 文件，如 `requirements-test.txt`。

### Q2: websockets 包是否需要单独添加到 requirements.txt？

**A:** 不需要。`uvicorn[standard]` 已经包含了 `websockets` 包，无需单独添加。如果使用 `uvicorn`（不带 [standard]），则需要单独添加。

### Q3: 如何确定依赖的版本范围？

**A:** 
1. 查看包的发布历史，了解大版本更新频率
2. 参考包的文档，了解版本兼容性
3. 使用 `>=最低版本,<下一个大版本` 的模式
4. 测试后确定合适的版本范围

### Q4: requirements.lock 应该提交到版本控制吗？

**A:** 是的，应该提交。Lock 文件用于：
- 确保生产环境版本一致性
- CI/CD 环境构建可重复性
- 团队协作时版本统一

### Q5: 如何处理可选依赖？

**A:** 
- 在 requirements.txt 中注释说明
- 根据项目需求决定是否安装
- 在文档中说明使用场景
- 代码中使用 try-except 处理可选依赖的导入

## 七、工具推荐

### 7.1 依赖管理工具

- **pip-tools**：生成和管理 requirements 文件
- **pip-audit**：检查依赖安全漏洞
- **safety**：检查已知安全漏洞
- **pipdeptree**：查看依赖树

### 7.2 使用示例

```bash
# 查看依赖树
pip install pipdeptree
pipdeptree

# 检查安全漏洞
pip install pip-audit
pip-audit

# 使用 pip-tools 管理依赖
pip install pip-tools
pip-compile requirements.in  # 生成 requirements.txt
pip-sync requirements.txt    # 同步环境
```

## 八、总结

### 8.1 核心原则

1. **版本范围约束**：使用 `>=最低版本,<下一个大版本` 的模式
2. **依赖分类管理**：核心依赖、开发依赖、可选依赖分开管理
3. **定期更新**：定期检查和更新依赖，关注安全公告
4. **环境隔离**：使用虚拟环境，开发和生产环境分离
5. **文档化**：在 requirements 文件中添加注释说明

### 8.2 维护建议

1. **每月检查一次**：检查依赖更新和安全公告
2. **测试后更新**：更新依赖后运行完整测试
3. **保持简洁**：只安装项目实际需要的依赖
4. **及时更新 lock**：修改 requirements.txt 后及时更新 lock 文件

### 8.3 项目特定说明

本项目的特点：

- 使用 `uvicorn[standard]` 提供完整的 WebSocket 支持
- 支持 PostgreSQL 和 MySQL 两种数据库
- Celery、Redis、Flower 为可选依赖
- 开发依赖通过 `-r requirements.txt` 引用核心依赖
- 使用 `requirements.lock` 确保生产环境版本一致性

---

**最后更新：** 2025-01-27  
**维护者：** GD25 Team

