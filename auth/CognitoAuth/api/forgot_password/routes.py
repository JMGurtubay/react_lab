from fastapi import APIRouter, HTTPException
from .models import (
    ForgotPasswordRequest, ConfirmForgotPasswordRequest,
    ForgotPasswordResponse, ForgotPasswordResponseError,
    ConfirmForgotPasswordResponse, ConfirmForgotPasswordResponseError
)
from shared.config import USER_POOL_ID, CLIENT_ID, client


router = APIRouter()

@router.post("/forgot-password", response_model=ForgotPasswordResponse, responses={404: {"model": ForgotPasswordResponseError}, 400: {"model": ForgotPasswordResponseError}})
async def forgot_password(request: ForgotPasswordRequest):
    '''
    Descripción:
        API para iniciar el proceso de recuperación de contraseña. Envía un código de verificación al correo electrónico o número de teléfono asociado al usuario.

    Request:
        - username (str): Nombre de usuario registrado en el sistema.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Código de verificación enviado".
        - description (str): Explicación de que el código de verificación fue enviado.
    '''
    try:
        response = client.forgot_password(
            ClientId=CLIENT_ID,
            Username=request.username
        )
        return ForgotPasswordResponse(
            code=200,
            message="Código de verificación enviado",
            description="Código de verificación enviado al correo o número de teléfono asociado."
        )
    except client.exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=404,
            detail=ForgotPasswordResponseError(
                code=404,
                message="Usuario no encontrado",
                description="No se encontró un usuario con el nombre de usuario proporcionado."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=ForgotPasswordResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )

@router.post("/confirm-forgot-password", response_model=ConfirmForgotPasswordResponse, responses={400: {"model": ConfirmForgotPasswordResponseError}})
async def confirm_forgot_password(request: ConfirmForgotPasswordRequest):
    '''
    Descripción:
        API para confirmar y completar el proceso de recuperación de contraseña. Verifica el código de recuperación y permite establecer una nueva contraseña.

    Request:
        - username (str): Nombre de usuario registrado.
        - confirmation_code (str): Código de verificación recibido por el usuario.
        - new_password (str): Nueva contraseña que el usuario desea establecer.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Contraseña restablecida".
        - description (str): Indicación de que la contraseña fue restablecida con éxito.
    '''
    try:
        response = client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=request.username,
            ConfirmationCode=request.confirmation_code,
            Password=request.new_password
        )
        return ConfirmForgotPasswordResponse(
            code=200,
            message="Contraseña restablecida",
            description="Contraseña restablecida con éxito."
        )
    except client.exceptions.CodeMismatchException:
        raise HTTPException(
            status_code=400,
            detail=ConfirmForgotPasswordResponseError(
                code=400,
                message="Código incorrecto",
                description="El código de verificación es incorrecto."
            ).dict()
        )
    except client.exceptions.ExpiredCodeException:
        raise HTTPException(
            status_code=400,
            detail=ConfirmForgotPasswordResponseError(
                code=400,
                message="Código expirado",
                description="El código de verificación ha expirado."
            ).dict()
        )
    except client.exceptions.InvalidPasswordException:
        raise HTTPException(
            status_code=400,
            detail=ConfirmForgotPasswordResponseError(
                code=400,
                message="Contraseña no válida",
                description="La nueva contraseña no cumple con los requisitos de seguridad."
            ).dict()
        )
    except client.exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=404,
            detail=ConfirmForgotPasswordResponseError(
                code=404,
                message="Usuario no encontrado",
                description="No se encontró un usuario con el nombre de usuario proporcionado."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=ConfirmForgotPasswordResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )
