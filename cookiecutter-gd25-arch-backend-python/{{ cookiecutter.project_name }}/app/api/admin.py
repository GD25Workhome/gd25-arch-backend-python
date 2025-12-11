"""
管理后台 API 路由

提供系统管理相关的 API 接口，包括：
- 系统信息查询
- 系统统计信息
- 数据库状态
- 配置信息查看（只读）
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies import get_db
from app.config import settings
from app.db.database import check_connection, get_engine
from app.utils.response import success_response

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/admin", tags=["管理后台"])


@router.get(
    "/system/info",
    response_model=dict,
    summary="获取系统信息",
    description="获取系统基本信息，包括应用名称、版本、环境等",
)
async def get_system_info() -> Dict[str, Any]:
    """
    获取系统信息
    
    Returns:
        dict: 系统信息
    """
    system_info = {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "log_level": settings.log_level,
        "log_format": settings.log_format,
        "current_time": datetime.now().isoformat(),
    }
    
    return success_response(
        data=system_info,
        message="系统信息获取成功"
    )


@router.get(
    "/system/health",
    response_model=dict,
    summary="获取系统健康状态",
    description="获取系统和数据库的健康状态",
)
async def get_system_health() -> Dict[str, Any]:
    """
    获取系统健康状态
    
    Returns:
        dict: 健康状态信息
    """
    health_status = {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.now().isoformat(),
    }
    
    # 检查数据库连接
    try:
        db_healthy = check_connection()
        health_status["database"] = {
            "status": "connected" if db_healthy else "disconnected",
            "healthy": db_healthy,
        }
    except Exception as e:
        logger.warning(f"数据库健康检查失败: {e}")
        health_status["database"] = {
            "status": "error",
            "healthy": False,
            "error": str(e),
        }
    
    # 判断整体健康状态
    if not health_status["database"]["healthy"]:
        health_status["status"] = "unhealthy"
    
    return success_response(
        data=health_status,
        message="健康状态获取成功"
    )


@router.get(
    "/database/stats",
    response_model=dict,
    summary="获取数据库统计信息",
    description="获取数据库连接和基本统计信息",
)
async def get_database_stats(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    获取数据库统计信息
    
    Args:
        db: 数据库会话
        
    Returns:
        dict: 数据库统计信息
    """
    stats = {
        "connected": False,
        "database_type": None,
        "tables_count": 0,
        "timestamp": datetime.now().isoformat(),
    }
    
    try:
        # 检查连接
        if check_connection():
            stats["connected"] = True
            
            # 判断数据库类型
            db_url = settings.database_url or ""
            if "postgresql" in db_url:
                stats["database_type"] = "PostgreSQL"
                # 获取表数量（PostgreSQL）
                result = db.execute(text("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                stats["tables_count"] = result.scalar() or 0
            elif "mysql" in db_url:
                stats["database_type"] = "MySQL"
                # 获取表数量（MySQL）
                result = db.execute(text("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                """))
                stats["tables_count"] = result.scalar() or 0
            else:
                stats["database_type"] = "Unknown"
        else:
            stats["connected"] = False
            stats["error"] = "数据库连接失败"
            
    except Exception as e:
        logger.error(f"获取数据库统计信息失败: {e}")
        stats["connected"] = False
        stats["error"] = str(e)
    
    return success_response(
        data=stats,
        message="数据库统计信息获取成功"
    )


@router.get(
    "/config/info",
    response_model=dict,
    summary="获取配置信息（只读）",
    description="获取系统配置信息（敏感信息已隐藏）",
)
async def get_config_info() -> Dict[str, Any]:
    """
    获取配置信息（只读，隐藏敏感信息）
    
    Returns:
        dict: 配置信息（敏感信息已隐藏）
    """
    # 隐藏敏感信息
    database_url = settings.database_url
    if database_url:
        # 只显示数据库类型和主机，隐藏用户名和密码
        if "postgresql://" in database_url:
            parts = database_url.split("@")
            if len(parts) > 1:
                database_url = f"postgresql://***@{parts[1]}"
        elif "mysql+pymysql://" in database_url:
            parts = database_url.split("@")
            if len(parts) > 1:
                database_url = f"mysql+pymysql://***@{parts[1]}"
    
    redis_url = settings.redis_url
    if redis_url:
        redis_url = "redis://***"  # 隐藏完整 URL
    
    celery_broker_url = settings.celery_broker_url
    if celery_broker_url:
        celery_broker_url = "***"  # 隐藏完整 URL
    
    config_info = {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "log_level": settings.log_level,
        "log_format": settings.log_format,
        "cors_origins": settings.cors_origins,
        "database_url": database_url,  # 已隐藏敏感信息
        "redis_url": redis_url,  # 已隐藏敏感信息
        "celery_broker_url": celery_broker_url,  # 已隐藏敏感信息
        "flower_port": settings.flower_port,
        "has_flower_auth": bool(settings.flower_basic_auth),
    }
    
    return success_response(
        data=config_info,
        message="配置信息获取成功"
    )


@router.get(
    "/stats/overview",
    response_model=dict,
    summary="获取系统概览统计",
    description="获取系统概览统计信息，包括用户数量等",
)
async def get_stats_overview(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    获取系统概览统计
    
    Args:
        db: 数据库会话
        
    Returns:
        dict: 系统概览统计信息
    """
    stats = {
        "timestamp": datetime.now().isoformat(),
        "users": {
            "total": 0,
            "active": 0,
        },
        "database": {
            "connected": False,
        },
    }
    
    try:
        # 检查数据库连接
        if check_connection():
            stats["database"]["connected"] = True
            
            # 获取用户统计（如果用户表存在）
            try:
                # 检查表是否存在
                db_url = settings.database_url or ""
                if "postgresql" in db_url:
                    result = db.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'users'
                        )
                    """))
                    table_exists = result.scalar()
                elif "mysql" in db_url:
                    result = db.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.tables 
                        WHERE table_schema = DATABASE() 
                        AND table_name = 'users'
                    """))
                    table_exists = result.scalar() > 0
                else:
                    table_exists = False
                
                if table_exists:
                    # 获取用户总数
                    result = db.execute(text("SELECT COUNT(*) FROM users"))
                    stats["users"]["total"] = result.scalar() or 0
                    
                    # 获取活跃用户数（is_active = True）
                    result = db.execute(text("""
                        SELECT COUNT(*) FROM users WHERE is_active = TRUE
                    """))
                    stats["users"]["active"] = result.scalar() or 0
            except Exception as e:
                logger.warning(f"获取用户统计失败: {e}")
                # 表可能不存在，忽略错误
        else:
            stats["database"]["connected"] = False
            
    except Exception as e:
        logger.error(f"获取系统概览统计失败: {e}")
        stats["error"] = str(e)
    
    return success_response(
        data=stats,
        message="系统概览统计获取成功"
    )
