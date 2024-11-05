// src/App.tsx
import React, { Suspense } from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import AuthProvider from './providers/AuthProvider';
import PrivateRoute from './routes/PrivateRoute';
import PublicRoute from './routes/PublicRoute';

// Lazy load pages for better performance
const LoginForm = React.lazy(() => import('./pages/LoginForm'));
const Home = React.lazy(() => import('./pages/Home'));
const PBI = React.lazy(() => import('./pages/PBI'));
const InfoPage = React.lazy(() => import('./pages/InfoPage'));

function App() {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<div className="text-white">Cargando...</div>}>
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
                  <InfoPage type="company" />
                </PrivateRoute>
              }
            />
            <Route
              path="/project"
              element={
                <PrivateRoute>
                  <InfoPage type="project" />
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
        </Suspense>
      </Router>
    </AuthProvider>
  );
}

export default App;
