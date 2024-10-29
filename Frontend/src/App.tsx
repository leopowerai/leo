import LoginForm from './components/LoginForm';
import PlatziLeo from './assets/LeoPlatzi.svg';
import './App.css'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
      <div className="mb-4 w-60 h-auto mx-auto">
        <img src={PlatziLeo} alt="Platzi Logo" className="w-full h-auto" />
      </div>
      <LoginForm />
    </div>
  );
}

export default App
