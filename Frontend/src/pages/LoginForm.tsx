import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import InputField from '../components/InputField';
import LoadingIndicator from '../components/LoadingIndicator';
import useAuth from '../hooks/useAuth';
import { ApiError, submitForm } from '../services/api';
import { ProjectData } from '../types/auth';
import LeoPlatziLogo from '/LeoPlatzi.svg';

const PLATZI_URL_REGEX = /^https:\/\/platzi\.com\/p\/[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*\/$/;

const validateUsername = (username: string): string | undefined => {
  if (!username) return 'Este campo es obligatorio';
  if (!PLATZI_URL_REGEX.test(username)) {
    return 'La URL debe seguir el formato: https://platzi.com/p/usuario/';
  }
  return undefined;
};

interface ErrorState {
  username?: string;
  form?: string;
}

const funnyPhrases = ["Afinando tu match perfecto",
  "Casi lo tenemos...",
  "Algo increíble se acerca",
  "Analizando las mejores opciones",
  "Trabajando en tu futuro...",
  "¡Tu próximo reto está cerca!",
  "Encontrando tu lugar ideal",
  "Un paso más cerca...",
  "Tu proyecto está en camino",
  "Preparando tu siguiente aventura",
  "Estamos buscando un proyecto para ti",
  "Rastreando oportunidades para ti",
  "Personalizando tu experiencia",
  "Tu talento merece lo mejor",
  "Optimizando tu asignación",
  "Ajustando parámetros",
  "Afinando detalles",
  "Potenciando tu talento",
  "Estudiando alternativas",
  "Creando tu camino",
]

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [funnyPhrase, setFunnyPhrase] = useState('');
  const [error, setError] = useState<ErrorState>({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const authContext = useAuth();

  useEffect(() => {
    const pickRandomPhrase = () => {
      const randomIndex = Math.floor(Math.random() * funnyPhrases.length);
      setFunnyPhrase(funnyPhrases[randomIndex]);
    };
    pickRandomPhrase();
    const intervalId = setInterval(pickRandomPhrase, 3000);
    return () => clearInterval(intervalId);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const usernameError = validateUsername(username);
    setError({ username: usernameError });
    if (usernameError) return;

    setLoading(true);

    try {
      const response = await submitForm({ username });

      if (response.isAssigned) {
        authContext.login(username, response.pbiId, response.iframeUrl);
        navigate('/home');
      } else {
        const projectData = response as ProjectData; // Ensure response matches ProjectData
        authContext.login(username, response.pbiId, response.iframeUrl, projectData);
        navigate('/company');
      }
    } catch (err) {
      console.error('Error submitting form:', err);
      let errorMessage = 'Hubo un error al enviar el formulario. Inténtalo nuevamente.';
      if (err instanceof ApiError) {
        errorMessage = err.message;
      }
      setError((prevError) => ({
        ...prevError,
        form: errorMessage,
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
      {loading ? (
        <LoadingIndicator message={funnyPhrase} />
      ) : (
        <>
          <div className="mb-4" style={{ width: '350px', height: 'auto' }}>
            <img src={LeoPlatziLogo} alt="Logo de LeoPlatzi" />
          </div>
          <form onSubmit={handleSubmit} className="w-96">
            <p className="text-white text-sm mt-1 text-center mb-4">
              Practica en un ambiente colaborativo
              <br />
              Tenemos un proyecto diseñado para lo que has aprendido
            </p>
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
            {error.form && (
              <p className="text-red-500 text-sm mt-1 text-center">{error.form}</p>
            )}
            <Button variant='secondary' type="submit" className="w-full p-3 mt-4">
              Aceptar
            </Button>
          </form>
        </>
      )}
    </div>
  );
};

export default LoginForm;
