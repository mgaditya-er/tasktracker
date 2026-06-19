from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    user = User(
        name=payload.name,
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user