from pydantic import BaseModel, EmailStr


class UserRegisterResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    mobile_number: str
    profile_image: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    userId: int
    fullName: str
