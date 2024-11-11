from fastapi import FastAPI
import boto3
from io import BytesIO 
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from api.users.routes import router as users_router
from api.mfa.routes import router as mfa_router
from api.forgot_password.routes import router as forgot_password_router

app = FastAPI()

"""
Descripción del proyecto:
    Este proyecto es una API de autenticación segura construida con FastAPI, diseñada para manejar el registro, autenticación multifactor (MFA) y recuperación de contraseñas de los usuarios. Utiliza AWS Cognito como sistema de identidad y autenticación, ofreciendo una infraestructura confiable y escalable para gestionar usuarios, sesiones y políticas de seguridad.

    La integración con AWS Cognito permite implementar mecanismos avanzados de autenticación, incluyendo autenticación multifactor (MFA) basada en TOTP (Time-Based One-Time Password) y un sistema robusto de administración de sesiones y recuperación de cuentas.

Dependencias clave:
    - **FastAPI**: Framework de Python que facilita la creación de APIs rápidas y de alto rendimiento. Ideal para aplicaciones que requieren escalabilidad y rendimiento.
    - **AWS Cognito**: Servicio de AWS para gestionar autenticación, autorización y usuarios. Cognito permite implementar MFA, administración de sesiones y recuperación de cuentas de manera segura.
    - **Boto3**: SDK de AWS para Python que permite la comunicación entre FastAPI y AWS Cognito para realizar operaciones como registro, autenticación y manejo de sesiones.
    - **Pydantic**: Biblioteca utilizada para la validación y gestión de datos en FastAPI, asegurando que las solicitudes y respuestas sean seguras y bien definidas.
    - **Uvicorn**: Servidor ASGI que permite ejecutar FastAPI con soporte para asincronía, facilitando el manejo de múltiples solicitudes de manera eficiente.

Beneficios del uso de AWS Cognito:
    - **Seguridad mejorada**: AWS Cognito ofrece funciones avanzadas de autenticación, como la autenticación multifactor (MFA) con códigos TOTP, y permite aplicar políticas de contraseñas fuertes, aumentando la seguridad del sistema.
    - **Gestión de sesiones**: Con Cognito, el sistema puede manejar sesiones de usuario con tokens de acceso (JWT) seguros, con soporte para expiración y renovación automática.
    - **Recuperación de contraseñas**: AWS Cognito proporciona un flujo seguro para la recuperación de cuentas, incluyendo el envío de códigos de verificación para restablecer contraseñas.
    - **Escalabilidad**: AWS Cognito es un servicio administrado y escalable, adecuado para manejar grandes volúmenes de usuarios sin necesidad de preocuparse por la infraestructura subyacente.

Flujos de API:
    La API incluye dos flujos principales:
    1. **Autenticación y MFA**:
        - Registro de usuarios, confirmación de correo electrónico, inicio de sesión, configuración y verificación de TOTP (MFA) y cierre de sesión.
    2. **Recuperación de Contraseña**:
        - Solicitud de recuperación de contraseña y confirmación de restablecimiento de contraseña con verificación.

    Este sistema proporciona un conjunto completo de funcionalidades de autenticación para asegurar que solo los usuarios autenticados y autorizados tengan acceso, con opciones adicionales de recuperación en caso de pérdida de acceso a la cuenta.

Flujo principal de autenticación:
1. **Registro de usuario** (`/register`):
    - Descripción: Registra un nuevo usuario en el sistema. Tras el registro, se envía un correo de verificación al usuario.
    - Request:
        - username: Nombre de usuario.
        - email: Correo electrónico.
        - password: Contraseña.
    - Response: Indica que el registro fue exitoso y que se envió un correo de verificación.

2. **Confirmación de email** (`/confirm-email`):
    - Descripción: Confirma el correo electrónico del usuario mediante el código de verificación enviado.
    - Request:
        - username: Nombre de usuario.
        - confirmation_code: Código de verificación recibido en el correo.
    - Response: Indica que el email fue confirmado exitosamente.

3. **Inicio de sesión inicial** (`/login`):
    - Descripción: Inicia sesión del usuario. Si es la primera vez o no tiene TOTP configurado, se requiere configuración de MFA.
    - Request:
        - username: Nombre de usuario.
        - password: Contraseña.
    - Response: Indica si se requiere configuración de MFA o un código TOTP para completar el inicio de sesión.

4. **Asociación de TOTP (autenticación multifactor)** (`/associate-totp`):
    - Descripción: Genera un código secreto para configurar TOTP en una aplicación de autenticación.
    - Request:
        - session: Sesión activa del usuario.
    - Response: Proporciona un código secreto que puede ser escaneado en una app de autenticación.

5. **Verificación de TOTP** (`/verify-totp`):
    - Descripción: Verifica el código TOTP proporcionado por el usuario, completando la configuración de autenticación multifactor.
    - Request:
        - session: Sesión activa del usuario.
        - user_code: Código TOTP de seis dígitos generado por la aplicación de autenticación.
    - Response: Indica que el TOTP fue configurado exitosamente.

6. **Inicio de sesión posterior** (`/login`):
    - Descripción: Una vez que TOTP ha sido configurado, el usuario puede iniciar sesión normalmente. Este paso puede requerir un código TOTP para completar la autenticación.
    - Request:
        - username: Nombre de usuario.
        - password: Contraseña.
    - Response: Devuelve la sesión o el estado de requerir un código TOTP.

7. **Respuesta al desafío TOTP** (`/respond-to-auth-challenge`):
    - Descripción: Completa el inicio de sesión al responder al desafío de TOTP, entregando tokens de autenticación (access_token, id_token, refresh_token).
    - Request:
        - session: Sesión activa del usuario.
        - username: Nombre de usuario.
        - user_code: Código TOTP generado en la aplicación de autenticación.
    - Response: Tokens de autenticación del usuario (access_token, id_token, refresh_token).

8. **Cierre de sesión** (`/logout`):
    - Descripción: Invalida el token de acceso del usuario, cerrando la sesión en AWS Cognito.
    - Request:
        - Authorization: Token de acceso en el encabezado de autorización.
    - Response: Indica que la sesión fue cerrada exitosamente.


Flujo de recuperación de contraseña:
1. **Solicitud de recuperación de contraseña** (`/forgot-password`):
    - Descripción: Inicia el proceso de recuperación de contraseña enviando un código de verificación al correo o número de teléfono asociado.
    - Request:
        - username: Nombre de usuario.
    - Response: Indica que el código de verificación fue enviado.

2. **Confirmación de recuperación de contraseña** (`/confirm-forgot-password`):
    - Descripción: Verifica el código de recuperación y permite establecer una nueva contraseña para el usuario.
    - Request:
        - username: Nombre de usuario.
        - confirmation_code: Código de verificación recibido.
        - new_password: Nueva contraseña que el usuario desea establecer.
    - Response: Indica que la contraseña fue restablecida exitosamente.

Este flujo asegura una autenticación robusta con verificación multifactor (MFA) opcional y un proceso seguro de recuperación de contraseña.
"""

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5174"],  # Puedes agregar más orígenes o usar ["*"] para permitir todos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Registro de rutas
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(mfa_router, prefix="/mfa", tags=["MFA"])
app.include_router(forgot_password_router, prefix="/forgot-password", tags=["Forgot Password"])

