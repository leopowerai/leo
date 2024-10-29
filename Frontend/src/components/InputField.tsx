import React from 'react';

interface InputFieldProps {
  id: string;
  type: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  label: string;
  error?: string;
}

const InputField: React.FC<InputFieldProps> = ({ id, type, value, onChange, label, error }) => {
  return (
    <div className="relative mb-4">
      <input
        type={type}
        id={id}
        value={value}
        onChange={onChange}
        className={`w-full p-3 border rounded focus:outline-none focus:ring-1  bg-input text-white peer ${error ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:ring-green-400'}`}
        placeholder=" "
      />
      <label htmlFor={id} className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4">
        {label}
      </label>
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
};

export default InputField;
