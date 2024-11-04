import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import InfoShow from '../components/InfoShow';
import AuthContext from '../contexts/AuthContext';
import { unassign } from '../services/api';

function PBI() {

    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    const { projectData, username, pbiId } = authContext || {};

    const onAccept = () => {
        navigate('/home');
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
                    title={projectData.pbiTitle ?? ""}
                    content={projectData.pbiDescription ?? ""}
                    cta={"Creemos que esta PBI es ideal para ti. ¿Aceptas esta misión?"}
                    onAccept={onAccept}
                    onCancel={onCancel}
                />
            )}
        </div>
    );
}

export default PBI;