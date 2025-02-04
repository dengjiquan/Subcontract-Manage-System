from prometheus_client import Counter, Histogram
import time
from typing import Callable
from fastapi import Request, Response
from .utils.logger import logger

# 定义指标
REQUEST_COUNT = Counter(
    'http_request_count',
    'HTTP Request Count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

DB_QUERY_LATENCY = Histogram(
    'db_query_latency_seconds',
    'Database Query Latency',
    ['operation']
)

class PrometheusMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        # 记录请求指标
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        # 记录延迟指标
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(time.time() - start_time)
        
        return response

def track_db_query(operation: str):
    """数据库查询性能跟踪装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = await func(*args, **kwargs)
            
            # 记录查询延迟
            query_time = time.time() - start_time
            DB_QUERY_LATENCY.labels(
                operation=operation
            ).observe(query_time)
            
            # 记录慢查询
            if query_time > 1.0:  # 超过1秒的查询
                logger.warning(
                    f"Slow query detected: {operation} "
                    f"Time: {query_time:.3f}s"
                )
            
            return result
        return wrapper
    return decorator 