export async function confirmEmail(requestData) {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/confirm-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
  
      const responseData = await response.json();
  
      if (!response.ok) {
        throw {
          code: responseData.code || response.status,
          message: responseData.message || 'Error en la verificación',
          description: responseData.detail || 'Hubo un problema al verificar el codigo',
        };
      }
  
      return {
        code: responseData.code || response.status,
        message: responseData.message || 'Verificación exitosa',
        description: responseData.detail || 'El email ha sido verificado correctamente',
      };
    } catch (error) {
      console.error('Error en la verificación de email:', error);
      throw error; // Se maneja el error para mostrarlo en el componente si es necesario
    }
  }
  