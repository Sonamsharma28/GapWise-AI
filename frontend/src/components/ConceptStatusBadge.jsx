import React from 'react';

export default function ConceptStatusBadge({ status }) {
  const getStatusConfig = () => {
    switch (status) {
      case 'mastered':
        return { text: 'Mastered', classes: 'bg-green-100 text-green-800' };
      case 'developing':
        return { text: 'Developing', classes: 'bg-yellow-100 text-yellow-800' };
      case 'needs_attention':
        return { text: 'Needs Attention', classes: 'bg-red-100 text-red-800' };
      default:
        return { text: 'Not Started', classes: 'bg-gray-100 text-gray-800' };
    }
  };
  const config = getStatusConfig();
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.classes}`}>
      {config.text}
    </span>
  );
}
