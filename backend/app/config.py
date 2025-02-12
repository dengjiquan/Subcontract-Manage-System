from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional, Set, List
import os

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "分包商管理系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # 添加环境配置
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///../../database/subcontractor.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 文件上传配置
    UPLOAD_DIR: Path = Path("static/uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Set[str] = {"pdf", "doc", "docx", "jpg", "jpeg", "png"}

    # Redis配置
    REDIS_HOST: str = "localhost"  # 修改为本地开发环境
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # 性能配置
    SLOW_QUERY_THRESHOLD: float = 1.0  # 秒
    CACHE_EXPIRE_TIME: int = 300  # 秒
    
    # 监控配置
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    # 数据库备份配置
    BACKUP_ENABLED: bool = True
    BACKUP_INTERVAL_HOURS: int = 24
    BACKUP_RETENTION_DAYS: int = 7
    
    # 安全配置
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100  # 请求次数
    RATE_LIMIT_PERIOD: int = 60  # 时间窗口（秒）
    
    # SSL配置
    SSL_KEYFILE: str = ""
    SSL_CERTFILE: str = ""
    
    # 密码策略
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPER: bool = True
    PASSWORD_REQUIRE_LOWER: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    class Config:
        env_file = ".env"

settings = Settings() 