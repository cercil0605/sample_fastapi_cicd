from unittest.mock import Mock
from app.usecase.user_usecase import UserUseCase
from app.domain.schema import UserCreate, UserUpdate, UserOut

def test_create_user_calls_repo_and_returns_id():
    repo = Mock()
    repo.create.return_value = "u1"
    uc = UserUseCase(repo)

    payload = UserCreate(
        name="A", age=20, gender="male", occupation="eng",
        tech_experience=["Py"]
    )
    got = uc.create_user(payload)

    repo.create.assert_called_once_with(payload.model_dump())
    assert got == "u1"

def test_get_user_converts_dict_to_userout_and_none_path():
    repo = Mock()
    uc = UserUseCase(repo)

    repo.get.return_value = {
        "id":"u1","name":"A","age":20,"gender":"male",
        "occupation":"eng","tech_experience":["Py"],
        "hobbies":None,"certifications":None,"desired_job_types":None,
        "preferred_locations":None,"portfolio_links":None,
        "availability":None,"additional_notes":None,
    }
    got = uc.get_user("u1")
    assert isinstance(got, UserOut)
    assert got.id == "u1"

    repo.get.return_value = None
    assert uc.get_user("missing") is None

def test_update_user_skips_when_empty_patch():
    repo = Mock()
    uc = UserUseCase(repo)

    ok = uc.update_user("u1", UserUpdate())
    assert ok is True
    repo.update.assert_not_called()

def test_update_user_calls_repo_with_partial_fields():
    repo = Mock()
    repo.update.return_value = True
    uc = UserUseCase(repo)

    patch = UserUpdate(name="B", preferred_locations=["Remote"])
    ok = uc.update_user("u1", patch)

    repo.update.assert_called_once_with("u1", {"name":"B","preferred_locations":["Remote"]})
    assert ok is True

def test_delete_user_calls_repo():
    repo = Mock()
    repo.delete.return_value = True
    uc = UserUseCase(repo)

    assert uc.delete_user("u1") is True
    repo.delete.assert_called_once_with("u1")

def test_search_users_forwards_params():
    repo = Mock()
    uc = UserUseCase(repo)

    uc.search_users(skill="Python", location="Tokyo", limit=10)
    repo.search.assert_called_once_with(skill="Python", location="Tokyo", limit=10)
