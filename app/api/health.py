from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/healthz")
def health_check():
    return {
        "status": "ok"
    }