// src/components/Button.tsx
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
}

const Button: React.FC<ButtonProps> = ({ type = 'button', className = '', children, variant = 'primary', ...props }) => {
  let variantClasses = '';
  switch (variant) {
    case 'primary':
      variantClasses = 'bg-green-500 text-white hover:bg-green-600 focus:ring-green-400';
      break;
    case 'secondary':
      variantClasses = 'bg-gray-200 text-black hover:bg-gray-300 focus:ring-gray-400';
      break;
    case 'danger':
      variantClasses = 'bg-red-500 text-white hover:bg-red-600 focus:ring-red-400';
      break;
    default:
      variantClasses = 'bg-white text-black hover:bg-gray-200 focus:ring-gray-400';
  }

  return (
    <button
      type={type}
      className={`${variantClasses} rounded focus:outline-none focus:ring-2 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
