import React from 'react';
import Draggable from 'react-draggable';

interface AlertModalProps {
  onAccept: () => void;
  onCancel: () => void;
}

const AlertModal: React.FC<AlertModalProps> = ({ onAccept, onCancel }) => {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-20 flex items-center justify-center z-50"
      role="dialog"
      aria-modal="true"
    >
      <Draggable>
        <div className="bg-white p-6 rounded shadow-lg w-96 text-center">
          <h2 className="text-xl font-semibold mb-4">¿Aceptas tu misión?</h2>
          <div className="flex justify-between mt-6">
            <button
              onClick={onCancel}
              className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
            >
              Cancelar
            </button>
            <button
              onClick={onAccept}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
            >
              Aceptar
            </button>
          </div>
        </div>
      </Draggable>
    </div>
  );
};

export default AlertModal;
