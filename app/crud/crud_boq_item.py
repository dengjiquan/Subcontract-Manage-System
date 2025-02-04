from typing import List, Union, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .base import CRUDBase
from ..models.boq_item import BOQItem
from ..schemas.boq_item import BOQItemCreate, BOQItemUpdate
from ..utils.validators import DataValidator
from ..utils.calculations import CalculationManager
from ..utils.transaction import TransactionManager
from ..utils.logger import logger

class CRUDBOQItem(CRUDBase[BOQItem, BOQItemCreate, BOQItemUpdate]):
    def get_by_contract(
        self, db: Session, *, contract_id: int, skip: int = 0, limit: int = 100
    ) -> List[BOQItem]:
        return (
            db.query(BOQItem)
            .filter(BOQItem.contract_id == contract_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_contract(
        self, db: Session, *, obj_in: BOQItemCreate, contract_id: int
    ) -> BOQItem:
        with TransactionManager(db):
            # 验证数量和单价
            if obj_in.total_quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="总数量必须大于0"
                )
            if obj_in.unit_price <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="单价必须大于0"
                )

            # 验证合同状态
            DataValidator.validate_contract_status(
                db, contract_id, expected_status="active"
            )
            
            db_obj = BOQItem(
                contract_id=contract_id,
                item_name=obj_in.item_name,
                unit_price=obj_in.unit_price,
                total_quantity=obj_in.total_quantity,
                unit=obj_in.unit,
                total_price=obj_in.unit_price * obj_in.total_quantity
            )
            db.add(db_obj)
            db.flush()
            
            # 更新合同金额
            CalculationManager.update_contract_amount(db, contract_id)
            
            logger.info(
                f"Created BOQ item: {db_obj.item_name} "
                f"for contract: {contract_id}, "
                f"amount: {db_obj.total_price}"
            )
            
            return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: BOQItem,
        obj_in: Union[BOQItemUpdate, Dict[str, Any]]
    ) -> BOQItem:
        with TransactionManager(db):
            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BOQItemUpdate) else obj_in
            
            # 验证合同状态
            DataValidator.validate_contract_status(
                db, db_obj.contract_id, expected_status="active"
            )
            
            # 验证数量和单价
            if "total_quantity" in update_data and update_data["total_quantity"] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="总数量必须大于0"
                )
            if "unit_price" in update_data and update_data["unit_price"] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="单价必须大于0"
                )
            
            # 更新单价或数量时重新计算总价
            if "unit_price" in update_data or "total_quantity" in update_data:
                unit_price = update_data.get("unit_price", db_obj.unit_price)
                total_quantity = update_data.get("total_quantity", db_obj.total_quantity)
                update_data["total_price"] = unit_price * total_quantity
            
            # 检查是否有已结算的数量
            if "total_quantity" in update_data:
                total_settled = db.query(
                    db.func.sum(SettlementDetail.completed_quantity)
                ).filter(
                    SettlementDetail.boq_item_id == db_obj.id
                ).scalar() or Decimal('0')
                
                if total_settled > update_data["total_quantity"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="新的总数量不能小于已结算数量"
                    )
            
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.flush()
            
            # 更新合同金额
            CalculationManager.update_contract_amount(db, db_obj.contract_id)
            
            logger.info(
                f"Updated BOQ item: {db_obj.item_name}, "
                f"new amount: {db_obj.total_price}"
            )
            
            return db_obj

    def remove(self, db: Session, *, id: int) -> BOQItem:
        with TransactionManager(db):
            db_obj = db.query(BOQItem).get(id)
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="工程量清单项目不存在"
                )
            
            # 验证合同状态
            DataValidator.validate_contract_status(
                db, db_obj.contract_id, expected_status="active"
            )
            
            # 检查是否已有结算
            if db_obj.settlement_details:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="已有结算记录的项目不能删除"
                )
            
            logger.warning(
                f"Deleting BOQ item: {db_obj.item_name} "
                f"from contract: {db_obj.contract_id}"
            )
            
            contract_id = db_obj.contract_id
            db.delete(db_obj)
            db.flush()
            
            # 更新合同金额
            CalculationManager.update_contract_amount(db, contract_id)
            
            return db_obj

boq_item = CRUDBOQItem(BOQItem) 