import LoginForm from './pages/LoginForm';
import PlatziLeo from './assets/PlatziLeo.svg';
import './App.css'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
      <div className=" w-60 h-auto mx-auto">
        <img src={PlatziLeo} alt="Platzi Logo"  />
      </div>
      <LoginForm />
    </div>
  );
}

export default App
