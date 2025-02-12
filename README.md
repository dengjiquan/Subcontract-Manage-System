# 分包管理系统

这是一个用于管理分包业务的系统。

## 项目结构

```
.
├── backend/              # 后端项目目录
│   ├── app/             # 后端应用主目录
│   ├── requirements.txt # Python依赖文件
│   └── setup.py        # Python包配置文件
├── database/            # 数据库相关文件
│   ├── alembic/        # 数据库迁移文件
│   ├── alembic.ini     # Alembic配置文件
│   └── schema.sql      # 数据库架构文件
├── deploy/             # 部署相关文件
│   ├── docker-compose.yml      # 开发环境Docker配置
│   ├── docker-compose.prod.yml # 生产环境Docker配置
│   ├── Dockerfile             # Docker构建文件
│   ├── nginx.conf            # Nginx配置文件
│   └── prometheus.yml        # Prometheus监控配置
├── frontend/           # 前端应用目录
├── tests/             # 测试文件目录
├── .env               # 开发环境配置
└── .env.prod.example  # 生产环境配置示例
```

## 开发环境设置

1. 安装后端依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量：
- 复制 `.env.prod.example` 到 `.env`
- 根据需要修改配置

3. 启动开发服务器：
```bash
# 后端
cd backend
python -m app

# 前端
cd frontend
npm install
npm run dev
```

## 部署

请参考 `deploy` 目录下的文件进行部署设置。 