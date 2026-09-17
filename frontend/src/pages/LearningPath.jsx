import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getPath } from '../api/learning';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import { Lock, Unlock, PlayCircle } from 'lucide-react';

export default function LearningPath() {
  const [path, setPath] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPath()
      .then(res => setPath(res.data.path || []))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;
  if (!path.length) return <div>Complete an assessment first to generate your path.</div>;

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-8 text-center">Your Personalized Learning Path</h1>
      <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-300 before:to-transparent">
        {path.map((step, idx) => (
          <div key={step.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
            <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-blue-100 text-blue-600 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
              {step.locked ? <Lock size={18} /> : <Unlock size={18} />}
            </div>
            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded border border-gray-100 bg-white shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-gray-900">{step.name}</span>
                <ConceptStatusBadge status={step.status} />
              </div>
              <p className="text-sm text-gray-500 mb-4">{step.reason}</p>
              {!step.locked && (
                <Link to={`/learning/concept/${step.id}`} className="inline-flex items-center gap-2 text-blue-600 font-medium text-sm hover:underline">
                  <PlayCircle size={16} /> Start Learning
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
