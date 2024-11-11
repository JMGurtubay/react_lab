import React, {useState, Fragment} from 'react'
import { ForgotPasswordRequest } from '../models/ForgotPasswordModel'
import { forgotPassword } from '../services/ForgotPasswordService'
import { FaUser } from 'react-icons/fa'
import Modal from '../components/Modal/Modal'
import { sanitizeInput } from '../shared/sanitize'
import { ConfirmForgotPassword } from '../components/ConfirmForgotPassword/ConfirmForgotPassword'
import { useNavigate } from "react-router-dom";

const BUTTON_WRAPPER_STYLES = {
    position: 'relative',
    zIndex: 1
  }

export const ForgotPassword = () => {

    const navigate = useNavigate();

    const [isOpen, setIsOpen] = useState(false)
    const [modalContent, setModalContent] = useState(<Fragment></Fragment>)

    const [formData, setFormData] = useState(ForgotPasswordRequest);


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
        const response = await forgotPassword(formData); // Captura la respuesta de la API
        console.log('Respuesta:',response)
        // Si la respuesta es exitosa, abre el modal con el componente de <CodeInput>
        const respondeMessage =  sanitizeInput(response.message)
        setModalContent(
            <ConfirmForgotPassword/>
        );
        setIsOpen(true);
    } catch (error) {
        // Maneja el mensaje de error de la respuesta
        const errorMessage = error.message ? sanitizeInput(error.message) : sanitizeInput(error.detail.description);
    
        setModalContent(
        <>{errorMessage}</>
        );
        setIsOpen(true);
    }
    };

  return (
    <>
      <div className='wrapper'>
        <form onSubmit={handleSubmit} className='form'>
          <h1 id="heading">Recover Password</h1>
          <div className="input-box">
            <input className='input-field' type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required/>
            <FaUser className='icon'/>
          </div>
          <div className="btn">
            <button className="button1" type="button" onClick={() => navigate('/login')}>Login</button>
            <button className="button2" type="submit" >Recover Now</button>
          </div>
        </form>
      </div>
      <div style={BUTTON_WRAPPER_STYLES}>

          <Modal open={isOpen} onClose={() => setIsOpen(false)}>
              {modalContent}
          </Modal>

      </div>
    </>
  )
}
