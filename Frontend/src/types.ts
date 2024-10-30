// src/types.ts
export interface Task {
    id: string;
    title: string;
    description?: string;
  }
  
  export interface Column {
    id: string;
    title: string;
    tasks: Task[];
  }
  