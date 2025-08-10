from typing import Optional, List, Dict, Any
from fastapi.testclient import TestClient

from app.main import app
from app.api.routers.users import get_service, UserUseCase
from app.api.routers.users import UserRepository

# set mock repository
class FakeRepo(UserRepository):
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}
        self._seq = 0

    def create(self, data: Dict[str, Any]) -> str:
        self._seq += 1
        uid = str(self._seq)
        self.store[uid] = {**data, "id": uid}
        return uid

    def get(self, uid: str) -> Optional[Dict[str, Any]]:
        return self.store.get(uid)

    def update(self, uid: str, patch: Dict[str, Any]) -> bool:
        if uid not in self.store:
            return False
        self.store[uid] = {**self.store[uid], **patch}
        return True

    def delete(self, uid: str) -> bool:
        return self.store.pop(uid, None) is not None

    def search(self, *, skill: Optional[str], location: Optional[str], limit: int = 50) -> List[Dict[str, Any]]:
        items = list(self.store.values())
        if skill:
            items = [x for x in items if skill in (x.get("tech_experience") or [])]
        if location:
            items = [x for x in items if location in (x.get("preferred_locations") or [])]
        return items[:limit]


shared_repo = FakeRepo()

def override_get_service() -> UserUseCase:
    return UserUseCase(shared_repo)

# テスト前実行
def setup_function():
    app.dependency_overrides[get_service] = override_get_service
# テスト後実行
def teardown_function():
    app.dependency_overrides.clear()

# テスト

def test_users_crud_flow():
    client = TestClient(app)

    # Create
    payload = {
        "name":"John","age":25,"gender":"male","occupation":"BE","tech_experience":["Python"],
        "preferred_locations":["Tokyo","Remote"]
    }
    r = client.post("/users", json=payload)
    assert r.status_code in (200, 201)
    user_id = r.json()["id"]

    # Get
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    assert r.json()["id"] == user_id

    # Search (skill, location)
    r = client.get("/users", params={"skill":"Python", "location":"Tokyo", "limit":50})
    assert r.status_code == 200
    assert any(u["id"] == user_id for u in r.json())

    # Update
    r = client.patch(f"/users/{user_id}", json={"name":"John U", "preferred_locations":["Remote"]})
    assert r.status_code == 200
    assert r.json() == {"updated": True}

    # Get after update
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "John U"
    assert data["preferred_locations"] == ["Remote"]

    # Delete
    r = client.delete(f"/users/{user_id}")
    assert r.status_code == 200
    assert r.json() == {"deleted": True}

    # Ensure 404
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 404

def test_404_paths():
    client = TestClient(app)
    # get
    assert client.get("/users/999").status_code == 404
    # update
    assert client.patch("/users/999", json={"name":"X"}).status_code == 404
    # delete
    assert client.delete("/users/999").status_code == 404
