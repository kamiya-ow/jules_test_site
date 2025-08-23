'use client';

import { useState, useEffect } from 'react';

// Define the type for a task
type Task = {
  id: number;
  text: string;
  completed: boolean;
};

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskText, setNewTaskText] = useState('');
  const [isClient, setIsClient] = useState(false); // To prevent hydration mismatch

  // Effect to set isClient to true once the component mounts
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Effect to load tasks from localStorage
  useEffect(() => {
    if (isClient) {
      try {
        const savedTasks = localStorage.getItem('tasks');
        if (savedTasks) {
          setTasks(JSON.parse(savedTasks));
        }
      } catch (error) {
        console.error('Failed to parse tasks from localStorage', error);
      }
    }
  }, [isClient]);

  // Effect to save tasks to localStorage
  useEffect(() => {
    // Only save tasks if it's the client and tasks have been loaded
    if (isClient) {
      localStorage.setItem('tasks', JSON.stringify(tasks));
    }
  }, [tasks, isClient]);

  // Handler to add a new task
  const handleAddTask = () => {
    if (newTaskText.trim() === '') {
      alert('タスクを入力してください。');
      return;
    }
    const newTask: Task = {
      id: Date.now(),
      text: newTaskText.trim(),
      completed: false,
    };
    setTasks([...tasks, newTask]);
    setNewTaskText('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleAddTask();
    }
  };

  const handleToggleComplete = (id: number) => {
    setTasks(
      tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const handleDeleteTask = (id: number) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  return (
    <main className="min-h-screen flex flex-col items-center pt-10">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-center text-2xl font-bold text-gray-700 mb-5">
          タスク管理ツール
        </h1>
        <div className="flex mb-5">
          <input
            type="text"
            value={newTaskText}
            onChange={(e) => setNewTaskText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="新しいタスクを入力"
            className="flex-1 p-2 border-2 border-gray-300 rounded text-base focus:outline-none focus:border-blue-500 transition-colors"
          />
          <button
            onClick={handleAddTask}
            className="p-2 px-4 bg-blue-500 text-white rounded text-base cursor-pointer ml-2 hover:bg-blue-700 transition-colors"
          >
            追加
          </button>
        </div>
        <ul className="list-none p-0 m-0">
          {isClient && tasks.map(task => (
            <li
              key={task.id}
              className={`p-3 rounded mb-2 flex justify-between items-center transition-colors ${
                task.completed ? 'bg-gray-200 text-gray-500' : 'bg-gray-50'
              }`}
            >
              <span
                onClick={() => handleToggleComplete(task.id)}
                className={`cursor-pointer flex-grow ${
                  task.completed ? 'line-through' : ''
                }`}
              >
                {task.text}
              </span>
              <button
                onClick={() => handleDeleteTask(task.id)}
                className="bg-red-500 text-white border-none p-1 px-2 rounded cursor-pointer text-xs hover:bg-red-700 transition-colors"
              >
                削除
              </button>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
