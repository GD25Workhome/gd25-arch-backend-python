# Redis vs RabbitMQ 方案对比

## 一、架构差异

### Redis 方案
```
FastAPI → Redis (Broker + Result Backend) → Celery Worker
```

### RabbitMQ 方案
```
FastAPI → RabbitMQ (Broker) → Celery Worker
         ↓
      Redis (Result Backend，可选)
```

## 二、需要修改的地方

### 1. **依赖包（requirements.txt）**

**Redis 方案：**
```python
# redis>=5.0.0,<6.0.0  # Redis 客户端
```

**RabbitMQ 方案：**
```python
# celery>=5.3.0,<6.0.0  # 异步任务队列
# kombu>=5.3.0,<6.0.0   # Celery 的消息库（已包含在 celery 中）
# amqp>=5.2.0,<6.0.0    # RabbitMQ 协议支持（已包含在 kombu 中）

# 如果仍需要 Result Backend，可以保留 Redis
# redis>=5.0.0,<6.0.0  # Redis 客户端（用于 Result Backend）
```

**说明：**
- Celery 本身支持 RabbitMQ，无需额外安装 RabbitMQ 客户端
- `kombu` 和 `amqp` 是 Celery 的依赖，会自动安装
- 如果只用 RabbitMQ 作为 Broker，Result Backend 可以继续用 Redis

### 2. **配置文件（app/config.py）**

**当前 Redis 方案：**
```python
# ==================== Redis 配置（可选）====================
redis_url: Optional[str] = Field(
    default=None,
    description="Redis 连接 URL，格式：redis://host:port/db",
)

# ==================== Celery 配置（可选）====================
celery_broker_url: Optional[str] = Field(
    default=None,
    description="Celery Broker URL，通常使用 Redis",
)
celery_result_backend: Optional[str] = Field(
    default=None,
    description="Celery 结果后端 URL，通常使用 Redis",
)
```

**改为 RabbitMQ 方案：**
```python
# ==================== RabbitMQ 配置（可选）====================
rabbitmq_url: Optional[str] = Field(
    default=None,
    description="RabbitMQ 连接 URL，格式：amqp://user:password@host:port/vhost",
)

# ==================== Redis 配置（可选，用于 Result Backend）====================
redis_url: Optional[str] = Field(
    default=None,
    description="Redis 连接 URL（用于 Result Backend），格式：redis://host:port/db",
)

# ==================== Celery 配置（可选）====================
celery_broker_url: Optional[str] = Field(
    default=None,
    description="Celery Broker URL，使用 RabbitMQ：amqp://user:password@host:port/vhost",
)
celery_result_backend: Optional[str] = Field(
    default=None,
    description="Celery 结果后端 URL，可以使用 Redis 或 RabbitMQ",
)
```

### 3. **环境变量（env.example）**

**Redis 方案：**
```bash
# ==================== Redis 配置（可选）====================
# REDIS_URL=redis://localhost:6379/0

# ==================== Celery 配置（可选）====================
# CELERY_BROKER_URL=redis://localhost:6379/1
# CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

**RabbitMQ 方案：**
```bash
# ==================== RabbitMQ 配置（可选）====================
# RABBITMQ_URL=amqp://guest:guest@localhost:5672/
# 或者
# CELERY_BROKER_URL=amqp://guest:guest@localhost:5672/

# ==================== Redis 配置（可选，用于 Result Backend）====================
# REDIS_URL=redis://localhost:6379/0

# ==================== Celery 配置（可选）====================
# CELERY_BROKER_URL=amqp://guest:guest@localhost:5672/
# CELERY_RESULT_BACKEND=redis://localhost:6379/0  # 或使用 RabbitMQ
```

### 4. **Celery 应用配置（app/tasks/celery_app.py）**

**Redis 方案：**
```python
from celery import Celery
from app.config import settings

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url or "redis://localhost:6379/1",
    backend=settings.celery_result_backend or "redis://localhost:6379/2",
)
```

**RabbitMQ 方案：**
```python
from celery import Celery
from app.config import settings

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url or "amqp://guest:guest@localhost:5672//",
    backend=settings.celery_result_backend or "redis://localhost:6379/0",  # 仍可用 Redis
)
```

### 5. **Docker 部署配置**

**Redis 方案（docker-compose.yml）：**
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

**RabbitMQ 方案（docker-compose.yml）：**
```yaml
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"    # AMQP 端口
      - "15672:15672"  # 管理界面端口
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  # 如果仍需要 Redis 作为 Result Backend
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  rabbitmq_data:
  redis_data:
