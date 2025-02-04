from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile
import shutil
import os
from .base import CRUDBase
from ..models.payment import Payment, ContractFile
from ..schemas.payment import PaymentCreate, PaymentUpdate, ContractFileCreate
from ..config import settings
from ..utils.validators import DataValidator
from ..utils.transaction import TransactionManager
from ..utils.logger import logger

class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_settlement(
        self, db: Session, *, settlement_id: int, skip: int = 0, limit: int = 100
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.settlement_id == settlement_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: PaymentCreate) -> Payment:
        with TransactionManager(db):
            # 验证付款金额
            DataValidator.validate_payment_amount(
                db, obj_in.settlement_id, obj_in.payment_amount
            )
            
            db_obj = Payment(
                settlement_id=obj_in.settlement_id,
                payment_date=obj_in.payment_date,
                payment_amount=obj_in.payment_amount,
                payment_method=obj_in.payment_method,
                remarks=obj_in.remarks
            )
            db.add(db_obj)
            db.flush()
            
            logger.info(
                f"Created payment: {obj_in.payment_amount} "
                f"for settlement: {obj_in.settlement_id}"
            )
            
            return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Payment,
        obj_in: Union[PaymentUpdate, Dict[str, Any]]
    ) -> Payment:
        with TransactionManager(db):
            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, PaymentUpdate) else obj_in
            
            # 如果更新付款金额，进行验证
            if "payment_amount" in update_data:
                DataValidator.validate_payment_amount(
                    db,
                    db_obj.settlement_id,
                    update_data["payment_amount"]
                )
            
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.flush()
            
            logger.info(f"Updated payment: {db_obj.id}")
            
            return db_obj

class CRUDContractFile(CRUDBase[ContractFile, ContractFileCreate, ContractFileCreate]):
    async def create_with_file(
        self, db: Session, *, contract_id: int, file: UploadFile
    ) -> ContractFile:
        # 确保上传目录存在
        upload_dir = settings.UPLOAD_DIR / str(contract_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # 保存文件
        file_path = upload_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 创建数据库记录
        db_obj = ContractFile(
            contract_id=contract_id,
            file_name=file.filename,
            file_path=str(file_path)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_with_file(self, db: Session, *, id: int) -> ContractFile:
        obj = db.query(ContractFile).get(id)
        if obj and os.path.exists(obj.file_path):
            os.remove(obj.file_path)
        db.delete(obj)
        db.commit()
        return obj

payment = CRUDPayment(Payment)
contract_file = CRUDContractFile(ContractFile) 