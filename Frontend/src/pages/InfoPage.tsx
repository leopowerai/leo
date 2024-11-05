// src/pages/InfoPage.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import InfoShow from '../components/InfoShow';
import useAuth from '../hooks/useAuth';

interface InfoPageProps {
    type: 'company' | 'project';
}

const InfoPage: React.FC<InfoPageProps> = ({ type }) => {
    const navigate = useNavigate();
    const { projectData, logout } = useAuth();

    React.useEffect(() => {
        if (!projectData) {
            navigate('/');
        }
    }, [projectData, navigate]);

    if (!projectData) {
        return null;
    }

    const onAccept = () => {
        navigate(type === 'company' ? '/project' : '/pbi');
    };

    const onCancel = () => {
        logout();
        navigate('/');
    };

    const title = type === 'company' ? projectData.companyName : projectData.projectName;
    const content =
        type === 'company'
            ? projectData.companyContext
            : `${projectData.projectBusinessContext} ${projectData.projectTechnicalContext}`;
    const cta =
        type === 'company'
            ? '¿Te gustaría hacer parte de nuestro equipo?'
            : `Hemos encontrado que tienes habilidades en ${projectData.projectSkills.join(
                ', '
            )}. ¿Te gustaría ser parte de este increíble proyecto?`;

    return (
        <div className="min-h-screen bg-primary p-8 flex items-center justify-center text-white">
            <InfoShow title={title} content={content} cta={cta} onAccept={onAccept} onCancel={onCancel} />
        </div>
    );
};

export default InfoPage;
