import logging
from datetime import datetime
from pathlib import Path
from ..config import settings

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 创建日志文件名（按日期）
log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

# 配置日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 文件处理器
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 创建日志记录器
logger = logging.getLogger(settings.PROJECT_NAME)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler) 