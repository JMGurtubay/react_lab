from fastapi import APIRouter, HTTPException
from .models import (
    VerifyTOTPRequest, AssociateTOTPRequest, RespondToChallengeRequest,
    VerifyTOTPResponse, VerifyTOTPResponseError,
    AssociateTOTPResponse, AssociateTOTPResponseError,
    RespondToChallengeResponse, RespondToChallengeResponseError
)
from shared.config import USER_POOL_ID, CLIENT_ID, client


router = APIRouter()

@router.post("/verify-totp", response_model=VerifyTOTPResponse, responses={400: {"model": VerifyTOTPResponseError}})
async def verify_totp(request: VerifyTOTPRequest):
    '''
    Descripción:
        API para verificar el código TOTP proporcionado por el usuario. Esta API completa la configuración de TOTP (autenticación multifactor) para el usuario.

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.
        - user_code (str): Código TOTP proporcionado por el usuario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "TOTP configurado".
        - description (str): Descripción del estado de la configuración de TOTP.
    '''
    try:
        response = client.verify_software_token(
            Session=request.session,
            UserCode=request.user_code
        )
        if response['Status'] == 'SUCCESS':
            return VerifyTOTPResponse(
                code=200,
                message="TOTP configurado",
                description="TOTP configurado correctamente."
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=VerifyTOTPResponseError(
                    code=400,
                    message="Verificación fallida",
                    description="Verificación de TOTP fallida."
                ).dict()
            )
    except client.exceptions.InvalidParameterException:
        raise HTTPException(
            status_code=400,
            detail=VerifyTOTPResponseError(
                code=400,
                message="Parámetros inválidos",
                description="Código TOTP o sesión inválidos."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=VerifyTOTPResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )

@router.post("/associate-totp", response_model=AssociateTOTPResponse, responses={400: {"model": AssociateTOTPResponseError}})
async def associate_totp(request: AssociateTOTPRequest):
    '''
    Descripción:
        API para asociar TOTP al usuario. Genera un código secreto que el usuario puede escanear o introducir en una aplicación de autenticación (como Google Authenticator) para configurar TOTP.

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Asociación de TOTP exitosa".
        - description (str): Descripción del estado de la asociación de TOTP.
        - secret_code (str): Código secreto para configurar TOTP en una aplicación de autenticación.
        - session (str): Nueva sesión que puede ser utilizada en el flujo de autenticación.
    '''
    try:
        response = client.associate_software_token(
            Session=request.session
        )
        return AssociateTOTPResponse(
            code=200,
            message="Asociación de TOTP exitosa",
            description="Se ha generado un código secreto para configurar TOTP.",
            secret_code=response['SecretCode'],
            session=response['Session']
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=AssociateTOTPResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )

@router.post("/respond-to-auth-challenge", response_model=RespondToChallengeResponse, responses={400: {"model": RespondToChallengeResponseError}})
async def respond_to_auth_challenge(request: RespondToChallengeRequest):
    '''
    Descripción:
        API para responder al desafío de autenticación de TOTP. Esta API completa el flujo de autenticación cuando se requiere autenticación multifactor (MFA).

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.
        - user_code (str): Código TOTP proporcionado por el usuario.
        - username (str): Nombre de usuario del destinatario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Desafío completado con éxito".
        - description (str): Descripción del estado de la autenticación.
        - access_token (str): Token de acceso generado tras la autenticación.
        - id_token (str): ID Token de usuario.
        - refresh_token (str): Token de actualización.
        - token_type (str): Tipo de token (por ejemplo, "Bearer").
    '''
    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName='SOFTWARE_TOKEN_MFA',
            Session=request.session,
            ChallengeResponses={
                'USERNAME': request.username,
                'SOFTWARE_TOKEN_MFA_CODE': request.user_code
            }
        )
        if 'AuthenticationResult' in response:
            access_token = response['AuthenticationResult']['AccessToken']
            
            # Configura la cookie segura con el token de acceso
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Strict"
            )

            return RespondToChallengeResponse(
                code=200,
                message="Desafío completado con éxito",
                description="El usuario ha completado el desafío TOTP correctamente.",
                access_token=access_token,
                id_token=response['AuthenticationResult']['IdToken'],
                refresh_token=response['AuthenticationResult']['RefreshToken'],
                token_type=response['AuthenticationResult']['TokenType']
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=RespondToChallengeResponseError(
                    code=400,
                    message="Desafío no completado",
                    description="El desafío no fue completado correctamente."
                ).dict()
            )
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(
            status_code=401,
            detail=RespondToChallengeResponseError(
                code=401,
                message="Código TOTP incorrecto",
                description="El código TOTP proporcionado es incorrecto."
            ).dict()
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=RespondToChallengeResponseError(
                code=400,
                message="Error de Cognito",
                description=e.response['Error']['Message']
            ).dict()
        )
