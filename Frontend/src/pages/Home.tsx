// src/pages/Home.tsx
import { useState, useContext, useEffect } from 'react';
import AuthContext from '../contexts/AuthContext';
import { FaCheck, FaTrashAlt } from 'react-icons/fa';
import AlertModal from '../components/AlertModal';
import PullRequestModal from '../components/PullRequestModal';
import { useNavigate } from 'react-router-dom';
import { unassign, updatePbiStatus } from '../services/api';
import { isAssigned } from '../services/api';

function Home() {
  const [isAlertVisible, setIsAlertVisible] = useState(true);
  const [isPullRequestModalVisible, setIsPullRequestModalVisible] = useState(false);
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);

  const { username, pbiId, iframeUrl, logout, updatePbi } = authContext || {};

  useEffect(() => {
    const checkAssignment = async () => {
      if (username) {
        try {
          const response = await isAssigned(username);
          if (response.isAssigned) {
            setIsAlertVisible(false);
          } else {
            setIsAlertVisible(true);
          }
        } catch (error) {
          console.error('Error checking assignment:', error);
        }
      }
    };    checkAssignment();
  }, [username, pbiId, iframeUrl, updatePbi, logout, navigate]);

  const handleAccept = async () => {
    if (pbiId) {
      try {
        await updatePbiStatus({ pbiId, status: 'in progress'});
        setIsAlertVisible(false);
      } catch (error) {
        console.error('Error updating PBI status:', error);
      }
    } else {
      console.error('pbiId is not available in the auth context');
    }
  };

  const handleCancel = async () => {
    if (username && pbiId) {
      try {
        await unassign({ username, pbiId });
        authContext?.logout();
        navigate('/');
      } catch (error) {
        console.error('Error unassigning user:', error);
      }
    } else {
      console.error('Username and pbiId are not available in the auth context');
    }
  };

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
      {isAlertVisible && (
        <AlertModal onAccept={handleAccept} onCancel={handleCancel} />
      )}

      {isPullRequestModalVisible && (
        <PullRequestModal
          onSubmit={handlePullRequestSubmit}
          onCancel={handlePullRequestCancel}
        />
      )}

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
