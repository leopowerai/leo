import React, { useState, useEffect } from 'react';
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import KanbanColumn from './KanbanColumn';
import { Column } from '../types';

const initialColumnsData: Column[] = [
  {
    id: 'todo',
    title: 'To Do',
    tasks: [
      { id: 'task-1', title: 'Task 1' },
      { id: 'task-2', title: 'Task 2' },
    ],
  },
  {
    id: 'in-progress',
    title: 'In Progress',
    tasks: [],
  },
  {
    id: 'done',
    title: 'Done',
    tasks: [],
  },
];

const KanbanBoard: React.FC = () => {
  const [columns, setColumns] = useState<Column[]>(() => {
    const storedColumns = localStorage.getItem('columns');
    return storedColumns ? JSON.parse(storedColumns) : initialColumnsData;
  });

  useEffect(() => {
    localStorage.setItem('columns', JSON.stringify(columns));
  }, [columns]);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over) return;

    const sourceTaskId = active.id; // task.id
    const destinationColumnId = over.id; // column.id

    if (!sourceTaskId || !destinationColumnId) return;

    setColumns((prevColumns) => {
      let sourceColumnIndex = -1;
      let taskIndex = -1;

      // Find the source column and task index
      for (let i = 0; i < prevColumns.length; i++) {
        const tasks = prevColumns[i].tasks;
        const index = tasks.findIndex((t) => t.id === sourceTaskId);
        if (index !== -1) {
          sourceColumnIndex = i;
          taskIndex = index;
          break;
        }
      }

      if (sourceColumnIndex === -1 || taskIndex === -1) return prevColumns;

      const sourceColumn = prevColumns[sourceColumnIndex];
      const task = sourceColumn.tasks[taskIndex];

      // Remove task from source column
      sourceColumn.tasks.splice(taskIndex, 1);

      // Add task to destination column
      const destinationColumn = prevColumns.find((col) => col.id === destinationColumnId);
      if (destinationColumn) {
        destinationColumn.tasks.unshift(task);
      }

      return [...prevColumns];
    });
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <div className="flex space-x-4 p-4">
        {columns.map((column) => (
          <KanbanColumn key={column.id} column={column} />
        ))}
      </div>
    </DndContext>
  );
};

export default KanbanBoard;
