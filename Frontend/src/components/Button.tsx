import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ type = 'button', className = '', children, ...props }) => {
  return (
    <button
      type={type}
      className={`bg-white text-primary-color rounded hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-color ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
