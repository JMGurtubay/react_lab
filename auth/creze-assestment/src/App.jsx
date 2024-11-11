import React from 'react';
import LoginForm from './pages/LoginForm';
import { RegisterForm } from './pages/RegisterForm';
import { BrowserRouter, Link, Route, Routes, Navigate } from 'react-router-dom';
import { ForgotPassword } from './pages/ForgotPassword';
import { Index } from './pages/Index';
import ProtectedRoute from '../src/shared/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<ProtectedRoute element={<Index />} redirectTo='/login' />} />
        <Route path='/login' element={<LoginForm />} />
        <Route path='/register' element={<RegisterForm />} />
        <Route path='/forgot-password' element={<ForgotPassword />} />
        <Route path='*' element={<Navigate to='/' />} /> {/* Ruta de fallback */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
