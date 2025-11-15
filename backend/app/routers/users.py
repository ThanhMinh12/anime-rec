from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(username: str, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
