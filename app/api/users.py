import logging

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    request: Request,
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        logger.warning(
            "user creation failed - email already exists",
            extra={"request_id": request_id}
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
        extra={"request_id": request_id}
    )

    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def get_users(
    request: Request,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    users = db.query(User).all()

    logger.info(
        "users fetched",
        extra={"request_id": request_id}
    )

    return users 


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:

        logger.warning(
            f"user not found id={user_id}",
            extra={"request_id": request_id}
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logger.info(
        f"user fetched id={user_id}",
        extra={"request_id": request_id}
    )

    return UserResponse.model_validate(user)