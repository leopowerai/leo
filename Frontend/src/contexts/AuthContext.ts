import { createContext } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  username: string;
  pbiId: string;
  login: (username: string, pbiId: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export default AuthContext;
export type { AuthContextType };
