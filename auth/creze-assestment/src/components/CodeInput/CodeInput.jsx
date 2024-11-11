import React, {useState} from 'react';
import { confirmEmail } from '../../services/ConfirmEmailService';
import { verifyTOTP } from '../../services/VerifyTOTPService';
import { respondToAuthChallenge } from '../../services/RespondToAuthChallengeService';
import { sanitizeInput } from '../../shared/sanitize';
import { setCookie, getCookie } from '../../shared/cookieUtils';
import { useNavigate } from 'react-router-dom';
import './CodeInput.css'




// Recibe el tipo de código como prop
export const CodeInput = ({ type, requestData }) => {

  const navigate = useNavigate();

  const [mensajeAPI, setMensajeAPI] = useState()
  const keyMapping = {
    'confirm-email': 'confirmation_code',
    'verify-totp': 'user_code',
    'respond-to-auth-challenge': 'user_code',
  };

  const [formData, setFormData] = useState({});
  // const [formData, setFormData] = useState({
  //   confirmation_code: ''
  // });

  const handleLoginSuccess = (response) => {
    if (response.access_token) {
      setCookie('access-token', response.access_token, 0.05); // 0.02 días es aproximadamente 30 minutos
    }
  };

  // const handleChange = (e) => {
  //   const { value } = e.target;
  //   const key = keyMapping[type]
  
  //   setFormData({
  //     ...formData,
  //     [key]: value,
  //   });
  // };
  
  const handleChange = (e) => {
    const { value } = e.target;
    const key = keyMapping[type];

    // Limita la longitud a 6 caracteres (ajustar según tu necesidad)
    const trimmedValue = value.slice(0, 6);

    setFormData({
      ...formData,
      [key]: trimmedValue,
    });
  };

  const confirmEmailApi = async (requestWithCode) => {
    try {
      console.log('Formulario enviado:', requestWithCode);
      const response = await confirmEmail(requestWithCode); // Captura la respuesta de la API
      console.log('Respuesta:',response)
      navigate('/login')

    } catch (error) {
      // Si hay un error, abre el modal con el mensaje de error de la respuesta
      console.error('Error en la verificación:', error);
      // Maneja el mensaje de error de la respuesta
      const errorMessage = error.description?.message ? sanitizeInput(error.description.message) : sanitizeInput(error.message);
      setMensajeAPI(errorMessage)
    }

  };

  const verifyTOTPApi = async (requestWithCode) => {
    try {
      console.log('Formulario enviado:', requestWithCode);
      const response = await verifyTOTP(requestWithCode); // Captura la respuesta de la API
      console.log('Respuesta:',response)
      const responseMessage = sanitizeInput(response.message)
      setMensajeAPI(responseMessage)


    } catch (error) {
      // Si hay un error, abre el modal con el mensaje de error de la respuesta
      console.error('Error en TOTP:', error);
      // Maneja el mensaje de error de la respuesta
      const errorMessage = sanitizeInput(error.message)
      setMensajeAPI(errorMessage)
  
    }
    // Lógica de llamada a la API de verificación de TOTP
  };

  const respondToAuthChallengeApi = async (requestWithCode) => {
    try {
      console.log('Formulario enviado:', requestWithCode);
      const response=await respondToAuthChallenge(requestWithCode); // Captura la respuesta de la API
      console.log(response)
      handleLoginSuccess(response)
      console.log(getCookie('access-token')); // Verifica que sea igual en 'setCookie'
      navigate('/');


    } catch (error) {
      // Si hay un error, abre el modal con el mensaje de error de la respuesta
      console.error('Error en TOTP:', error);
      // Maneja el mensaje de error de la respuesta
      const errorMessage = sanitizeInput(error.message)
      setMensajeAPI(errorMessage)
  
    }
    // Lógica de llamada a la API de respuesta al desafío de autenticación
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const requestWithCode = {
      ...requestData,
      ...formData // Aquí `formData` tendrá la clave correcta (user_code o confirmation_code)
    };

    try {
      switch (type) {
        case 'confirm-email':
          await confirmEmailApi(requestWithCode);
          break;
        case 'verify-totp':
          await verifyTOTPApi(requestWithCode);
          break;
        case 'respond-to-auth-challenge':
          await respondToAuthChallengeApi(requestWithCode);
          break;
        default:
          console.error('Tipo de código no reconocido');
      }
      console.log('API llamada exitosamente');
    } catch (error) {
      console.error('Error al llamar la API:', error);
    }
  };

  return (
    <div className='code-wrapper'>
      <form onSubmit={handleSubmit} className='code-form'>
        <label htmlFor="code-input">Enter Code:</label>
        <div className="code-container">
          <input
            className="code-input"
            type="text"
            maxLength="6" // Limita el número de caracteres ingresables
            value={formData[keyMapping[type]] || ''}
            onChange={handleChange}
            style={{ position: 'absolute', opacity: 0, zIndex: -1 }} // Esconde el input real
          />
          <div className="input-overlay" onClick={() => document.querySelector('.code-input').focus()}>
            {[...Array(6)].map((_, index) => (
              <div key={index} className="input-char">
                {(formData[keyMapping[type]] || '')[index] || ''}
              </div>
            ))}
          </div>
        </div>
        <button className='code-btn' type="submit"><span>Enviar</span><span></span></button>
      </form>
    </div>
    
  );
};