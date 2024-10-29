import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

const LoginForm = React.lazy(() => import('./pages/LoginForm'));
const Home = React.lazy(() => import('./pages/Home'));

function App() {
  const hasUserData = () => localStorage.getItem('username') && localStorage.getItem('githubUrl');

  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}></Suspense>
      <Routes>
        <Route path="/" element={hasUserData() ? <Navigate to="/home" /> : <LoginForm />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
