# FastAPI 路由机制说明

## 问题现象

访问 `http://127.0.0.1:8100/` 时返回 **404 Not Found** 错误。

## 问题原因

**FastAPI 的路由匹配机制**：FastAPI 只会响应**已注册的路由**，如果访问的路径没有对应的路由处理器，就会返回 404 错误。

### 原理解析

#### 1. FastAPI 路由注册机制

FastAPI 使用**装饰器模式**来注册路由：

```python
@app.get("/health")  # 注册 GET /health 路由
async def health_check():
    return {"status": "ok"}
```

**关键点**：
- 只有使用 `@app.get()`, `@app.post()` 等装饰器注册的路径才能被访问
- 未注册的路径会返回 404
- 路由匹配是**精确匹配**（除非使用路径参数）

#### 2. 路由匹配顺序

FastAPI 按照以下顺序匹配路由：

1. **精确路径匹配**：`/health` 只匹配 `/health`
2. **路径参数匹配**：`/users/{user_id}` 匹配 `/users/1`, `/users/2` 等
3. **静态文件匹配**：如果注册了静态文件服务
4. **404 处理**：如果都不匹配，返回 404

#### 3. 为什么 `/` 返回 404？

在修复前，`app/main.py` 中只定义了以下路由：

```python
@app.get("/health")      # ✅ 可以访问
@app.get("/version")      # ✅ 可以访问
@app.get("/admin")        # ✅ 可以访问
@app.get("/ws/stats")     # ✅ 可以访问
# 没有定义 @app.get("/")  # ❌ 所以访问 / 返回 404
```

**没有定义根路径 `/` 的路由**，所以访问 `http://127.0.0.1:8100/` 时，FastAPI 找不到匹配的路由，返回 404。

## 解决方案

### 方案 1：添加根路径路由（已实现）

在 `app/main.py` 中添加根路径路由：

```python
@app.get("/", tags=["系统"])
async def root() -> Dict[str, Any]:
    """
    根路径接口
    
    返回应用的基本信息和可用端点。
    """
    return success_response(
        data={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "endpoints": {
                "health": "/health",
                "version": "/version",
                "docs": "/docs",
                "redoc": "/redoc",
                "admin": "/admin",
                "api": "/api/v1",
            },
        },
        message="欢迎使用 FastAPI 后端服务"
    )
```

**效果**：
- 访问 `http://127.0.0.1:8100/` 会返回欢迎信息和可用端点列表
- 用户可以通过根路径了解 API 结构

### 方案 2：重定向到管理界面

如果希望访问根路径时自动跳转到管理界面：

```python
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    """根路径重定向到管理界面"""
    return RedirectResponse(url="/admin")
```

**效果**：
- 访问 `http://127.0.0.1:8100/` 会自动跳转到 `http://127.0.0.1:8100/admin`

### 方案 3：返回简单的欢迎信息

```python
@app.get("/")
async def root():
    """根路径返回欢迎信息"""
    return {"message": "Welcome to FastAPI Backend", "version": "1.0.0"}
```

## FastAPI 路由机制详解

### 1. 路由注册方式

#### 方式一：使用装饰器（推荐）

```python
@app.get("/users")
async def get_users():
    return {"users": []}

@app.post("/users")
async def create_user():
    return {"message": "created"}
```

#### 方式二：使用 `add_api_route`

```python
async def get_users():
    return {"users": []}

app.add_api_route("/users", get_users, methods=["GET"])
```

#### 方式三：使用 APIRouter（推荐用于模块化）

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"users": []}

app.include_router(router, prefix="/api/v1")
```

### 2. 路由匹配规则

#### 精确匹配

```python
@app.get("/users")      # 只匹配 /users
@app.get("/users/")     # 只匹配 /users/（注意末尾的斜杠）
```

**注意**：`/users` 和 `/users/` 是**不同的路径**！

#### 路径参数匹配

```python
@app.get("/users/{user_id}")  # 匹配 /users/1, /users/2, /users/abc 等
async def get_user(user_id: int):
    return {"user_id": user_id}
```

#### 查询参数

```python
@app.get("/users")  # 匹配 /users?page=1&size=10
async def get_users(page: int = 1, size: int = 10):
    return {"page": page, "size": size}
```

### 3. 路由优先级

FastAPI 按照**注册顺序**匹配路由，但有一些规则：

1. **更具体的路径优先**：`/users/me` 优先于 `/users/{user_id}`
2. **静态路径优先于动态路径**：`/users/active` 优先于 `/users/{status}`
3. **先注册的路由优先**（如果路径相同）

**示例**：

```python
@app.get("/users/{user_id}")  # 动态路径
async def get_user(user_id: int):
    pass

@app.get("/users/me")  # 静态路径（更具体）
async def get_me():
    pass

# 访问 /users/me 会匹配 get_me，而不是 get_user
```

### 4. 路由冲突处理

如果注册了冲突的路由，FastAPI 会按照注册顺序处理：

```python
@app.get("/users/{user_id}")  # 先注册
async def get_user(user_id: int):
    pass

@app.get("/users/me")  # 后注册，但更具体
async def get_me():
    pass

# FastAPI 会智能处理：/users/me 匹配 get_me，/users/123 匹配 get_user
```

### 5. 404 处理机制

当请求的路径没有匹配的路由时：

1. FastAPI 检查所有注册的路由
2. 如果都不匹配，返回 404
3. 可以通过自定义异常处理器来定制 404 响应

**自定义 404 处理**：

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "path": request.url.path,
            "message": "请求的路径不存在"
        }
    )
```

## 实际应用建议

### 1. 始终定义根路径

建议为 API 服务定义根路径，提供：
- 服务信息
- 可用端点列表
- 版本信息
- 文档链接

### 2. 使用 APIRouter 组织路由

```python
# app/api/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["用户"])

@router.get("/")
async def get_users():
    pass

# app/main.py
from app.api import users
app.include_router(users.router, prefix="/api/v1")
```

### 3. 统一错误处理

```python
# 自定义 404 响应
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "message": "资源未找到",
            "path": request.url.path
        }
    )
```

### 4. 路由文档化

使用 `tags` 和 `summary` 来组织 API 文档：

```python
@app.get(
    "/users",
    tags=["用户"],
    summary="获取用户列表",
    description="分页获取所有用户",
    response_model=UserListResponse
)
async def get_users():
    pass
```

## 总结

1. **FastAPI 只响应已注册的路由**，未注册的路径返回 404
2. **路由匹配是精确的**，`/users` 和 `/users/` 是不同的路径
3. **更具体的路径优先匹配**，静态路径优先于动态路径
4. **建议始终定义根路径**，提供 API 概览信息
5. **使用 APIRouter 组织路由**，提高代码可维护性

## 验证

修复后，访问以下路径应该都能正常工作：

- ✅ `http://127.0.0.1:8100/` - 根路径（返回欢迎信息）
- ✅ `http://127.0.0.1:8100/health` - 健康检查
- ✅ `http://127.0.0.1:8100/version` - 版本信息
- ✅ `http://127.0.0.1:8100/admin` - 管理界面
- ✅ `http://127.0.0.1:8100/docs` - API 文档
- ✅ `http://127.0.0.1:8100/api/v1/users` - 用户 API
