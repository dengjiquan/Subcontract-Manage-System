from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .config import settings
from .routers import (
    auth_router,
    subcontractors_router,
    contracts_router,
    boq_items_router,
    settlements_router,
    payments_router
)
from .middlewares.error_handler import error_handler_middleware
from .middlewares.logging import logging_middleware
from .middlewares.security import security_middleware
from .tasks import setup_scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    分包商管理系统API文档
    
    主要功能：
    * 分包商管理
    * 合同管理
    * 工程量清单管理
    * 结算管理
    * 付款管理
    """,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # 自定义安全方案
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # 为所有路由添加安全要求
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加错误处理中间件
app.middleware("http")(error_handler_middleware)

# 添加日志中间件
app.middleware("http")(logging_middleware)

# 添加安全中间件
app.middleware("http")(security_middleware)

# 注册路由
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(subcontractors_router, prefix=settings.API_V1_STR)
app.include_router(contracts_router, prefix=settings.API_V1_STR)
app.include_router(boq_items_router, prefix=settings.API_V1_STR)
app.include_router(settlements_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "欢迎使用分包商管理系统"}

@app.on_event("startup")
async def startup_event():
    # 启动定时任务
    setup_scheduler() 