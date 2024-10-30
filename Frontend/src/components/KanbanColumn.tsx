// src/components/KanbanColumn.tsx
import React from 'react';
import { Column } from '../types';
import KanbanCard from './KanbanCard';
import { useDroppable } from '@dnd-kit/core';

interface KanbanColumnProps {
  column: Column;
}

const KanbanColumn: React.FC<KanbanColumnProps> = ({ column }) => {
  const { setNodeRef } = useDroppable({
    id: `${column.id}-column`,
  });

  return (
    <div ref={setNodeRef} className="w-1/3 bg-secondary p-4 rounded">
      <h2 className="text-xl font-semibold text-white mb-4">{column.title}</h2>
      <div className="space-y-2">
        {column.tasks.map((task) => (
          <KanbanCard key={task.id} task={task} columnId={column.id} />
        ))}
      </div>
    </div>
  );
};

export default KanbanColumn;
