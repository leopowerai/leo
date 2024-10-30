// src/AuthContext.tsx
import React, { createContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
    isAuthenticated: boolean;
    login: (username: string, githubUrl: string) => void;
    logout: () => void;
  }
  
  export const AuthContext = createContext<AuthContextType | null>(null);
  
  interface AuthProviderProps {
    children: ReactNode;
  }

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    const user = localStorage.getItem('username');
    const githubUrl = localStorage.getItem('githubUrl');
    setIsAuthenticated(!!(user && githubUrl));
  }, []);

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

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
