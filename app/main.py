from fastapi import FastAPI
from app.database.database import Base, engine
import app.models.user
from app.api.auth import router as auth_router
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.users import router as user_router
from app.api.dashboard import router as dashboard_router
import app.models.audit_log
from app.api.audit import router as audit_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "API Running"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
