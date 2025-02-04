from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from ..crud import contract, contract_file
from ..schemas.contract import (
    Contract,
    ContractCreate,
    ContractUpdate,
    ContractWithDetails
)
from ..schemas.payment import ContractFileInDB
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/contracts", tags=["合同"])

@router.get("/", response_model=List[Contract])
def read_contracts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: dict = Depends(get_current_user)
):
    """获取合同列表"""
    return contract.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Contract)
def create_contract(
    *,
    db: Session = Depends(get_db),
    obj_in: ContractCreate,
    _: dict = Depends(get_current_user)
):
    """创建合同"""
    return contract.create(db=db, obj_in=obj_in)

@router.get("/{id}", response_model=ContractWithDetails)
def read_contract(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """获取合同详情"""
    db_obj = contract.get_with_details(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )
    return db_obj

@router.put("/{id}", response_model=Contract)
def update_contract(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: ContractUpdate,
    _: dict = Depends(get_current_user)
):
    """更新合同"""
    db_obj = contract.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )
    return contract.update(db=db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=Contract)
def delete_contract(
    *,
    db: Session = Depends(get_db),
    id: int,
    _: dict = Depends(get_current_user)
):
    """删除合同"""
    db_obj = contract.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )
    return contract.remove(db=db, id=id)

@router.post("/{id}/files", response_model=ContractFileInDB)
async def upload_contract_file(
    *,
    db: Session = Depends(get_db),
    id: int,
    file: UploadFile = File(...),
    _: dict = Depends(get_current_user)
):
    """上传合同文件"""
    db_obj = contract.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )
    return await contract_file.create_with_file(db=db, contract_id=id, file=file) 