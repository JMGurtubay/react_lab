import React, { Fragment, useState } from 'react'
import { MdOutlineAlternateEmail } from "react-icons/md";
import { FaUser,FaLock } from "react-icons/fa";
import { Link } from 'react-router-dom';
import { registerUser } from '../services/RegisterService';
import Modal from '../components/Modal/Modal'
import { CodeInput } from '../components/CodeInput/CodeInput';
import { RegisterRequest } from '../models/RegisterModel'; // Ajusta la ruta según tu estructura de proyecto
import { ConfirmEmailRequest } from '../models/ConfirmEmailModel';
import { sanitizeInput } from '../shared/sanitize';
import { useNavigate } from "react-router-dom";




const BUTTON_WRAPPER_STYLES = {
  position: 'relative',
  zIndex: 1
}



export const RegisterForm = () => {
    const navigate = useNavigate();

    const [isOpen, setIsOpen] = useState(false)
    const [modalContent, setModalContent] = useState(<Fragment></Fragment>)

    const [formData, setFormData] = useState(RegisterRequest);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
          ...formData,
          [name]: value,
        });
      };
    

      const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          console.log('Formulario enviado:', formData);
          const response = await registerUser(formData); // Captura la respuesta de la API
          console.log('Respuesta:',response)
          // Si la respuesta es exitosa, abre el modal con el componente de <CodeInput>
          const respondeMessage =  sanitizeInput(response.message)
          setModalContent(
            <>
              {respondeMessage}
              <CodeInput type={'confirm-email'} requestData={{ ...ConfirmEmailRequest, username: formData.username }}/>
            </>
          );
          setIsOpen(true);
        } catch (error) {
          // Si hay un error, abre el modal con el mensaje de error de la respuesta
          console.error('Error en el registro:', error);
      
          // Maneja el mensaje de error de la respuesta
          // const errorMessage = error.description.message ? error.description.message : error.message
          const errorMessage = error.description?.message ? sanitizeInput(error.description.message) : sanitizeInput(error.message);
      
          setModalContent(
            <>{errorMessage}</>
          );
          setIsOpen(true);
        }
      };

  return (
    <div className="wrapper">
        <form onSubmit={handleSubmit} className="form">
            <h1 id="heading">Sign Up</h1>
            <div className="input-box">
                <input className='input-field' type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required/>
                <FaUser className='icon'/>
            </div>
            <div className="input-box">
                <input className='input-field' type="text" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required/>
                <MdOutlineAlternateEmail className='icon'/>
            </div>
            <div className="input-box">
                <input className='input-field' type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required/>
                <FaLock className='icon'/>
            </div>
            <div className="btn">
              <button className="button1" type="button" onClick={() => navigate('/login')}>Login</button>
              <button className="button2" type="submit" >Sign Up</button>
            </div>
            <button className="button3" type="button" onClick={() => navigate('/forgot-password')}>Forgot Password</button>
        </form>
        <>
          <div style={BUTTON_WRAPPER_STYLES}>

            <Modal open={isOpen} onClose={() => setIsOpen(false)}>
              {modalContent}
            </Modal>

          </div>
        </>
    </div>
  )
}
