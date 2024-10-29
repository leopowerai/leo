import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState({ username: '', githubUrl: '' });
  const navigate = useNavigate();  // Hook para navegación

   // Función de validación de URL de GitHub
   const validateGithubUrl = (url: string) => {
    // Validación básica de URL
    try {
      new URL(url);
    } catch {
      return 'La URL no es válida';
    }

    // Validación específica de GitHub
    const githubUrlPattern = /^https:\/\/github\.com\/[\w-]+(?:\/[\w.-]+)*\/?$/;
    if (!githubUrlPattern.test(url)) {
      return 'La URL debe ser de GitHub (ejemplo: https://github.com/usuario)';
    }

    // Validación de caracteres especiales en el username de GitHub
    const username = url.split('github.com/')[1]?.split('/')[0];
    if (username && !/^[\w-]+$/.test(username)) {
      return 'El nombre de usuario de GitHub contiene caracteres no válidos';
    }

    return ''; // URL válida
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newError = { username: '', githubUrl: '' };
    let hasError = false;

    if (!username) {
      newError.username = 'Este campo es obligatorio';
      hasError = true;
    } else if (username.length < 3) {
      newError.username = 'El nombre de usuario debe tener al menos 3 caracteres';
      hasError = true;
    } else if (username.length < 3) {
      newError.username = 'El nombre de usuario no puede exceder 50 caracteres';  
      hasError = true;
    }
    if (!githubUrl) {
      newError.githubUrl = 'Este campo es obligatorio';
      hasError = true;
    } else {
      const urlError = validateGithubUrl(githubUrl);
      if (urlError) {
        newError.githubUrl = urlError;
        hasError = true;
      }  
    }

    setError(newError);

    if (hasError) return;

    try {
      //Simular envío exitoso
      //Comentado temporalmente hasta que el backend esté listo
      /*const response = await fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, githubUrl }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Server response:', data);
      */
      
      // Guardar datos en localStorage
      localStorage.setItem('username', username);
      localStorage.setItem('githubUrl', githubUrl);

      // Navegar a la página home
      navigate('/home');

    } catch (error) {
      console.error('Error submitting form:', error);
      // Mostrar un mensaje de error al usuario
      setError({
        username: '',
        githubUrl: 'Error al enviar los datos. Por favor, intenta nuevamente.'
      });
    }
  };
      // Validación en tiempo real de la URL de GitHub
      const handleGithubUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const url = e.target.value;
      setGithubUrl(url);
    
      if (url) {
      const urlError = validateGithubUrl(url);
      setError(prev => ({
        ...prev,
        githubUrl: urlError
      }));
      } else {
      setError(prev => ({
        ...prev,
        githubUrl: ''
      }));
    }
  };


  return (
    <form onSubmit={handleSubmit} className="w-96">
      <h2 className="text-2xl mb-6 text-center text-white">Iniciar sesión en Leo</h2>
      <div className="relative mb-4">
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className={`w-full p-3 border rounded focus:outline-none focus:ring-1 focus:ring-green-400 bg-input text-white peer ${error.username ? 'border-red-500 focus:border-red-500' : 'border-gray-600'}`}
          placeholder=" "
          required
        />
        <label htmlFor="username" className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4">
          Nombre de usuario
        </label>
        {error.username && (
          <p className="text-red-500 text-xs mt-1">{error.username}</p>
        )}
      </div>
      <div className="relative mb-6">
        <input
          type="url"
          id="githubUrl"
          value={githubUrl}
          onChange={handleGithubUrlChange}
          className={`w-full p-3 border rounded focus:outline-none focus:ring-1 focus:ring-green-400 bg-input text-white peer
            ${error.githubUrl ? 'border-red-500 focus:border-red-500' : 'border-gray-600'}`}
          placeholder=" "
          required
        />
        <label htmlFor="githubUrl" className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4">
          URL Github
        </label>
        {error.githubUrl && (
          <p className="text-red-500 text-xs mt-1">{error.githubUrl}</p>
        )}
      </div>
      <button
        type="submit"
        className="w-full p-3 bg-white text-primary-color rounded hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-color"
      >
        Aceptar
      </button>
    </form>
  );
};

export default LoginForm;