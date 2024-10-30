import { createContext } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (username: string, githubUrl: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export default AuthContext;
export type { AuthContextType };