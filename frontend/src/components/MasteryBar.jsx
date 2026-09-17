import React from 'react';

export default function MasteryBar({ score }) {
  const getBarColor = () => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="flex items-center gap-3 w-full">
      <div className="flex-1 bg-gray-200 rounded-full h-2.5">
        <div className={`h-2.5 rounded-full ${getBarColor()}`} style={{ width: `${score}%` }}></div>
      </div>
      <span className="text-sm font-medium text-gray-700">{Math.round(score)}%</span>
    </div>
  );
}
