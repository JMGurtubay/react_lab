import { LogoutResponse, LogoutResponseError } from "../models/LogoutModel";
import { getCookie, deleteCookie } from "../shared/cookieUtils"; // Función para obtener cookies

export async function logoutUser() {
  try {
    // Obtiene el access-token de las cookies
    const accessToken = getCookie("access-token");

    if (!accessToken) {
      throw {
        ...LogoutResponseError,
        detail: {
          message: "Token de acceso no encontrado",
          description: "No se encontró un token de acceso en las cookies."
        }
      };
    }

    const response = await fetch('http://127.0.0.1:8000/users/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    const responseData = await response.json();

    if (!response.ok) {
      const errorResponse = {
        ...LogoutResponseError,
        detail: {
          message: responseData.detail?.message || 'Error en la solicitud',
          description: responseData.detail?.description || 'Hubo un problema al cerrar sesión'
        }
      };
      throw errorResponse;
    }
    deleteCookie('access-token')
    return {
      ...LogoutResponse,
      message: responseData.message || 'Sesión cerrada exitosamente',
      description: responseData.description || 'La sesión se ha cerrado correctamente'
    };
  } catch (error) {
    console.error('Error al cerrar sesión:', error);
    throw error; // Se maneja el error para mostrarlo en el componente si es necesario
  }
}