# Configuraciones de seguridad adicionales pueden ir aquí (por ejemplo, manejo de cookies HTTPOnly, uso de HTTPS, etc.)

# Endpoint raíz para verificar que la API esté corriendo
@app.get("/")
async def root():
    return {"message": "API de autenticación con FastAPI y AWS Cognito en funcionamiento"}


# USER_POOL_ID = 'us-east-1_sO3N5A2WH'
# CLIENT_ID = '3brp960d8igu313rn94pcu5sso'
# client = boto3.client('cognito-idp', region_name='us-east-1')


# class User(BaseModel):
#     username: str
#     email:EmailStr
#     password: str

# # Modelo de datos para la confirmación de email
# class ConfirmEmail(BaseModel):
#     username: str
#     confirmation_code: str

# class LoginRequest(BaseModel):
#     username: str
#     password: str

# class VerifyTOTPRequest(BaseModel):
#     session: str
#     user_code: str

# class RespondToChallengeRequest(BaseModel):
#     session: str
#     user_code: str
#     username: str  # Es importante incluir el nombre de usuario para responder al desafío

# class ForgotPasswordRequest(BaseModel):
#     username: str

# class ConfirmForgotPasswordRequest(BaseModel):
#     username: str
#     confirmation_code: str
#     new_password: str

