// src/pages/Home.tsx
import { useContext, useState } from 'react';
import { FaCheck, FaTrashAlt, FaWhatsapp } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import PullRequestModal from '../components/PullRequestModal';
import AuthContext from '../contexts/AuthContext';
import { unassign, updatePbiStatus } from '../services/api';

function Home() {
  const [isPullRequestModalVisible, setIsPullRequestModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  const { username, pbiId, iframeUrl } = authContext || {};

  const handleComplete = () => {
    setIsPullRequestModalVisible(true);
  };

  const handlePullRequestSubmit = async (link: string) => {
    if (pbiId) {
      try {
        setLoading(true);
        await updatePbiStatus({ pbiId, status: 'in review', urlPR: link });
        setIsPullRequestModalVisible(false);
      } catch (error) {
        console.error('Error submitting pull request link:', error);
      }
      finally {
        setLoading(false);
      }
    } else {
      console.error('pbiId is not available in the auth context');
    }
  };

  const handlePullRequestCancel = () => {
    setIsPullRequestModalVisible(false);
  };

  const handleAbandon = async () => {
    console.log('clicked')
    if (username && pbiId) {
      try {
        setLoading(true);
        await unassign({ username, pbiId });
        authContext?.logout();
        navigate('/');
      } catch (error) {
        console.error('Error abandoning project:', error);
      }
      finally {
        setLoading(true);
      }
    } else {
      console.error('Username and pbiId are not available in the auth context');
    }
  };

  return (
    <div className={`min-h-screen bg-primary p-8 relative ${loading ? 'cursor-wait' : 'cursor-default'}`}>

      {isPullRequestModalVisible && (
        <PullRequestModal
          onSubmit={!loading ? () => handlePullRequestSubmit : () => { }}
          onCancel={handlePullRequestCancel}
        />
      )}

      {/* <button
        onClick={handleComplete}
        className="absolute top-4 right-72  border-gray-500 text-gray-400 px-4 py-2 rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 flex items-center whitespace-nowrap"
      >
        Ir al repositorio
      </button> */}

      <a
        href='https://chat.whatsapp.com/EXRWl1tuQ6b0e9uckUqcjw'
        className="absolute top-4 left-8 bg-green-400 text-white px-4 py-2 rounded hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center whitespace-nowrap"
        target='_blank'
      >
        <FaWhatsapp className="mr-2" />
        Ir a la comunidad del proyecto
      </a>

      <button
        onClick={handleComplete}
        className="absolute top-4 right-8 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 flex items-center whitespace-nowrap"
      >
        <FaCheck className="mr-2" />
        Adjuntar Resultados
      </button>

      <div className="mx-auto mt-10 mb-10">
        <iframe
          src={iframeUrl}
          className="w-full min-h-screen relative z-10"
          title="Home Content"
        />
      </div>

      <button
        onClick={!loading ? () => handleAbandon() : () => { }}
        className="absolute bottom-4 left-8 border-2 border-red-500 text-white px-4 py-2 rounded hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-red-400 flex items-center whitespace-nowrap"
      >
        <FaTrashAlt className="mr-2" />
        Abandonar Proyecto
      </button>
    </div>
  );
}

export default Home;
