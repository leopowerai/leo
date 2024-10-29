import { useState } from "react";
import AlertModal from "../components/AlertModal";
import { useNavigate } from "react-router-dom";

function Home() {
  const [isVisible, setIsVisible] = useState(true);
  const navigate = useNavigate();
  
  const onAccept = () => {
    setIsVisible(false);
  };
  const onCancel = () => {
    setIsVisible(false);
    navigate('/');
  };

    return (
      <div className="min-h-screen bg-primary p-8">
        {isVisible && <AlertModal onAccept={onAccept} onCancel = {onCancel}/>}
        <div className="text-white">Hola</div>
        
      </div>
    );
  }
  
  export default Home;