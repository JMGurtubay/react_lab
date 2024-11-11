import { AssociateTOTPResponse, AssociateTOTPResponseError } from "../models/AssociateTOTPModel";

export async function associateTOTP(requestData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/mfa/associate-totp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw {
        ...AssociateTOTPResponseError,
        detail: {
          ...AssociateTOTPResponseError.detail,
          code: responseData.code || response.status,
          description: responseData.detail?.description || response.description,
          message: responseData.message || response.message,
        }
      };
    }

    return {
      ...AssociateTOTPResponse,
      code: responseData.code || response.status,
      description: responseData.description || response.description,
      message: responseData.message || response.message,
      secret_code: responseData.secret_code || '',
      session: responseData.session || ''
    };
  } catch (error) {
    console.error('Error en la asociación de TOTP:', error);
    throw error;
  }
}
