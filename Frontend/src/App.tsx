import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './pages/LoginForm';
import Home from './pages/Home';
import './App.css'

function App() {
  const hasUserData = () => localStorage.getItem('username') && localStorage.getItem('githubUrl');

  return (
    <Router>
      <Routes>
        <Route path="/" element={hasUserData() ? <Navigate to="/home" /> : <LoginForm />}/>
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;