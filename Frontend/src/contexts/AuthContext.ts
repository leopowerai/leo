// src/contexts/AuthContext.ts
import { createContext } from 'react';
import { AuthContextType } from '../types/auth';

const AuthContext = createContext<AuthContextType | null>(null);

export default AuthContext;
