import { useState } from "react";
import { FaCheck , FaTrashAlt } from 'react-icons/fa';
import AlertModal from "../components/AlertModal";
import { useNavigate } from "react-router-dom";
//import KanbanBoard from '../components/KanbanBoard';

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
    <div className="min-h-screen bg-primary p-8 relative">


      {isVisible && <AlertModal onAccept={onAccept} onCancel={onCancel} />}

      <button
  className="absolute top-4 right-8 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center whitespace-nowrap"
>
<FaCheck className="mr-2"/>
  Marcar como completado
</button>

<div className=" mx-auto mt-10 mb-10">
<iframe
  src={IFRAME_SRC}
  className="w-full min-h-screen relative z-10"
  title="Home Content"
/>
</div>

      {/*<div className="min-h-screen bg-primary p-8">
        <KanbanBoard />
      </div>*/}
      <button
  className="absolute bottom-4 left-8 border-2 border-red-500 text-white px-4 py-2 rounded hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center whitespace-nowrap"
>
<FaTrashAlt className="mr-2"/>
  Abandonar Proyecto
</button>
    </div>
  );
}

export default Home;
