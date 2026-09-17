import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { startReassessment, submitReassessment } from '../api/reassessment';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import { TrendingUp, ArrowRight, RotateCw, CheckCircle2, ShieldCheck, Award } from 'lucide-react';

export default function Reassessment() {
  const [state, setState] = useState('intro'); // intro, loading, questions, submitting, result
  const [assessmentId, setAssessmentId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const handleStart = async () => {
    setState('loading');
    try {
      const res = await startReassessment();
      setAssessmentId(res.data.id || res.data.assessment_id);
      setQuestions(res.data.questions || []);
      setAnswers({});
      setCurrentIdx(0);
      setState('questions');
    } catch (err) {
      console.error(err);
      setState('intro');
    }
  };

  const handleAnswerSelect = (qId, optionLabel) => {
    setAnswers({ ...answers, [qId]: optionLabel });
  };

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setState('submitting');
    try {
      const res = await submitReassessment(assessmentId, { answers });
      setResult(res.data);
      setState('result');
    } catch (err) {
      console.error(err);
      setState('questions');
    }
  };

  if (state === 'loading' || state === 'submitting') {
    return (
      <div className="text-center mt-20">
        <LoadingSpinner />
        <p className="mt-4 text-gray-500 font-medium">
          {state === 'loading' ? 'Generating targeted reassessment questions...' : 'AI is re-evaluating your mastery growth...'}
        </p>
      </div>
    );
  }

  if (state === 'intro') {
    return (
      <div className="max-w-2xl mx-auto mt-12 bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center space-y-6">
        <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto">
          <RotateCw size={32} />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Targeted Mastery Reassessment</h1>
          <p className="text-gray-600 mt-2 max-w-md mx-auto">
            This reassessment focuses on the concepts you recently practiced. It benchmarks your new mastery against your initial diagnostic baseline.
          </p>
        </div>

        <div className="bg-blue-50/70 p-4 rounded-xl border border-blue-100 text-left space-y-2 text-sm text-blue-900">
          <div className="flex items-center gap-2 font-semibold">
            <ShieldCheck size={18} className="text-blue-600" /> Continuous Adaptive Loop
          </div>
          <p className="text-blue-800">
            Completing this test will update your Concept Mastery Map and automatically unlock advanced topics in your Personalized Learning Path.
          </p>
        </div>

        <button
          onClick={handleStart}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
        >
          Begin Reassessment
        </button>
      </div>
    );
  }

  if (state === 'questions') {
    const q = questions[currentIdx];
    const isAnswered = !!answers[q?.id];

    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>Question {currentIdx + 1} of {questions.length}</span>
          <span className="text-blue-600 font-bold bg-blue-50 px-2.5 py-1 rounded">
            {q?.concept_name}
          </span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-1.5">
          <div
            className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${((currentIdx + 1) / questions.length) * 100}%` }}
          ></div>
        </div>

        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 space-y-6">
          <h2 className="text-lg font-semibold text-gray-900 leading-relaxed">{q?.text}</h2>

          <div className="space-y-3">
            {q?.options?.map((opt) => {
              const selected = answers[q.id] === opt.label;
              return (
                <button
                  key={opt.id}
                  onClick={() => handleAnswerSelect(q.id, opt.label)}
                  className={`w-full text-left p-4 rounded-xl border-2 transition flex items-center gap-4 ${
                    selected
                      ? 'border-blue-600 bg-blue-50/70 text-blue-900 ring-2 ring-blue-500/20'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <span className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shrink-0 ${
                    selected ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'
                  }`}>
                    {opt.label}
                  </span>
                  <span className="text-base">{opt.text}</span>
                </button>
              );
            })}
          </div>

          <div className="flex justify-between items-center pt-4 border-t border-gray-100">
            <button
              onClick={() => setCurrentIdx(Math.max(0, currentIdx - 1))}
              disabled={currentIdx === 0}
              className="text-gray-500 px-4 py-2 text-sm font-medium hover:text-gray-700 disabled:opacity-30"
            >
              Previous
            </button>
            <button
              onClick={handleNext}
              disabled={!isAnswered}
              className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {currentIdx < questions.length - 1 ? 'Next' : 'Submit Reassessment'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Result state - Before vs After Comparison
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header Banner */}
      <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center space-y-3">
        <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto">
          <Award size={36} />
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Reassessment Complete</h1>
        <p className="text-gray-500">
          Reassessment Score:{' '}
          <span className="font-extrabold text-blue-600 text-xl">{Math.round(result?.score || 0)}%</span>
        </p>

        {result?.overall_improvement !== undefined && (
          <div className="inline-flex items-center gap-2 bg-green-50 text-green-800 px-4 py-2 rounded-full font-bold text-sm border border-green-200">
            <TrendingUp size={16} className="text-green-600" />
            Overall Growth: +{Math.max(0, Math.round(result.overall_improvement))}%
          </div>
        )}
      </div>

      {/* Before vs After Comparison Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Concept Mastery: Before vs. After</h2>
          <span className="text-xs text-gray-500 font-semibold uppercase">Continuous Mastery Loop</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th className="p-3.5 rounded-tl-lg">Concept</th>
                <th className="p-3.5 text-center">Initial Score</th>
                <th className="p-3.5 text-center">Reassessed Score</th>
                <th className="p-3.5 text-center">Mastery Status</th>
                <th className="p-3.5 text-right rounded-tr-lg">Progress</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {result?.comparison?.map((c, i) => (
                <tr key={i} className="hover:bg-gray-50/60 transition">
                  <td className="p-3.5 font-semibold text-gray-900">{c.concept_name}</td>
                  <td className="p-3.5 text-center text-gray-500 font-medium">{Math.round(c.before_score)}%</td>
                  <td className="p-3.5 text-center font-bold text-blue-600">{Math.round(c.after_score)}%</td>
                  <td className="p-3.5 text-center">
                    <ConceptStatusBadge status={c.after_status} />
                  </td>
                  <td className="p-3.5 text-right">
                    {c.improved ? (
                      <span className="inline-flex items-center gap-1 text-green-600 font-bold text-xs bg-green-50 px-2 py-1 rounded">
                        <TrendingUp size={12} /> +{Math.round(c.score_diff)}% Improved
                      </span>
                    ) : (
                      <span className="text-gray-400 text-xs">Maintained</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row justify-center gap-4">
        <Link
          to="/dashboard"
          className="flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
        >
          View Updated Dashboard
        </Link>
        <Link
          to="/learning/path"
          className="flex items-center justify-center gap-2 bg-white text-blue-600 border border-blue-200 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition"
        >
          View Learning Path <ArrowRight size={16} />
        </Link>
      </div>
    </div>
  );
}
