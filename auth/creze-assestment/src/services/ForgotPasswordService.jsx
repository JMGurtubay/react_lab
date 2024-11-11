import { ForgotPasswordConfirmationResponse, ForgotPasswordConfirmationResponseError, ForgotPasswordResponse, ForgotPasswordResponseError } from "../models/ForgotPasswordModel";



export async function forgotPassword(requestData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/forgot-password/forgot-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw {
        ...ForgotPasswordResponseError,
        detail: {
          ...ForgotPasswordResponseError.detail,
          code: responseData.code || response.status,
          description: responseData.detail?.description || response.description,
          message: responseData.message || response.message,
        }
      };
    }

    return {
      ...ForgotPasswordResponse,
      code: responseData.code || response.status,
      description: responseData.description || response.description,
      message: responseData.message || response.message,
    };
  } catch (error) {
    console.error('Error al enviar codigo de verificación:', error);
    throw error;
  }
}

export async function forgotPasswordConfirmation(requestData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/forgot-password/confirm-forgot-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw {
        ...ForgotPasswordConfirmationResponseError,
        detail: {
          ...ForgotPasswordConfirmationResponseError.detail,
          code: responseData.code || response.status,
          description: responseData.detail?.description || response.description,
          message: responseData.message || response.message,
        }
      };
    }

    return {
      ...ForgotPasswordConfirmationResponse,
      code: responseData.code || response.status,
      description: responseData.description || response.description,
      message: responseData.message || response.message,
    };
  } catch (error) {
    console.error('Error en la asociación de TOTP:', error);
    throw error;
  }
}
