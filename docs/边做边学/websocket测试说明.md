# WebSocket 测试说明

本文档介绍如何测试 WebSocket 功能，提供多种测试方法供选择。

## 目录

- [前置准备](#前置准备)
- [测试方法](#测试方法)
  - [方法一：浏览器控制台测试（最简单）](#方法一浏览器控制台测试最简单)
  - [方法二：Python 单元测试（推荐）](#方法二python-单元测试推荐)
  - [方法三：命令行工具测试](#方法三命令行工具测试)
  - [方法四：Python 客户端脚本](#方法四python-客户端脚本)
- [测试场景](#测试场景)
- [常见问题](#常见问题)

---

## 前置准备

### 1. 启动服务

首先需要启动 FastAPI 应用：

```bash
# 方式一：使用 uvicorn 直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式二：使用项目启动脚本
bash scripts/start_dev.sh
```

服务启动后，WebSocket 端点地址为：`ws://localhost:8000/ws/{user_id}`

### 2. 确认服务运行

访问健康检查接口确认服务正常运行：

```bash
curl http://localhost:8000/health
```

---

## 测试方法

### 方法一：浏览器控制台测试（最简单）

这是最快速、最简单的测试方法，适合快速验证功能。

#### 步骤

**⚠️ 重要提示：** 如果遇到 CSP（Content Security Policy）错误，请使用 HTML 测试页面（方法一）或 Python 测试脚本。

1. 打开浏览器（Chrome、Firefox、Edge 等）
2. **在新标签页中打开任意网站**（如 `about:blank` 或 `https://www.example.com`）
   - ⚠️ 不要在扩展页面、Chrome 内部页面等有 CSP 限制的页面运行
3. 按 `F12` 打开开发者工具
4. 切换到 `Console` 标签
5. 复制并执行以下代码：

```javascript
// 创建 WebSocket 连接
const ws = new WebSocket('ws://localhost:8000/ws/test_user');

// 连接成功
ws.onopen = () => {
  console.log('✅ WebSocket 连接已建立');
  
  // 发送 ping 消息
  ws.send(JSON.stringify({
    type: 'ping',
    timestamp: Date.now()
  }));
};

// 接收消息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('📨 收到消息:', data);
  
  // 根据消息类型处理
  if (data.type === 'welcome') {
    console.log('👋 欢迎消息:', data.message);
  } else if (data.type === 'pong') {
    console.log('🏓 Pong 响应:', data);
  }
};

// 连接错误
ws.onerror = (error) => {
  console.error('❌ WebSocket 错误:', error);
};

// 连接关闭
ws.onclose = (event) => {
  console.log('🔌 WebSocket 连接已关闭', event.code, event.reason);
};

// 发送其他消息（可以在控制台手动调用）
window.sendMessage = (type, content) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type, content }));
  } else {
    console.error('WebSocket 未连接');
  }
};
```

#### 测试示例

在控制台中执行：

```javascript
// 发送 echo 消息
sendMessage('echo', 'Hello, WebSocket!');

// 发送自定义消息
ws.send(JSON.stringify({
  type: 'custom',
  data: { message: '测试消息' }
}));
```

#### 优点

- ✅ 无需安装任何工具
- ✅ 即时反馈，所见即所得
- ✅ 适合快速验证功能

#### 缺点

- ❌ 无法自动化测试
- ❌ 不适合复杂测试场景
- ⚠️ 可能受到页面 CSP 策略限制

#### ⚠️ 常见错误：CSP 限制

如果遇到以下错误：
```
Refused to connect to 'ws://localhost:8000/ws/test_user' because it violates 
the following Content Security Policy directive: "connect-src ..."
```

**原因：** 当前页面有 Content Security Policy 限制，不允许连接 WebSocket。

**解决方案：**
1. **推荐：使用 HTML 测试页面**（见下方"方法一：HTML 测试页面"）
2. 在新标签页打开 `about:blank` 或任意普通网站，然后在控制台运行代码
3. 使用 Python 测试脚本（见"方法四"）

---

### 方法一：HTML 测试页面（推荐，最简单，无 CSP 限制）

使用项目提供的 HTML 测试页面，提供图形化界面，不受 CSP 限制。

#### 使用步骤

1. **启动服务**：
   ```bash
   uvicorn app.main:app --reload
   ```

2. **打开测试页面**：
   ```bash
   # 方式一：直接在浏览器中打开文件
   open tests/websocket_test.html
   
   # 方式二：双击 tests/websocket_test.html 文件
   
   # 方式三：使用 Python 启动简单 HTTP 服务器
   cd tests
   python -m http.server 8080
   # 然后在浏览器访问 http://localhost:8080/websocket_test.html
   ```

3. **使用界面**：
   - 输入用户 ID（默认：`test_user`）
   - 点击"连接"按钮
   - 使用快捷按钮测试 Ping、Echo 等功能
   - 查看实时消息日志

#### 优点

- ✅ 图形化界面，操作简单
- ✅ 实时查看消息
- ✅ 不受 CSP 限制
- ✅ 无需编写代码
- ✅ 支持多种消息类型测试

#### 缺点

- ❌ 需要手动操作
- ❌ 无法自动化测试

---

### 方法二：浏览器控制台测试

在浏览器控制台中直接运行 JavaScript 代码测试。

#### 步骤

**⚠️ 重要提示：** 如果遇到 CSP（Content Security Policy）错误，请使用 HTML 测试页面（方法一）或 Python 测试脚本。

1. 打开浏览器（Chrome、Firefox、Edge 等）
2. **在新标签页中打开任意网站**（如 `about:blank` 或 `https://www.example.com`）
   - ⚠️ 不要在扩展页面、Chrome 内部页面等有 CSP 限制的页面运行
3. 按 `F12` 打开开发者工具
4. 切换到 `Console` 标签
5. 复制并执行以下代码：

```javascript
// 创建 WebSocket 连接
const ws = new WebSocket('ws://localhost:8000/ws/test_user');

// 连接成功
ws.onopen = () => {
  console.log('✅ WebSocket 连接已建立');
  
  // 发送 ping 消息
  ws.send(JSON.stringify({
    type: 'ping',
    timestamp: Date.now()
  }));
};

// 接收消息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('📨 收到消息:', data);
  
  // 根据消息类型处理
  if (data.type === 'welcome') {
    console.log('👋 欢迎消息:', data.message);
  } else if (data.type === 'pong') {
    console.log('🏓 Pong 响应:', data);
  }
};

// 连接错误
ws.onerror = (error) => {
  console.error('❌ WebSocket 错误:', error);
};

// 连接关闭
ws.onclose = (event) => {
  console.log('🔌 WebSocket 连接已关闭', event.code, event.reason);
};

// 发送其他消息（可以在控制台手动调用）
window.sendMessage = (type, content) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type, content }));
  } else {
    console.error('WebSocket 未连接');
  }
};
```

#### 测试示例

在控制台中执行：

```javascript
// 发送 echo 消息
sendMessage('echo', 'Hello, WebSocket!');

// 发送自定义消息
ws.send(JSON.stringify({
  type: 'custom',
  data: { message: '测试消息' }
}));
```

#### 优点

- ✅ 无需安装任何工具
- ✅ 即时反馈，所见即所得
- ✅ 适合快速验证功能

#### 缺点

- ❌ 无法自动化测试
- ❌ 不适合复杂测试场景
- ⚠️ 可能受到页面 CSP 策略限制

#### ⚠️ 常见错误：CSP 限制

如果遇到以下错误：
```
Refused to connect to 'ws://localhost:8000/ws/test_user' because it violates 
the following Content Security Policy directive: "connect-src ..."
```

**原因：** 当前页面有 Content Security Policy 限制，不允许连接 WebSocket。

**解决方案：**
1. **推荐：使用 HTML 测试页面**（见上方"方法一：HTML 测试页面"）
2. 在新标签页打开 `about:blank` 或任意普通网站，然后在控制台运行代码
3. 使用 Python 测试脚本（见"方法四"）

---

### 方法三：Python 单元测试（推荐用于自动化）

使用 pytest 运行单元测试，适合自动化测试和 CI/CD。

#### 运行测试

```bash
# 运行所有 WebSocket 测试
pytest tests/test_websocket.py -v

# 运行特定测试
pytest tests/test_websocket.py::test_websocket_connection -v

# 显示详细输出
pytest tests/test_websocket.py -v -s

# 直接执行测试文件
python tests/test_websocket.py
```

#### 测试覆盖

测试文件 `tests/test_websocket.py` 包含以下测试：

- ✅ 连接建立测试
- ✅ 欢迎消息测试
- ✅ Ping/Pong 心跳测试
- ✅ 消息回显测试
- ✅ 连接管理测试
- ✅ 统计接口测试
- ✅ 错误处理测试
- ✅ 多用户连接测试

#### 优点

- ✅ 自动化测试
- ✅ 适合 CI/CD
- ✅ 测试覆盖全面
- ✅ 可以集成到开发流程

#### 缺点

- ❌ 需要了解 pytest
- ❌ 测试代码需要维护

---

### 方法四：命令行工具测试

使用 `wscat` 命令行工具测试 WebSocket。

#### 安装 wscat

```bash
# 使用 npm 安装
npm install -g wscat

# 或使用 npx（无需安装）
npx wscat -c ws://localhost:8000/ws/test_user
```

#### 使用示例

```bash
# 连接到 WebSocket
wscat -c ws://localhost:8000/ws/test_user

# 连接成功后，可以输入消息：
{"type":"ping","timestamp":1234567890}
{"type":"echo","content":"Hello, WebSocket!"}
```

#### 优点

- ✅ 命令行工具，适合脚本化
- ✅ 可以快速测试连接

#### 缺点

- ❌ 需要安装 Node.js 和 npm
- ❌ 交互式测试，不够自动化

---

### 方法五：Python 客户端脚本

创建独立的 Python 客户端脚本进行测试。

#### 创建测试脚本

创建文件 `tests/websocket_client_test.py`：

```python
"""
WebSocket 客户端测试脚本

使用方法：
    python tests/websocket_client_test.py
"""

import asyncio
import json
import websockets
from typing import Optional


async def test_websocket(user_id: str = "test_user"):
    """
    测试 WebSocket 连接
    
    Args:
        user_id: 用户 ID
    """
    uri = f"ws://localhost:8000/ws/{user_id}"
    
    try:
        print(f"🔌 正在连接到 {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket 连接已建立")
            
            # 接收欢迎消息
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"📨 收到欢迎消息: {welcome_data}")
            
            # 发送 ping 消息
            ping_data = {
                "type": "ping",
                "timestamp": 1234567890
            }
            await websocket.send(json.dumps(ping_data))
            print(f"📤 发送 ping: {ping_data}")
            
            # 接收 pong 响应
            pong = await websocket.recv()
            pong_data = json.loads(pong)
            print(f"📨 收到 pong: {pong_data}")
            
            # 发送 echo 消息
            echo_data = {
                "type": "echo",
                "content": "Hello, WebSocket!"
            }
            await websocket.send(json.dumps(echo_data))
            print(f"📤 发送 echo: {echo_data}")
            
            # 接收回显
            echo_response = await websocket.recv()
            echo_response_data = json.loads(echo_response)
            print(f"📨 收到回显: {echo_response_data}")
            
            print("✅ 测试完成")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    user_id = sys.argv[1] if len(sys.argv) > 1 else "test_user"
    
    print("=" * 50)
    print("WebSocket 客户端测试")
    print("=" * 50)
    
    asyncio.run(test_websocket(user_id))
```

#### 安装依赖

```bash
pip install websockets
```

#### 运行测试

```bash
# 使用默认用户 ID
python tests/websocket_client_test.py

# 指定用户 ID
python tests/websocket_client_test.py my_user
```

#### 优点

- ✅ 可以编写复杂的测试逻辑
- ✅ 适合集成测试
- ✅ 可以模拟真实客户端行为

#### 缺点

- ❌ 需要安装额外依赖（websockets）
- ❌ 需要编写和维护脚本

---

## 测试场景

### 场景 1：基本连接测试

测试 WebSocket 连接是否可以正常建立。

**测试步骤：**
1. 建立连接
2. 验证收到欢迎消息
3. 断开连接

**预期结果：**
- ✅ 连接成功建立
- ✅ 收到欢迎消息（type: "welcome"）
- ✅ 连接正常断开

### 场景 2：Ping/Pong 心跳测试

测试心跳机制是否正常工作。

**测试步骤：**
1. 建立连接
2. 发送 ping 消息
3. 验证收到 pong 响应

**预期结果：**
- ✅ 收到 pong 响应
- ✅ pong 中包含原始 timestamp

### 场景 3：消息回显测试

测试消息回显功能。

**测试步骤：**
1. 建立连接
2. 发送 echo 消息
3. 验证收到回显

**预期结果：**
- ✅ 收到回显消息
- ✅ 回显内容与发送内容一致

### 场景 4：多用户连接测试

测试多个用户同时连接。

**测试步骤：**
1. 用户 A 建立连接
2. 用户 B 建立连接
3. 查询统计信息

**预期结果：**
- ✅ 两个用户都成功连接
- ✅ 统计信息显示 2 个连接
- ✅ 统计信息显示 2 个用户

### 场景 5：连接管理测试

测试连接管理功能。

**测试步骤：**
1. 建立连接
2. 查询统计信息
3. 断开连接
4. 再次查询统计信息

**预期结果：**
- ✅ 连接时统计信息正确
- ✅ 断开后统计信息更新

### 场景 6：错误处理测试

测试错误消息处理。

**测试步骤：**
1. 建立连接
2. 发送无效 JSON
3. 验证错误处理

**预期结果：**
- ✅ 不会导致连接断开
- ✅ 收到错误响应或默认处理

---

## 常见问题

### Q1: 连接失败，提示 "Connection refused"

**原因：** 服务未启动或端口不正确

**解决方法：**
1. 确认服务已启动：`curl http://localhost:8000/health`
2. 检查端口是否正确（默认 8000）
3. 检查防火墙设置

### Q2: 浏览器控制台提示 CSP 错误（Content Security Policy）

**错误信息：**
```
Refused to connect to 'ws://localhost:8000/ws/test_user' because it violates 
the following Content Security Policy directive: "connect-src ..."
```

**原因：** 当前页面有 Content Security Policy 限制，不允许连接 WebSocket。

**解决方法：**
1. **推荐：使用 HTML 测试页面**（`tests/websocket_test.html`）
   - 不受 CSP 限制
   - 图形化界面，操作简单
2. 在新标签页打开 `about:blank`，然后在控制台运行代码
3. 使用 Python 测试脚本（见"方法五"）
4. 使用 Python 单元测试（见"方法三"）

### Q3: 浏览器控制台提示 "WebSocket connection failed"

**原因：** 可能是 CORS 或协议问题

**解决方法：**
1. 确认使用 `ws://` 协议（不是 `http://`）
2. 检查服务是否正常运行
3. 检查浏览器控制台的详细错误信息
4. 如果遇到 CSP 错误，参考 Q2 的解决方案

### Q4: 测试时连接立即断开

**原因：** 可能是服务端错误或客户端发送了无效消息

**解决方法：**
1. 查看服务端日志
2. 检查发送的消息格式是否正确
3. 使用浏览器控制台测试，查看详细错误

### Q5: 如何测试广播功能？

**说明：** 广播功能需要从服务端触发，可以通过以下方式测试：

1. **使用 API 接口触发**（需要实现）：
   ```bash
   curl -X POST http://localhost:8000/api/broadcast \
     -H "Content-Type: application/json" \
     -d '{"message": "广播消息"}'
   ```

2. **在 Python 代码中测试**：
   ```python
   from app.websocket import manager
   await manager.broadcast({"type": "announcement", "content": "系统通知"})
   ```

### Q6: 如何测试个人消息推送？

**说明：** 个人消息推送也需要从服务端触发，可以通过以下方式测试：

1. **在 Python 代码中测试**：
   ```python
   from app.websocket import manager
   await manager.send_personal_message(
       {"type": "notification", "content": "个人消息"},
       "user_id"
   )
   ```

2. **创建测试 API 接口**（可选）：
   ```python
   @app.post("/api/send-message/{user_id}")
   async def send_message(user_id: str, message: dict):
       await manager.send_personal_message(message, user_id)
       return {"status": "sent"}
   ```

---

## 总结

推荐使用以下测试方法：

1. **快速验证（推荐）**：使用 HTML 测试页面（`tests/websocket_test.html`）
   - ✅ 不受 CSP 限制
   - ✅ 图形化界面，操作简单
   - ✅ 实时查看消息
2. **自动化测试**：使用 Python 单元测试
3. **复杂场景**：使用 Python 客户端脚本
4. **命令行测试**：使用 wscat 工具

**如果遇到 CSP 错误，强烈推荐使用 HTML 测试页面！**

根据实际需求选择合适的测试方法即可。

