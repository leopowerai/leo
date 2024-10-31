// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthProvider from './providers/AuthProvider';
import AuthContext from './contexts/AuthContext';
import LoginForm from './pages/LoginForm';
import Home from './pages/Home';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          <Route
            path="/"
            element={
              <PublicRoute>
                <LoginForm />
              </PublicRoute>
            }
          />   
          <Route path="*" element={<Navigate to="/" />} />       
        </Routes>
      </Router>
    </AuthProvider>
  );
}

function PrivateRoute({ children }: { children: JSX.Element }) {
  const authContext = React.useContext(AuthContext);

  if (authContext === null) {
    // Render the loading spinner while loading
    return null;
  }

  return authContext.isAuthenticated ? children : <Navigate to="/" />;
}

function PublicRoute({ children }: { children: JSX.Element }) {
  const authContext = React.useContext(AuthContext);

  if (authContext === null) {
    // Render the loading spinner while loading
    return null;
  }

  return authContext.isAuthenticated ? <Navigate to="/home" /> : children;
}

export default App;
