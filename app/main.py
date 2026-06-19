from fastapi import FastAPI
from app.core.startup import validate_settings
from app.core.logger import setup_logger

from app.api.health import router as health_router
from app.api.ready import router as ready_router
from app.api.users import router as user_router
from app.api.tasks import router as task_router

from app.middleware.request_id import RequestIDMiddleware
validate_settings()
logger = setup_logger()

app = FastAPI(
    title="TaskTracker API"
)
app.add_middleware(RequestIDMiddleware)

app.include_router(health_router)
app.include_router(ready_router)
app.include_router(user_router)
app.include_router(task_router)