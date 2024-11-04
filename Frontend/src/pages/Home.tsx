// src/pages/Home.tsx
import { useContext, useState } from 'react';
import { FaCheck, FaDiscord, FaTrashAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import PullRequestModal from '../components/PullRequestModal';
import AuthContext from '../contexts/AuthContext';
import { unassign, updatePbiStatus } from '../services/api';

function Home() {
  const [isPullRequestModalVisible, setIsPullRequestModalVisible] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  const { username, pbiId, iframeUrl, projectData } = authContext || {};

  const handleComplete = () => {
    setIsPullRequestModalVisible(true);
  };

  const handlePullRequestSubmit = async (link: string) => {
    if (pbiId) {
      try {
        await updatePbiStatus({ pbiId, status: 'in review', urlPR: link });
        setIsPullRequestModalVisible(false);
      } catch (error) {
        console.error('Error submitting pull request link:', error);
      }
    } else {
      console.error('pbiId is not available in the auth context');
    }
  };

  const handlePullRequestCancel = () => {
    setIsPullRequestModalVisible(false);
  };

  const handleAbandon = async () => {
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
    <div className="min-h-screen bg-primary p-8 relative">

      {isPullRequestModalVisible && (
        <PullRequestModal
          onSubmit={handlePullRequestSubmit}
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
        href='https://discord.gg/CzHWvWUTdP'
        className="absolute top-4 left-8 bg-blue-400 text-white px-4 py-2 rounded hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 flex items-center whitespace-nowrap"
        target='_blank'
      >
        <FaDiscord className="mr-2" />
        Ir a la comunidad de {projectData?.projectName}
      </a>

      <button
        onClick={handleComplete}
        className="absolute top-4 right-8 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center whitespace-nowrap"
      >
        <FaCheck className="mr-2" />
        Adjuntar Pull Request Link
      </button>

      <div className="mx-auto mt-10 mb-10">
        <iframe
          src={iframeUrl}
          className="w-full min-h-screen relative z-10"
          title="Home Content"
        />
      </div>

      <button
        onClick={handleAbandon}
        className="absolute bottom-4 left-8 border-2 border-red-500 text-white px-4 py-2 rounded hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-red-400 flex items-center whitespace-nowrap"
      >
        <FaTrashAlt className="mr-2" />
        Abandonar Proyecto
      </button>
    </div>
  );
}

export default Home;
