import time
from fastapi import Request
from ..utils.logger import logger

async def performance_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 记录请求开始
    logger.info(
        f"Request started: {request.method} {request.url.path} "
        f"Client: {request.client.host if request.client else 'Unknown'}"
    )
    
    # 执行请求
    response = await call_next(request)
    
    # 计算处理时间
    process_time = time.time() - start_time
    
    # 记录性能指标
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Process Time: {process_time:.3f}s"
    )
    
    # 添加性能指标到响应头
    response.headers["X-Process-Time"] = str(process_time)
    
    return response 