import { useState } from "react";
import { submitForm } from "../services/api";

import InputField from "../components/InputField";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [error, setError] = useState({ username: "", githubUrl: "", form: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newError = { username: "", githubUrl: "", form: "" };
    let hasError = false;

    if (!username) {
      newError.username = "Este campo es obligatorio";
      hasError = true;
    } else {
      hasError = false;
      newError.username = "";
    }
    if (!githubUrl) {
      newError.githubUrl = "Este campo es obligatorio";
      hasError = true;
    } else {
      hasError = false;
      newError.githubUrl = "";
    }

    setError(newError);

    if (hasError) return;

    try {
      const data = await submitForm({ username, githubUrl });
      console.log("Server response:", data);
      navigate('/home');
      
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
      <div className="mb-4 w-32 h-auto mx-auto">
        <svg fill="none" viewBox="0 0 92 32" xmlns="http://www.w3.org/2000/svg">
          <g fill="#0AE98A" clipPath="url(#platzi-logo-new_svg__a)">
            <path d="M25.334 25.135V6.106h8.77c1.897 0 3.355.555 4.386 1.663s1.546 2.606 1.546 4.473-.515 3.364-1.546 4.473c-1.03 1.108-2.499 1.662-4.385 1.662H28.63v6.748h-3.306zm3.306-9.675h5.26c.837 0 1.488-.214 1.965-.651q.7-.657.7-1.867v-1.39c0-.807-.234-1.44-.7-1.867-.467-.438-1.119-.652-1.965-.652h-5.26v6.437zm32.797 9.675c-.836 0-1.478-.243-1.935-.72-.447-.476-.72-1.088-.816-1.827h-.146c-.292.953-.827 1.682-1.604 2.168q-1.165.73-2.84.73-2.362-.001-3.646-1.226c-.856-.817-1.274-1.925-1.274-3.306 0-1.517.554-2.664 1.653-3.423q1.648-1.137 4.842-1.137h2.752V15.11q0-1.398-.758-2.168c-.506-.506-1.294-.759-2.373-.759q-1.34 0-2.197.584a5.2 5.2 0 0 0-1.43 1.488l-1.906-1.721c.506-.856 1.216-1.566 2.14-2.12.914-.554 2.12-.836 3.597-.836 1.974 0 3.481.457 4.531 1.37 1.05.915 1.576 2.237 1.576 3.948v7.633h1.604v2.606h-1.789zM55 23.055c.992 0 1.819-.224 2.46-.662.642-.437.963-1.03.963-1.77v-2.197H55.73c-2.207 0-3.306.68-3.306 2.052v.525c0 .68.233 1.196.69 1.536s1.09.515 1.887.515m18.689 2.08v-2.577l8.158-10.034h-7.895V9.879l11.668.039v2.46l-8.275 10.151h8.479v2.606zm-29.841.01a1.89 1.89 0 0 1-1.896-1.896V6.126h3.189v16.413h2.11v2.606zM89.11 8.022a1.896 1.896 0 1 0 0-3.792 1.896 1.896 0 0 0 0 3.792M63.499 9.889h-.282v2.645h2.44v9.305c0 1.05.282 1.867.846 2.44.564.574 1.4.866 2.519.866h2.78v-2.606h-2.955V12.534h3.189V9.889h-3.19V6.106h-2.868v1.887c0 1.04-.846 1.886-1.886 1.886h-.593zm24.017.039h3.19v15.207h-3.19z" />
            <path
              fillRule="evenodd"
              d="m9.65 4.803-8.07 8.07a3.81 3.81 0 0 0 0 5.388l8.08 8.08a3.81 3.81 0 0 0 5.387 0l2.693-2.694-2.693-2.693-2.694 2.693-8.08-8.08 8.07-8.07 5.387 5.387-5.387 5.386 2.694 2.694 5.387-5.387a3.81 3.81 0 0 0 0-5.387l-5.387-5.387a3.81 3.81 0 0 0-5.387 0"
              clipRule="evenodd"
            />
          </g>
          <defs>
            <clipPath id="platzi-logo-new_svg__a">
              <path fill="#fff" d="M.461 0h91.077v32H.461z" />
            </clipPath>
          </defs>
        </svg>
      </div>
      <form onSubmit={handleSubmit} className="w-96">
        <h2 className="text-2xl mb-6 text-center text-white">Iniciar sesión</h2>
        <InputField
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          label="URL Perfil Platzi"
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
        {error.form && (
          <p className="text-red-500 text-sm mt-1 text-center">{error.form}</p>
        )}
        <Button type="submit" className="w-full p-3 mt-4">
          Aceptar
        </Button>
      </form>
    </div>
  );
};

export default LoginForm;
