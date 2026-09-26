from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    login: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str