// src/providers/AuthProvider.tsx
import { ReactNode, useEffect, useState } from 'react';
import AuthContext, { AuthContextType, ProjectData } from '../contexts/AuthContext';

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [username, setUsername] = useState<string>('');
  const [pbiId, setPbiId] = useState<string>('');
  const [iframeUrl, setIframeUrl] = useState<string>('');
  const [projectData, setProjectData] = useState<ProjectData | null>(null);

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    const storedPbiId = localStorage.getItem('pbiId');
    const storedIframeUrl = localStorage.getItem('iframeUrl');
    const storedProjectData = localStorage.getItem('projectData');

    if (storedUsername && storedPbiId && storedIframeUrl && storedProjectData) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
      setPbiId(storedPbiId);
      setIframeUrl(storedIframeUrl);
      setProjectData(JSON.parse(storedProjectData));
    }
  }, []);

  const login = (
    username: string,
    pbiId: string,
    iframeUrl: string,
    projectData?: ProjectData
  ) => {
    localStorage.setItem('username', username);
    localStorage.setItem('pbiId', pbiId);
    localStorage.setItem('iframeUrl', iframeUrl);
    localStorage.setItem('projectData', JSON.stringify(projectData));
    setIsAuthenticated(true);
    setUsername(username);
    setPbiId(pbiId);
    setIframeUrl(iframeUrl);
    setProjectData(projectData || null);
  };


  const logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('pbiId');
    localStorage.removeItem('iframeUrl');
    localStorage.removeItem('projectData');
    setIsAuthenticated(false);
    setUsername('');
    setPbiId('');
    setIframeUrl('');
    setProjectData(null);
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
    projectData,
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
