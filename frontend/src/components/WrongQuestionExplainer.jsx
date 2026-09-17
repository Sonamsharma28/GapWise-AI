import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuestionExplanation } from '../api/ai';
import {
  Bot,
  XCircle,
  CheckCircle2,
  Lightbulb,
  BookOpen,
  ChevronRight,
  RefreshCw,
  Pencil,
  Target,
  GraduationCap
} from 'lucide-react';

/**
 * WrongQuestionExplainer
 * Reusable component that fetches and renders a structured AI explanation
 * for a specific wrong question. Used in:
 *  - StudentDashboard (inline expandable card)
 *  - AIMentor page (structured panel alongside chat)
 *
 * Props:
 *  - questionId: number
 *  - questionNum: number (display only)
 *  - conceptId: number (for Practice link)
 *  - conceptName: string (display label)
 *  - onClose?: () => void  (optional close handler)
 */
export default function WrongQuestionExplainer({ questionId, questionNum, conceptId, conceptName, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fetched, setFetched] = useState(false);

  const fetchExplanation = async () => {
    if (fetched) return; // already loaded
    setLoading(true);
    setError(null);
    try {
      const res = await getQuestionExplanation(questionId);
      setData(res.data);
      setFetched(true);
    } catch (err) {
      setError('Could not load explanation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch when mounted
  React.useEffect(() => {
    fetchExplanation();
  }, [questionId]);

  if (loading) {
    return (
      <div className="flex items-center gap-3 p-5 bg-indigo-50 rounded-xl border border-indigo-100 text-indigo-800 text-sm">
        <RefreshCw size={18} className="animate-spin text-indigo-500 shrink-0" />
        <span>AI Teacher is preparing your personalised explanation...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 rounded-xl border border-red-100 text-red-700 text-sm flex items-center gap-2">
        <XCircle size={16} className="shrink-0" />
        {error}
        <button onClick={fetchExplanation} className="ml-auto text-xs underline font-semibold">Retry</button>
      </div>
    );
  }

  if (!data) return null;

  const {
    question_text,
    concept_name,
    concept_id: cId,
    student_answer_label,
    student_answer_text,
    correct_answer_label,
    correct_answer_text,
    all_options,
    why_wrong,
    step_by_step,
    golden_rule,
    mini_challenge,
    teacher_tip
  } = data;

  const practiceConceptId = conceptId || cId;

  return (
    <div className="rounded-2xl border border-indigo-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-700 text-white px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-sm">
          <GraduationCap size={18} />
          <span>AI Teacher — Question #{questionNum} Explained</span>
          <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">{concept_name}</span>
        </div>
        {onClose && (
          <button onClick={onClose} className="text-white/70 hover:text-white transition">
            <XCircle size={18} />
          </button>
        )}
      </div>

      <div className="p-5 space-y-5 text-sm">
        {/* The Problem */}
        <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
          <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5">📌 The Question</div>
          <p className="text-gray-900 font-medium leading-relaxed">{question_text}</p>

          {/* Options */}
          {all_options && all_options.length > 0 && (
            <div className="mt-3 space-y-1.5">
              {all_options.map(opt => {
                const isStudentPick = opt.label === student_answer_label;
                const isCorrect = opt.is_correct;
                return (
                  <div
                    key={opt.label}
                    className={`flex items-center gap-2.5 px-3 py-2 rounded-lg border text-xs font-medium ${
                      isCorrect
                        ? 'bg-green-50 border-green-300 text-green-800'
                        : isStudentPick
                        ? 'bg-red-50 border-red-300 text-red-800'
                        : 'bg-white border-gray-200 text-gray-600'
                    }`}
                  >
                    {isCorrect ? (
                      <CheckCircle2 size={14} className="text-green-600 shrink-0" />
                    ) : isStudentPick ? (
                      <XCircle size={14} className="text-red-500 shrink-0" />
                    ) : (
                      <span className="w-3.5 h-3.5 rounded-full border border-gray-300 shrink-0" />
                    )}
                    <span className="font-bold mr-1">{opt.label}.</span>
                    <span>{opt.text}</span>
                    {isStudentPick && !isCorrect && (
                      <span className="ml-auto text-xs bg-red-100 text-red-700 px-1.5 py-0.5 rounded font-bold">Your Answer</span>
                    )}
                    {isCorrect && (
                      <span className="ml-auto text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-bold">Correct</span>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Why Wrong */}
        <div className="bg-amber-50 rounded-xl p-4 border border-amber-200">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-xs uppercase tracking-wider mb-2">
            <XCircle size={14} className="text-red-500" />
            Why Option {student_answer_label} is a Common Trap
          </div>
          <p className="text-amber-900 leading-relaxed">{why_wrong}</p>
        </div>

        {/* Step-by-Step Solution */}
        <div className="bg-blue-50 rounded-xl p-4 border border-blue-100 space-y-3">
          <div className="flex items-center gap-2 text-blue-900 font-bold text-xs uppercase tracking-wider">
            <Bot size={14} className="text-blue-600" />
            Step-by-Step Solution (The Right Way)
          </div>
          {step_by_step && step_by_step.map((step, i) => (
            <div key={i} className="flex gap-3 items-start">
              <span className="shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-black">
                {i === step_by_step.length - 1 ? '✓' : i + 1}
              </span>
              <p className={`leading-relaxed ${i === step_by_step.length - 1 ? 'text-blue-900 font-semibold' : 'text-blue-800'}`}>
                {i === step_by_step.length - 1 ? (
                  <>✅ {step}. <strong>Answer: Option {correct_answer_label} — "{correct_answer_text}"</strong></>
                ) : (
                  <>{step}.</>
                )}
              </p>
            </div>
          ))}
        </div>

        {/* Golden Rule */}
        <div className="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl p-4 border border-yellow-200">
          <div className="flex items-center gap-2 text-yellow-900 font-bold text-xs uppercase tracking-wider mb-2">
            <Lightbulb size={14} className="text-yellow-500" />
            Golden Rule to Never Forget
          </div>
          <p className="text-yellow-900 leading-relaxed font-medium">{golden_rule}</p>
        </div>

        {/* Teacher Tip (prerequisite) */}
        {teacher_tip && (
          <div className="bg-purple-50 rounded-xl p-4 border border-purple-100">
            <div className="flex items-center gap-2 text-purple-900 font-bold text-xs uppercase tracking-wider mb-1.5">
              <Target size={14} className="text-purple-600" />
              Prerequisite Alert
            </div>
            <p className="text-purple-900 leading-relaxed">{teacher_tip}</p>
          </div>
        )}

        {/* Mini Challenge */}
        <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-200">
          <div className="flex items-center gap-2 text-emerald-900 font-bold text-xs uppercase tracking-wider mb-2">
            <Pencil size={14} className="text-emerald-600" />
            Mini Challenge — Test Yourself!
          </div>
          <p className="text-emerald-800 font-medium leading-relaxed">{mini_challenge}</p>
          <p className="text-emerald-700 text-xs mt-2 italic">Try it, then ask the AI Mentor "Is my answer correct?" to get it checked!</p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-2 pt-1">
          {practiceConceptId && (
            <Link
              to={`/concept/${practiceConceptId}`}
              className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition shadow-sm"
            >
              <BookOpen size={14} />
              Study this Concept
            </Link>
          )}
          <Link
            to={`/ai-mentor?questionId=${questionId}&questionNum=${questionNum}`}
            className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition shadow-sm"
          >
            <Bot size={14} />
            Chat with AI Teacher
          </Link>
          {practiceConceptId && (
            <Link
              to={`/practice`}
              className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition shadow-sm"
            >
              <ChevronRight size={14} />
              Practice Questions
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
