import { useState} from "react";
import { submitForm } from "../services/api";
import InputField from "../components/InputField";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import LeoPlatziLogo from "/LeoPlatzi.svg";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [error, setError] = useState({ username: "", githubUrl: "", form: "" });
  const navigate = useNavigate();

  const validateUsername = (username: string) => {
    // Validar que el usuario tenga la URL de Platzi en el formato correcto
    const platziUrlRegex = /^https:\/\/platzi\.com\/p\/[a-zA-Z0-9_-]{3,20}\/$/;
    if (!username) {
      return "Este campo es obligatorio";
    }
    if (!platziUrlRegex.test(username)) {
      return "La URL debe seguir el formato: https://platzi.com/p/usuario/";
    }
    return "";
  };

  const validateGithubUrl = (url: string) => {
    const githubUrlRegex = /^https:\/\/github\.com\/[a-zA-Z0-9_-]{1,39}$/;
    if (!url) {
      return "Este campo es obligatorio";
    }
    if (!githubUrlRegex.test(url)) {
      return "Debe ingresar una URL válida de GitHub (https://github.com/usuario)";
    }
    return "";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newError = { username: "", githubUrl: "", form: "" };
    let hasError = false;

    // Validación del nombre de usuario
    newError.username = validateUsername(username);
    if (newError.username) hasError = true;

    // Validación de la URL de GitHub
    newError.githubUrl = validateGithubUrl(githubUrl);
    if (newError.githubUrl) hasError = true;

    setError(newError);

    if (hasError) return;

    try {
      const data = await submitForm({ username, githubUrl });
      console.log("Server response:", data);
      navigate('/home');
      
    } catch (error) {
      console.error("Error submitting form:", error);
      setError((prevError) => ({
        ...prevError,
        form: "Hubo un error al enviar el formulario. Inténtalo nuevamente.",
      }));
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
    <div className="mb-4" style={{ width: "350px", height: "auto" }}> {/* Ancho ajustado a 138px */}
      <img src={LeoPlatziLogo} alt="Logo de LeoPlatzi" />
    </div>
      <form onSubmit={handleSubmit} className="w-96">
        <InputField
          id="username"
          type="text"
          value={username}
          onChange={(e) => {
            const newValue = e.target.value;
            setUsername(newValue);
            setError((prevError) => ({
              ...prevError,
              username: validateUsername(newValue),
            }));
          }}
          label="URL Perfil Platzi"
          error={error.username}
        />
        <InputField
          id="githubUrl"
          type="url"
          value={githubUrl}
          onChange={(e) => {
            const newValue = e.target.value;
            setGithubUrl(newValue);
            setError((prevError) => ({
              ...prevError,
              githubUrl: validateGithubUrl(newValue),
            }));
          }}
          label="URL Github"
          error={error.githubUrl}
        />
        {error.form && (
          <p className="text-red-500 text-sm mt-1 text-center">{error.form}</p>
        )}
        <Button type="submit" className="w-full p-3 mt-4">
          Iniciar Sesión
        </Button>
      </form>
    </div>
  );
};

export default LoginForm;
