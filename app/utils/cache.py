from functools import wraps
from typing import Optional
import json
from datetime import datetime, date
from decimal import Decimal
from redis import Redis
from ..config import settings

# Redis连接
redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

class JSONEncoder(json.JSONEncoder):
    """自定义JSON编码器，处理特殊类型"""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def cache(expire: int = 300):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            cached_result = redis.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            redis.setex(
                cache_key,
                expire,
                json.dumps(result, cls=JSONEncoder)
            )
            
            return result
        return wrapper
    return decorator 