# class RevokeTokenRequest(BaseModel):
#     token: str
#     client_id: str = CLIENT_ID

# class LogoutRequest(BaseModel):
#     access_token: str

# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# class AssociateTOTPRequest(BaseModel):
#     session:str

# # Configuración de CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://localhost:5174"],  # Puedes agregar más orígenes o usar ["*"] para permitir todos
#     allow_credentials=True,
#     allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
#     allow_headers=["*"],  # Permitir todos los encabezados
# )
# @app.post("/login")
# async def login(user: LoginRequest):
#     try:
#         # Paso 1: Inicia la autenticación
#         response = client.initiate_auth(
#             ClientId=CLIENT_ID,
#             AuthFlow='USER_PASSWORD_AUTH',
#             AuthParameters={
#                 'USERNAME': user.username,
#                 'PASSWORD': user.password
#             }
#         )

#         # Caso 1: El usuario necesita configurar el TOTP (MFA_SETUP)
#         if 'ChallengeName' in response and response['ChallengeName'] == 'MFA_SETUP':
#             session = response['Session']
#             return {
#                 "code": 200,
#                 "successCode": "MFA_SETUP_REQUIRED",
#                 "message": "Configuración de MFA requerida",
#                 "description": "El usuario necesita configurar MFA.",
#                 "session": session  # Devuelve la sesión para usar en la API de asociación
#             }

#         # Caso 2: El usuario ya tiene configurado el TOTP (SOFTWARE_TOKEN_MFA)
#         if 'ChallengeName' in response and response['ChallengeName'] == 'SOFTWARE_TOKEN_MFA':
#             return {
#                 "code": 200,
#                 "successCode": "TOTP_CHALLENGE",
#                 "message": "Se requiere TOTP",
#                 "description": "Se requiere un código TOTP para completar el inicio de sesión.",
#                 "session": response['Session']  # Devuelve la sesión para responder al desafío
#             }

#         # Caso de éxito no definido en el ejemplo original
#         return {
#             "code": 200,
#             "message": "Inicio de sesión exitoso",
#             "description": "El usuario ha iniciado sesión correctamente.",
#             "data": response.get('AuthenticationResult', {})
#         }

#     except client.exceptions.NotAuthorizedException:
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "code": 401,
#                 "message": "Credenciales incorrectas",
#                 "description": "El nombre de usuario o la contraseña son incorrectos."
#             }
#         )
#     except client.exceptions.UserNotFoundException:
#         raise HTTPException(
#             status_code=404,
#             detail={
#                 "code": 404,
#                 "message": "Usuario no encontrado",
#                 "description": "No se encontró un usuario con las credenciales proporcionadas."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )

# @app.post("/respond-to-auth-challenge")
# async def respond_to_auth_challenge(request: RespondToChallengeRequest):
#     try:
#         response = client.respond_to_auth_challenge(
#             ClientId=CLIENT_ID,
#             ChallengeName='SOFTWARE_TOKEN_MFA',
#             Session=request.session,
#             ChallengeResponses={
#                 'USERNAME': request.username,
#                 'SOFTWARE_TOKEN_MFA_CODE': request.user_code
#             }
#         )

#         # Devuelve los tokens de autenticación si el desafío fue completado con éxito
#         if 'AuthenticationResult' in response:
#             return {
#                 "code": 200,
#                 "message": "Desafío completado con éxito",
#                 "description": "El usuario ha completado el desafío TOTP correctamente.",
#                 "access_token": response['AuthenticationResult']['AccessToken'],
#                 "id_token": response['AuthenticationResult']['IdToken'],
#                 "refresh_token": response['AuthenticationResult']['RefreshToken'],
#                 "token_type": response['AuthenticationResult']['TokenType']
#             }
#         else:
#             raise HTTPException(
#                 status_code=400,
#                 detail={
#                     "code": 400,
#                     "message": "Desafío no completado",
#                     "description": "El desafío no fue completado correctamente."
#                 }
#             )

#     except client.exceptions.NotAuthorizedException:
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "code": 401,
#                 "message": "Código TOTP incorrecto",
#                 "description": "El código TOTP proporcionado es incorrecto."
#             }
#         )
#     except client.exceptions.SessionExpiredException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Sesión expirada",
#                 "description": "La sesión ha expirado. Inicie sesión nuevamente."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )


# @app.post("/confirm-email")
# async def confirm_email(data: ConfirmEmail):
#     try:
#         # Llama al método de Cognito para confirmar el registro del usuario
#         response = client.confirm_sign_up(
#             ClientId=CLIENT_ID,
#             Username=data.username,
#             ConfirmationCode=data.confirmation_code
#         )   
#         return {
#             "code": 200,
#             "message": "Email confirmado",
#             "description": "Email confirmado exitosamente. La cuenta está ahora activa."
#         }
#     except client.exceptions.CodeMismatchException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Código incorrecto",
#                 "description": "El código de verificación es incorrecto."
#             }
#         )
#     except client.exceptions.ExpiredCodeException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Código expirado",
#                 "description": "El código de verificación ha expirado."
#             }
#         )
#     except client.exceptions.UserNotFoundException:
#         raise HTTPException(
#             status_code=404,
#             detail={
#                 "code": 404,
#                 "message": "Usuario no encontrado",
#                 "description": "No se encontró un usuario con las credenciales proporcionadas."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )

# @app.post("/forgot-password")
# async def forgot_password(request: ForgotPasswordRequest):
#     try:
#         response = client.forgot_password(
#             ClientId=CLIENT_ID,
#             Username=request.username
#         )
#         return {
#             "code": 200,
#             "message": "Código de verificación enviado",
#             "description": "Código de verificación enviado al correo o número de teléfono asociado."
#         }
#     except client.exceptions.UserNotFoundException:
#         raise HTTPException(
#             status_code=404,
#             detail={
#                 "code": 404,
#                 "message": "Usuario no encontrado",
#                 "description": "No se encontró un usuario con el nombre de usuario proporcionado."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )


# @app.post("/confirm-forgot-password")
# async def confirm_forgot_password(request: ConfirmForgotPasswordRequest):
#     try:
#         response = client.confirm_forgot_password(
#             ClientId=CLIENT_ID,
#             Username=request.username,
#             ConfirmationCode=request.confirmation_code,
#             Password=request.new_password
#         )
#         return {
#             "code": 200,
#             "message": "Contraseña restablecida",
#             "description": "Contraseña restablecida con éxito."
#         }
#     except client.exceptions.CodeMismatchException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Código incorrecto",
#                 "description": "El código de verificación es incorrecto."
#             }
#         )
#     except client.exceptions.ExpiredCodeException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Código expirado",
#                 "description": "El código de verificación ha expirado."
#             }
#         )
#     except client.exceptions.InvalidPasswordException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Contraseña no válida",
#                 "description": "La nueva contraseña no cumple con los requisitos de seguridad."
#             }
#         )
#     except client.exceptions.UserNotFoundException:
#         raise HTTPException(
#             status_code=404,
#             detail={
#                 "code": 404,
#                 "message": "Usuario no encontrado",
#                 "description": "No se encontró un usuario con el nombre de usuario proporcionado."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )


# @app.post("/logout")
# async def logout(request: Request):
#     try:
#         # Obtiene el access token desde el header Authorization
#         access_token = request.headers.get("Authorization")
#         if not access_token or not access_token.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=401,
#                 detail={
#                     "code": 401,
#                     "message": "Token no proporcionado",
#                     "description": "El token de acceso no fue proporcionado o es inválido."
#                 }
#             )

