import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getReport } from '../api/assessment';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import MasteryBar from '../components/MasteryBar';
import { 
  Award, 
  AlertTriangle, 
  ArrowRight, 
  GitBranch, 
  CheckCircle2, 
  XCircle, 
  Network, 
  Bot, 
  BookOpen, 
  ChevronDown, 
  ChevronUp,
  Filter
} from 'lucide-react';

export default function AssessmentReport() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filterMode, setFilterMode] = useState('all'); // 'all', 'incorrect', 'correct'
  const [expandedQuestions, setExpandedQuestions] = useState({});

  useEffect(() => {
    getReport(id)
      .then(res => setReport(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  const toggleExpand = (qId) => {
    setExpandedQuestions(prev => ({
      ...prev,
      [qId]: !prev[qId]
    }));
  };

  const handleAskAI = (q) => {
    navigate(`/ai-mentor?questionId=${q.question_id}&questionNum=${q.question_num}`);
  };

  if (loading) return <LoadingSpinner />;
  if (!report) return <div className="text-center py-12 text-gray-500">Assessment report not found.</div>;

  const scoreNum = Math.round(report.score || 0);
  const allQuestions = report.questions_review || [];
  const incorrectQuestions = report.incorrect_questions || allQuestions.filter(q => !q.is_correct);
  const correctQuestions = allQuestions.filter(q => q.is_correct);

  const displayedQuestions = filterMode === 'incorrect' 
    ? incorrectQuestions 
    : filterMode === 'correct' 
    ? correctQuestions 
    : allQuestions;

  return (
    <div className="space-y-8 max-w-4xl mx-auto pb-12">
      {/* Assessment Summary Header */}
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center space-y-3">
        <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto">
          <Award size={36} />
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Diagnostic Assessment Complete</h1>
        <div className="text-5xl font-black text-blue-600 my-2">{scoreNum}%</div>
        <p className="text-gray-500 text-sm">
          Completed on {report.date ? new Date(report.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Today'}
        </p>
        <div className="flex justify-center gap-4 pt-2 text-xs font-semibold">
          <span className="bg-green-50 text-green-700 px-3 py-1 rounded-full border border-green-200">
            ✓ {correctQuestions.length} Correct
          </span>
          <span className="bg-red-50 text-red-700 px-3 py-1 rounded-full border border-red-200">
            ✗ {incorrectQuestions.length} Needs Review
          </span>
        </div>
      </div>

      {/* Root-Cause Prerequisite Analysis (Crucial USP for SIH) */}
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
        <div className="flex items-center justify-between border-b border-gray-100 pb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              <GitBranch className="text-blue-600" /> 🔍 AI Root Learning Gap Diagnosis
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              Prerequisite graph traversal reveals the underlying conceptual weakness causing struggle in advanced topics.
            </p>
          </div>
          <span className="text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-700 px-3 py-1 rounded-full shrink-0">
            Prerequisite Engine
          </span>
        </div>

        {report.rootCauses?.length > 0 || report.root_cause_analysis?.length > 0 ? (
          <div className="space-y-4">
            {(report.rootCauses || report.root_cause_analysis).map((rc, idx) => (
              <div key={idx} className="p-5 bg-gradient-to-r from-red-50/80 to-amber-50/40 border border-red-100 rounded-xl space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <AlertTriangle size={18} className="text-red-600 shrink-0" />
                    <span className="font-bold text-red-950 text-base">{rc.targetConcept}</span>
                  </div>
                  <span className="text-xs font-semibold bg-red-100 text-red-800 px-2.5 py-0.5 rounded">
                    Needs Attention
                  </span>
                </div>

                <div className="bg-white/80 p-3 rounded-lg border border-red-100/60 text-sm">
                  <div className="text-xs font-bold text-red-800 uppercase tracking-wider mb-1">
                    Root Prerequisite Cause Identified:
                  </div>
                  <div className="text-gray-900 font-semibold">{rc.prerequisiteConcept}</div>
                </div>

                <p className="text-sm text-gray-700 leading-relaxed">{rc.explanation}</p>

                {rc.chain_display && (
                  <div className="pt-2 text-xs font-mono text-gray-600 bg-white/50 p-2 rounded">
                    <strong>Prerequisite Dependency Chain:</strong> {rc.chain_display}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6 bg-green-50 rounded-xl border border-green-100 text-center text-green-900 space-y-1">
            <CheckCircle2 size={28} className="text-green-600 mx-auto mb-2" />
            <div className="font-bold">No Critical Prerequisite Bottlenecks Detected!</div>
            <p className="text-xs text-green-800">Your foundational concepts are solid. You are ready to proceed with advanced modules.</p>
          </div>
        )}
      </div>

      {/* SECTION: Question-by-Question Diagnostic Review */}
      {allQuestions.length > 0 && (
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                <span>📝 Question-by-Question Diagnostic Review</span>
              </h2>
              <p className="text-xs text-gray-500 mt-1">
                Review every question from your diagnostic test. Click <strong>Ask AI Teacher</strong> for an intuitive personal breakdown.
              </p>
            </div>

            {/* Filter Pills */}
            <div className="flex items-center gap-1.5 bg-gray-100 p-1 rounded-xl text-xs font-semibold shrink-0">
              <button
                onClick={() => setFilterMode('all')}
                className={`px-3 py-1.5 rounded-lg transition ${filterMode === 'all' ? 'bg-white text-gray-900 shadow-xs' : 'text-gray-600 hover:text-gray-900'}`}
              >
                All ({allQuestions.length})
              </button>
              <button
                onClick={() => setFilterMode('incorrect')}
                className={`px-3 py-1.5 rounded-lg transition ${filterMode === 'incorrect' ? 'bg-red-500 text-white shadow-xs' : 'text-red-700 hover:bg-red-50'}`}
              >
                Incorrect ({incorrectQuestions.length})
              </button>
              <button
                onClick={() => setFilterMode('correct')}
                className={`px-3 py-1.5 rounded-lg transition ${filterMode === 'correct' ? 'bg-green-600 text-white shadow-xs' : 'text-green-700 hover:bg-green-50'}`}
              >
                Correct ({correctQuestions.length})
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {displayedQuestions.map((q) => {
              const isExpanded = !!expandedQuestions[q.question_id];
              return (
                <div 
                  key={q.question_id}
                  className={`p-5 rounded-xl border transition space-y-3 ${
                    q.is_correct 
                      ? 'border-green-100 bg-green-50/20' 
                      : 'border-red-100 bg-red-50/20'
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className={`font-extrabold text-xs px-2.5 py-1 rounded-md ${
                        q.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        Question #{q.question_num}
                      </span>
                      <span className="bg-blue-50 text-blue-800 font-semibold text-xs px-2.5 py-1 rounded-md">
                        {q.concept_name}
                      </span>
                      <span className="text-gray-400 text-xs font-medium">
                        Difficulty: {q.difficulty}/5
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleAskAI(q)}
                        className="flex items-center gap-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold shadow-xs transition"
                      >
                        <Bot size={13} /> Ask AI Teacher
                      </button>
                      <Link
                        to={`/concept/${q.concept_id}`}
                        className="flex items-center gap-1 text-gray-600 hover:text-blue-600 text-xs font-semibold px-2 py-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 transition"
                      >
                        <BookOpen size={12} /> Concept
                      </Link>
                    </div>
                  </div>

                  <div className="text-sm sm:text-base font-medium text-gray-900 leading-relaxed">
                    {q.text}
                  </div>

                  {/* Options List */}
                  <div className="grid sm:grid-cols-2 gap-2 text-xs">
                    {q.options?.map((opt) => {
                      const isStudent = opt.label === q.student_answer;
                      const isRight = opt.is_correct || opt.label === q.correct_answer;
                      return (
                        <div
                          key={opt.id || opt.label}
                          className={`p-2.5 rounded-lg border flex items-center gap-2 ${
                            isRight
                              ? 'bg-green-50 border-green-300 text-green-900 font-medium'
                              : isStudent
                              ? 'bg-red-50 border-red-300 text-red-900 font-medium'
                              : 'bg-white border-gray-200 text-gray-600'
                          }`}
                        >
                          <span className={`w-5 h-5 rounded flex items-center justify-center font-bold text-xs shrink-0 ${
                            isRight ? 'bg-green-600 text-white' : isStudent ? 'bg-red-500 text-white' : 'bg-gray-100 text-gray-700'
                          }`}>
                            {opt.label}
                          </span>
                          <span>{opt.text}</span>
                          {isRight && <span className="text-green-600 ml-auto font-bold text-xs">✓ Correct</span>}
                          {isStudent && !isRight && <span className="text-red-500 ml-auto font-bold text-xs">✗ Your Pick</span>}
                        </div>
                      );
                    })}
                  </div>

                  {/* Collapsible Solution */}
                  <div className="pt-1">
                    <button
                      onClick={() => toggleExpand(q.question_id)}
                      className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                    >
                      {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      {isExpanded ? 'Hide Solution' : 'View Textbook Solution'}
                    </button>

                    {isExpanded && (
                      <div className="mt-2 p-3 bg-white rounded-lg text-xs text-gray-800 border border-gray-200 leading-relaxed">
                        <strong className="text-gray-900">Explanation:</strong> {q.explanation}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Concept Mastery Map */}
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
        <div className="flex items-center justify-between border-b border-gray-100 pb-4">
          <h2 className="text-xl font-bold text-gray-900">Concept Mastery Map</h2>
          <span className="text-xs text-gray-500 font-semibold uppercase">12 Mathematics Topics</span>
        </div>

        <div className="space-y-4">
          {(report.concepts || report.concept_mastery || []).map((c) => (
            <div key={c.id || c.concept_id} className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl hover:bg-gray-50 transition">
              <div className="sm:w-1/3 font-semibold text-gray-900 text-sm">{c.name}</div>
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

      {/* Next Step Recommendations */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-8 rounded-2xl border border-blue-100 text-center space-y-4 shadow-sm">
        <h2 className="text-xl font-bold text-blue-950">Recommended Next Steps</h2>
        <p className="text-blue-800 text-sm max-w-md mx-auto">
          We have synthesized your assessment data into an optimized, prerequisite-ordered personalized learning path.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-3 pt-2">
          <Link
            to="/learning/path"
            className="flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-md"
          >
            Start Personalized Path <ArrowRight size={18} />
          </Link>
          <Link
            to="/knowledge-graph"
            className="flex items-center justify-center gap-2 bg-white text-blue-600 border border-blue-200 px-6 py-3 rounded-xl font-semibold hover:bg-blue-50 transition"
          >
            <Network size={18} /> View Knowledge Graph
          </Link>
        </div>
      </div>
    </div>
  );
}
