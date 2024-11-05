import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import InfoShow from '../components/InfoShow';
import AuthContext from '../contexts/AuthContext';

function Project() {

    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    const { projectData } = authContext || {};

    const onAccept = () => {
        navigate('/PBI');
    };

    const onCancel = async () => {
        authContext?.logout();
        navigate('/');
    };


    return (
        <div className="min-h-screen bg-primary p-8 flex items-center justify-center text-white">
            {projectData && (
                <InfoShow
                    title={projectData.projectName ?? ""}
                    content={projectData.projectBusinessContext + " " + projectData.projectTechnicalContext}
                    cta={"Hemos encontrado que tienes habilidades en " + projectData.projectSkills.join(', ') + ". ¿Te gustaría ser parte de este increible proyecto?"}
                    onAccept={onAccept}
                    onCancel={onCancel}
                />
            )}
        </div>
    );
}

export default Project;
