# Flower 监控配置说明

## 概述

Flower 是 Celery 的实时 Web 监控工具，用于监控和管理 Celery 任务执行情况。本文档说明如何配置和使用 Flower。

## 功能特性

- **实时监控**：查看正在执行、等待、成功、失败的任务
- **Worker 管理**：查看 Worker 状态、性能指标、资源使用情况
- **任务历史**：查看任务执行历史、耗时、结果
- **任务控制**：可以撤销、终止正在执行的任务
- **性能统计**：任务执行时间、吞吐量、成功率等统计信息
- **任务详情**：查看任务的参数、结果、异常信息等

## 安装

### 方式一：从 requirements.txt 安装（推荐）

在 `requirements.txt` 中取消注释 Flower 依赖：

```bash
# 取消注释这一行
flower>=2.0.0,<3.0.0
```

然后安装：

```bash
pip install -r requirements.txt
```

### 方式二：单独安装

```bash
pip install flower
```

## 配置

### 环境变量配置

在 `.env` 文件中添加以下配置（可选）：

```bash
# Flower 监控配置
FLOWER_PORT=5555                    # Flower 服务端口（默认：5555）
FLOWER_BASIC_AUTH=admin:admin123    # 基本认证（生产环境建议配置，格式：username:password）
FLOWER_URL_PREFIX=/flower           # URL 前缀（用于反向代理，可选）
```

### 配置说明

#### 1. FLOWER_PORT

Flower Web 服务的监听端口，默认值为 `5555`。

```bash
FLOWER_PORT=5555
```

#### 2. FLOWER_BASIC_AUTH（生产环境强烈建议配置）

基本认证配置，格式为 `username:password`。**生产环境必须配置**，防止未授权访问。

```bash
FLOWER_BASIC_AUTH=admin:admin123
```

#### 3. FLOWER_URL_PREFIX（可选）

URL 前缀，用于反向代理场景。例如，如果配置为 `/flower`，访问地址为 `http://localhost:5555/flower`。

```bash
FLOWER_URL_PREFIX=/flower
```

## 启动方式

### 方式一：使用启动脚本（推荐）

```bash
# 使用默认配置启动
bash scripts/start_flower.sh

# 或使用环境变量自定义配置
FLOWER_PORT=5555 FLOWER_BASIC_AUTH=admin:admin123 bash scripts/start_flower.sh
```

### 方式二：直接使用 Celery 命令

```bash
# 基本启动
celery -A app.tasks.celery_app flower --port=5555

# 带基本认证
celery -A app.tasks.celery_app flower --port=5555 --basic_auth=admin:admin123

# 带 URL 前缀
celery -A app.tasks.celery_app flower --port=5555 --url_prefix=/flower
```

### 方式三：使用 Python 代码启动

```python
from app.tasks.celery_app import celery_app
from flower.command import FlowerCommand

# 创建 Flower 命令实例
flower = FlowerCommand()
flower.app = celery_app
flower.port = 5555
flower.basic_auth = "admin:admin123"  # 可选
flower.url_prefix = "/flower"  # 可选

# 启动 Flower
flower.run()
```

## 访问监控界面

启动 Flower 后，在浏览器中访问：

- **开发环境**：http://localhost:5555
- **带 URL 前缀**：http://localhost:5555/flower（如果配置了 `FLOWER_URL_PREFIX=/flower`）

如果配置了基本认证，会弹出登录对话框，输入配置的用户名和密码。

## 主要功能说明

### 1. Dashboard（仪表盘）

- **Workers**：显示所有 Worker 的状态、活跃任务数、处理的任务总数
- **Tasks**：显示任务统计信息（总数、成功、失败、重试等）
- **Graphs**：显示任务执行时间、吞吐量等图表

### 2. Workers（Worker 管理）

- 查看每个 Worker 的详细信息
- 查看 Worker 的 CPU、内存使用情况
- 查看 Worker 处理的任务列表
- 可以关闭 Worker（谨慎操作）

### 3. Tasks（任务管理）

