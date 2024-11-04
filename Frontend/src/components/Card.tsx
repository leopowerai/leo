import React from 'react';

interface CardProps {
    onClick: () => void;
    title: string;
    description: string;
}

const Card: React.FC<CardProps> = ({ onClick, title, description }) => {
    return (
        <div
            onClick={onClick}
            className="flex mb-4 flex-col rounded-lg bg-white hover:bg-neutral-200 md:max-w-xl md:flex-row transition-all duration-300 ease-in-out cursor-pointer"
        >
            <div className="flex flex-col justify-start p-6">
                <h5 className="mb-2 text-xl font-medium text-neutral-800">
                    {title}
                </h5>
                <p className="mb-0 text-base text-neutral-600 overflow-hidden max-h-0 transition-all duration-300 ease-in-out hover:max-h-40">
                    {description}
                </p>
            </div>
        </div>
    );
};

export default Card;
