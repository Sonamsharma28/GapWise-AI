import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProgress } from '../api/student';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import MasteryBar from '../components/MasteryBar';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';
import { TrendingUp, Calendar, Award, BookOpen, RotateCcw } from 'lucide-react';

export default function Progress() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProgress()
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  const hasTimeline = data?.timeline?.length > 0;
  const avgScore = hasTimeline
    ? Math.round(data.timeline.reduce((acc, curr) => acc + curr.score, 0) / data.timeline.length)
    : 0;

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Your Learning & Mastery Progress</h1>
        <p className="text-gray-500 text-sm">
          Track your longitudinal mastery growth, assessment performance trends, and concept retention.
        </p>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <Calendar size={24} />
          </div>
          <div>
            <div className="text-sm font-medium text-gray-500">Assessments Completed</div>
            <div className="text-2xl font-bold text-gray-900">{data?.total_assessments || 0}</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-green-50 text-green-600 flex items-center justify-center shrink-0">
            <TrendingUp size={24} />
          </div>
          <div>
            <div className="text-sm font-medium text-gray-500">Average Performance</div>
            <div className="text-2xl font-bold text-green-600">{avgScore}%</div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center shrink-0">
            <Award size={24} />
          </div>
          <div>
            <div className="text-sm font-medium text-gray-500">Active Curriculum</div>
            <div className="text-2xl font-bold text-purple-600">Class 9–10 Math</div>
          </div>
        </div>
      </div>

      {/* Performance Over Time Chart */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4">
        <h2 className="text-lg font-bold text-gray-900">Score & Mastery Timeline</h2>
        {hasTimeline ? (
          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.timeline} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="session" stroke="#94a3b8" fontSize={12} tickLine={false} />
                <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={12} tickLine={false} />
                <Tooltip
                  formatter={(val) => [`${val}%`, 'Score']}
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}
                />
                <Area type="monotone" dataKey="score" stroke="#2563eb" strokeWidth={3} fillOpacity={1} fill="url(#scoreGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="py-12 text-center text-gray-400">
            No assessment sessions completed yet. Take an assessment to start tracking your timeline.
          </div>
        )}
      </div>

      {/* Concept Breakdown Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-4">
        <h2 className="text-lg font-bold text-gray-900">Detailed Concept Breakdown</h2>
        {data?.concept_breakdown?.length > 0 ? (
          <div className="divide-y divide-gray-100">
            {data.concept_breakdown.map((c, i) => (
              <div key={i} className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="sm:w-1/3">
                  <div className="font-semibold text-gray-900 text-sm">{c.name}</div>
                  <div className="text-xs text-gray-400">{c.attempts} assessment/practice sessions</div>
                </div>
                <div className="flex-1 max-w-xs">
                  <MasteryBar score={c.score} />
                </div>
                <div className="sm:w-1/4 text-right">
                  <ConceptStatusBadge status={c.status} />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-8 text-center text-gray-400">No concept mastery data recorded yet.</div>
        )}
      </div>

      {/* Quick Action CTA */}
      <div className="flex justify-center gap-4">
        <Link
          to="/reassessment"
          className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700"
        >
          <RotateCcw size={16} /> Take Reassessment
        </Link>
        <Link
          to="/learning/path"
          className="flex items-center gap-2 bg-white text-blue-600 border border-blue-200 px-6 py-2.5 rounded-lg font-medium hover:bg-blue-50"
        >
          <BookOpen size={16} /> View Learning Path
        </Link>
      </div>
    </div>
  );
}
