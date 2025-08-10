from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.infra.firestore_client import get_db

class UserRepository(ABC):
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> str: ...
    @abstractmethod
    def get(self, user_id: str) -> Optional[Dict[str, Any]]: ...
    @abstractmethod
    def update(self, user_id: str, patch: Dict[str, Any]) -> bool: ...
    @abstractmethod
    def delete(self, user_id: str) -> bool: ...
    @abstractmethod
    def search(self, *, skill: Optional[str], location: Optional[str], limit: int = 50) -> List[Dict[str, Any]]: ...

# 抽象メソッドの中身を定義する
class FirestoreUserRepository(UserRepository):
    # 
    def __init__(self) -> None:
        self.db = get_db()
        self.col = self.db.collection("users")

    def create(self, data: Dict[str, Any]) -> str:
        doc_ref = self.col.document()  # 自動ID
        doc_ref.set(data)
        return doc_ref.id

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        snap = self.col.document(user_id).get()
        if not snap.exists:
            return None
        doc = snap.to_dict()
        if doc is None:
            return None
        doc["id"] = snap.id
        return doc

    def update(self, user_id: str, patch: Dict[str, Any]) -> bool:
        doc_ref = self.col.document(user_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.update(patch)
        return True

    def delete(self, user_id: str) -> bool:
        doc_ref = self.col.document(user_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
    
    # スキル，場所によって50件絞ったものを返す
    def search(self, *, skill: Optional[str], location: Optional[str], limit: int = 50) -> List[Dict[str, Any]]:
        q = self.col
        if skill: # スキル指定の場合
            q = q.where("tech_experience", "array_contains", skill)
        if location: # 場所指定の場合
            docs = [d for d in q.stream()]
            result = []
            for snap in docs:
                data = snap.to_dict()
                locs = data.get("preferred_locations", [])
                if isinstance(locs, list) and location in locs: # 該当するものだけ格納
                    data["id"] = snap.id
                    result.append(data)
                    if len(result) >= limit:
                        break
            return result
        else: # 場所指定無しの場合
            result = []
            for snap in q.limit(limit).stream():
                data = snap.to_dict()
                data["id"] = snap.id
                result.append(data)
            return result
