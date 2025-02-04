from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import payment
from ..schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentInDB
)
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["付款"])

@router.get("/settlement/{settlement_id}", response_model=List[PaymentInDB])
def read_payments_by_settlement(
    settlement_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_user)
):
    """获取结算下的付款记录"""
    return payment.get_by_settlement(db=db, settlement_id=settlement_id, skip=skip, limit=limit)

@router.post("/", response_model=PaymentInDB)
def create_payment(
    *,
    db: Session = Depends(get_db),
    obj_in: PaymentCreate,
    _: dict = Depends(get_current_user)
):
    """创建付款记录"""
    return payment.create(db=db, obj_in=obj_in)

@router.get("/{id}", response_model=PaymentInDB)
def read_payment(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """获取付款记录详情"""
    db_obj = payment.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="付款记录不存在"
        )
    return db_obj

@router.put("/{id}", response_model=PaymentInDB)
def update_payment(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: PaymentUpdate,
    _: dict = Depends(get_current_user)
):
    """更新付款记录"""
    db_obj = payment.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="付款记录不存在"
        )
    return payment.update(db=db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=PaymentInDB)
def delete_payment(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """删除付款记录"""
    db_obj = payment.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="付款记录不存在"
        )
    return payment.remove(db=db, id=id) 