import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './pages/LoginForm';
import Home from './pages/Home';
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />}/>
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;