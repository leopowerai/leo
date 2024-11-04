import React, { useState } from 'react';

interface CardProps {
    onClick: () => void;
    title: string;
    description: string;
}

const Card: React.FC<CardProps> = ({ onClick, title, description }) => {
    const [hovered, setHovered] = useState(false);

    return (
        <div
            onClick={onClick}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            className="flex mb-4 flex-col rounded-lg bg-white hover:bg-neutral-200 md:max-w-xl md:flex-row transition-all duration-300 ease-in-out cursor-pointer"
        >
            <div className="flex flex-col justify-start p-6">
                <h5 className="mb-2 text-xl font-medium text-neutral-800">
                    {title}
                </h5>
                <div
                    className={`transition-max-height duration-500 ease-in-out overflow-hidden ${hovered ? 'max-h-40' : 'max-h-0'
                        }`}
                >
                    <p className="text-base text-neutral-600">
                        {description}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Card;
