from typing import List, Union, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models.settlement import Settlement, SettlementDetail
from ..schemas.settlement import SettlementCreate, SettlementUpdate
from fastapi import HTTPException, status
from ..utils.validators import DataValidator
from ..utils.calculations import CalculationManager
from ..utils.transaction import TransactionManager
from ..utils.logger import logger

class CRUDSettlement(CRUDBase[Settlement, SettlementCreate, SettlementUpdate]):
    def create_with_details(
        self, db: Session, *, obj_in: SettlementCreate
    ) -> Settlement:
        with TransactionManager(db):
            # 验证结算日期
            DataValidator.validate_settlement_date(
                db, obj_in.contract_id, obj_in.settlement_date
            )
            
            # 验证合同状态
            DataValidator.validate_contract_status(
                db, obj_in.contract_id, expected_status="active"
            )
            
            # 创建结算主表
            db_obj = Settlement(
                contract_id=obj_in.contract_id,
                settlement_date=obj_in.settlement_date,
                remarks=obj_in.remarks
            )
            db.add(db_obj)
            db.flush()

            total_settlement_amount = Decimal('0')
            
            # 创建结算明细
            for detail in obj_in.details:
                # 验证结算数量
                if not CalculationManager.validate_settlement_quantity(
                    db, detail.boq_item_id, detail.completed_quantity
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"BOQ项目ID {detail.boq_item_id} 的结算数量超过合同数量"
                    )
                
                # 计算结算金额
                settlement_amount = CalculationManager.calculate_settlement_amount(
                    db, detail.boq_item_id, detail.completed_quantity
                )
                
                db_detail = SettlementDetail(
                    settlement_id=db_obj.id,
                    boq_item_id=detail.boq_item_id,
                    completed_quantity=detail.completed_quantity,
                    settlement_amount=settlement_amount
                )
                db.add(db_detail)
                total_settlement_amount += settlement_amount
            
            db.flush()
            
            # 更新结算总金额
            CalculationManager.update_settlement_amount(db, db_obj.id)
            
            logger.info(
                f"Created settlement for contract {obj_in.contract_id}, "
                f"date: {obj_in.settlement_date}, "
                f"amount: {total_settlement_amount}"
            )
            
            return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Settlement,
        obj_in: Union[SettlementUpdate, Dict[str, Any]]
    ) -> Settlement:
        with TransactionManager(db):
            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, SettlementUpdate) else obj_in
            
            # 验证合同状态
            DataValidator.validate_contract_status(
                db, db_obj.contract_id, expected_status="active"
            )
            
            # 如果更新日期，进行验证
            if "settlement_date" in update_data:
                DataValidator.validate_settlement_date(
                    db, db_obj.contract_id, update_data["settlement_date"]
                )
            
            # 检查是否已有付款记录
            if db_obj.payments:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="已有付款记录的结算不能修改"
                )
            
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.flush()
            
            logger.info(
                f"Updated settlement {db_obj.id}, "
                f"contract: {db_obj.contract_id}"
            )
            
            return db_obj

    def remove(self, db: Session, *, id: int) -> Settlement:
        with TransactionManager(db):
            db_obj = db.query(Settlement).get(id)
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="结算记录不存在"
                )
            
            # 验证合同状态
            DataValidator.validate_contract_status(
                db, db_obj.contract_id, expected_status="active"
            )
            
            # 检查是否已有付款记录
            if db_obj.payments:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="已有付款记录的结算不能删除"
                )
            
            logger.warning(
                f"Deleting settlement {db_obj.id}, "
                f"contract: {db_obj.contract_id}, "
                f"amount: {db_obj.settlement_amount}"
            )
            
            db.delete(db_obj)
            return db_obj

    def get_by_contract(
        self, db: Session, *, contract_id: int, skip: int = 0, limit: int = 100
    ) -> List[Settlement]:
        return (
            db.query(Settlement)
            .filter(Settlement.contract_id == contract_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

settlement = CRUDSettlement(Settlement) 