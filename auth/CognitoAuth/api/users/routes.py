from fastapi import APIRouter, HTTPException, Request
from .models import (
    User, LoginRequest, ConfirmEmail, LogoutRequest,
    RegisterResponse, RegisterResponseError,
    LoginResponse, LoginResponseError,
    ConfirmEmailResponse, ConfirmEmailResponseError,
    LogoutResponse, LogoutResponseError
)
from shared.config import USER_POOL_ID, CLIENT_ID, client


router = APIRouter()

from fastapi import APIRouter, Response

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, responses={400: {"model": RegisterResponseError}})
async def register_user(user: User):
    '''
    Descripción:
        API para registrar un nuevo usuario en el sistema mediante AWS Cognito. Al registrarse, el usuario recibe un correo de verificación.

    Request:
        - username (str): Nombre de usuario único.
        - email (EmailStr): Dirección de correo electrónico.
        - password (str): Contraseña segura.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Registro exitoso".
        - description (str): Descripción del estado del registro.
    '''
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=user.username,
            Password=user.password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': user.email
                }
            ]
        )
        return RegisterResponse(
            code=200,
            message="Registro exitoso",
            description="Usuario registrado. Se ha enviado un correo de verificación al email proporcionado."
        )
    except client.exceptions.UsernameExistsException:
        raise HTTPException(
            status_code=400,
            detail=RegisterResponseError(
                code=400,
                message="Nombre de usuario ya existente",
                description="El nombre de usuario ya existe."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=RegisterResponseError(
                code=400,
                message="Error de cliente",
                description=str(e)
            ).dict()
        )

@router.post("/login", response_model=LoginResponse, responses={401: {"model": LoginResponseError}, 400: {"model": LoginResponseError}})
async def login(user: LoginRequest):
    '''
    Descripción:
        API para autenticar a un usuario. Esta API inicia el flujo de autenticación en AWS Cognito y puede requerir MFA (autenticación multifactor).

    Request:
        - username (str): Nombre de usuario.
        - password (str): Contraseña del usuario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Inicio de sesión exitoso" o mensajes relacionados con la configuración de MFA.
        - description (str): Descripción del estado de autenticación.
        - data (dict): Información adicional, incluyendo un token de acceso o la sesión MFA requerida.
    '''
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': user.username,
                'PASSWORD': user.password
            }
        )
        if 'ChallengeName' in response and response['ChallengeName'] == 'MFA_SETUP':
            return LoginResponse(
                code=200,
                message="Configuración de MFA requerida",
                description="El usuario necesita configurar MFA.",
                data={"session": response['Session']}
            )

        if 'ChallengeName' in response and response['ChallengeName'] == 'SOFTWARE_TOKEN_MFA':
            return LoginResponse(
                code=200,
                message="Se requiere TOTP",
                description="Se requiere un código TOTP para completar el inicio de sesión.",
                data={"session": response['Session']}
            )

        return LoginResponse(
            code=200,
            message="Inicio de sesión exitoso",
            description="El usuario ha iniciado sesión correctamente.",
            data=response.get('AuthenticationResult', {})
        )

    except client.exceptions.NotAuthorizedException:
        raise HTTPException(
            status_code=401,
            detail=LoginResponseError(
                code=401,
                message="Credenciales incorrectas",
                description="El nombre de usuario o la contraseña son incorrectos."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=LoginResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )

@router.post("/confirm-email", response_model=ConfirmEmailResponse, responses={400: {"model": ConfirmEmailResponseError}})
async def confirm_email(data: ConfirmEmail):
    '''
    Descripción:
        API para confirmar el correo electrónico de un usuario mediante un código de verificación enviado por correo electrónico.

    Request:
        - username (str): Nombre de usuario del destinatario.
        - confirmation_code (str): Código de verificación recibido en el correo electrónico.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Email confirmado".
        - description (str): Descripción del estado de la confirmación.
    '''
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=data.username,
            ConfirmationCode=data.confirmation_code
        )
        return ConfirmEmailResponse(
            code=200,
            message="Email confirmado",
            description="Email confirmado exitosamente. La cuenta está ahora activa."
        )
    except client.exceptions.CodeMismatchException:
        raise HTTPException(
            status_code=400,
            detail=ConfirmEmailResponseError(
                code=400,
                message="Código incorrecto",
                description="El código de verificación es incorrecto."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=ConfirmEmailResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )

@router.post("/logout", response_model=LogoutResponse, responses={401: {"model": LogoutResponseError}, 400: {"model": LogoutResponseError}})
async def logout(request: Request):
    '''
    Descripción:
        API para cerrar la sesión del usuario. Invalida el token de acceso del usuario en AWS Cognito.

    Request:
        - Authorization (str): Token de acceso del usuario en el encabezado de la solicitud, en formato "Bearer {access_token}".

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Sesión cerrada".
        - description (str): Descripción del estado del cierre de sesión.
    '''
    access_token = request.headers.get("Authorization")
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail=LogoutResponseError(
                code=401,
                message="Token no proporcionado",
                description="El token de acceso no fue proporcionado o es inválido."
            ).dict()
        )

    access_token = access_token.split(" ")[1]

    try:
        client.global_sign_out(AccessToken=access_token)
        return LogoutResponse(
            code=200,
            message="Sesión cerrada",
            description="Sesión cerrada con éxito."
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=LogoutResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )
