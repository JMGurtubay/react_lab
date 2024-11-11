import boto3
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuraciones de Cognito
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
REGION_NAME = os.getenv('REGION_NAME')

# Cliente de Cognito
client = boto3.client('cognito-idp', region_name=REGION_NAME)
