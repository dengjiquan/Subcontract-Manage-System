from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import settlement
from ..schemas.settlement import (
    Settlement,
    SettlementCreate,
    SettlementUpdate
)
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/settlements", tags=["结算"])

@router.get("/contract/{contract_id}", response_model=List[Settlement])
def read_settlements_by_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_user)
):
    """获取合同下的结算记录"""
    return settlement.get_by_contract(db=db, contract_id=contract_id, skip=skip, limit=limit)

@router.post("/", response_model=Settlement)
def create_settlement(
    *,
    db: Session = Depends(get_db),
    obj_in: SettlementCreate,
    _: dict = Depends(get_current_user)
):
    """创建结算记录"""
    return settlement.create_with_details(db=db, obj_in=obj_in)

@router.get("/{id}", response_model=Settlement)
def read_settlement(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """获取结算记录详情"""
    db_obj = settlement.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="结算记录不存在"
        )
    return db_obj

@router.put("/{id}", response_model=Settlement)
def update_settlement(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: SettlementUpdate,
    _: dict = Depends(get_current_user)
):
    """更新结算记录"""
    db_obj = settlement.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="结算记录不存在"
        )
    return settlement.update(db=db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=Settlement)
def delete_settlement(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """删除结算记录"""
    db_obj = settlement.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="结算记录不存在"
        )
    return settlement.remove(db=db, id=id) 