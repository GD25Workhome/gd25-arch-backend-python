# WebSocket 基础原理

本文档从基础原理的角度介绍 WebSocket 技术，包括原理、技术栈、应用场景等内容。

## 目录

- [什么是 WebSocket](#什么是-websocket)
- [WebSocket 原理](#websocket-原理)
  - [协议升级机制](#协议升级机制)
  - [连接建立过程](#连接建立过程)
  - [数据帧格式](#数据帧格式)
  - [心跳机制](#心跳机制)
- [技术栈](#技术栈)
  - [协议标准](#协议标准)
  - [服务端实现](#服务端实现)
  - [客户端实现](#客户端实现)
  - [相关工具](#相关工具)
- [WebSocket vs HTTP](#websocket-vs-http)
  - [HTTP 轮询](#http-轮询)
  - [HTTP 长轮询](#http-长轮询)
  - [Server-Sent Events (SSE)](#server-sent-events-sse)
  - [WebSocket](#websocket)
- [应用场景](#应用场景)
  - [实时通信](#实时通信)
  - [实时数据推送](#实时数据推送)
  - [协作编辑](#协作编辑)
  - [游戏应用](#游戏应用)
  - [监控和日志](#监控和日志)
- [架构设计](#架构设计)
  - [单机架构](#单机架构)
  - [分布式架构](#分布式架构)
  - [负载均衡](#负载均衡)
- [安全性考虑](#安全性考虑)
  - [协议升级安全](#协议升级安全)
  - [消息验证](#消息验证)
  - [连接限制](#连接限制)
- [性能优化](#性能优化)
  - [连接管理](#连接管理)
  - [消息压缩](#消息压缩)
  - [心跳优化](#心跳优化)
- [本项目实现](#本项目实现)

---

## 什么是 WebSocket

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议。它允许服务端主动向客户端推送数据，解决了传统 HTTP 请求-响应模式无法实现实时双向通信的问题。

### 核心特性

- **全双工通信**：客户端和服务端可以同时发送和接收数据
- **持久连接**：建立连接后保持打开状态，无需重复建立连接
- **低延迟**：相比 HTTP 轮询，延迟更低
- **低开销**：数据帧头部开销小（2-14 字节）
- **支持二进制和文本**：可以传输文本和二进制数据

---

## WebSocket 原理

### 协议升级机制

WebSocket 连接通过 HTTP 协议升级建立，这是一个"握手"过程：

1. **客户端发起升级请求**
   ```
   GET /ws HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
   Sec-WebSocket-Version: 13
   ```

2. **服务端响应升级**
   ```
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
   ```

3. **连接升级完成**
   - HTTP 连接升级为 WebSocket 连接
   - 后续通信使用 WebSocket 协议

### 连接建立过程

```
客户端                          服务端
   |                              |
   |--- HTTP Upgrade Request ---->|
   |                              |
   |<-- 101 Switching Protocols --|
   |                              |
   |=== WebSocket 连接建立 ===|
   |                              |
   |<==== 双向数据传输 =====>|
   |                              |
```

**关键点：**
- 使用 HTTP 101 状态码表示协议切换
- `Sec-WebSocket-Key` 用于安全验证
- `Sec-WebSocket-Accept` 是服务端对 Key 的响应
- 升级后，底层 TCP 连接保持不变

### 数据帧格式

WebSocket 数据以帧（Frame）的形式传输，每个帧包含：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1 |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

**帧字段说明：**

- **FIN (1 bit)**：表示这是消息的最后一个片段
- **RSV (3 bits)**：保留字段，必须为 0
- **Opcode (4 bits)**：
  - `0x0`：连续帧
  - `0x1`：文本帧
  - `0x2`：二进制帧
  - `0x8`：连接关闭
  - `0x9`：Ping
  - `0xA`：Pong
- **MASK (1 bit)**：客户端发送的帧必须掩码，服务端发送的帧不能掩码
- **Payload Length (7/16/64 bits)**：负载长度
- **Masking-Key (32 bits)**：掩码密钥（仅客户端发送时存在）
- **Payload Data**：实际数据

### 心跳机制

WebSocket 使用 Ping/Pong 帧实现心跳检测：

1. **服务端发送 Ping**
   - 定期发送 Ping 帧（opcode `0x9`）
   - 检测连接是否存活

2. **客户端响应 Pong**
   - 收到 Ping 后自动回复 Pong（opcode `0xA`）
   - 也可以主动发送 Pong

3. **超时处理**
   - 如果长时间未收到 Pong，认为连接断开
   - 主动关闭连接并清理资源

**本项目实现：**
- 客户端可以发送 `{"type": "ping"}` 消息
- 服务端响应 `{"type": "pong"}` 消息
- 用于保持连接活跃和检测连接状态

---

## 技术栈

### 协议标准

- **RFC 6455**：WebSocket 协议标准（2011年）
- **RFC 7692**：WebSocket 压缩扩展（permessage-deflate）
- **W3C WebSocket API**：浏览器 WebSocket API 标准

### 服务端实现

#### Python

- **FastAPI**：现代 Python Web 框架，内置 WebSocket 支持
  ```python
  @app.websocket("/ws/{user_id}")
  async def websocket_endpoint(websocket: WebSocket, user_id: str):
      await websocket.accept()
      # 处理连接
  ```

- **Django Channels**：Django 的 WebSocket 支持
- **Tornado**：异步 Web 框架，支持 WebSocket
- **aiohttp**：异步 HTTP 客户端/服务器，支持 WebSocket

#### Node.js

- **Socket.io**：最流行的 WebSocket 库，支持自动降级
- **ws**：轻量级 WebSocket 库
- **uWebSockets**：高性能 WebSocket 库

#### Java

- **Spring WebSocket**：Spring 框架的 WebSocket 支持
- **Jetty WebSocket**：Jetty 服务器的 WebSocket 实现
- **Netty**：高性能网络框架，支持 WebSocket

#### Go

- **gorilla/websocket**：Go 语言的 WebSocket 实现
- **nhooyr.io/websocket**：现代 Go WebSocket 库

### 客户端实现

#### 浏览器

- **原生 WebSocket API**：所有现代浏览器都支持
  ```javascript
  const ws = new WebSocket('ws://example.com/ws');
  ws.onopen = () => console.log('Connected');
  ws.onmessage = (event) => console.log(event.data);
  ws.send('Hello');
  ```

#### Python

- **websockets**：异步 WebSocket 客户端/服务器库
- **websocket-client**：同步 WebSocket 客户端库

#### 其他语言

- **Java**：Java-WebSocket、Tyrus
- **C#**：System.Net.WebSockets
- **Go**：gorilla/websocket

### 相关工具

- **wscat**：命令行 WebSocket 客户端工具
- **Postman**：支持 WebSocket 测试
- **Chrome DevTools**：可以查看 WebSocket 连接和消息

---

## WebSocket vs HTTP

### HTTP 轮询

**工作原理：**
- 客户端定期发送 HTTP 请求
- 服务端立即响应（有数据或空响应）

**缺点：**
- 高延迟：需要等待轮询间隔
- 资源浪费：大量无效请求
- 实时性差：无法及时获取更新

**示例：**
```javascript
// 每 1 秒轮询一次
setInterval(() => {
  fetch('/api/updates')
    .then(res => res.json())
    .then(data => console.log(data));
}, 1000);
```

### HTTP 长轮询

**工作原理：**
- 客户端发送 HTTP 请求
- 服务端保持连接打开，直到有数据或超时
- 客户端收到响应后立即发送新请求

**优点：**
- 比短轮询延迟更低
- 减少无效请求

**缺点：**
- 仍然需要频繁建立连接
- 服务端需要维护大量连接
- 每次请求都有 HTTP 头部开销

**示例：**
```javascript
function longPoll() {
  fetch('/api/updates')
    .then(res => res.json())
    .then(data => {
      console.log(data);
      longPoll(); // 立即发起下一次请求
    });
}
```

### Server-Sent Events (SSE)

**工作原理：**
- 客户端发送 HTTP 请求
- 服务端保持连接打开，持续推送数据
- 单向通信（服务端 → 客户端）

**优点：**
- 自动重连
- 简单易用
- 基于 HTTP，兼容性好

**缺点：**
- 只能服务端推送，客户端无法发送数据
- 不支持二进制数据

**示例：**
```javascript
const eventSource = new EventSource('/api/events');
eventSource.onmessage = (event) => {
  console.log(event.data);
};
```

### WebSocket

**工作原理：**
- 通过 HTTP 升级建立持久连接
- 双向全双工通信
- 低延迟、低开销

**优点：**
- ✅ 真正的双向通信
- ✅ 低延迟
- ✅ 低开销（小数据帧头部）
- ✅ 支持二进制和文本
- ✅ 持久连接，无需重复握手

**缺点：**
- ❌ 需要服务端和客户端都支持
- ❌ 代理服务器可能不支持
- ❌ 连接管理更复杂

**对比表：**

| 特性 | HTTP 轮询 | HTTP 长轮询 | SSE | WebSocket |
|------|----------|------------|-----|-----------|
| 延迟 | 高 | 中 | 低 | 最低 |
| 开销 | 高 | 中 | 低 | 最低 |
| 双向通信 | ✅ | ✅ | ❌ | ✅ |
| 浏览器支持 | ✅ | ✅ | ✅ | ✅ |
| 实现复杂度 | 低 | 中 | 低 | 中 |
| 适用场景 | 低频更新 | 中频更新 | 服务端推送 | 实时交互 |

---

## 应用场景

### 实时通信

**聊天应用**
- 即时消息（IM）
- 群聊
- 私聊
- 消息状态（已读、正在输入等）

**示例：**
```python
# 用户 A 发送消息给用户 B
await manager.send_personal_message(
    {"type": "chat", "content": "Hello"},
    "user_b"
)
```

### 实时数据推送

**金融数据**
- 股票价格实时更新
- 交易数据推送
- 市场行情

**IoT 数据**
- 传感器数据实时推送
- 设备状态监控
- 实时告警

**示例：**
```python
# 推送股票价格更新
await manager.broadcast({
    "type": "stock_price",
    "symbol": "AAPL",
    "price": 150.25
})
```

### 协作编辑

**在线文档**
- 多人同时编辑
- 实时同步光标位置
- 冲突解决

**代码协作**
- 实时代码共享
- 协同调试

### 游戏应用

**多人在线游戏**
- 实时位置同步
- 游戏状态更新
- 玩家交互

**示例：**
```python
# 推送玩家位置更新
await manager.broadcast({
    "type": "player_move",
    "player_id": "player_1",
    "x": 100,
    "y": 200
})
```

### 监控和日志

**系统监控**
- 实时系统指标
- 性能监控
- 告警通知

**日志流**
- 实时日志查看
- 调试信息推送

**示例：**
```python
# 推送系统监控数据
await manager.broadcast({
    "type": "monitor",
    "cpu": 45.2,
    "memory": 60.5,
    "timestamp": 1234567890
})
```

### 其他场景

- **在线客服**：实时客服对话
- **直播弹幕**：实时弹幕推送
- **在线教育**：实时互动、白板协作
- **社交网络**：实时通知、动态更新

---

## 架构设计

### 单机架构

**简单场景：**
```
客户端1 ──┐
客户端2 ──┼──> WebSocket 服务器 ──> 数据库
客户端3 ──┘
```

**特点：**
- 所有连接在同一服务器
- 连接管理简单
- 适合小规模应用

**本项目实现：**
- 使用 `ConnectionManager` 管理所有连接
- 连接存储在内存中（字典）
- 支持单服务器场景

### 分布式架构

**多服务器场景：**
```
客户端1 ──┐
客户端2 ──┼──> WebSocket 服务器 1 ──┐
客户端3 ──┘                          │
                                     ├──> 消息队列 ──> 数据库
客户端4 ──┐                          │
客户端5 ──┼──> WebSocket 服务器 2 ──┘
客户端6 ──┘
```

**挑战：**
- 跨服务器消息推送
- 连接状态同步
- 负载均衡

**解决方案：**
1. **消息队列（Redis Pub/Sub、RabbitMQ）**
   ```python
   # 服务器 1 收到消息，通过消息队列通知服务器 2
   await redis.publish("websocket:user_123", message)
   ```

2. **共享状态（Redis）**
   ```python
   # 连接信息存储在 Redis
   await redis.sadd("websocket:connections", connection_id)
   ```

3. **Sticky Session（会话粘性）**
   - 同一用户的所有连接路由到同一服务器
   - 使用负载均衡器的会话保持功能

### 负载均衡

**问题：**
- WebSocket 是持久连接，不能像 HTTP 那样简单负载均衡

**解决方案：**

1. **Layer 4 负载均衡（IP 层）**
   - 基于 IP 和端口
   - 连接建立后保持到同一服务器
   - 例如：HAProxy、Nginx Stream

2. **Layer 7 负载均衡（应用层）**
   - 基于 HTTP 头部（如用户 ID）
   - 需要支持 WebSocket 升级
   - 例如：Nginx、HAProxy

**Nginx 配置示例：**
```nginx
upstream websocket {
    server 127.0.0.1:8100;
    server 127.0.0.1:8001;
}

server {
    location /ws/ {
        proxy_pass http://websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

---

## 安全性考虑

### 协议升级安全

**Sec-WebSocket-Key 验证：**
- 客户端发送随机生成的 `Sec-WebSocket-Key`
- 服务端使用固定算法计算 `Sec-WebSocket-Accept`
- 防止非 WebSocket 客户端连接

**实现：**
```python
import base64
import hashlib

def generate_accept(key: str) -> str:
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    combined = key + GUID
    sha1 = hashlib.sha1(combined.encode()).digest()
    return base64.b64encode(sha1).decode()
```

### 消息验证

**身份认证：**
- 在 WebSocket 升级时验证用户身份
- 使用 Token 或 Session
- 拒绝未认证的连接

**示例：**
```python
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, token: str):
    # 验证 token
    if not verify_token(token):
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    await manager.connect(websocket, user_id)
```

**消息内容验证：**
- 验证消息格式
- 防止注入攻击
- 限制消息大小

### 连接限制

**防止资源耗尽：**
- 限制每个 IP 的连接数
- 限制每个用户的连接数
- 实现连接超时

**示例：**
```python
class ConnectionManager:
    MAX_CONNECTIONS_PER_USER = 5
    MAX_CONNECTIONS_PER_IP = 10
    
    async def connect(self, websocket: WebSocket, user_id: str):
        # 检查连接数限制
        if len(self.active_connections.get(user_id, set())) >= self.MAX_CONNECTIONS_PER_USER:
            await websocket.close(code=1008, reason="Too many connections")
            return
        # ...
```

### 其他安全措施

- **使用 WSS（WebSocket Secure）**：在生产环境使用 `wss://`
- **CORS 配置**：限制允许的来源
- **速率限制**：防止消息洪水攻击
- **输入验证**：验证所有接收的消息

---

## 性能优化

### 连接管理

**连接池：**
- 复用连接对象
- 减少内存占用
- 快速查找连接

**本项目实现：**
```python
# 使用字典和集合管理连接
self.active_connections: Dict[str, Set[WebSocket]] = {}
self.connection_to_user: Dict[WebSocket, str] = {}
```

**连接清理：**
- 及时清理断开的连接
- 定期检查连接状态
- 使用心跳检测

### 消息压缩

**permessage-deflate 扩展：**
- WebSocket 支持压缩扩展
- 减少网络传输量
- 适合文本消息

**启用压缩：**
```python
# FastAPI 自动支持压缩（如果客户端支持）
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    # 如果客户端支持，会自动启用压缩
```

### 心跳优化

**自适应心跳：**
- 根据网络状况调整心跳间隔
- 减少不必要的心跳消息
- 快速检测断线

**示例：**
```python
class ConnectionManager:
    def __init__(self):
        self.heartbeat_interval = 30  # 默认 30 秒
        self.heartbeat_timeout = 60   # 60 秒未响应认为断开
    
    async def send_heartbeat(self, websocket: WebSocket):
        try:
            await websocket.send_json({"type": "ping"})
        except:
            # 连接已断开，清理
            await self.disconnect(websocket)
```

### 批量消息

**合并小消息：**
- 将多个小消息合并发送
- 减少网络往返
- 适合高频更新场景

**示例：**
```python
class MessageBuffer:
    def __init__(self, max_size=10, max_wait=0.1):
        self.buffer = []
        self.max_size = max_size
        self.max_wait = max_wait
    
    async def add_and_send(self, message, websocket):
        self.buffer.append(message)
        if len(self.buffer) >= self.max_size:
            await self.flush(websocket)
    
    async def flush(self, websocket):
        if self.buffer:
            await websocket.send_json({"type": "batch", "messages": self.buffer})
            self.buffer.clear()
```

---

## 本项目实现

### 架构概览

本项目实现了基于 FastAPI 的 WebSocket 模块，包括：

1. **ConnectionManager** (`app/websocket/manager.py`)
   - 连接管理
   - 消息推送（个人、广播）
   - 连接统计

2. **WebSocketHandler** (`app/websocket/handler.py`)
   - 连接处理框架
   - 消息接收框架
   - 扩展接口

3. **路由集成** (`app/main.py`)
   - WebSocket 端点定义
   - 使用示例

### 核心特性

- ✅ 支持多用户连接
- ✅ 支持一个用户多个连接（多设备）
- ✅ 个人消息推送
- ✅ 广播消息推送
- ✅ 连接状态跟踪
- ✅ Ping/Pong 心跳支持
- ✅ 消息回显功能
- ✅ 统计接口

### 使用示例

**服务端：**
```python
from app.websocket import manager

# 广播消息
await manager.broadcast({"type": "announcement", "content": "系统通知"})

# 个人消息
await manager.send_personal_message(
    {"type": "notification", "content": "个人消息"},
    "user_id"
)
```

**客户端：**
```javascript
const ws = new WebSocket('ws://localhost:8100/ws/test_user');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('收到消息:', data);
};

ws.send(JSON.stringify({
    type: 'ping',
    timestamp: Date.now()
}));
```

### 扩展建议

1. **添加身份认证**
   - Token 验证
   - 用户权限检查

2. **添加消息队列支持**
   - Redis Pub/Sub
   - RabbitMQ
   - 支持分布式部署

3. **添加消息持久化**
   - 离线消息存储
   - 消息历史记录

4. **添加房间/频道功能**
   - 支持分组通信
   - 房间管理

5. **性能监控**
   - 连接数监控
   - 消息吞吐量监控
   - 延迟监控

---

## 总结

WebSocket 是一种强大的实时通信技术，适用于需要双向实时通信的场景。通过理解其原理、技术栈和应用场景，可以更好地设计和实现 WebSocket 应用。

**关键要点：**
- WebSocket 通过 HTTP 升级建立持久连接
- 支持全双工通信，低延迟、低开销
- 适用于实时通信、数据推送、协作编辑等场景
- 需要考虑安全性、性能和可扩展性

**相关文档：**
- [WebSocket 测试说明](./websocket测试说明.md)：详细的测试方法和示例
- [开发计划](../开发计划.md)：项目开发计划和进度

