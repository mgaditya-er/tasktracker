from fastapi import FastAPI
from app.core.startup import validate_settings

from app.api.health import router as health_router
from app.api.ready import router as ready_router
from app.api.users import router as user_router
from app.api.tasks import router as task_router

validate_settings()

app = FastAPI(
    title="TaskTracker API"
)

app.include_router(health_router)
app.include_router(ready_router)
app.include_router(user_router)
app.include_router(task_router)