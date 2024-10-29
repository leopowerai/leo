import { useState } from 'react';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [githubUrl, setGithubUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Username:', username);
    console.log('Github URL:', githubUrl);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded shadow-md w-96">
      <h2 className="text-2xl mb-6 text-center text-white">Iniciar sesión</h2>
      <div className="mb-4">
        <label htmlFor="username" className="block mb-2 text-sm font-medium text-white">
          Nombre de usuario
        </label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white"
          required
        />
      </div>
      <div className="mb-6">
        <label htmlFor="githubUrl" className="block mb-2 text-sm font-medium text-white">
          URL Github
        </label>
        <input
          type="url"
          id="githubUrl"
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          className="w-full p-3 border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full p-3 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Aceptar
      </button>
    </form>
  );
};

export default LoginForm;