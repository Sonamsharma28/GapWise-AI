import React from 'react';

export default function EmptyState({ title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center bg-white rounded-xl shadow-sm border border-gray-100 min-h-[300px]">
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-6">{description}</p>
      {action && <div>{action}</div>}
    </div>
  );
}
