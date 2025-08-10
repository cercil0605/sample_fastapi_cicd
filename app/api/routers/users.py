from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from app.domain.schema import UserCreate, UserUpdate, UserOut
from app.infra.repository import FirestoreUserRepository, UserRepository
from app.usecase.user_usecase import UserUseCase

router = APIRouter(prefix="/users", tags=["users"])

def get_service() -> UserUseCase:
    repo: UserRepository = FirestoreUserRepository()
    return UserUseCase(repo)

@router.post("", response_model=dict)
def create_user(payload: UserCreate, svc: UserUseCase = Depends(get_service)):
    user_id = svc.create_user(payload)
    return {"id": user_id}

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, svc: UserUseCase = Depends(get_service)):
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.patch("/{user_id}", response_model=dict)
def update_user(user_id: str, patch: UserUpdate, svc: UserUseCase = Depends(get_service)):
    ok = svc.update_user(user_id, patch)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"updated": True}

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: str, svc: UserUseCase = Depends(get_service)):
    ok = svc.delete_user(user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"deleted": True}

@router.get("", response_model=List[Dict[str, Any]])
def search_users(
    skill: Optional[str] = Query(default=None, description="技術スキルの完全一致（array_contains）"),
    location: Optional[str] = Query(default=None, description="希望勤務地の完全一致（array_contains）"),
    limit: int = Query(default=50, ge=1, le=200),
    svc: UserUseCase = Depends(get_service),
):
    return svc.search_users(skill=skill, location=location, limit=limit)
