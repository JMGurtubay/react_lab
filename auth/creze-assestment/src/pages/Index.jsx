import React from 'react'
import { useNavigate } from 'react-router-dom';
import { sanitizeInput } from '../shared/sanitize';
import { logoutUser } from '../services/LogoutService';
import '../styles/index.css'; // Importa el archivo CSS




export const Index = () => {
    
    const navigate = useNavigate();


    const handleLogout = async () => {
        try {
            console.log('Intentando cerrar sesión...');
            await logoutUser(); // Captura la respuesta de la API
            // Si la respuesta es exitosa, redirige al usuario al inicio de sesión
            navigate('/login');

        } catch (error) {
            // Maneja el mensaje de error de la respuesta
            console.error('Error al cerrar sesión:', error);
            const errorMessage = error.message ? sanitizeInput(error.message) : sanitizeInput(error.detail.description);

            setModalContent(
                <>
                    {errorMessage}
                </>
            );
            setIsOpen(true);
        }
    };

  return (
    <button className='logout-btn' onClick={handleLogout}>Logout</button>
  )
}
