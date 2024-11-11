import React from 'react'
import ReactDom from 'react-dom'
import { IoMdCloseCircleOutline } from "react-icons/io";

const MODAL_STYLES = {
  position: 'fixed',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  backgroundColor: '#222',
  padding: '50px',
  zIndex: 1000,
  borderRadius: '50px',
  background: '#222222',
  boxShadow: '5px 5px 60px #1d1d1d, -5px -5px 60px #272727'
};


const OVERLAY_STYLES = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, .7)',
  zIndex: 1000
}

const CLOSE_ICON_STYLES = {
  position: 'absolute',
  width:'50px',
  top: '10px',
  right: '10px',
  cursor: 'pointer',
  fontSize: '24px',
  color: 'white'
};

const CHILDREN_STYLES = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center', // Centra los elementos horizontalmente
  justifyContent: 'space-evenly', // Distribuye el espacio de manera uniforme entre los elementos
  height: '100%', // Opcional, si quieres que el contenedor ocupe toda la altura disponible
};


export default function Modal({ open, children, onClose }) {

  if (!open) return null

  return ReactDom.createPortal(
    <>
      <div style={OVERLAY_STYLES} />
      <div style={MODAL_STYLES}>
        <IoMdCloseCircleOutline onClick={onClose} style={CLOSE_ICON_STYLES}/>
        <div style={CHILDREN_STYLES}>
          {children}
        </div>  
      </div>
    </>,
    document.getElementById('portal')
  )
}