from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import boq_item
from ..schemas.boq_item import (
    BOQItem,
    BOQItemCreate,
    BOQItemUpdate
)
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/boq-items", tags=["工程量清单"])

@router.get("/contract/{contract_id}", response_model=List[BOQItem])
def read_boq_items_by_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_user)
):
    """获取合同下的工程量清单项目"""
    return boq_item.get_by_contract(db=db, contract_id=contract_id, skip=skip, limit=limit)

@router.post("/", response_model=BOQItem)
def create_boq_item(
    *,
    db: Session = Depends(get_db),
    obj_in: BOQItemCreate,
    _: dict = Depends(get_current_user)
):
    """创建工程量清单项目"""
    return boq_item.create_with_contract(db=db, obj_in=obj_in, contract_id=obj_in.contract_id)

@router.get("/{id}", response_model=BOQItem)
def read_boq_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """获取工程量清单项目详情"""
    db_obj = boq_item.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工程量清单项目不存在"
        )
    return db_obj

@router.put("/{id}", response_model=BOQItem)
def update_boq_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: BOQItemUpdate,
    _: dict = Depends(get_current_user)
):
    """更新工程量清单项目"""
    db_obj = boq_item.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工程量清单项目不存在"
        )
    return boq_item.update(db=db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=BOQItem)
def delete_boq_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """删除工程量清单项目"""
    db_obj = boq_item.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工程量清单项目不存在"
        )
    return boq_item.remove(db=db, id=id) 