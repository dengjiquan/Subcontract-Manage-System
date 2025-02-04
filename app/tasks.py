from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .utils.backup import DatabaseBackup
from .config import settings
from .utils.logger import logger

scheduler = AsyncIOScheduler()

def setup_scheduler():
    """设置定时任务"""
    if settings.BACKUP_ENABLED:
        # 添加数据库备份任务
        scheduler.add_job(
            backup_database,
            CronTrigger(hour=0),  # 每天0点执行
            id="database_backup",
            replace_existing=True
        )
        
        # 添加清理旧备份任务
        scheduler.add_job(
            cleanup_old_backups,
            CronTrigger(hour=1),  # 每天1点执行
            id="cleanup_backups",
            replace_existing=True
        )
    
    scheduler.start()
    logger.info("Scheduler started")

async def backup_database():
    """执行数据库备份"""
    try:
        backup = DatabaseBackup()
        backup.create_backup()
    except Exception as e:
        logger.error(f"Database backup failed: {str(e)}")

async def cleanup_old_backups():
    """清理旧备份"""
    try:
        backup = DatabaseBackup()
        backup.cleanup_old_backups(settings.BACKUP_RETENTION_DAYS)
    except Exception as e:
        logger.error(f"Backup cleanup failed: {str(e)}") 