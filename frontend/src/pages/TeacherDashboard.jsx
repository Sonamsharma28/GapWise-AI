import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getDashboard } from '../api/teacher';
import LoadingSpinner from '../components/LoadingSpinner';

export default function TeacherDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard()
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;
  if (!data) return <div>Failed to load dashboard</div>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Teacher Dashboard</h1>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Total Students" value={data.stats.totalStudents} />
        <StatCard title="Avg Class Mastery" value={`${Math.round(data.stats.avgMastery)}%`} color="text-blue-600" />
        <StatCard title="Needs Attention" value={data.stats.needsAttention} color="text-red-600" />
        <StatCard title="Assessments Taken" value={data.stats.assessmentsTaken} />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-bold mb-4">Concept Performance</h2>
          <div className="space-y-4">
            {data.conceptPerformance?.map((c, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">{c.name}</span>
                  <span className={c.struggling > 0 ? 'text-red-600 font-medium' : 'text-gray-500'}>
                    {c.struggling} struggling
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className={`h-2 rounded-full ${c.avgScore >= 70 ? 'bg-green-500' : c.avgScore >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${c.avgScore}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-bold mb-4">Students</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-500 uppercase bg-gray-50">
                <tr>
                  <th className="px-4 py-2 rounded-tl-lg">Name</th>
                  <th className="px-4 py-2">Mastery</th>
                  <th className="px-4 py-2 rounded-tr-lg">Status</th>
                </tr>
              </thead>
              <tbody>
                {data.students?.map((s) => (
                  <tr key={s.id} className="border-b last:border-0 hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-900">
                      <Link to={`/teacher/student/${s.id}`} className="hover:text-blue-600">{s.name}</Link>
                    </td>
                    <td className="px-4 py-3">{Math.round(s.overallMastery)}%</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${s.status === 'Needs Support' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                        {s.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, color = "text-gray-900" }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-sm font-medium text-gray-500 mb-2">{title}</h3>
      <div className={`text-3xl font-bold ${color}`}>{value}</div>
    </div>
  );
}
