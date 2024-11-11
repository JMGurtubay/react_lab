from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

# Modelos de solicitud
class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ConfirmEmail(BaseModel):
    username: str
    confirmation_code: str

class LogoutRequest(BaseModel):
    access_token: str

class RevokeTokenRequest(BaseModel):
    token: str
    client_id: str

# Modelos de respuesta
class RegisterResponse(BaseModel):
    code: int
    message: str
    description: str

class RegisterResponseError(BaseModel):
    code: int
    message: str
    description: str

class LoginResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Dict]

class LoginResponseError(BaseModel):
    code: int
    message: str
    description: str

class ConfirmEmailResponse(BaseModel):
    code: int
    message: str
    description: str

class ConfirmEmailResponseError(BaseModel):
    code: int
    message: str
    description: str

class LogoutResponse(BaseModel):
    code: int
    message: str
    description: str

class LogoutResponseError(BaseModel):
    code: int
    message: str
    description: str
