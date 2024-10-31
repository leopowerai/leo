// src/components/PullRequestModal.tsx
import React, { useState } from 'react';
import Draggable from 'react-draggable';

interface PullRequestModalProps {
  onSubmit: (link: string) => void;
  onCancel: () => void;
}

const PullRequestModal: React.FC<PullRequestModalProps> = ({ onSubmit, onCancel }) => {
  const [link, setLink] = useState('');

  const handleSubmit = () => {
    const githubPRRegex = /^https:\/\/github\.com\/.+\/.+\/pull\/\d+$/;
    if (!githubPRRegex.test(link)) {
      alert('Por favor, ingresa un enlace válido de Pull Request de GitHub.');
      return;
    }
    onSubmit(link);
    setLink('');
  };
  

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-20 flex items-center justify-center z-50"
      role="dialog"
      aria-modal="true"
    >
      <Draggable>
        <div className="bg-white p-6 rounded shadow-lg w-96 text-center">
          <h2 className="text-xl font-semibold mb-4">Adjuntar Pull Request Link</h2>
          <input
            type="url"
            value={link}
            onChange={(e) => setLink(e.target.value)}
            placeholder="https://github.com/usuario/repositorio/pull/123"
            className="w-full p-2 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          <div className="flex justify-between mt-6">
            <button
              onClick={onCancel}
              className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
            >
              Cancelar
            </button>
            <button
              onClick={handleSubmit}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
            >
              Enviar
            </button>
          </div>
        </div>
      </Draggable>
    </div>
  );
};

export default PullRequestModal;
