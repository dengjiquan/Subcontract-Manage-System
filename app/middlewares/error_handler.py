from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from ..utils.exceptions import BusinessError

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except BusinessError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except IntegrityError as e:
        return JSONResponse(
            status_code=400,
            content={"detail": "数据完整性错误，可能是唯一约束或外键约束被违反"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "服务器内部错误"}
        ) 