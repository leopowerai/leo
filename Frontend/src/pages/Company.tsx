import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import InfoShow from '../components/InfoShow';
import AuthContext from '../contexts/AuthContext';
import { unassign } from '../services/api';



function Company() {
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);

    if (!authContext || !authContext.projectData) {
        navigate('/');
    }

    const { projectData, username, pbiId } = authContext || {};

    const onAccept = async () => {
        navigate('/project');
    };


    const onCancel = async () => {
        if (username && pbiId) {
            try {
                await unassign({ username, pbiId });
                authContext?.logout();
                navigate('/');
            } catch (error) {
                console.error('Error abandoning project:', error);
            }
        } else {
            console.error('Username and pbiId are not available in the auth context');
        }
    };

    return (
        <div className="min-h-screen bg-primary p-8 flex items-center justify-center text-white">
            {projectData && (
                <InfoShow
                    title={projectData.companyName ?? ""}
                    content={projectData.companyContext ?? ""}
                    cta={"¿Te gustaría hacer parte de nuestro equipo?" ?? ""}
                    onAccept={onAccept}
                    onCancel={onCancel}
                />
            )}
        </div>
    );
}

export default Company;
