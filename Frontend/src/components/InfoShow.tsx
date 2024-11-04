interface InfoShowProps {
    title: string;
    content: string;
    cta: string;
    onAccept: () => void;
    onCancel: () => void;
}

const InfoShow: React.FC<InfoShowProps> = ({ title, content, cta, onAccept, onCancel }) => {
    return (
        <div className="w-96 text-center">
            <h2 className="text-xl font-semibold mb-4">{title}</h2>
            <p className="text-justify mb-6">
                {content}
            </p>
            <p className="text-justify mb-6">
                {cta}
            </p>
            <div className="flex justify-between mt-6 gap-4">
                <button
                    onClick={onCancel}
                    className="w-32 py-3 bg-gray-200 text-black rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
                >
                    Cancelar
                </button>
                <button
                    onClick={onAccept}
                    className="w-32 py-3 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                    Aceptar
                </button>
            </div>
        </div>
    );
};

export default InfoShow;
