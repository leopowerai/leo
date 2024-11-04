import { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import InputField from '../components/InputField';
import AuthContext, { ProjectData } from '../contexts/AuthContext';
import { ApiError, submitForm } from '../services/api';
import Leo from '/LEO loader.svg';
import LeoPlatziLogo from '/LeoPlatzi.svg';

const PLATZI_URL_REGEX = /^https:\/\/platzi\.com\/p\/[a-zA-Z0-9._-]{3,20}\/$/;

const validateUsername = (username: string): string => {
  if (!username) return 'Este campo es obligatorio';
  if (!PLATZI_URL_REGEX.test(username))
    return '';
  //return 'La URL debe seguir el formato: https://platzi.com/p/usuario/';
  return '';
};

interface ErrorState {
  username?: string;
  form?: string;
}

const funnyPhrasesAboutProjectManagers = ["Afinando tu match perfecto",
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

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [funnyPhrase, setFunnyPhrase] = useState('');
  const [error, setError] = useState<ErrorState>({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    // Function to pick a random phrase
    const pickRandomPhrase = () => {
      const randomIndex = Math.floor(Math.random() * funnyPhrasesAboutProjectManagers.length);
      setFunnyPhrase(funnyPhrasesAboutProjectManagers[randomIndex]);
    };

    // Pick an initial phrase
    pickRandomPhrase();

    // Set interval to pick a new phrase every 3 seconds
    const intervalId = setInterval(pickRandomPhrase, 3000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newError: ErrorState = {
      username: validateUsername(username),
    };

    setError(newError);

    const hasError = Object.values(newError).some((err) => err);

    if (hasError) return;

    setLoading(true);

    try {
      const response = await submitForm({ username });

      if (response.isAssigned) {
        authContext?.login(username, response.pbiId, response.iframeUrl);
        navigate('/home');
      } else {
        const projectData: ProjectData = {
          projectId: response.projectId,
          projectName: response.projectName,
          projectSkills: response.projectSkills,
          projectBusinessContext: response.projectBusinessContext,
          projectTechnicalContext: response.projectTechnicalContext,
          companyName: response.companyName,
          companyContext: response.companyContext,
          pbiTitle: response.pbiTitle,
          pbiDescription: response.pbiDescription,
          pbiSkills: response.pbiSkills,
        };
        authContext?.login(username, response.pbiId, response.iframeUrl, projectData);
        navigate('/company');
      }
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
      {loading ? (
        // Loading state: display the Leo.svg logo
        <div className="flex flex-col items-center">
          <img src={Leo} alt="Loading Leo" className="w-28 h-28 slow-spin" />
          <p className="text-white text-sm mt-1 text-center loader-dots">{funnyPhrase}</p>
        </div>
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
            <Button type="submit" className="w-full p-3 mt-4">
              Aceptar
            </Button>
          </form>
        </>
      )}
    </div>
  );
};

export default LoginForm;
