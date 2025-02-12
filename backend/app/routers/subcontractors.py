from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import subcontractor
from ..schemas.subcontractor import (
    Subcontractor,
    SubcontractorCreate,
    SubcontractorUpdate,
    SubcontractorWithContracts
)
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/subcontractors", tags=["分包商"])

@router.get("/", response_model=List[Subcontractor])
def read_subcontractors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_user)
):
    """获取分包商列表"""
    return subcontractor.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Subcontractor)
def create_subcontractor(
    *,
    db: Session = Depends(get_db),
    obj_in: SubcontractorCreate,
    _: dict = Depends(get_current_user)
):
    """创建分包商"""
    return subcontractor.create(db=db, obj_in=obj_in)

@router.get("/{id}", response_model=SubcontractorWithContracts)
def read_subcontractor(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """获取分包商详情"""
    db_obj = subcontractor.get_with_contracts(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分包商不存在"
        )
    return db_obj

@router.put("/{id}", response_model=Subcontractor)
def update_subcontractor(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: SubcontractorUpdate,
    _: dict = Depends(get_current_user)
):
    """更新分包商"""
    db_obj = subcontractor.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分包商不存在"
        )
    return subcontractor.update(db=db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=Subcontractor)
def delete_subcontractor(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """删除分包商"""
    db_obj = subcontractor.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分包商不存在"
        )
    return subcontractor.remove(db=db, id=id) 