// src/providers/AuthProvider.tsx
import { useState, ReactNode } from 'react';
import AuthContext, { AuthContextType } from '../contexts/AuthContext';

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);


  const login = (username: string, githubUrl: string) => {
    localStorage.setItem('username', username);
    localStorage.setItem('githubUrl', githubUrl);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('githubUrl');
    setIsAuthenticated(false);
  };

  const authContextValue: AuthContextType = {
    isAuthenticated,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
