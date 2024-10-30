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
          <Route path="/" element={<LoginForm />} />
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          {/* Add any other routes here */}
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

export default App;
