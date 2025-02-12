from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .base import CRUDBase
from ..models.subcontractor import Subcontractor
from ..schemas.subcontractor import SubcontractorCreate, SubcontractorUpdate
from ..utils.transaction import TransactionManager
from ..utils.logger import logger

class CRUDSubcontractor(CRUDBase[Subcontractor, SubcontractorCreate, SubcontractorUpdate]):
    def create(self, db: Session, *, obj_in: SubcontractorCreate) -> Subcontractor:
        with TransactionManager(db):
            # 检查名称是否已存在
            existing = db.query(Subcontractor).filter(
                Subcontractor.name == obj_in.name
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="分包商名称已存在"
                )
            
            db_obj = Subcontractor(
                name=obj_in.name,
                contact_name=obj_in.contact_name,
                contact_phone=obj_in.contact_phone,
                remarks=obj_in.remarks
            )
            db.add(db_obj)
            db.flush()
            
            logger.info(f"Created subcontractor: {db_obj.name}")
            
            return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Subcontractor,
        obj_in: Union[SubcontractorUpdate, Dict[str, Any]]
    ) -> Subcontractor:
        with TransactionManager(db):
            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, SubcontractorUpdate) else obj_in
            
            # 如果更新名称，检查是否已存在
            if "name" in update_data and update_data["name"] != db_obj.name:
                existing = db.query(Subcontractor).filter(
                    Subcontractor.name == update_data["name"]
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="分包商名称已存在"
                    )
            
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.flush()
            
            logger.info(f"Updated subcontractor: {db_obj.name}")
            
            return db_obj

    def remove(self, db: Session, *, id: int) -> Subcontractor:
        with TransactionManager(db):
            obj = db.query(Subcontractor).get(id)
            if not obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="分包商不存在"
                )
            
            # 检查是否有关联的合同
            if obj.contracts:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="无法删除已有合同的分包商"
                )
            
            logger.warning(f"Deleting subcontractor: {obj.name}")
            
            db.delete(obj)
            return obj

    def get_by_name(self, db: Session, *, name: str) -> List[Subcontractor]:
        return db.query(Subcontractor).filter(
            Subcontractor.name.ilike(f"%{name}%")
        ).all()

    def get_with_contracts(self, db: Session, *, id: int) -> Subcontractor:
        return db.query(Subcontractor).filter(Subcontractor.id == id).first()

subcontractor = CRUDSubcontractor(Subcontractor) 