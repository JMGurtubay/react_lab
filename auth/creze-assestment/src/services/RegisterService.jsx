export async function registerUser(userData) {
  try {
    const response = await fetch('http://127.0.0.1:8000/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const responseData = await response.json();

    if (!response.ok) {
      throw {
        code: responseData.code || response.status,
        message: responseData.message || 'Error en la solicitud',
        description: responseData.detail || 'Hubo un problema al registrar al usuario',
      };
    }

    return {
      code: responseData.code || response.status,
      message: responseData.message || 'Registro exitoso',
      description: responseData.detail || 'El usuario ha sido registrado correctamente',
    };
  } catch (error) {
    console.error('Error en el registro:', error);
    throw error; // Se maneja el error para mostrarlo en el componente si es necesario
  }
}
