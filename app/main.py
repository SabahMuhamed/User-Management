from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import Base, engine

import app.models.user
import app.models.audit_log

from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.dashboard import router as dashboard_router
from app.api.audit import router as audit_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    version="1.0"
)

# Serve uploaded profile images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "User Management API is running",
        "version": "1.0"
    }


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
