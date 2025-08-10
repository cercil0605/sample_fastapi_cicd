from typing import List, Optional
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    # 必須
    name: str
    age: int
    gender: str
    occupation: str
    tech_experience: List[str] = Field(default_factory=list)
    # 任意 初期値を設定
    hobbies: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    desired_job_types: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    portfolio_links: Optional[list[dict]] = None
    availability: Optional[str] = None
    additional_notes: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    tech_experience: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    desired_job_types: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    portfolio_links: Optional[list[dict]] = None
    availability: Optional[str] = None
    additional_notes: Optional[str] = None

class UserOut(UserCreate):
    id: str
