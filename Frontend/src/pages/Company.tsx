import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import InfoShow from '../components/InfoShow';
import AuthContext from '../contexts/AuthContext';



function Company() {
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);

    if (!authContext || !authContext.projectData) {
        navigate('/');
    }

    const { projectData } = authContext || {};

    const onAccept = async () => {
        navigate('/project');
    };


    const onCancel = async () => {
        authContext?.logout();
        navigate('/');
    };

    return (
        <div className="min-h-screen bg-primary p-8 flex items-center justify-center text-white">
            {projectData && (
                <InfoShow
                    title={projectData.companyName ?? ""}
                    content={projectData.companyContext ?? ""}
                    cta={"¿Te gustaría hacer parte de nuestro equipo?"}
                    onAccept={onAccept}
                    onCancel={onCancel}
                />
            )}
        </div>
    );
}

export default Company;
