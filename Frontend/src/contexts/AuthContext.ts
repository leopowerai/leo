// src/contexts/AuthContext.ts
import { createContext } from 'react';

interface PBIData {
  pbiId: string;
  pbiTitle: string;
  pbiDescription: string;
  pbiSkills: string[];
}

interface ProjectData {
  projectId: string;
  projectName: string;
  projectSkills: string[];
  projectBusinessContext: string;
  projectTechnicalContext: string;
  companyName: string;
  companyContext: string;
  suggestedPbis: PBIData[];
}

interface AuthContextType {
  isAuthenticated: boolean;
  username: string;
  pbiId: string;
  iframeUrl: string;
  projectData: ProjectData | null;
  login: (
    username: string,
    pbiId: string,
    iframeUrl: string,
    projectData?: ProjectData
  ) => void;
  logout: () => void;
  updatePbi: (pbiId: string, iframeUrl: string) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export default AuthContext;
export type { AuthContextType, ProjectData };
