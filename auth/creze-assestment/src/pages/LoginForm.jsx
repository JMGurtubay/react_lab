import React, {Fragment,useState} from "react";
import { FaUser,FaLock } from "react-icons/fa";
import { Link } from 'react-router-dom';
import { loginUser } from "../services/LoginService";
import { LoginRequest } from "../models/LoginModel";
import Modal from "../components/Modal/Modal";
import { CodeInput } from "../components/CodeInput/CodeInput";
import QrCode from "../components/QrCode/QrCode";
import { AssociateTOTPRequest } from "../models/AssociateTOTPModel";
import { associateTOTP } from "../services/AssociateTOTPService";
import { VerifyTOTPRequest } from "../models/VerifyTOTPModel";
import  { RespondToAuthChallengeRequest } from "../models/RespondToAuthChallengeModel";
import { sanitizeInput } from '../shared/sanitize';
import { useNavigate } from "react-router-dom";
import '../styles/form.css'; // Importa el archivo CSS




const BUTTON_WRAPPER_STYLES = {
    position: 'relative',
    zIndex: 1
  }
  

const LoginForm = () => {
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false)
    const [modalContent, setModalContent] = useState(<Fragment></Fragment>)

    const [formData, setFormData] = useState(LoginRequest);



    const AssociateTOTPApi = async (session) => {
        try {
            const AssociateTOTP = {
            ...AssociateTOTPRequest,
            session: session
            };
            
            console.log('Formulario enviado:', AssociateTOTP);
            const response = await associateTOTP(AssociateTOTP); // Captura la respuesta de la API
            console.log('Respuesta:',response)
            return response
        
    
        } catch (error) {
          // Si hay un error, abre el modal con el mensaje de error de la respuesta
          console.error('Error en la asociación de TOTP:', error);
          return error      
        }
    
      };

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
          const response = await loginUser(formData); // Captura la respuesta de la API
          console.log('Respuesta:', response);
          const responseMesagge= sanitizeInput(response.message)

          // Maneja los diferentes flujos según el código de éxito en la respuesta
          if (response.successCode === 'MFA_SETUP_REQUIRED') {

            const associateResponse = await AssociateTOTPApi(response.session);
            

            setModalContent(
              <>
                {responseMesagge}
                <QrCode secretCode={associateResponse.secret_code}/>
                <CodeInput type="verify-totp" requestData={{ ...VerifyTOTPRequest, session: associateResponse.session }} />
              </>
            );
          } else if (response.successCode === 'TOTP_CHALLENGE') {
            setModalContent(
              <>
                {responseMesagge}
                <CodeInput type="respond-to-auth-challenge" requestData={{ ...RespondToAuthChallengeRequest, session:response.session, username:formData.username}} />
              </>
            );
          } else {
            setModalContent(<>{responseMesagge}</>); // Muestra un mensaje genérico en caso de éxito
          }
      
          setIsOpen(true);
        } catch (error) {
          // Si hay un error, abre el modal con el mensaje de error de la respuesta
          console.error('Error en el inicio de sesión:', error);
      
          // Maneja el mensaje de error de la respuesta
          const errorMessage = sanitizeInput(error.detail?.message) || 'Error desconocido al iniciar sesión';
      
          setModalContent(
            <>
              {errorMessage}
            </>
          );
          setIsOpen(true);
        }
      };
      

    return (
        <div className="wrapper">
            <form onSubmit={handleSubmit} className="form">
                <h1 id="heading">Login</h1>
                <div className="input-box">
                    <input className='input-field'  type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required/>
                    <FaUser className='icon'/>
                </div>
                <div className="input-box">
                    <input className="input-field" type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required/>
                    <FaLock className='icon'/>
                </div>
                <div className="btn">
                  <button className="button1" type="submit">Login</button>
                  <button className="button2" type="button" onClick={() => navigate('/register')}>Sign Up</button>
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
    );
};

export default LoginForm;