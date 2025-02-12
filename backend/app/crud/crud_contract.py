from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .base import CRUDBase
from ..models.contract import Contract
from ..schemas.contract import ContractCreate, ContractUpdate
from ..utils.validators import DataValidator
from ..utils.transaction import TransactionManager
from ..utils.logger import logger

class CRUDContract(CRUDBase[Contract, ContractCreate, ContractUpdate]):
    def create(self, db: Session, *, obj_in: ContractCreate) -> Contract:
        with TransactionManager(db):
            # 验证日期
            DataValidator.validate_contract_dates(obj_in.start_date, obj_in.end_date)
            
            db_obj = Contract(
                subcontractor_id=obj_in.subcontractor_id,
                contract_number=obj_in.contract_number,
                start_date=obj_in.start_date,
                end_date=obj_in.end_date,
                status=obj_in.status
            )
            db.add(db_obj)
            db.flush()
            
            logger.info(
                f"Created contract: {db_obj.contract_number} "
                f"for subcontractor: {db_obj.subcontractor_id}"
            )
            
            return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Contract,
        obj_in: Union[ContractUpdate, Dict[str, Any]]
    ) -> Contract:
        with TransactionManager(db):
            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, ContractUpdate) else obj_in
            
            # 如果更新日期，进行验证
            if "start_date" in update_data or "end_date" in update_data:
                start_date = update_data.get("start_date", db_obj.start_date)
                end_date = update_data.get("end_date", db_obj.end_date)
                DataValidator.validate_contract_dates(start_date, end_date)
            
            # 如果更新状态，进行验证
            if "status" in update_data:
                # 这里可以添加状态转换的验证逻辑
                logger.info(
                    f"Contract status change: {db_obj.contract_number} "
                    f"from {db_obj.status} to {update_data['status']}"
                )
            
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.flush()
            
            logger.info(f"Updated contract: {db_obj.contract_number}")
            
            return db_obj

    def remove(self, db: Session, *, id: int) -> Contract:
        with TransactionManager(db):
            obj = db.query(Contract).get(id)
            if not obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="合同不存在"
                )
            
            # 验证合同是否可以删除
            if obj.status != "draft":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="只能删除草稿状态的合同"
                )
            
            logger.warning(f"Deleting contract: {obj.contract_number}")
            
            db.delete(obj)
            return obj

    def get_by_number(self, db: Session, *, contract_number: str) -> Optional[Contract]:
        return db.query(Contract).filter(Contract.contract_number == contract_number).first()

    def get_by_subcontractor(
        self, db: Session, *, subcontractor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contract]:
        return (
            db.query(Contract)
            .filter(Contract.subcontractor_id == subcontractor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_details(self, db: Session, *, id: int) -> Optional[Contract]:
        return db.query(Contract).filter(Contract.id == id).first()

contract = CRUDContract(Contract) 