# Python 装饰器与 Celery 任务装饰器教程

## 目录

1. [Python 装饰器基础](#python-装饰器基础)
2. [装饰器的工作原理](#装饰器的工作原理)
3. [Celery 任务装饰器](#celery-任务装饰器)
4. [任务对象的异步方法](#任务对象的异步方法)
5. [实际应用示例](#实际应用示例)

---

## Python 装饰器基础

### 什么是装饰器？

**装饰器（Decorator）** 是 Python 中的一个高级特性，它允许你在不修改原函数代码的情况下，为函数添加新功能。

### 装饰器的基本语法

```python
@decorator
def my_function():
    pass
```

这个语法等价于：

```python
def my_function():
    pass

my_function = decorator(my_function)
```

### 简单示例

#### 示例 1：最简单的装饰器

```python
def my_decorator(func):
    """一个简单的装饰器"""
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# 调用函数
say_hello()
# 输出：
# 函数执行前
# Hello!
# 函数执行后
```

#### 示例 2：带参数的装饰器

```python
def repeat(times):
    """带参数的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# 输出：
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### 装饰器的执行流程

```
┌─────────────────────────────────────┐
│  @decorator                         │
│  def my_function():                 │
│      pass                           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  1. Python 解析装饰器语法            │
│  2. 调用 decorator(my_function)     │
│  3. 返回新的函数对象                 │
│  4. 将新对象赋值给 my_function      │
└─────────────────────────────────────┘
```

---

## 装饰器的工作原理

### 装饰器的本质

装饰器实际上是一个**高阶函数**（接受函数作为参数，返回函数）：

```python
def decorator(func):
    """
    装饰器函数
    
    Args:
        func: 被装饰的函数
    
    Returns:
        新的函数对象（通常是包装后的函数）
    """
    # 在这里可以添加额外的逻辑
    def wrapper(*args, **kwargs):
        # 执行前的操作
        result = func(*args, **kwargs)  # 调用原函数
        # 执行后的操作
        return result
    return wrapper
```

### 装饰器的执行顺序

当使用多个装饰器时，执行顺序是**从下往上**：

```python
@decorator1
@decorator2
@decorator3
def my_function():
    pass

# 等价于：
# my_function = decorator1(decorator2(decorator3(my_function)))
```

### 保留原函数的元信息

使用 `functools.wraps` 可以保留原函数的元信息（如函数名、文档字符串等）：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def add(a, b):
    """加法函数"""
    return a + b

print(add.__name__)  # 输出: add（而不是 wrapper）
print(add.__doc__)   # 输出: 加法函数
```

---

## Celery 任务装饰器

### 什么是 Celery 任务装饰器？

Celery 任务装饰器将普通 Python 函数转换为**异步任务**，可以在后台执行，不阻塞主程序。

### 项目中的任务装饰器

在 `app/tasks/base.py` 中定义了一个自定义的任务装饰器：

```python
from app.tasks.base import task

@task(name="test.decorated_task")
def test_task_func(x: int) -> int:
    return x * 2
```

### 装饰器的实现

让我们看看 `task` 装饰器的实现：

```python
def task(
    name: Optional[str] = None,
    bind: bool = False,
    base: type = BaseTask,
    max_retries: int = 3,
    default_retry_delay: int = 60,
    **kwargs
) -> Callable:
    """
    任务装饰器
    
    Args:
        name: 任务名称（可选，默认使用函数名）
        bind: 是否绑定任务实例（允许访问 self）
        base: 基础任务类（默认使用 BaseTask）
        max_retries: 最大重试次数
        default_retry_delay: 默认重试延迟（秒）
        **kwargs: 其他 Celery 任务参数
    
    Returns:
        Callable: 装饰后的任务函数
    """
    def decorator(func: Callable) -> Callable:
        # 使用 celery_app.task 装饰器
        task_func = celery_app.task(
            name=name or f"app.tasks.{func.__name__}",
            bind=bind,
            base=base,
            max_retries=max_retries,
            default_retry_delay=default_retry_delay,
            **kwargs
        )(func)
        
        return task_func
    
    return decorator
```

### 装饰器的工作流程

```
┌─────────────────────────────────────────┐
│  @task(name="test.decorated_task")     │
│  def test_task_func(x: int) -> int:    │
│      return x * 2                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  1. task(name="test.decorated_task")    │
│     返回 decorator 函数                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. decorator(test_task_func) 被调用   │
│     内部调用 celery_app.task(...)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. celery_app.task() 返回任务对象      │
│     这是一个 Celery Task 实例           │
│     不再是普通函数！                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. test_task_func 被替换为任务对象     │
│     现在具有 delay、apply_async 等方法  │
└─────────────────────────────────────────┘
```

### 装饰前后的区别

#### 装饰前：普通函数

```python
def test_task_func(x: int) -> int:
    return x * 2

# 直接调用（同步执行）
result = test_task_func(5)  # 返回 10
print(type(test_task_func))  # <class 'function'>

# 没有这些方法：
# test_task_func.delay()      # ❌ AttributeError
# test_task_func.apply_async() # ❌ AttributeError
```

#### 装饰后：Celery 任务对象

```python
@task(name="test.decorated_task")
def test_task_func(x: int) -> int:
    return x * 2

# 类型已经改变
print(type(test_task_func))  # <class 'celery.local.CallableTask'>

# 现在有了这些方法：
assert hasattr(test_task_func, "delay")        # ✅ True
assert hasattr(test_task_func, "apply_async")  # ✅ True

# 可以异步调用
result = test_task_func.delay(5)  # 异步执行，返回 AsyncResult
```

---

## 任务对象的异步方法

### 为什么任务对象有 `delay` 和 `apply_async`？

当函数被 `@task` 装饰器装饰后，它不再是普通函数，而是变成了 **Celery Task 对象**。这个对象继承自 `celery.Task` 类，该类提供了异步执行的方法。

### `delay` 方法

**`delay(*args, **kwargs)`** 是异步调用的**简化接口**：

```python
@task(name="add_numbers")
def add(a: int, b: int) -> int:
    return a + b

# 使用 delay 异步调用
result = add.delay(3, 5)

# result 是 AsyncResult 对象
print(type(result))  # <class 'celery.result.AsyncResult'>

# 获取结果（会阻塞直到任务完成）
final_result = result.get()
print(final_result)  # 8
```

**`delay` 方法的等价写法：**

```python
# 这两种写法是等价的：
result = add.delay(3, 5)
result = add.apply_async(args=(3, 5))
```

### `apply_async` 方法

**`apply_async(args=(), kwargs={}, **options)`** 是更**灵活的异步调用接口**，支持更多选项：

```python
@task(name="send_email")
def send_email(to: str, subject: str, body: str):
    # 发送邮件的逻辑
    pass

# 使用 apply_async 可以设置更多选项
result = send_email.apply_async(
    args=("user@example.com", "Hello", "World"),
    countdown=10,        # 10 秒后执行
    expires=3600,        # 1 小时后过期
    priority=9,          # 高优先级
    queue="high_priority" # 指定队列
)
```

### 常用选项说明

| 选项 | 说明 | 示例 |
|------|------|------|
| `countdown` | 延迟执行时间（秒） | `countdown=10` |
| `eta` | 指定执行时间 | `eta=datetime.now() + timedelta(seconds=10)` |
| `expires` | 任务过期时间（秒） | `expires=3600` |
| `priority` | 任务优先级（0-9） | `priority=9` |
| `queue` | 指定队列名称 | `queue="high_priority"` |
| `routing_key` | 路由键 | `routing_key="email"` |

### 方法对比

```python
@task(name="process_data")
def process_data(data: dict) -> dict:
    # 处理数据
    return {"status": "success"}

# 方式 1：使用 delay（简单）
result1 = process_data.delay({"key": "value"})

# 方式 2：使用 apply_async（灵活）
result2 = process_data.apply_async(
    args=({"key": "value"},),
    countdown=5,
    priority=8
)

# 两种方式都返回 AsyncResult 对象
assert type(result1) == type(result2)  # True
```

---

## 实际应用示例

### 示例 1：基本任务定义

```python
from app.tasks.base import task

@task(name="calculate.sum")
def calculate_sum(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b

# 同步调用（直接执行，不通过 Celery）
result = calculate_sum(3, 5)  # 返回 8

# 异步调用（通过 Celery 执行）
async_result = calculate_sum.delay(3, 5)
final_result = async_result.get()  # 返回 8
```

### 示例 2：带重试的任务

```python
from app.tasks.base import task

@task(name="fetch_data", max_retries=3, default_retry_delay=60)
def fetch_data(url: str) -> dict:
    """获取数据，失败时自动重试"""
    import requests
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        # 抛出异常，Celery 会自动重试
        raise fetch_data.retry(exc=exc, countdown=60)
```

### 示例 3：绑定任务（访问任务实例）

```python
from app.tasks.base import task

@task(name="process_file", bind=True)
def process_file(self, file_path: str) -> str:
    """
    处理文件，可以访问任务实例
    
    Args:
        self: 任务实例（因为 bind=True）
        file_path: 文件路径
    """
    # 可以通过 self 访问任务信息
    task_id = self.request.id
    print(f"任务 ID: {task_id}")
    
    # 可以更新任务状态
    self.update_state(state="PROCESSING", meta={"progress": 50})
    
    # 处理文件
    with open(file_path, 'r') as f:
        content = f.read()
    
    return f"处理完成: {len(content)} 字符"
```

### 示例 4：任务链（Chain）

```python
from celery import chain
from app.tasks.base import task

@task(name="step1")
def step1(data: str) -> str:
    return f"Step1: {data}"

@task(name="step2")
def step2(data: str) -> str:
    return f"Step2: {data}"

@task(name="step3")
def step3(data: str) -> str:
    return f"Step3: {data}"

# 创建任务链（按顺序执行）
workflow = chain(
    step1.s("input"),
    step2.s(),
    step3.s()
)

# 执行任务链
result = workflow.apply_async()
final_result = result.get()  # 返回 "Step3: Step2: Step1: input"
```

### 示例 5：任务组（Group）

```python
from celery import group
from app.tasks.base import task

@task(name="process_item")
def process_item(item: str) -> str:
    return f"Processed: {item}"

# 创建任务组（并行执行）
items = ["item1", "item2", "item3"]
job = group(process_item.s(item) for item in items)

# 执行任务组
result = job.apply_async()
results = result.get()  # 返回所有任务的结果列表
# ['Processed: item1', 'Processed: item2', 'Processed: item3']
```

---

## 总结

### 关键概念

1. **装饰器语法**：`@decorator` 等价于 `func = decorator(func)`
2. **任务装饰器**：将普通函数转换为 Celery 任务对象
3. **任务对象**：不再是普通函数，具有 `delay` 和 `apply_async` 方法
4. **异步执行**：通过 `delay` 或 `apply_async` 异步调用任务

### 常见问题

#### Q1: 为什么装饰后的函数有 `delay` 方法？

**A:** 因为装饰器将函数替换为了 Celery Task 对象，该对象继承自 `celery.Task` 类，提供了 `delay` 和 `apply_async` 等异步方法。

#### Q2: `delay` 和 `apply_async` 有什么区别？

**A:** 
- `delay` 是简化接口，只接受函数参数
- `apply_async` 是完整接口，可以设置更多选项（如 `countdown`、`priority` 等）

#### Q3: 可以直接调用装饰后的函数吗？

**A:** 可以，但这是**同步调用**，不会通过 Celery 执行。要异步执行，必须使用 `delay` 或 `apply_async`。

#### Q4: 如何获取异步任务的结果？

**A:** 使用 `AsyncResult.get()` 方法：

```python
result = my_task.delay(1, 2)
final_result = result.get()  # 阻塞直到任务完成
```

---

## 参考资源

- [Python 装饰器官方文档](https://docs.python.org/3/glossary.html#term-decorator)
- [Celery 任务文档](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [项目任务模块](../app/tasks/base.py)
- [项目任务示例](../app/tasks/examples.py)

