import React, {useState} from 'react'
import { ForgotPasswordConfirmationRequest } from '../../models/ForgotPasswordModel'
import {forgotPasswordConfirmation } from '../../services/ForgotPasswordService'
import { FaLock, FaUser } from 'react-icons/fa'
import Modal from '../Modal/Modal'
import { sanitizeInput } from '../../shared/sanitize'

export const ConfirmForgotPassword = () => {
    const [mensajeAPI, setMensajeAPI] = useState()

    const [formData, setFormData] = useState(ForgotPasswordConfirmationRequest);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
          ...formData,
          [name]: value,
        });
      };

      const handleConfirmationSubmit = async (e) =>{
        e.preventDefault();
        try {
            console.log('Formulario enviado:', formData);
            const response = await forgotPasswordConfirmation(formData); // Captura la respuesta de la API
            console.log('Respuesta:',response)
            // Si la respuesta es exitosa, abre el modal con el componente de <CodeInput>
            const respondeMessage =  sanitizeInput(response.message)
            setMensajeAPI(respondeMessage)
        } catch (error) {
            // Si hay un error, abre el modal con el mensaje de error de la respuesta
            console.error('Error en el registro:', error);
       
            // Maneja el mensaje de error de la respuesta
            const errorMessage = error.description?.message ? sanitizeInput(error.description.message) : sanitizeInput(error.message);
            setMensajeAPI(errorMessage)

        };
    }

  return (
    <>
      <div className='code-wrapper'>
      <form onSubmit={handleConfirmationSubmit} className='code-form'>
        <h1 id="heading">Password Recovery</h1>
        <div className="input-box">
          <input className='input-field' type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required/>
          <FaUser className='icon'/>
        </div>
        <div className="input-box">
          <input className='input-field' type="password" name="password" placeholder="Password" value={formData.new_password} onChange={handleChange} required/>
          <FaLock className='icon'/>
        </div>
        <label htmlFor="username">Enter Code</label>
        <div className="code-container">
          <input
            className="code-input"
            type="text"
            maxLength="6" // Limita el número de caracteres ingresables
            value={formData.confirmation_code}
            onChange={handleChange}
            style={{ position: 'absolute', opacity: 0, zIndex: -1 }} // Esconde el input real
          />
          <div className="input-overlay" onClick={() => document.querySelector('.password-input').focus()}>
            {[...Array(6)].map((_, index) => (
              <div key={index} className="input-char">
                {(formData.confirmation_code || '')[index] || ''}
              </div>
            ))}
          </div>
        </div>
        <button className='code-btn' type="submit"><span>Send</span><span></span></button>  
      </form>
      <p>{mensajeAPI}</p>
      </div>
  </>
  )
}
