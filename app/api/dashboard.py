from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(db: Session = Depends(get_db)):

    total_users = db.query(User).count()

    active_users = db.query(User).filter(
        User.is_active == True
    ).count()

    inactive_users = db.query(User).filter(
        User.is_active == False
    ).count()

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    recent_users = db.query(User).filter(
        User.created_at >= seven_days_ago
    ).count()

    return {
        "totalUsers": total_users,
        "activeUsers": active_users,
        "inactiveUsers": inactive_users,
        "recentUsers": recent_users
    }
