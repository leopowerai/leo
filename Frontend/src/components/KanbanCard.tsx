// src/components/KanbanCard.tsx
import React from 'react';
import { Task } from '../types';
import { useDraggable } from '@dnd-kit/core';

interface KanbanCardProps {
  task: Task;
  columnId: string;
}

const KanbanCard: React.FC<KanbanCardProps> = ({ task, columnId }) => {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: `${columnId}-${task.id}`,
  });

  const style = {
    transform: transform ? `translate(${transform.x}px, ${transform.y}px)` : undefined,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="bg-white p-4 rounded shadow cursor-pointer"
    >
      <h3 className="font-semibold">{task.title}</h3>
      {task.description && <p className="text-sm text-gray-600">{task.description}</p>}
    </div>
  );
};

export default KanbanCard;
