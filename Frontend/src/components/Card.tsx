import React, { useState } from 'react';

interface CardProps {
    onClick: () => void;
    title: string;
    description: string;
    badges: string[];
}

const Card: React.FC<CardProps> = ({ onClick, title, description, badges }) => {
    const [hovered, setHovered] = useState(false);

    return (
        <div
            onClick={onClick}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            className="flex flex-col rounded-lg bg-white hover:bg-neutral-200 md:max-w-xl md:flex-row transition-all duration-300 ease-in-out cursor-pointer"
        >
            <div className="flex flex-col justify-start p-6">
                <h5 className="mb-2 text-xl font-medium text-neutral-800">
                    {title}
                </h5>
                <div className='inline-flex'>
                    {badges.map(badge => (
                        <span className=" items-center gap-x-1.5 py-1.5 px-3 mr-2 rounded-full text-xs font-medium border border-gray-500 text-gray-500 ">{badge}</span>
                    ))}

                </div>
                <div className={`transition-max-height duration-500 ease-in-out overflow-hidden ${hovered ? 'max-h-40' : 'max-h-0'
                    }`}
                >
                    <p className="text-base text-neutral-600 mt-2">
                        {description}
                    </p>

                </div>
            </div>
        </div>
    );
};

export default Card;
