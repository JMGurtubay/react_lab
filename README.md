
# Project Name

## Overview

This project consists of a **frontend** built with React and a **backend** built with FastAPI, integrated with AWS Cognito for secure authentication, including multi-factor authentication (MFA). 

The project’s primary goal is to provide a secure and modular system for user authentication, password recovery, and session management using Cognito.

## Project Structure

```
react_lab/
└── auth/
    ├── creze-assessment/     # Frontend (React)
    └── CognitoAuth/          # Backend (FastAPI)
```

## Features

### Backend (FastAPI)
- User Registration
- Email Confirmation
- Login with MFA Support
- Password Recovery
- Token Revocation
- Modularized structure for better maintainability and scalability

### Frontend (React)
- User-friendly interface for authentication
- Support for MFA configuration and verification

## Setup Instructions

### Prerequisites
- Python 3.8+ for the backend
- Node.js and npm for the frontend
- AWS account with Cognito configured for the project

### Backend Setup

1. **Clone the repository and navigate to the backend folder**:
   ```bash
   cd react_lab/auth/CognitoAuth
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   - Configure `.env` file with the following values:
     ```plaintext
     USER_POOL_ID=<Your_Cognito_User_Pool_ID>
     CLIENT_ID=<Your_Cognito_Client_ID>
     ```

4. **Run the backend server**:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd react_lab/auth/creze-assessment
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the frontend server**:
   ```bash
   npm start
   ```

## AWS Cognito MFA Setup

To configure MFA for a user in the AWS Cognito Console:
1. Go to the Cognito console and select your user pool.
2. Select the user for whom you want to enable MFA.
3. Go to **Actions** > **Update MFA**.
4. Enable or disable MFA by toggling the checkbox.

## API Documentation

Each API endpoint follows a structured request/response format. Here is a high-level description of the API flow:

### User Registration
- **Endpoint**: `/users/register`
- **Request**: `{ "username": "user", "email": "email@example.com", "password": "password123" }`
- **Response** (success): `{ "code": 200, "message": "Registro exitoso", "description": "Usuario registrado." }`

### Email Confirmation
- **Endpoint**: `/users/confirm-email`
- **Request**: `{ "username": "user", "confirmation_code": "123456" }`
- **Response** (success): `{ "code": 200, "message": "Email confirmado", "description": "Email confirmado exitosamente." }`

### Login
- **Endpoint**: `/users/login`
- **Request**: `{ "username": "user", "password": "password123" }`
- **Response** (success): `{ "code": 200, "message": "Inicio de sesión exitoso" }`

Additional routes include `/mfa/associate-totp`, `/mfa/verify-totp`, `/forgot-password`, and more. Each route is documented in detail in the code.

## Dependencies

### Backend (FastAPI)
- `fastapi`
- `uvicorn`
- `boto3`
- `python-dotenv`
- `pydantic`

### Frontend (React)
- `react`
- `axios`
- `react-router-dom`
- Other dependencies can be found in `package.json` for the frontend and `requirements.txt` for the backend.

## Security Considerations

- Implemented CSRF protection and HTTPS configuration.
- `HttpOnly` cookies for secure token handling.
- Tested for unauthorized access and robust error handling.
