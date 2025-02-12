import os
import subprocess
from datetime import datetime
from pathlib import Path
from ..config import settings
from ..utils.logger import logger

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self):
        """创建数据库备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.sql"
        backup_path = self.backup_dir / filename
        
        try:
            # 执行pg_dump
            subprocess.run([
                "pg_dump",
                "-h", settings.DB_HOST,
                "-U", settings.DB_USER,
                "-d", settings.DB_NAME,
                "-f", str(backup_path)
            ], check=True, env={
                "PGPASSWORD": settings.DB_PASSWORD
            })
            
            logger.info(f"Database backup created: {filename}")
            return backup_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {str(e)}")
            raise
    
    def restore_backup(self, backup_file: Path):
        """从备份文件恢复数据库"""
        try:
            # 执行psql恢复
            subprocess.run([
                "psql",
                "-h", settings.DB_HOST,
                "-U", settings.DB_USER,
                "-d", settings.DB_NAME,
                "-f", str(backup_file)
            ], check=True, env={
                "PGPASSWORD": settings.DB_PASSWORD
            })
            
            logger.info(f"Database restored from: {backup_file.name}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {str(e)}")
            raise
    
    def cleanup_old_backups(self, keep_days: int = 7):
        """清理旧的备份文件"""
        current_time = datetime.now()
        
        for backup_file in self.backup_dir.glob("backup_*.sql"):
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            age_days = (current_time - file_time).days
            
            if age_days > keep_days:
                backup_file.unlink()
                logger.info(f"Deleted old backup: {backup_file.name}") 