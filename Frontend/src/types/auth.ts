// src/types/auth.ts
export interface PBIData {
    pbiId: string;
    pbiTitle: string;
    pbiDescription: string;
    pbiSkills: string[];
}

export interface ProjectData {
    projectId: string;
    projectName: string;
    projectSkills: string[];
    projectBusinessContext: string;
    projectTechnicalContext: string;
    companyName: string;
    companyContext: string;
    suggestedPbis: PBIData[];
}

export interface AuthContextType {
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
