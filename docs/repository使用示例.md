# Repository 使用示例

本文档提供 Repository 基础类的使用示例，包括基本用法、继承示例和常见场景。

## 目录

- [基础用法](#基础用法)
- [继承示例](#继承示例)
- [CRUD 操作](#crud-操作)
- [分页查询](#分页查询)
- [通用查询](#通用查询)
- [在 FastAPI 中使用](#在-fastapi-中使用)

---

## 基础用法

### 1. 定义模型

首先，需要定义一个 SQLAlchemy 模型，继承自 `BaseModel`：

```python
from app.db.base import BaseModel
from sqlalchemy import Column, String, Integer, Boolean

class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"
    
    name = Column(String(100), nullable=False, comment="用户名")
    email = Column(String(255), unique=True, nullable=False, comment="邮箱")
    age = Column(Integer, nullable=True, comment="年龄")
    is_active = Column(Boolean, default=True, comment="是否激活")
```

### 2. 创建 Repository

创建 Repository 类，继承自 `BaseRepository`：

```python
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session
from app.models.user import User  # 假设模型在 app.models.user 中

class UserRepository(BaseRepository[User]):
    """用户 Repository"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
```

### 3. 使用 Repository

```python
from app.db.session import get_db_session

# 获取数据库会话
db = get_db_session()

# 创建 Repository 实例
user_repo = UserRepository(db)

try:
    # 创建用户
    user = user_repo.create({
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
        "is_active": True
    })
    print(f"创建用户成功: {user.id}")
    
    # 根据 ID 获取用户
    user = user_repo.get_by_id(1)
    if user:
        print(f"用户: {user.name}, 邮箱: {user.email}")
    
    # 更新用户
    updated_user = user_repo.update(1, {"name": "李四"})
    if updated_user:
        print(f"更新成功: {updated_user.name}")
    
    # 删除用户
    if user_repo.delete(1):
        print("删除成功")
    
finally:
    db.close()
```

---

## 继承示例

### 扩展 Repository 功能

可以继承 `BaseRepository` 并添加自定义方法：

```python
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User

class UserRepository(BaseRepository[User]):
    """用户 Repository（带自定义方法）"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户（自定义方法）
        
        Args:
            email: 邮箱地址
            
        Returns:
            Optional[User]: 用户对象或 None
        """
        return self.filter_one(email=email)
    
    def get_active_users(self) -> List[User]:
        """
        获取所有激活的用户（自定义方法）
        
        Returns:
            List[User]: 激活用户列表
        """
        return self.filter_by(is_active=True)
    
    def search_users(self, keyword: str) -> List[User]:
        """
        搜索用户（自定义方法）
        
        Args:
            keyword: 搜索关键字
            
        Returns:
            List[User]: 符合条件的用户列表
        """
        return self.search(
            search_fields=["name", "email"],
            keyword=keyword
        )
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[User]:
        """
        根据年龄范围获取用户（使用查询构建器）
        
        Args:
            min_age: 最小年龄
            max_age: 最大年龄
            
        Returns:
            List[User]: 符合条件的用户列表
        """
        return self.query_builder().filter(
            User.age >= min_age,
            User.age <= max_age
        ).all()
```

---

## CRUD 操作

### Create（创建）

```python
# 创建单条记录
user = user_repo.create({
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25
})

# 批量创建
users = user_repo.create_many([
    {"name": "张三", "email": "zhangsan@example.com", "age": 25},
    {"name": "李四", "email": "lisi@example.com", "age": 30},
    {"name": "王五", "email": "wangwu@example.com", "age": 28},
])
```

### Read（读取）

```python
# 根据 ID 获取
user = user_repo.get_by_id(1)

# 获取所有记录
all_users = user_repo.get_all()

# 分页获取
users = user_repo.get_all(skip=0, limit=10)

# 获取总数
total = user_repo.get_count()

# 检查是否存在
if user_repo.exists(1):
    print("用户存在")
```

### Update（更新）

```python
# 更新记录
updated_user = user_repo.update(1, {"name": "新名称", "age": 26})

# 更新或创建（如果不存在则创建）
user = user_repo.update_or_create(
    filter_data={"email": "test@example.com"},
    update_data={"name": "更新名称"},
    create_data={"name": "新用户", "email": "test@example.com", "age": 20}
)
```

### Delete（删除）

```python
# 删除单条记录
if user_repo.delete(1):
    print("删除成功")

# 批量删除
deleted_count = user_repo.delete_many([1, 2, 3])
print(f"删除了 {deleted_count} 条记录")

# 删除所有记录（谨慎使用！）
# deleted_count = user_repo.delete_all()
```

---

## 分页查询

### 基本分页

```python
# 基本分页查询
result = user_repo.paginate(page=1, page_size=10)

print(f"总数: {result.total}")
print(f"当前页: {result.page}")
print(f"每页数量: {result.page_size}")
print(f"总页数: {result.total_pages}")
print(f"是否有下一页: {result.has_next}")
print(f"是否有上一页: {result.has_prev}")

# 遍历当前页数据
for user in result.items:
    print(f"用户: {user.name}, 邮箱: {user.email}")
```

### 带排序的分页

```python
# 按创建时间降序排列
result = user_repo.paginate(
    page=1,
    page_size=10,
    order_by="created_at",
    order_desc=True
)

# 按年龄升序排列
result = user_repo.paginate(
    page=1,
    page_size=10,
    order_by="age",
    order_desc=False
)
```

### 转换为字典格式

```python
result = user_repo.paginate(page=1, page_size=10)
data = result.to_dict()

# 返回格式：
# {
#     "items": [
#         {"id": 1, "name": "张三", "email": "zhangsan@example.com", ...},
#         {"id": 2, "name": "李四", "email": "lisi@example.com", ...},
#     ],
#     "pagination": {
#         "total": 100,
#         "page": 1,
#         "page_size": 10,
#         "total_pages": 10,
#         "has_next": True,
#         "has_prev": False,
#     }
# }
```

---

## 通用查询

### 条件过滤

```python
# 单条件过滤
users = user_repo.filter_by(name="张三")

# 多条件过滤
users = user_repo.filter_by(name="张三", is_active=True)

# 使用字典过滤
users = user_repo.filter_by_dict({"name": "张三", "is_active": True})

# 获取单条记录
user = user_repo.filter_one(email="zhangsan@example.com")
```

### 关键字搜索

```python
# 在多个字段中搜索关键字
users = user_repo.search(
    search_fields=["name", "email"],
    keyword="张"
)

# 带分页的搜索
users = user_repo.search(
    search_fields=["name", "email"],
    keyword="张",
    skip=0,
    limit=10
)
```

### 使用查询构建器

```python
# 获取查询构建器，进行复杂查询
query = user_repo.query_builder()

# 复杂条件查询
users = query.filter(
    User.age >= 18,
    User.age <= 65,
    User.is_active == True
).order_by(User.created_at.desc()).limit(10).all()

# 使用 OR 条件
from sqlalchemy import or_
users = query.filter(
    or_(
        User.name.like("%张%"),
        User.email.like("%zhang%")
    )
).all()
```

---

## 在 FastAPI 中使用

### 在路由中使用 Repository

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories.base import BaseRepository
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

@router.get("/")
def get_users(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """获取用户列表（分页）"""
    user_repo = UserRepository(db)
    result = user_repo.paginate(page=page, page_size=page_size)
    return result.to_dict()

@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """根据 ID 获取用户"""
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user.to_dict()

@router.post("/")
def create_user(
    data: dict,
    db: Session = Depends(get_db)
):
    """创建用户"""
    user_repo = UserRepository(db)
    try:
        user = user_repo.create(data)
        return user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    """更新用户"""
    user_repo = UserRepository(db)
    user = user_repo.update(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user.to_dict()

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """删除用户"""
    user_repo = UserRepository(db)
    if not user_repo.delete(user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "删除成功"}
```

### 使用依赖注入优化

可以创建一个依赖函数来获取 Repository 实例：

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories.base import BaseRepository
from app.models.user import User

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """获取用户 Repository 依赖"""
    return UserRepository(db)

@router.get("/")
def get_users(
    page: int = 1,
    page_size: int = 10,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """获取用户列表（分页）"""
    result = user_repo.paginate(page=page, page_size=page_size)
    return result.to_dict()
```

---

## 完整示例

### 示例模型

```python
# app/models/user.py
from app.db.base import BaseModel
from sqlalchemy import Column, String, Integer, Boolean

class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"
    
    name = Column(String(100), nullable=False, comment="用户名")
    email = Column(String(255), unique=True, nullable=False, comment="邮箱")
    age = Column(Integer, nullable=True, comment="年龄")
    is_active = Column(Boolean, default=True, comment="是否激活")
```

### 示例 Repository

```python
# app/repositories/user_repository.py
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User

class UserRepository(BaseRepository[User]):
    """用户 Repository"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.filter_one(email=email)
    
    def get_active_users(self) -> List[User]:
        """获取所有激活的用户"""
        return self.filter_by(is_active=True)
```

### 示例 API 路由

```python
# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """获取用户 Repository 依赖"""
    return UserRepository(db)

@router.get("/")
def get_users(
    page: int = 1,
    page_size: int = 10,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """获取用户列表（分页）"""
    result = user_repo.paginate(page=page, page_size=page_size)
    return result.to_dict()

@router.get("/{user_id}")
def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """根据 ID 获取用户"""
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user.to_dict()
```

---

## 注意事项

1. **数据库会话管理**：使用 `get_db()` 依赖注入时，会话会自动管理；手动创建会话时，记得关闭会话。

2. **事务处理**：Repository 中的操作会自动提交事务，如果发生异常会自动回滚。

3. **唯一性约束**：创建或更新时如果违反唯一性约束，会抛出 `IntegrityError`，需要适当处理。

4. **性能考虑**：批量操作时使用 `create_many()` 和 `delete_many()` 比循环调用单条操作更高效。

5. **查询优化**：对于复杂查询，可以使用 `query_builder()` 方法获取查询对象，进行更灵活的查询构建。

---

## 总结

Repository 基础类提供了完整的数据访问层功能，包括：

- ✅ 基础 CRUD 操作
- ✅ 分页查询
- ✅ 通用查询方法
- ✅ 批量操作
- ✅ 灵活的查询构建

通过继承 `BaseRepository` 并添加自定义方法，可以轻松扩展 Repository 功能，满足各种业务需求。

