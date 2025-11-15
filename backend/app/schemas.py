from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class AnimeCreate(BaseModel):
    title: str
    synopsis: Optional[str] = None
    image_url: Optional[str] = None
    year: Optional[int] = None
    jikan_id: Optional[int] = None
    score: Optional[float] = None

class AnimeOut(AnimeCreate):
    id: int
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    anime_id: int
    rating: int
    text: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    user_id: int
    anime_id: int
    rating: int
    text: Optional[str]
    class Config:
        from_attributes = True
