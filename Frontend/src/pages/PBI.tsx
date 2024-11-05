import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import AuthContext from '../contexts/AuthContext';
import { assign } from '../services/api';

function PBI() {
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    const [loading, setLoading] = useState(false);

    if (!authContext) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary p-4 text-center text-xl text-white font-bold">
                Cargando...
            </div>
        );
    }

    const { projectData, username, updatePbi } = authContext;

    const onClick = async (pbiId: string) => {
        if (username) {
            try {
                setLoading(true);
                const response = await assign({ username, pbiId });
                updatePbi(pbiId, response.iframeUrl);
                navigate('/home');
            } catch (error) {
                console.error('Error al asignar PBI:', error);
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div
            className={`flex flex-col items-center justify-center min-h-screen w-full bg-primary p-4 ${loading ? 'cursor-wait' : 'cursor-default'
                }`}
        >

            <h1 className="font-bold text-xl text-white mb-8 mt-4">
                Selecciona la tarea que más te guste
            </h1>
            {projectData ? (
                <div className="grid grid-cols-1 gap-6">
                    {projectData.suggestedPbis.map((pbi) => (
                        <Card
                            key={pbi.pbiId}
                            onClick={!loading ? () => onClick(pbi.pbiId) : () => { }}
                            title={pbi.pbiTitle}
                            description={pbi.pbiDescription}
                            badges={pbi.pbiSkills}
                        />
                    ))}
                </div>
            ) : (
                <p className="text-white text-lg">Cargando proyectos...</p>
            )}
        </div>
    );
}

export default PBI;
