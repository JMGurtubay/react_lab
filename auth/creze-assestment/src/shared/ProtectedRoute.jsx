import React from 'react';
import { Navigate } from 'react-router-dom';
import { getCookie } from './cookieUtils';

function ProtectedRoute({ element, redirectTo }) {
  const accessToken = getCookie('access-token'); // Lee el token de las cookies

  return accessToken ? element : <Navigate to={redirectTo} />;
}

export default ProtectedRoute;