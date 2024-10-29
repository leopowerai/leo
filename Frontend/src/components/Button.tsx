import React from 'react';

interface ButtonProps {
  type: 'button' | 'submit' | 'reset';
  className?: string;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ type, className, children }) => {
  return (
    <button
      type={type}
      className={`bg-white text-primary-color rounded hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-color ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;