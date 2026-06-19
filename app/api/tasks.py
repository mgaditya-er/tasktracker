import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    status
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

VALID_STATUS = ["pending", "in_progress", "completed"]


# ---------------- CREATE TASK ----------------
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(
    request: Request,
    payload: TaskCreate,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    owner = db.query(User).filter(User.id == payload.owner_id).first()

    if not owner:
        logger.warning(
            "task creation failed - owner not found",
            extra={"request_id": request_id}
        )
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

    logger.info(
        f"task created id={task.id}",
        extra={"request_id": request_id}
    )

    return task


# ---------------- GET TASKS ----------------
@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    request: Request,
    status: str | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if owner_id:
        query = query.filter(Task.owner_id == owner_id)

    tasks = query.all()

    logger.info(
        "tasks fetched",
        extra={"request_id": request_id}
    )

    return tasks


# ---------------- GET TASK BY ID ----------------
@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logger.warning(
            f"task not found id={task_id}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    logger.info(
        f"task fetched id={task_id}",
        extra={"request_id": request_id}
    )

    return task


# ---------------- UPDATE TASK ----------------
@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    request: Request,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logger.warning(
            f"task update failed id={task_id}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if payload.status and payload.status not in VALID_STATUS:
        logger.warning(
            f"invalid task status={payload.status}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=400,
            detail="Invalid task status"
        )

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    logger.info(
        f"task updated id={task_id}",
        extra={"request_id": request_id}
    )

    return task


# ---------------- DELETE TASK ----------------
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    request_id = getattr(request.state, "request_id", "N/A")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logger.warning(
            f"task delete failed id={task_id}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    logger.info(
        f"task deleted id={task_id}",
        extra={"request_id": request_id}
    )

    return None