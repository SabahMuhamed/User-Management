from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/api/audit",
    tags=["Audit Logs"]
)


@router.get("")
def get_logs(
    db: Session = Depends(get_db)
):

    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return logs
