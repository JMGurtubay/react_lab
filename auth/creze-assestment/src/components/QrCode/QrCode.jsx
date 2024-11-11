import React from 'react';
import { QRCodeSVG } from 'qrcode.react'; // Usa QRCodeCanvas si prefieres

export default function QrCode({secretCode}){
  const qrSecretCode = secretCode // Reemplázalo por tu código
  const qrValue = `otpauth://totp/Fintech_APP?secret=${secretCode}&issuer=Creze`;

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h3>Escanea este código QR con tu aplicación de autenticación</h3>
      <QRCodeSVG value={qrValue} size={256} />
    </div>
  );
};
