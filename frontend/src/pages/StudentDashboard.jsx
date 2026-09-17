import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getDashboard } from '../api/student';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import MasteryBar from '../components/MasteryBar';
import WrongQuestionExplainer from '../components/WrongQuestionExplainer';
import {
  AlertCircle,
  Sparkles,
  ArrowRight,
  Bot,
  BookOpen,
  ChevronDown,
  ChevronUp,
  CheckCircle2,
  XCircle,
  Network,
  GraduationCap
} from 'lucide-react';

export default function StudentDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  // Track which question's AI explanation panel is open  { [questionId]: bool }
  const [openExplainer, setOpenExplainer] = useState({});
  // Track collapsed quick-textbook view { [questionId]: bool }
  const [expandedTextbook, setExpandedTextbook] = useState({});

  useEffect(() => {
    getDashboard()
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const toggleExplainer = (qId) => {
    setOpenExplainer(prev => ({ ...prev, [qId]: !prev[qId] }));
  };

  const toggleTextbook = (qId) => {
    setExpandedTextbook(prev => ({ ...prev, [qId]: !prev[qId] }));
  };

  if (loading) return <LoadingSpinner />;

  if (!data?.hasAssessment) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Welcome, {user.name}! 👋</h1>
        <EmptyState
          title="Start Your Diagnostic Assessment"
          description="Take your first diagnostic test to identify conceptual gaps, discover prerequisite root causes, and get your personalized AI learning path."
          action={
            <Link to="/assessment" className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl transition shadow-md inline-flex items-center gap-2">
              Take Diagnostic Assessment <ArrowRight size={18} />
            </Link>
          }
        />
      </div>
    );
  }

  const incorrectList = data.recent_incorrect_questions || [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-gray-100">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Welcome back, {user.name}! 👋</h1>
          <p className="text-gray-500 text-sm mt-1">Here is your continuous learning progress and personalized AI diagnosis.</p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/ai-mentor"
            className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition"
          >
            <Bot size={18} /> Ask AI Teacher
          </Link>
          <Link
            to="/assessment"
            className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2.5 rounded-xl font-semibold text-sm transition"
          >
            Retake Test
          </Link>
        </div>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Overall Mastery" value={`${Math.round(data.overallMastery)}%`} color="text-blue-600" />
        <StatCard title="Mastered Topics" value={data.counts.mastered} color="text-green-600" />
        <StatCard title="Developing Topics" value={data.counts.developing} color="text-amber-600" />
        <StatCard title="Needs Attention" value={data.counts.needs_attention} color="text-red-600" />
      </div>

      {/* ── SECTION: Questions Needing Attention ── */}
      {incorrectList.length > 0 && (
        <div className="bg-white rounded-2xl shadow-sm border border-red-100 overflow-hidden">
          {/* Section Header */}
          <div className="bg-gradient-to-r from-red-50 to-amber-50 p-6 border-b border-red-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2 text-red-900 font-bold text-lg">
                <AlertCircle className="text-red-600" size={22} />
                <span>Questions Needing Attention — {incorrectList.length} Misconception{incorrectList.length > 1 ? 's' : ''} Found</span>
              </div>
              <p className="text-xs sm:text-sm text-red-700 mt-1">
                Each question below was answered incorrectly. Click <strong>"Get AI Explanation"</strong> to get a personalized step-by-step breakdown — no teacher needed!
              </p>
            </div>
            <span className="text-xs font-bold uppercase tracking-wider bg-red-100 text-red-800 px-3 py-1 rounded-full shrink-0">
              Diagnostic Review
            </span>
          </div>

          <div className="p-6 space-y-6">
            {incorrectList.map((q) => {
              const isExplainerOpen = !!openExplainer[q.question_id];
              const isTextbookOpen = !!expandedTextbook[q.question_id];

              // Find full texts of student's answer and correct answer from options
              const studentOptFull = q.options?.find(o => o.label === q.student_answer);
              const correctOptFull = q.options?.find(o => o.label === q.correct_answer);

              return (
                <div
                  key={q.question_id}
                  className="rounded-2xl border border-gray-200 hover:border-blue-200 transition bg-white shadow-xs overflow-hidden"
                >
                  {/* Question Card Top Bar */}
                  <div className="p-5 space-y-4">
                    {/* Row: Question Number + Concept + Difficulty */}
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="bg-red-100 text-red-800 font-extrabold text-xs px-2.5 py-1 rounded-md">
                          Question #{q.question_num}
                        </span>
                        <span className="bg-blue-50 text-blue-800 font-semibold text-xs px-2.5 py-1 rounded-md">
                          {q.concept_name}
                        </span>
                        <span className="text-gray-400 text-xs font-medium">
                          Difficulty: {q.difficulty}/5
                        </span>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          onClick={() => toggleExplainer(q.question_id)}
                          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold shadow-xs transition ${
                            isExplainerOpen
                              ? 'bg-indigo-700 text-white'
                              : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white'
                          }`}
                        >
                          <GraduationCap size={14} />
                          {isExplainerOpen ? 'Hide AI Explanation' : 'Get AI Explanation'}
                        </button>
                        <Link
                          to={`/concept/${q.concept_id}`}
                          className="flex items-center gap-1 text-gray-600 hover:text-blue-600 text-xs font-semibold px-2.5 py-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 transition"
                        >
                          <BookOpen size={13} /> Learn Concept
                        </Link>
                      </div>
                    </div>

                    {/* Question Text */}
                    <div className="text-sm sm:text-base font-medium text-gray-900 leading-relaxed">
                      {q.text}
                    </div>

                    {/* Answer Comparison — full option text */}
                    <div className="grid sm:grid-cols-2 gap-2 text-xs sm:text-sm">
                      <div className="flex items-start gap-2 bg-red-50 text-red-800 font-medium p-3 rounded-xl border border-red-100">
                        <XCircle size={16} className="text-red-500 shrink-0 mt-0.5" />
                        <div>
                          <div className="font-bold mb-0.5">Your Answer: Option {q.student_answer}</div>
                          {studentOptFull && (
                            <div className="text-red-700 font-normal">{studentOptFull.text}</div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-start gap-2 bg-green-50 text-green-800 font-medium p-3 rounded-xl border border-green-100">
                        <CheckCircle2 size={16} className="text-green-600 shrink-0 mt-0.5" />
                        <div>
                          <div className="font-bold mb-0.5">Correct Answer: Option {q.correct_answer}</div>
                          {correctOptFull && (
                            <div className="text-green-700 font-normal">{correctOptFull.text}</div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Collapsible Quick Textbook Explanation */}
                    <div>
                      <button
                        onClick={() => toggleTextbook(q.question_id)}
                        className="text-xs font-semibold text-gray-500 hover:text-blue-600 flex items-center gap-1 transition"
                      >
                        {isTextbookOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                        {isTextbookOpen ? 'Hide Textbook Solution' : 'View Quick Textbook Solution'}
                      </button>

                      {isTextbookOpen && (
                        <div className="mt-2.5 p-3.5 bg-blue-50/50 rounded-lg text-xs text-blue-950 border border-blue-100 leading-relaxed">
                          <div className="font-bold text-blue-900 mb-1">Textbook Solution:</div>
                          <p>{q.explanation}</p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Inline AI Explainer Card (toggled) */}
                  {isExplainerOpen && (
                    <div className="border-t border-indigo-100 bg-slate-50/60 p-5">
                      <WrongQuestionExplainer
                        questionId={q.question_id}
                        questionNum={q.question_num}
                        conceptId={q.concept_id}
                        conceptName={q.concept_name}
                        onClose={() => toggleExplainer(q.question_id)}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Main Content Grid: Concept Mastery & Recommendations */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column: Concept Mastery Breakdown */}
        <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-gray-100 pb-4">
            <div>
              <h2 className="text-lg font-bold text-gray-900">Concept Mastery Map</h2>
              <p className="text-xs text-gray-500 mt-0.5">Real-time mastery status across 12 Class 9-10 topics.</p>
            </div>
            <Link to="/knowledge-graph" className="flex items-center gap-1 text-xs font-bold text-blue-600 hover:underline">
              <Network size={14} /> Graph View
            </Link>
          </div>

          <div className="space-y-4">
            {data.concepts.map(c => (
              <div key={c.id} className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-2.5 rounded-xl hover:bg-gray-50 transition">
                <Link to={`/concept/${c.id}`} className="sm:w-1/3 truncate font-semibold text-gray-900 hover:text-blue-600 text-sm">
                  {c.name}
                </Link>
                <div className="flex-1 max-w-xs">
                  <MasteryBar score={c.score} />
                </div>
                <div className="sm:w-1/4 text-right">
                  <ConceptStatusBadge status={c.status} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: AI Recommendations & Quick Links */}
        <div className="space-y-6">
          {/* Smart Recommendation Card */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50/70 rounded-2xl shadow-sm border border-blue-100 p-6 space-y-4">
            <div className="flex items-center gap-2 text-blue-900 font-bold">
              <Sparkles size={18} className="text-blue-600" />
              <span>Recommended Next Step</span>
            </div>
            <p className="text-blue-900 text-sm leading-relaxed">
              {data.recommendation?.message || "Continue your personalized learning path to strengthen foundational prerequisites."}
            </p>
            <Link
              to="/learning/path"
              className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-bold text-sm w-full transition shadow-md"
            >
              Open Learning Path <ArrowRight size={16} />
            </Link>
          </div>

          {/* AI Virtual Teacher Card */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-3">
            <div className="flex items-center gap-2 text-gray-900 font-bold">
              <Bot size={20} className="text-indigo-600" />
              <span>Your Personal AI Math Teacher</span>
            </div>
            <p className="text-xs text-gray-600 leading-relaxed">
              Available 24/7 to explain any question you got wrong, answer doubts in plain English, give step-by-step worked examples, and guide you to full concept mastery — no human teacher needed.
            </p>
            {incorrectList.length > 0 && (
              <div className="bg-amber-50 rounded-lg p-2.5 border border-amber-100 text-xs text-amber-800 font-semibold">
                🎯 {incorrectList.length} question{incorrectList.length > 1 ? 's' : ''} ready for AI explanation above ↑
              </div>
            )}
            <Link
              to="/ai-mentor"
              className="flex items-center justify-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 px-4 py-2.5 rounded-xl font-bold text-sm w-full transition"
            >
              <GraduationCap size={16} /> Chat with AI Teacher
            </Link>
          </div>

          {/* Quick Actions List */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-3">
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider">Quick Actions</h3>
            <div className="flex flex-col gap-1.5 text-sm">
              <Link to="/practice" className="p-2.5 hover:bg-gray-50 text-gray-700 hover:text-blue-600 font-medium rounded-lg transition flex items-center justify-between">
                <span>Targeted Practice</span> <ArrowRight size={14} />
              </Link>
              <Link to="/knowledge-graph" className="p-2.5 hover:bg-gray-50 text-gray-700 hover:text-blue-600 font-medium rounded-lg transition flex items-center justify-between">
                <span>Knowledge Graph</span> <ArrowRight size={14} />
              </Link>
              <Link to="/reassessment" className="p-2.5 hover:bg-gray-50 text-gray-700 hover:text-blue-600 font-medium rounded-lg transition flex items-center justify-between">
                <span>Take Reassessment</span> <ArrowRight size={14} />
              </Link>
              <Link to="/progress" className="p-2.5 hover:bg-gray-50 text-gray-700 hover:text-blue-600 font-medium rounded-lg transition flex items-center justify-between">
                <span>View Growth Analytics</span> <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, color = "text-gray-900" }) {
  return (
    <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
      <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">{title}</h3>
      <div className={`text-2xl sm:text-3xl font-black ${color}`}>{value}</div>
    </div>
  );
}