```

### 6. **文档更新**

需要更新以下文档：
- `README.md` - 技术栈说明
- `docs/开发计划.md` - Celery 配置说明
- `env.example` - 环境变量示例

## 三、URL 格式对比

### Redis URL 格式
```
redis://[password@]host[:port][/db]
redis://localhost:6379/1
redis://:password@localhost:6379/0
```

### RabbitMQ URL 格式
```
amqp://[user:password@]host[:port][/vhost]
amqp://guest:guest@localhost:5672/
amqp://admin:password@localhost:5672/my_vhost
```

**注意：**
- RabbitMQ 的 vhost 路径必须以 `/` 开头
- 默认 vhost 是 `/`，可以省略
- 如果指定 vhost，格式为 `/vhost_name`

## 四、功能对比

| 特性 | Redis | RabbitMQ |
|------|-------|----------|
| **作为 Broker** | ✅ 支持 | ✅ 支持（推荐） |
| **作为 Result Backend** | ✅ 支持 | ✅ 支持（但性能不如 Redis） |
| **消息持久化** | 需配置 | 默认支持 |
| **消息确认机制** | 基础支持 | 完整支持（ACK/NACK） |
| **路由功能** | 简单 | 强大（Exchange、Queue、Routing Key） |
| **管理界面** | 无（需第三方工具） | 自带 Web 管理界面 |
| **性能** | 高（内存存储） | 较高 |
| **资源占用** | 低 | 中等 |
| **配置复杂度** | 简单 | 中等 |
| **生产环境适用性** | 中小型项目 | 大型项目推荐 |

## 五、推荐方案

### 方案 A：纯 RabbitMQ（推荐用于生产环境）
```
Broker: RabbitMQ
Result Backend: RabbitMQ 或 Redis
```
- **优点：** 功能完整、可靠性高、适合生产环境
- **缺点：** 需要部署 RabbitMQ，资源占用稍高

### 方案 B：混合方案（推荐）
```
Broker: RabbitMQ
Result Backend: Redis
```
- **优点：** 兼顾可靠性和性能
- **缺点：** 需要同时部署两个服务

### 方案 C：纯 Redis（适合开发/小型项目）
```
Broker: Redis
Result Backend: Redis
```
- **优点：** 简单、轻量、快速
- **缺点：** 功能相对简单，不适合大型生产环境

## 六、迁移步骤

如果要从 Redis 迁移到 RabbitMQ：

1. **更新依赖**
   ```bash
   # 无需额外安装，Celery 已支持 RabbitMQ
   ```

2. **更新配置**
   - 修改 `app/config.py`
   - 更新 `.env` 文件中的连接 URL

3. **更新 Docker 配置**
   - 添加 RabbitMQ 服务
   - 更新环境变量

4. **测试验证**
   ```bash
   # 启动 RabbitMQ
   docker-compose up -d rabbitmq
   
   # 启动 Celery Worker
   celery -A app.tasks.celery_app worker --loglevel=info
   
   # 测试任务提交
   ```

5. **更新文档**
   - README.md
   - docs/开发计划.md
   - env.example

## 七、总结

**改为 RabbitMQ 的主要影响：**

1. ✅ **依赖包：** 无需额外安装（Celery 已支持）
2. ✅ **配置文件：** 需要修改 URL 格式和描述
3. ✅ **环境变量：** 需要更新连接字符串格式
4. ✅ **Docker 配置：** 需要添加 RabbitMQ 服务
5. ✅ **文档：** 需要更新相关说明

**代码层面影响很小：**
- Celery 应用初始化代码基本相同
- 任务定义代码无需修改
- 只是连接 URL 格式不同

**建议：**
- 开发环境：继续使用 Redis（简单快速）
- 生产环境：使用 RabbitMQ（功能完整、可靠性高）
- 混合方案：RabbitMQ 作为 Broker，Redis 作为 Result Backend（最佳实践）

