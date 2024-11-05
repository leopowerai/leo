// src/providers/AuthProvider.tsx
import { ReactNode, useEffect, useState } from 'react';
import AuthContext from '../contexts/AuthContext';
import { AuthContextType, ProjectData } from '../types/auth';

const LOCAL_STORAGE_KEYS = {
  USERNAME: 'username',
  PBI_ID: 'pbiId',
  IFRAME_URL: 'iframeUrl',
  PROJECT_DATA: 'projectData',
};

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
    const storedUsername = localStorage.getItem(LOCAL_STORAGE_KEYS.USERNAME);
    const storedPbiId = localStorage.getItem(LOCAL_STORAGE_KEYS.PBI_ID);
    const storedIframeUrl = localStorage.getItem(LOCAL_STORAGE_KEYS.IFRAME_URL);
    const storedProjectData = localStorage.getItem(LOCAL_STORAGE_KEYS.PROJECT_DATA);

    if (storedUsername && storedPbiId && storedIframeUrl) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
      setPbiId(storedPbiId);
      setIframeUrl(storedIframeUrl);
      setProjectData(storedProjectData ? JSON.parse(storedProjectData) : null);
    }
  }, []);

  const login = (
    username: string,
    pbiId: string,
    iframeUrl: string,
    projectData?: ProjectData
  ) => {
    localStorage.setItem(LOCAL_STORAGE_KEYS.USERNAME, username);
    localStorage.setItem(LOCAL_STORAGE_KEYS.PBI_ID, pbiId);
    localStorage.setItem(LOCAL_STORAGE_KEYS.IFRAME_URL, iframeUrl);
    if (projectData) {
      localStorage.setItem(LOCAL_STORAGE_KEYS.PROJECT_DATA, JSON.stringify(projectData));
    } else {
      localStorage.removeItem(LOCAL_STORAGE_KEYS.PROJECT_DATA);
    }
    setIsAuthenticated(true);
    setUsername(username);
    setPbiId(pbiId);
    setIframeUrl(iframeUrl);
    setProjectData(projectData || null);
  };

  const logout = () => {
    Object.values(LOCAL_STORAGE_KEYS).forEach((key) => localStorage.removeItem(key));
    setIsAuthenticated(false);
    setUsername('');
    setPbiId('');
    setIframeUrl('');
    setProjectData(null);
  };

  const updatePbi = (pbiId: string, iframeUrl: string) => {
    localStorage.setItem(LOCAL_STORAGE_KEYS.PBI_ID, pbiId);
    localStorage.setItem(LOCAL_STORAGE_KEYS.IFRAME_URL, iframeUrl);
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

  return <AuthContext.Provider value={authContextValue}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
