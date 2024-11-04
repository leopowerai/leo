// src/App.tsx
import React from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import AuthContext from './contexts/AuthContext';
import Company from './pages/Company';
import Home from './pages/Home';
import LoginForm from './pages/LoginForm';
import PBI from './pages/PBI';
import Project from './pages/Project';
import AuthProvider from './providers/AuthProvider';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <PublicRoute>
                <LoginForm />
              </PublicRoute>
            }
          />
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          <Route
            path="/company"
            element={
              <PrivateRoute>
                <Company />
              </PrivateRoute>
            }
          />
          <Route
            path="/project"
            element={
              <PrivateRoute>
                <Project />
              </PrivateRoute>
            }
          />
          <Route
            path="/pbi"
            element={
              <PrivateRoute>
                <PBI />
              </PrivateRoute>
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
