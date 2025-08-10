from typing import Optional, List, Dict, Any
from app.domain.schema import UserCreate, UserOut, UserUpdate
from app.infra.repository import UserRepository

class UserUseCase:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def create_user(self,payload: UserCreate) -> str:
        return self.repo.create(payload.dict())
    
    def get_user(self, user_id: str) -> Optional[UserOut]:
        doc = self.repo.get(user_id)
        return UserOut(**doc) if doc else None # ** の意味
    
    def update_user(self,user_id: str,patch: UserUpdate) -> bool:
        data = patch.dict(exclude_unset=True)
        if not data:
            return True
        return self.repo.update(user_id,data)
    
    def delete_user(self, user_id: str) -> bool:
        return self.repo.delete(user_id)
    
    def search_users(self, *, skill: Optional[str], location: Optional[str], limit: int = 50) -> List[Dict[str, Any]]:
        return self.repo.search(skill=skill,location=location,limit=limit)
    