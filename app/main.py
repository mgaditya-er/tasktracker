from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.ready import router as ready_router

app = FastAPI(
    title="TaskTracker API"
)

app.include_router(health_router)
app.include_router(ready_router)