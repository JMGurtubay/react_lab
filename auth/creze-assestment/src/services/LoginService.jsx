import { LoginResponse, LoginResponseError } from "../models/LoginModel";

export async function loginUser(userData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/users/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      const errorResponse = {
        ...LoginResponseError,
        detail: {
          message: responseData.detail?.message || 'Error en la solicitud',
          description: responseData.detail?.description || 'Hubo un problema al iniciar sesión'
        }
      };
      throw errorResponse;
    }

    return {
      ...LoginResponse,
      successCode: responseData.successCode || '',
      message: responseData.message || 'Inicio de sesión exitoso',
      description: responseData.description || 'El usuario ha iniciado sesión correctamente',
      session: responseData.session || ''
    };
  } catch (error) {
    console.error('Error en el inicio de sesión:', error);
    throw error; // Se maneja el error para mostrarlo en el componente si es necesario
  }
}