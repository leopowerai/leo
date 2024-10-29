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
    <form onSubmit={handleSubmit} className="w-96">
      <h2 className="text-2xl mb-6 text-center text-white">Iniciar sesión</h2>
      <div className="relative mb-4">
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 border border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-green-400 focus:border-green-400 bg-input text-white peer"
          placeholder=" "
          required
        />
        <label htmlFor="username" className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4">
          Nombre de usuario
        </label>
      </div>
      <div className="relative mb-6">
        <input
          type="url"
          id="githubUrl"
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          className="w-full p-3 border border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-green-400 focus:border-green-400 bg-input text-white peer"
          placeholder=" "
          required
        />
        <label htmlFor="githubUrl" className="absolute left-3 top-4 text-sm text-white transition-all transform -translate-y-4 scale-90 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-4">
          URL Github
        </label>
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