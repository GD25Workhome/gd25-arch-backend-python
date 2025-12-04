#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
装饰器示例代码

演示 Python 装饰器的基本用法，包括：
1. 简单的装饰器
2. 带参数的装饰器
3. 保留函数元信息的装饰器
4. 多个装饰器的组合使用
"""

from functools import wraps


# ==================== 示例 1：简单的装饰器 ====================

def my_decorator(func):
    """一个简单的装饰器"""
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper


@my_decorator
def say_hello():
    """打招呼函数"""
    print("Hello!")


# ==================== 示例 2：带参数的装饰器 ====================

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
    """问候函数"""
    print(f"Hello, {name}!")


# ==================== 示例 3：保留函数元信息的装饰器 ====================

def timing_decorator(func):
    """计时装饰器，保留原函数的元信息"""
    @wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result
    return wrapper


@timing_decorator
def calculate_sum(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


# ==================== 示例 4：带参数的计时装饰器 ====================

def log_execution(prefix: str = "[LOG]"):
    """带参数的日志装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{prefix} 调用函数: {func.__name__}")
            print(f"{prefix} 参数: args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"{prefix} 返回值: {result}")
            return result
        return wrapper
    return decorator


@log_execution(prefix="[INFO]")
def multiply(a: int, b: int) -> int:
    """乘法函数"""
    return a * b


# ==================== 示例 5：多个装饰器组合 ====================

@timing_decorator
@log_execution(prefix="[DEBUG]")
def complex_calculation(x: int, y: int) -> int:
    """复杂计算函数"""
    result = x ** 2 + y ** 2
    return result


# ==================== 示例 6：类装饰器 ====================

class CountCalls:
    """统计函数调用次数的类装饰器"""
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        wraps(func)(self)  # 保留原函数元信息
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"函数 {self.func.__name__} 被调用了 {self.count} 次")
        return self.func(*args, **kwargs)


@CountCalls
def fibonacci(n: int) -> int:
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ==================== 主程序 ====================

def main():
    """主函数，演示所有装饰器的使用"""
    
    print("=" * 60)
    print("示例 1：简单的装饰器")
    print("=" * 60)
    say_hello()
    print()
    
    print("=" * 60)
    print("示例 2：带参数的装饰器（repeat）")
    print("=" * 60)
    greet("Alice")
    print()
    
    print("=" * 60)
    print("示例 3：保留函数元信息的装饰器（timing）")
    print("=" * 60)
    result = calculate_sum(3, 5)
    print(f"计算结果: {result}")
    print(f"函数名: {calculate_sum.__name__}")
    print(f"函数文档: {calculate_sum.__doc__}")
    print()
    
    print("=" * 60)
    print("示例 4：带参数的日志装饰器")
    print("=" * 60)
    result = multiply(4, 7)
    print(f"最终结果: {result}")
    print()
    
    print("=" * 60)
    print("示例 5：多个装饰器组合")
    print("=" * 60)
    result = complex_calculation(3, 4)
    print(f"最终结果: {result}")
    print()
    
    print("=" * 60)
    print("示例 6：类装饰器（统计调用次数）")
    print("=" * 60)
    # 注意：由于递归调用，计数会包含所有递归调用
    result = fibonacci(5)
    print(f"fibonacci(5) = {result}")
    print()


if __name__ == "__main__":
    main()