#         # Elimina el prefijo 'Bearer ' para obtener solo el token
#         access_token = access_token.split(" ")[1]

#         # Cierra todas las sesiones activas del usuario
#         client.global_sign_out(
#             AccessToken=access_token
#         )
#         return {
#             "code": 200,
#             "message": "Sesión cerrada",
#             "description": "Sesión cerrada con éxito."
#         }
#     except client.exceptions.NotAuthorizedException:
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "code": 401,
#                 "message": "Token no autorizado",
#                 "description": "Token de acceso no válido o ya expirado."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )


# @app.post("/revoke-token")
# async def revoke_token(request: RevokeTokenRequest):
#     try:
#         client.revoke_token(
#             Token=request.token,
#             ClientId=request.client_id
#         )
#         return {
#             "code": 200,
#             "message": "Token revocado",
#             "description": "Token revocado con éxito."
#         }
#     except client.exceptions.InvalidParameterException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Token no válido",
#                 "description": "El token proporcionado no es válido."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )

# @app.post("/register")
# async def register_user(user: User):
#     try:
#         response = client.sign_up(
#             ClientId=CLIENT_ID,
#             Username=user.username,
#             Password=user.password,
#             UserAttributes=[
#                 {
#                     'Name': 'email',
#                     'Value': user.email
#                 }
#             ]
#         )
#         return {
#             "code": 200,
#             "message": "Registro exitoso",
#             "description": "Usuario registrado. Se ha enviado un correo de verificación al email proporcionado."
#         }

#     except client.exceptions.UsernameExistsException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Nombre de usuario ya existente",
#                 "description": "El nombre de usuario ya existe."
#             }
#         )
#     except client.exceptions.UserLambdaValidationException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Correo ya registrado",
#                 "description": "El correo electrónico ya está registrado en el sistema."
#             }
#         )
#     except client.exceptions.InvalidPasswordException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Contraseña inválida",
#                 "description": "La contraseña no cumple con los requisitos de seguridad."
#             }
#         )
#     except client.exceptions.InvalidParameterException as e:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Parámetros inválidos",
#                 "description": "Parámetros inválidos: " + str(e)
#             }
#         )
#     except client.exceptions.ClientError as e:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de cliente",
#                 "description": str(e)
#             }
#         )



# @app.post("/verify-totp")
# async def verify_totp(request: VerifyTOTPRequest):
#     try:
#         response = client.verify_software_token(
#             Session=request.session,
#             UserCode=request.user_code
#         )
#         if response['Status'] == 'SUCCESS':
#             return {
#                 "code": 200,
#                 "message": "TOTP configurado",
#                 "description": "TOTP configurado correctamente."
#             }
#         else:
#             raise HTTPException(
#                 status_code=400,
#                 detail={
#                     "code": 400,
#                     "message": "Verificación fallida",
#                     "description": "Verificación de TOTP fallida."
#                 }
#             )
#     except client.exceptions.InvalidParameterException:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Parámetros inválidos",
#                 "description": "Código TOTP o sesión inválidos."
#             }
#         )
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )

# @app.post("/associate-totp")
# async def associate_topt(request: AssociateTOTPRequest):
#     try:
#         response = client.associate_software_token(
#             Session=request.session
#         )
#         secret_code = response['SecretCode']
#         session = response['Session']
#         return {
#             "code": 200,
#             "message": "Asociación de TOTP exitosa",
#             "description": "Se ha generado un código secreto para configurar TOTP.",
#             "secret_code": secret_code,
#             "session": session  # Devuelve el código para que el frontend lo convierta en un QR.
#         }
#     except client.exceptions.ClientError as e:
#         error_message = e.response['Error']['Message']
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "code": 400,
#                 "message": "Error de Cognito",
#                 "description": error_message
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "code": 500,
#                 "message": "Error interno",
#                 "description": str(e)
#             }
#         )


