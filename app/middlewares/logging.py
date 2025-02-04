import time
from fastapi import Request
from ..utils.logger import logger

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 记录请求信息
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Client: {request.client.host if request.client else 'Unknown'}"
    )
    
    response = await call_next(request)
    
    # 记录响应信息
    process_time = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} "
        f"Process Time: {process_time:.3f}s"
    )
    
    return response 