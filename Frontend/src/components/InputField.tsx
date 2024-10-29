import React from 'react';

interface InputFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  id: string;
  label: string;
  error?: string;
}

const InputField: React.FC<InputFieldProps> = ({
  id,
  type = 'text',
  value,
  onChange,
  label,
  error,
  ...props
}) => {
  return (
    <div className="relative mb-4">
      <input
        type={type}
        id={id}
        value={value}
        onChange={onChange}
        className={`w-full p-3 border rounded focus:outline-none focus:ring-1 bg-input text-white peer ${
          error ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:ring-green-400'
        }`}
        placeholder=" "
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        {...props}
      />
      <label
        htmlFor={id}
        className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4"
      >
        {label}
      </label>
      {error && (
        <p id={`${id}-error`} className="text-red-500 text-sm mt-1">
          {error}
        </p>
      )}
    </div>
  );
};

export default InputField;