- **Active**：正在执行的任务
- **Reserved**：已保留但未开始执行的任务
- **Scheduled**：计划执行的任务
- **Revoked**：已撤销的任务
- **Success**：成功完成的任务
- **Failed**：执行失败的任务

### 4. Task Details（任务详情）

点击任务可以查看详细信息：
- 任务 ID、名称、状态
- 任务参数（args、kwargs）
- 任务结果
- 执行时间、耗时
- 异常信息（如果失败）
- 可以撤销或重试任务

### 5. Monitor（监控）

- 实时任务执行监控
- 任务执行时间统计
- 任务成功率统计
- Worker 性能监控

## 生产环境配置建议

### 1. 必须配置基本认证

```bash
FLOWER_BASIC_AUTH=your_username:your_strong_password
```

### 2. 使用反向代理（推荐）

使用 Nginx 或 Apache 作为反向代理，提供 HTTPS 支持：

```nginx
# Nginx 配置示例
location /flower {
    proxy_pass http://localhost:5555;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 3. 限制访问 IP（可选）

在启动脚本中添加 IP 限制：

```bash
celery -A app.tasks.celery_app flower \
    --port=5555 \
    --basic_auth=admin:admin123 \
    --address=127.0.0.1  # 只允许本地访问
```

### 4. 使用系统服务（systemd）

创建 systemd 服务文件 `/etc/systemd/system/flower.service`：

```ini
[Unit]
Description=Flower Celery Monitor
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/project
Environment="FLOWER_PORT=5555"
Environment="FLOWER_BASIC_AUTH=admin:admin123"
ExecStart=/path/to/venv/bin/celery -A app.tasks.celery_app flower --port=${FLOWER_PORT} --basic_auth=${FLOWER_BASIC_AUTH}
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable flower
sudo systemctl start flower
sudo systemctl status flower
```

## 常见问题

### 1. 无法连接到 Broker

**问题**：Flower 启动后无法显示 Worker 信息。

**解决方案**：
- 检查 Celery Broker 配置是否正确
- 确保 RabbitMQ/Redis 服务正在运行
- 检查网络连接和防火墙设置

### 2. 认证失败

**问题**：配置了基本认证但无法登录。

**解决方案**：
- 检查 `FLOWER_BASIC_AUTH` 格式是否正确（`username:password`）
- 确保没有多余的空格
- 检查用户名和密码是否包含特殊字符（可能需要 URL 编码）

### 3. 端口被占用

**问题**：启动 Flower 时提示端口被占用。

**解决方案**：
- 更改 `FLOWER_PORT` 环境变量
- 或使用 `--port` 参数指定其他端口
- 检查是否有其他 Flower 实例正在运行

### 4. Worker 不显示

**问题**：Flower 界面中看不到 Worker。

**解决方案**：
- 确保 Celery Worker 正在运行
- 检查 Worker 是否连接到同一个 Broker
- 检查 Worker 的日志，确认连接正常

## 与 Celery Worker 配合使用

### 启动顺序

1. **启动 RabbitMQ/Redis**（Broker）
2. **启动 Celery Worker**
3. **启动 Flower**（监控工具）

### 完整启动示例

```bash
# 1. 启动 RabbitMQ（如果使用 Docker）
docker start rabbitmq-gd25

# 2. 启动 Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# 3. 启动 Flower（新终端窗口）
bash scripts/start_flower.sh
```

## 相关文档

- [Celery 官方文档](https://docs.celeryq.dev/)
- [Flower GitHub 仓库](https://github.com/mher/flower)
- [Flower 官方文档](https://flower.readthedocs.io/)

## 注意事项

1. **性能影响**：Flower 会定期查询 Broker 和 Worker，对性能有轻微影响，生产环境建议限制访问频率
2. **安全性**：生产环境必须配置基本认证，建议使用 HTTPS
3. **资源消耗**：Flower 本身资源消耗较小，但大量任务历史可能占用内存
4. **数据保留**：Flower 默认不持久化任务历史，重启后会丢失（可以通过配置持久化）

