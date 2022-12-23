from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.crud import CRUD
from db.models.user import UserRead, UserCreate, User, UserUpdate
from dependencies import get_session

router = APIRouter(prefix="/users",
                   tags=["user"])


@router.get("/", response_model=list[UserRead])
def read_users(session: Session = Depends(get_session)):
    return CRUD.get_all(User, session)


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return CRUD.create(User, session, user)


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    return CRUD.get_id(User, session, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    return CRUD.patch(User, session, user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return CRUD.delete(User, session, user_id)

