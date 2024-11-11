from pydantic import BaseModel

# Modelos de solicitud
class VerifyTOTPRequest(BaseModel):
    session: str
    user_code: str

class AssociateTOTPRequest(BaseModel):
    session: str

class RespondToChallengeRequest(BaseModel):
    session: str
    user_code: str
    username: str

# Modelos de respuesta
class VerifyTOTPResponse(BaseModel):
    code: int
    message: str
    description: str

class VerifyTOTPResponseError(BaseModel):
    code: int
    message: str
    description: str

class AssociateTOTPResponse(BaseModel):
    code: int
    message: str
    description: str
    secret_code: str
    session: str

class AssociateTOTPResponseError(BaseModel):
    code: int
    message: str
    description: str

class RespondToChallengeResponse(BaseModel):
    code: int
    message: str
    description: str
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str

class RespondToChallengeResponseError(BaseModel):
    code: int
    message: str
    description: str
