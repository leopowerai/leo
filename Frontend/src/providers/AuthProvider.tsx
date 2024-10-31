// src/providers/AuthProvider.tsx
import { useState, ReactNode } from 'react';
import AuthContext, { AuthContextType } from '../contexts/AuthContext';

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");
  const [pbiId, setPbiId] = useState<string>("");


  const login = (username: string, pbiId: string) => {
    localStorage.setItem('username', username);
    localStorage.setItem('pbiId', pbiId);
    setIsAuthenticated(true);
    setUsername(username);
    setPbiId(pbiId);
  };

  const logout = () => {
    localStorage.removeItem('username');
    setIsAuthenticated(false);
    setUsername("");
    setPbiId("");
  };


  const authContextValue: AuthContextType = {
    isAuthenticated,
    username,
    pbiId,
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
