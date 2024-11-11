import { VerifyTOTPResponse, VerifyTOTPResponseError } from "../models/VerifyTOTPModel";

export async function verifyTOTP(requestData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/mfa/verify-totp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw {
        ...VerifyTOTPResponseError,
        detail: {
          ...VerifyTOTPResponseError.detail,
          code: responseData.code || response.status,
          description: responseData.detail?.description || response.description,
          message: responseData.message || response.message,
        }
      };
    }

    return {
      ...VerifyTOTPResponse,
      code: responseData.code || response.status,
      description: responseData.detail?.description || response.description,
      message: responseData.message || response.message,
    };
  } catch (error) {
    console.error('Error en la verificación de TOTP:', error);
    throw error;
  }
}
