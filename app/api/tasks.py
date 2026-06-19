from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

VALID_STATUS = [
    "pending",
    "in_progress",
    "completed"
]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db)
):

    owner = db.query(User).filter(
        User.id == payload.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    task = Task(
        title=payload.title,
        description=payload.description,
        owner_id=payload.owner_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("")
def get_tasks(
    status: str | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if owner_id:
        query = query.filter(Task.owner_id == owner_id)

    return query.all()


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if payload.status and payload.status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Invalid task status"
        )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()