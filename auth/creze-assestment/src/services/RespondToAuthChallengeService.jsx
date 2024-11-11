import { RespondToAuthChallengeRespond, RespondToAuthChallengeRespondError } from "../models/RespondToAuthChallengeModel";

export async function respondToAuthChallenge(requestData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/mfa/respond-to-auth-challenge', {
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
          ...RespondToAuthChallengeRespondError.detail,
          code: responseData.code || response.status,
          description: responseData.detail?.description || response.description,
          message: responseData.message || response.message,
        }
      };
    }

    return {
      ...RespondToAuthChallengeRespond,
      code: responseData.code || response.status,
      description: responseData.description || response.description,
      message: responseData.message || response.message,
      access_token: responseData.access_token,
      id_token: responseData.id_token,
      refresh_token: responseData.refresh_token,
      token_type: responseData.token_type
    };
  } catch (error) {
    console.error('Error en la asociación de TOTP:', error);
    throw error;
  }
}
