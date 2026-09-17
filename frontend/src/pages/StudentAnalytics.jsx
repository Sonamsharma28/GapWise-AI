import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getStudentDetail } from '../api/teacher';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import MasteryBar from '../components/MasteryBar';

export default function StudentAnalytics() {
  const { id } = useParams();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStudentDetail(id)
      .then(res => setStudent(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (!student) return <div>Student not found</div>;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{student.name}</h1>
          <p className="text-gray-500">{student.email}</p>
        </div>
        <Link to="/teacher/dashboard" className="text-blue-600 hover:underline text-sm font-medium">Back to Students</Link>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center justify-center">
          <h3 className="text-lg font-bold text-gray-700 mb-4">Overall Mastery</h3>
          <div className="text-5xl font-extrabold text-blue-600 mb-2">{Math.round(student.overallMastery)}%</div>
          <ConceptStatusBadge status={student.overallMastery >= 70 ? 'mastered' : student.overallMastery >= 50 ? 'developing' : 'needs_attention'} />
        </div>

        <div className="md:col-span-2 bg-red-50 p-6 rounded-xl shadow-sm border border-red-100">
          <h3 className="text-lg font-bold text-red-900 mb-4">Identified Learning Gaps (Root Causes)</h3>
          {student.learningGaps?.length > 0 ? (
            <ul className="space-y-3">
              {student.learningGaps.map((gap, i) => (
                <li key={i} className="bg-white p-3 rounded shadow-sm text-sm">
                  <span className="font-bold text-red-800">{gap.prerequisite}</span> is causing struggles in <span className="font-medium">{gap.target}</span>.
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-red-700">No major gaps identified.</p>
          )}
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold mb-4">Concept Mastery</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {student.concepts?.map(c => (
            <div key={c.id} className="flex items-center justify-between gap-4 p-3 border border-gray-50 rounded bg-gray-50">
              <div className="w-1/3 truncate text-sm font-medium">{c.name}</div>
              <div className="flex-1"><MasteryBar score={c.score} /></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
