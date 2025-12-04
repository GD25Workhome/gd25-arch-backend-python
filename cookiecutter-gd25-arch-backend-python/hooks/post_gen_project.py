#!/usr/bin/env python
"""
CookieCutter 后处理脚本

在项目生成后执行，用于：
- 删除不需要的可选模块文件
- 清理不需要的测试文件

注意：CookieCutter 会在生成项目后自动执行此脚本
"""

import os
import shutil
import json
import sys


def remove_path(path: str) -> None:
    """删除文件或目录"""
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"✓ 已删除目录: {path}")
        else:
            os.remove(path)
            print(f"✓ 已删除文件: {path}")


def main():
    """主函数"""
    # CookieCutter 会将上下文变量作为 JSON 字符串传递给脚本
    # 通过环境变量 COOKIECUTTER_CONTEXT 获取
    context_json = os.environ.get("COOKIECUTTER_CONTEXT", "{}")
    
    try:
        context = json.loads(context_json)
    except json.JSONDecodeError:
        # 如果无法解析 JSON，使用默认值
        context = {}
    
    # 获取变量值，默认为 'y'（包含）
    include_celery = context.get("include_celery", "y")
    include_websocket = context.get("include_websocket", "n")
    
    project_dir = os.getcwd()
    
    print("开始后处理...")
    print(f"  include_celery: {include_celery}")
    print(f"  include_websocket: {include_websocket}")
    
    # 删除不需要的 Celery 相关文件
    if include_celery != "y":
        remove_path(os.path.join(project_dir, "app", "tasks"))
        remove_path(os.path.join(project_dir, "tests", "test_celery.py"))
        remove_path(os.path.join(project_dir, "scripts", "start_worker.sh"))
        remove_path(os.path.join(project_dir, "scripts", "start_flower.sh"))
        print("  ✓ 已移除 Celery 相关文件")
    
    # 删除不需要的 WebSocket 相关文件
    if include_websocket != "y":
        remove_path(os.path.join(project_dir, "app", "websocket"))
        remove_path(os.path.join(project_dir, "tests", "test_websocket.py"))
        remove_path(os.path.join(project_dir, "tests", "websocket_test.html"))
        print("  ✓ 已移除 WebSocket 相关文件")
    
    print("后处理完成！")


if __name__ == "__main__":
    main()

