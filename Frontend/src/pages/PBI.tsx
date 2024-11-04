import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import AuthContext from '../contexts/AuthContext';

function PBI() {

    const navigate = useNavigate();
    const authContext = useContext(AuthContext);
    const { projectData, username, pbiId } = authContext || {};

    const onClick = () => {
        navigate('/home');
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full bg-primary">
            <h1 className='fond-bold text-xl text-white mb-4 mt-4 '>Selecciona la tarea que más te guste</h1>
            {projectData && (
                <div>
                    {projectData.suggestedPbis.map(pbi => (
                        <Card onClick={onClick} title={pbi.pbiTitle} description={pbi.pbiDescription} />
                    ))}
                </div>
            )
            }
        </div>
    );
}

export default PBI;