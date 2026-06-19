from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["Readiness"])


@router.get("/readyz")
def readiness_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database not ready"
        )