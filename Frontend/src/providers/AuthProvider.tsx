// src/providers/AuthProvider.tsx
import  { useState, useEffect, ReactNode } from 'react';
import AuthContext, { AuthContextType } from '../contexts/AuthContext';

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [username, setUsername] = useState<string>('');
  const [pbiId, setPbiId] = useState<string>('');
  const [iframeUrl, setIframeUrl] = useState<string>('');

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    const storedPbiId = localStorage.getItem('pbiId');
    const storedIframeUrl = localStorage.getItem('iframeUrl');
    if (storedUsername && storedPbiId && storedIframeUrl) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
      setPbiId(storedPbiId);
      setIframeUrl(storedIframeUrl);
    }
  }, []);

  const login = (username: string, pbiId: string, iframeUrl: string) => {
    localStorage.setItem('username', username);
    localStorage.setItem('pbiId', pbiId);
    localStorage.setItem('iframeUrl', iframeUrl);
    setIsAuthenticated(true);
    setUsername(username);
    setPbiId(pbiId);
    setIframeUrl(iframeUrl);
  };

  const logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('pbiId');
    localStorage.removeItem('iframeUrl');
    setIsAuthenticated(false);
    setUsername('');
    setPbiId('');
    setIframeUrl('');
  };

  const updatePbi = (pbiId: string, iframeUrl: string) => {
    localStorage.setItem('pbiId', pbiId);
    localStorage.setItem('iframeUrl', iframeUrl);
    setPbiId(pbiId);
    setIframeUrl(iframeUrl);
  };

  const authContextValue: AuthContextType = {
    isAuthenticated,
    username,
    pbiId,
    iframeUrl,
    login,
    logout,
    updatePbi,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
