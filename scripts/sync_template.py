#!/usr/bin/env python3
"""
模版同步脚本

用于将项目代码同步到 CookieCutter 模版目录。

功能：
- 同步 app/ 目录下的代码文件
- 同步其他配置文件（requirements.txt, pyproject.toml 等）
- 自动处理文件重命名、删除、新增
- 排除不需要同步的文件（.env, __pycache__, .pyc 等）

使用方法：
    python scripts/sync_template.py

或者：
    python scripts/sync_template.py --dry-run  # 仅显示将要执行的操作，不实际执行
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Set, Tuple
import difflib


# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
# 模版目录
TEMPLATE_DIR = PROJECT_ROOT / "cookiecutter-gd25-arch-backend-python" / "{{ cookiecutter.project_name }}"
# 源目录（项目代码）
SOURCE_DIR = PROJECT_ROOT

# 需要同步的目录和文件
SYNC_PATHS = [
    "app/",
    "alembic/",
    "tests/",
    "scripts/",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements.lock",
    "pyproject.toml",
    "pytest.ini",
    "alembic.ini",
    "env.example",
    "LICENSE",
]

# 需要排除的文件和目录模式
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".coverage",
    "coverage.xml",
    ".env",
    ".env.local",
    ".git",
    ".gitignore",
    ".idea",
    ".vscode",
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "*.log",
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "venv/",
    "env/",
    ".venv/",
    "node_modules/",
    "dist/",
    "build/",
    "*.egg-info/",
    ".mypy_cache/",
    ".ruff_cache/",
    "htmlcov/",
    ".tox/",
    "docs/",  # 文档目录不同步（模版有自己的文档）
    "cursor_test/",
    "cursor_docs/",
    "README.md",  # README 不同步（模版有自己的 README）
    "cookiecutter-gd25-arch-backend-python/",  # 模版目录本身不同步
    ".git/",
]


def should_exclude(path: Path) -> bool:
    """
    判断文件或目录是否应该被排除
    
    Args:
        path: 文件或目录路径
        
    Returns:
        bool: 如果应该排除返回 True
    """
    path_str = str(path)
    
    # 检查是否匹配排除模式
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str or path.name == pattern.replace("*", "").replace("/", ""):
            return True
    
    # 检查是否是隐藏文件（除了 .gitkeep）
    if path.name.startswith(".") and path.name != ".gitkeep":
        return True
    
    return False


def get_all_files(directory: Path, relative_to: Path = None) -> Set[Path]:
    """
    获取目录下所有文件的相对路径集合
    
    Args:
        directory: 目录路径
        relative_to: 相对路径的基准目录（默认为 directory）
        
    Returns:
        Set[Path]: 文件相对路径集合
    """
    if relative_to is None:
        relative_to = directory
    
    files = set()
    
    if not directory.exists():
        return files
    
    for root, dirs, filenames in os.walk(directory):
        # 过滤掉需要排除的目录
        dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
        
        for filename in filenames:
            file_path = Path(root) / filename
            if not should_exclude(file_path):
                relative_path = file_path.relative_to(relative_to)
                files.add(relative_path)
    
    return files


def sync_file(source: Path, target: Path, dry_run: bool = False) -> bool:
    """
    同步单个文件
    
    Args:
        source: 源文件路径
        target: 目标文件路径
        dry_run: 是否为试运行模式
        
    Returns:
        bool: 是否成功
    """
    if not source.exists():
        return False
    
    # 确保目标目录存在
    target.parent.mkdir(parents=True, exist_ok=True)
    
    if dry_run:
        print(f"  [DRY RUN] 将复制: {source} -> {target}")
        return True
    
    try:
        shutil.copy2(source, target)
        print(f"  ✓ 已同步: {source.relative_to(PROJECT_ROOT)}")
        return True
    except Exception as e:
        print(f"  ✗ 同步失败: {source.relative_to(PROJECT_ROOT)} - {e}")
        return False


def sync_directory(source_dir: Path, target_dir: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    同步目录
    
    Args:
        source_dir: 源目录
        target_dir: 目标目录
        dry_run: 是否为试运行模式
        
    Returns:
        Tuple[int, int]: (成功数量, 失败数量)
    """
    if not source_dir.exists():
        return 0, 0
    
    source_files = get_all_files(source_dir, relative_to=PROJECT_ROOT)
    target_files = get_all_files(target_dir, relative_to=TEMPLATE_DIR) if target_dir.exists() else set()
    
    # 需要同步的文件（在源目录中存在）
    files_to_sync = source_files
    
    # 需要删除的文件（在目标目录中存在，但在源目录中不存在）
    files_to_delete = target_files - source_files
    
    success_count = 0
    fail_count = 0
    
    # 同步文件
    for rel_path in files_to_sync:
        source_file = PROJECT_ROOT / rel_path
        target_file = TEMPLATE_DIR / rel_path
        
        if sync_file(source_file, target_file, dry_run):
            success_count += 1
        else:
            fail_count += 1
    
    # 删除不再需要的文件
    for rel_path in files_to_delete:
        target_file = TEMPLATE_DIR / rel_path
        if dry_run:
            print(f"  [DRY RUN] 将删除: {target_file}")
        else:
            try:
                if target_file.is_file():
                    target_file.unlink()
                    print(f"  ✓ 已删除: {rel_path}")
                elif target_file.is_dir():
                    shutil.rmtree(target_file)
                    print(f"  ✓ 已删除目录: {rel_path}")
            except Exception as e:
                print(f"  ✗ 删除失败: {rel_path} - {e}")
                fail_count += 1
    
    return success_count, fail_count


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="同步项目代码到 CookieCutter 模版")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="试运行模式，只显示将要执行的操作，不实际执行"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细信息"
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("模版同步脚本")
    print("=" * 60)
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"模版目录: {TEMPLATE_DIR}")
    print(f"模式: {'试运行（不实际执行）' if args.dry_run else '实际执行'}")
    print("=" * 60)
    print()
    
    if not TEMPLATE_DIR.parent.exists():
        print(f"错误: 模版目录不存在: {TEMPLATE_DIR.parent}")
        return 1
    
    # 确保模版目录存在
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    
    total_success = 0
    total_fail = 0
    
    # 同步各个路径
    for sync_path in SYNC_PATHS:
        source_path = PROJECT_ROOT / sync_path
        target_path = TEMPLATE_DIR / sync_path
        
        if not source_path.exists():
            if args.verbose:
                print(f"跳过不存在的路径: {sync_path}")
            continue
        
        print(f"同步: {sync_path}")
        
        if source_path.is_file():
            # 同步单个文件
            if sync_file(source_path, target_path, args.dry_run):
                total_success += 1
            else:
                total_fail += 1
        elif source_path.is_dir():
            # 同步目录
            success, fail = sync_directory(source_path, target_path, args.dry_run)
            total_success += success
            total_fail += fail
        else:
            print(f"  ⚠ 跳过未知类型: {sync_path}")
        
        print()
    
    # 总结
    print("=" * 60)
    print("同步完成")
    print("=" * 60)
    print(f"成功: {total_success}")
    print(f"失败: {total_fail}")
    
    if args.dry_run:
        print("\n提示: 这是试运行模式，没有实际执行任何操作。")
        print("      要实际执行同步，请运行: python scripts/sync_template.py")
    
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    exit(main())
