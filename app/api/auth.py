import os
import uuid
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from jose import JWTError
from app.models.user import User
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.token import (
    create_access_token,
    create_refresh_token,
    decode_access_token
)
from app.schemas.refresh_token import RefreshTokenRequest
from datetime import datetime
from app.models.audit_log import AuditLog


security = HTTPBearer()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

UPLOAD_DIR = "uploads/users"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB


def save_profile_image(file: UploadFile) -> str:
    filename = file.filename.lower()
    ext = os.path.splitext(filename)[1]

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Profile image must be jpg, jpeg, or png"
        )

    content = file.file.read()

    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Maximum image size is 2 MB"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path.replace("\\", "/")


@router.post("/register")
async def register(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password minimum 8 characters"
        )

    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email must be unique")

    existing_mobile = db.query(User).filter(
        User.mobile_number == mobile_number).first()
    if existing_mobile:
        raise HTTPException(
            status_code=400, detail="Mobile number must be unique")

    image_path = save_profile_image(profile_image)

    new_user = User(
        full_name=full_name,
        email=email,
        mobile_number=mobile_number,
        password=hash_password(password),
        profile_image=image_path,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    audit = AuditLog(
        user_id=new_user.id,
        action="USER_CREATED"
    )
    db.add(audit)
    db.commit()
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "fullName": new_user.full_name,
            "email": new_user.email,
            "mobileNumber": new_user.mobile_number,
            "profileImage": new_user.profile_image
        }
    }


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid Email"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Wrong Password"
        )

    user.last_login = datetime.utcnow()
    db.commit()

    access_token = create_access_token(
        {
            "user_id": user.id
        }
    )
    refresh_token = create_refresh_token(
        {
            "user_id": user.id
        }
    )
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "last_login": user.last_login
        }
    }


@router.get("/profile")
def profile(

    credentials: HTTPAuthorizationCredentials = Depends(security),

    db: Session = Depends(get_db)

):

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user = db.query(User).filter(
        User.id == payload["user_id"]
    ).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return {

        "id": user.id,

        "full_name": user.full_name,

        "email": user.email,

        "mobile": user.mobile_number,

        "profile_image": user.profile_image,

        "is_active": user.is_active
    }


@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):

    try:
        payload = decode_access_token(data.refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid Refresh Token"
            )

        user_id = payload.get("user_id")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh Token"
        )

    access_token = create_access_token(
        {
            "user_id": user_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
