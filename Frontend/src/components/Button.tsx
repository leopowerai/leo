import React from 'react';

interface ButtonProps {
  type: 'button' | 'submit' | 'reset';
  className?: string;
  children: React.ReactNode;
  //Deshabilitar botón
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ type, className, children, disabled }) => {
  return (
    <button
      type={type}
      className={`rounded focus:outline-none focus:ring-2 focus:ring-primary-color ${
        disabled
          ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
          : 'bg-white text-primary-color hover:bg-gray-200'
      } ${className}`}
      disabled={disabled}
      title={disabled ? "Formulario incompleto o con errores" : undefined} // Mensaje emergente para el estado deshabilitado
    >
      {children}
    </button>
  );
};

export default Button;