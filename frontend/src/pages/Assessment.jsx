import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startAssessment, submitAssessment } from '../api/assessment';
import LoadingSpinner from '../components/LoadingSpinner';
import { BookOpen, ShieldCheck, ArrowRight, ArrowLeft } from 'lucide-react';

export default function Assessment() {
  const [state, setState] = useState('intro'); // intro, loading, questions, submitting
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [assessmentId, setAssessmentId] = useState(null);
  const navigate = useNavigate();

  const handleStart = async () => {
    setState('loading');
    try {
      const res = await startAssessment({});
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

  const handleAnswer = (val) => {
    setAnswers({ ...answers, [questions[currentIdx].id]: val });
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
      await submitAssessment(assessmentId, { answers });
      navigate(`/assessment/${assessmentId}/report`);
    } catch (err) {
      console.error(err);
      setState('questions');
    }
  };

  if (state === 'intro') {
    return (
      <div className="max-w-2xl mx-auto mt-12 bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center space-y-6">
        <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto">
          <BookOpen size={32} />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Mathematics Diagnostic Assessment</h1>
          <p className="text-gray-600 mt-2 max-w-md mx-auto text-sm sm:text-base">
            This comprehensive test evaluates your foundational understanding across Class 9–10 mathematics topics.
          </p>
        </div>

        <div className="bg-blue-50/70 p-4 rounded-xl border border-blue-100 text-left space-y-2 text-xs sm:text-sm text-blue-950">
          <div className="flex items-center gap-2 font-bold text-blue-900">
            <ShieldCheck size={18} className="text-blue-600" /> AI-Powered Prerequisite Diagnosis
          </div>
          <p className="text-blue-800">
            Answer naturally. Even if you get a question wrong, our AI analyzes whether your gap is in the question's topic or its earlier prerequisites.
          </p>
        </div>

        <button
          onClick={handleStart}
          className="bg-blue-600 text-white px-8 py-3.5 rounded-xl font-bold text-base hover:bg-blue-700 transition shadow-md"
        >
          Begin Diagnostic Assessment
        </button>
      </div>
    );
  }

  if (state === 'loading' || state === 'submitting') {
    return (
      <div className="text-center mt-20 space-y-4">
        <LoadingSpinner />
        <p className="text-gray-600 font-medium">
          {state === 'loading' ? 'Loading mathematics assessment questions...' : 'AI is analyzing your responses and tracing prerequisite root causes...'}
        </p>
      </div>
    );
  }

  const q = questions[currentIdx];
  const isAnswered = !!answers[q?.id];

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Progress header */}
      <div className="flex items-center justify-between text-sm text-gray-500 font-medium">
        <span>Question {currentIdx + 1} of {questions.length}</span>
        <span className="text-blue-600 font-bold bg-blue-50 px-2.5 py-1 rounded text-xs">
          {q?.concept_name}
        </span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-1.5">
        <div
          className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
          style={{ width: `${((currentIdx + 1) / questions.length) * 100}%` }}
        ></div>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
        <h2 className="text-lg font-semibold text-gray-900 leading-relaxed">{q?.text}</h2>

        <div className="space-y-3">
          {q?.options?.map((opt) => {
            const optLabel = typeof opt === 'string' ? opt : opt.label;
            const optText = typeof opt === 'string' ? opt : opt.text;
            const isSelected = answers[q.id] === optLabel;

            return (
              <button
                key={opt.id || optLabel}
                type="button"
                onClick={() => handleAnswer(optLabel)}
                className={`w-full text-left p-4 rounded-xl border-2 transition flex items-center gap-4 ${
                  isSelected
                    ? 'border-blue-600 bg-blue-50/70 text-blue-900 ring-2 ring-blue-500/20'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <span className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shrink-0 ${
                  isSelected ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'
                }`}>
                  {optLabel}
                </span>
                <span className="text-base font-normal">{optText}</span>
              </button>
            );
          })}
        </div>

        <div className="flex justify-between items-center pt-4 border-t border-gray-100">
          <button
            type="button"
            disabled={currentIdx === 0}
            onClick={() => setCurrentIdx(Math.max(0, currentIdx - 1))}
            className="flex items-center gap-1 text-gray-500 px-4 py-2 text-sm font-medium hover:text-gray-700 disabled:opacity-30"
          >
            <ArrowLeft size={16} /> Previous
          </button>

          <button
            type="button"
            disabled={!isAnswered}
            onClick={handleNext}
            className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-blue-700 disabled:opacity-50 transition shadow-sm"
          >
            {currentIdx === questions.length - 1 ? 'Submit Assessment' : 'Next'}
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
