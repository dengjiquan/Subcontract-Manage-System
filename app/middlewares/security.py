from fastapi import Request, HTTPException, status
from ..config import settings
from ..utils.logger import logger

async def security_middleware(request: Request, call_next):
    # 检查请求头
    if settings.ENVIRONMENT == "production":
        # 检查必要的安全头
        if "X-Content-Type-Options" not in request.headers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing security headers"
            )
    
    # 添加安全响应头
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response

def rate_limit(request: Request):
    """速率限制检查"""
    client_ip = request.client.host
    # 这里可以添加具体的速率限制逻辑，比如使用Redis记录请求次数
    return True 