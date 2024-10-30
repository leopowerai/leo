import { useState } from "react";
import AlertModal from "../components/AlertModal";
import { useNavigate } from "react-router-dom";
import KanbanBoard from '../components/KanbanBoard';

const IFRAME_SRC =
  'https://v2-embednotion.com/theffs/Plataforma-de-Gesti-n-de-Tareas-Colaborativas-12e3386028bd8066a3afe385ed758696?p=12e3386028bd81b48459d62eba3036a4&pm=s';


function Home() {
  const [isVisible, setIsVisible] = useState(true);
  const navigate = useNavigate();

  const onAccept = () => {
    setIsVisible(false);
  };
  const onCancel = () => {
    setIsVisible(false);

    localStorage.removeItem("username");
    localStorage.removeItem("githubUrl");

    navigate("/");
  };

  return (
    <div className="min-h-screen bg-primary p-8">
      {isVisible && <AlertModal onAccept={onAccept} onCancel={onCancel} />}

      {/* <iframe
        src={IFRAME_SRC}
        className="w-full min-h-screen"
        title="Home Content"
      /> */}

      <div className="min-h-screen bg-primary p-8">
        <KanbanBoard />
      </div>
    </div>
  );
}

export default Home;
