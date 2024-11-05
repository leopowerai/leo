// src/components/LoadingIndicator.tsx
import React from 'react';
import Leo from '/LEO loader.svg';

interface LoadingIndicatorProps {
    message: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ message }) => {
    return (
        <div className="flex flex-col items-center">
            <img src={Leo} alt="Loading..." className="w-28 h-28 slow-spin" />
            <p className="text-white text-sm mt-1 text-center loader-dots">{message}</p>
        </div>
    );
};

export default LoadingIndicator;
