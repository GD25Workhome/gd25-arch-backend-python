"""
配置管理模块

使用 Pydantic Settings 进行配置验证和管理，支持环境变量读取和 .env 文件加载。
提供配置扩展机制，允许项目添加自定义配置项。
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类
    
    使用 Pydantic Settings 进行配置验证，支持从环境变量和 .env 文件加载配置。
    所有配置项都可以通过环境变量设置，环境变量名使用大写字母和下划线。
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 允许额外的配置项，用于扩展
    )

    # ==================== 应用配置 ====================
    app_name: str = Field(
        default="gd25-arch-backend",
        description="应用名称",
    )
    app_version: str = Field(
        default="1.0.0",
        description="应用版本",
    )
    debug: bool = Field(
        default=False,
        description="调试模式",
    )
    environment: str = Field(
        default="development",
        description="运行环境：development, testing, production",
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """验证环境值"""
        allowed = ["development", "testing", "production"]
        if v not in allowed:
            raise ValueError(f"environment 必须是 {allowed} 之一")
        return v

    # ==================== 数据库配置 ====================
    database_url: str = Field(
        ...,
        description="数据库连接 URL，格式：postgresql://user:password@host:port/dbname 或 mysql+pymysql://user:password@host:port/dbname",
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """验证数据库 URL 格式"""
        if not v:
            raise ValueError("database_url 不能为空")
        # 基本格式检查
        if not (v.startswith("postgresql://") or v.startswith("mysql+pymysql://")):
            raise ValueError(
                "database_url 必须以 postgresql:// 或 mysql+pymysql:// 开头"
            )
        return v

    # ==================== Redis 配置（可选）====================
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis 连接 URL，格式：redis://host:port/db",
    )

    # ==================== Celery 配置（可选）====================
    celery_broker_url: Optional[str] = Field(
        default=None,
        description="Celery Broker URL，通常使用 Redis",
    )
    celery_result_backend: Optional[str] = Field(
        default=None,
        description="Celery 结果后端 URL，通常使用 Redis",
    )

    # ==================== 日志配置 ====================
    log_level: str = Field(
        default="INFO",
        description="日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )
    log_format: str = Field(
        default="json",
        description="日志格式：json 或 text",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """验证日志级别"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level 必须是 {allowed} 之一")
        return v.upper()

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """验证日志格式"""
        allowed = ["json", "text"]
        if v.lower() not in allowed:
            raise ValueError(f"log_format 必须是 {allowed} 之一")
        return v.lower()

    # ==================== CORS 配置 ====================
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"],
        description="CORS 允许的源列表，多个源用逗号分隔",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """解析 CORS 源列表"""
        if isinstance(v, str):
            # 从字符串解析，支持逗号分隔
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            return []

    # ==================== 服务器配置 ====================
    host: str = Field(
        default="0.0.0.0",
        description="服务器监听地址",
    )
    port: int = Field(
        default=8000,
        description="服务器监听端口",
        ge=1,
        le=65535,
    )

    # ==================== 配置扩展点 ====================
    # 子类可以继承此类并添加自定义配置项
    # 示例：
    # class CustomSettings(Settings):
    #     custom_config: str = Field(default="default_value")

    def is_development(self) -> bool:
        """判断是否为开发环境"""
        return self.environment == "development"

    def is_testing(self) -> bool:
        """判断是否为测试环境"""
        return self.environment == "testing"

    def is_production(self) -> bool:
        """判断是否为生产环境"""
        return self.environment == "production"

    def get_database_url_sync(self) -> str:
        """
        获取同步数据库 URL
        
        如果使用异步数据库驱动，需要转换 URL。
        """
        return self.database_url

    def get_database_url_async(self) -> str:
        """
        获取异步数据库 URL
        
        将 postgresql:// 转换为 postgresql+asyncpg://
        将 mysql+pymysql:// 转换为 mysql+aiomysql://
        """
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("mysql+pymysql://"):
            return url.replace("mysql+pymysql://", "mysql+aiomysql://", 1)
        return url


# 创建全局配置实例
# 注意：在实际使用中，可以根据需要创建不同的配置实例
settings = Settings()


# 配置扩展示例
# 如果项目需要添加自定义配置项，可以这样扩展：
#
# class ProjectSettings(Settings):
#     """项目自定义配置"""
#     api_key: str = Field(..., description="API 密钥")
#     max_retries: int = Field(default=3, ge=1, le=10, description="最大重试次数")
#
# project_settings = ProjectSettings()

