import logging

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    request: Request,
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        logger.warning(
            "user creation failed - email already exists",
            extra={
                "request_id": request.state.request_id
            }
        )

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

    logger.info(
        f"user created id={user.id}",
        extra={
            "request_id": request.state.request_id
        }
    )

    return user


@router.get("")
def get_users(
    request: Request,
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    logger.info(
        "users fetched",
        extra={
            "request_id": request.state.request_id
        }
    )

    return users


@router.get("/{user_id}")
def get_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        logger.warning(
            f"user not found id={user_id}",
            extra={
                "request_id": request.state.request_id
            }
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logger.info(
        f"user fetched id={user_id}",
        extra={
            "request_id": request.state.request_id
        }
    )

    return user