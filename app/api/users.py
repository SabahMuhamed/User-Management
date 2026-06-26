from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.schemas.update_user import UpdateUser
from app.models.audit_log import AuditLog


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("")
def get_users(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1),
    search: str = "",
    db: Session = Depends(get_db)
):

    query = db.query(User)

    if search:
        query = query.filter(
            (User.full_name.contains(search)) |
            (User.email.contains(search))
        )

    total = query.count()

    users = (
        query
        .offset((page - 1) * pageSize)
        .limit(pageSize)
        .all()
    )

    return {
        "page": page,
        "pageSize": pageSize,
        "total": total,
        "data": users
    }


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UpdateUser,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Update user
    user.full_name = data.full_name
    user.mobile_number = data.mobile_number
    user.is_active = data.is_active

    # Create audit log
    audit = AuditLog(
        user_id=user.id,
        action="USER_UPDATED"
    )

    db.add(audit)

    # Save both the user update and audit log together
    db.commit()

    db.refresh(user)

    return {
        "message": "User updated successfully"
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="User is already deleted"
        )

    # Soft Delete
    user.is_active = False

    # Audit Log
    audit = AuditLog(
        user_id=user.id,
        action="USER_DELETED"
    )

    db.add(audit)

    # Save both changes together
    db.commit()

    db.refresh(user)

    return {
        "message": "User deleted successfully"
    }
