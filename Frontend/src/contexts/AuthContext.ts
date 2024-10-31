// src/contexts/AuthContext.ts
import { createContext } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  username: string;
  pbiId: string;
  iframeUrl: string;
  login: (username: string, pbiId: string, iframeUrl: string) => void;
  logout: () => void;
  updatePbi: (pbiId: string, iframeUrl: string) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export default AuthContext;
export type { AuthContextType };
