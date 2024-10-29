import { useState } from 'react';
import { submitForm } from '../services/api';

import InputField from '../components/InputField';
import Button from '../components/Button';


const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState({ username: '', githubUrl: '', form: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newError = { username: '', githubUrl: '', form: '' };
    let hasError = false;

    if (!username) {
      newError.username = 'Este campo es obligatorio';
      hasError = true;
    }else{
      hasError = false;
      newError.username = '';
    }
    if (!githubUrl) {
      newError.githubUrl = 'Este campo es obligatorio';
      hasError = true;
    }else{
      hasError = false;
      newError.githubUrl = '';
    }

    setError(newError);

    if (hasError) return;

    try {
      const data = await submitForm({ username, githubUrl });
      console.log('Server response:', data);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };


  return (
    <form onSubmit={handleSubmit} className="w-96">
    <h2 className="text-2xl mb-6 text-center text-white">Iniciar sesión</h2>
    <InputField
      id="username"
      type="text"
      value={username}
      onChange={(e) => setUsername(e.target.value)}
      label="Nombre de usuario"
      error={error.username}
    />
    <InputField
      id="githubUrl"
      type="url"
      value={githubUrl}
      onChange={(e) => setGithubUrl(e.target.value)}
      label="URL Github"
      error={error.githubUrl}
    />
    {error.form && <p className="text-red-500 text-sm mt-1 text-center">{error.form}</p>}
    <Button type="submit" className="w-full p-3 mt-4">Aceptar</Button>
  </form>
  );
};

export default LoginForm;