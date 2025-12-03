# 测试配置加载
import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.config import settings

# 测试必需配置项
assert settings.app_name is not None
assert settings.app_version is not None
assert settings.environment is not None

# 测试可选配置项（如果未配置，可能为 None）
print(f"App name: {settings.app_name}")
print(f"App version: {settings.app_version}")
print(f"Environment: {settings.environment}")
print(f"Database URL: {settings.database_url}")  # 可能为 None
print(f"CORS origins: {settings.cors_origins}")  # 应该有默认值