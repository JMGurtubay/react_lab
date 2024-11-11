from pydantic import BaseModel

# Modelos de solicitud
class ForgotPasswordRequest(BaseModel):
    username: str

class ConfirmForgotPasswordRequest(BaseModel):
    username: str
    confirmation_code: str
    new_password: str

# Modelos de respuesta
class ForgotPasswordResponse(BaseModel):
    code: int
    message: str
    description: str

class ForgotPasswordResponseError(BaseModel):
    code: int
    message: str
    description: str

class ConfirmForgotPasswordResponse(BaseModel):
    code: int
    message: str
    description: str

class ConfirmForgotPasswordResponseError(BaseModel):
    code: int
    message: str
    description: str
