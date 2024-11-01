// src/pages/LoginForm.tsx
import React, { useState, useContext } from 'react';
import AuthContext from '../contexts/AuthContext';
import { submitForm, ApiError } from '../services/api';
import InputField from '../components/InputField';
import Button from '../components/Button';
import { useNavigate } from 'react-router-dom';
import LeoPlatziLogo from '/LeoPlatzi.svg';

const PLATZI_URL_REGEX = /^https:\/\/platzi\.com\/p\/[a-zA-Z0-9._-]{3,20}\/$/;
const GITHUB_URL_REGEX = /^https:\/\/github\.com\/[a-zA-Z0-9_-]{1,39}$/;

const validateUsername = (username: string): string => {
  if (!username) return 'Este campo es obligatorio';
  if (!PLATZI_URL_REGEX.test(username))
    return 'La URL debe seguir el formato: https://platzi.com/p/usuario/';
  return '';
};

const validateGithubUrl = (url: string): string => {
  if (!url) return 'Este campo es obligatorio';
  if (!GITHUB_URL_REGEX.test(url))
    return 'Debe ingresar una URL válida de GitHub (https://github.com/usuario)';
  return '';
};

interface ErrorState {
  username?: string;
  githubUrl?: string;
  form?: string;
}

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState<ErrorState>({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newError: ErrorState = {
      username: validateUsername(username),
      githubUrl: validateGithubUrl(githubUrl),
    };

    setError(newError);

    const hasError = Object.values(newError).some((err) => err);

    if (hasError) return;

    setLoading(true);

    try {
      const response = await submitForm({ username, githubUrl });
      authContext?.login(username, response.pbiId, response.iframeUrl);
      navigate('/home');
    } catch (error) {
      console.error('Error submitting form:', error);

      let errorMessage = 'Hubo un error al enviar el formulario. Inténtalo nuevamente.';

      if (error instanceof ApiError) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      }

      setError((prevError) => ({
        ...prevError,
        form: errorMessage,
      }));
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
      <div className="mb-4" style={{ width: '350px', height: 'auto' }}>
        <img src={LeoPlatziLogo} alt="Logo de LeoPlatzi" />
      </div>
      <form onSubmit={handleSubmit} className="w-96">
        <InputField
          id="username"
          type="text"
          value={username}
          onChange={(e) => {
            const inputValue = e.target.value.replace(
              'https://platzi.com/@',
              'https://platzi.com/p/'
            );
            setUsername(inputValue);
            setError((prevError) => ({
              ...prevError,
              username: validateUsername(inputValue),
            }));
          }}
          label="URL Perfil Platzi"
          error={error.username}
          disabled={loading}
        />
        <InputField
          id="githubUrl"
          type="url"
          value={githubUrl}
          onChange={(e) => {
            setGithubUrl(e.target.value);
            setError((prevError) => ({
              ...prevError,
              githubUrl: validateGithubUrl(e.target.value),
            }));
          }}
          label="URL Github"
          error={error.githubUrl}
          disabled={loading}
        />
        {error.form && (
          <p className="text-red-500 text-sm mt-1 text-center">{error.form}</p>
        )}
        <Button type="submit" className="w-full p-3 mt-4">
          {loading ? <span className="loader-dots">Cargando...</span> : 'Aceptar'}
        </Button>
      </form>
    </div>
  );
};

export default LoginForm;
