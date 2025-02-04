from contextlib import contextmanager
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

@contextmanager
def transaction(db: Session):
    """数据库事务管理器"""
    try:
        yield
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

class TransactionManager:
    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc_val)
            )
        self.db.commit() 