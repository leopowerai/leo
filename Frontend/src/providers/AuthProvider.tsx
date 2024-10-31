// src/providers/AuthProvider.tsx
import { useState, ReactNode } from 'react';
import AuthContext, { AuthContextType } from '../contexts/AuthContext';

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");


  const login = (username: string, githubUrl: string) => {
    localStorage.setItem('username', username);
    localStorage.setItem('githubUrl', githubUrl);
    setIsAuthenticated(true);
    setUsername(username);
  };

  const logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('githubUrl');
    setIsAuthenticated(false);
    setUsername("");
  };


  const authContextValue: AuthContextType = {
    isAuthenticated,
    username,
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
