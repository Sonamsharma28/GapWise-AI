import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { getPracticeQuestions, submitPractice, getConcept } from '../api/learning';
import { getConcepts } from '../api/graph';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import { CheckCircle2, XCircle, ArrowRight, RotateCcw, Award, Lightbulb, BookOpen } from 'lucide-react';

export default function Practice() {
  const [searchParams, setSearchParams] = useSearchParams();
  const conceptIdParam = searchParams.get('concept');

  const [conceptsList, setConceptsList] = useState([]);
  const [selectedConceptId, setSelectedConceptId] = useState(conceptIdParam ? parseInt(conceptIdParam) : null);
  const [conceptInfo, setConceptInfo] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedOption, setSelectedOption] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [sessionScore, setSessionScore] = useState({ correct: 0, total: 0 });
  const [isFinished, setIsFinished] = useState(false);

  useEffect(() => {
    // Load concepts list for selector
    getConcepts()
      .then(res => {
        const cList = res.data.concepts || [];
        setConceptsList(cList);
        if (!selectedConceptId && cList.length > 0) {
          // Default to first concept needing attention, or first in list
          const weak = cList.find(c => c.status === 'needs_attention') || cList[0];
          setSelectedConceptId(weak.id);
        }
      })
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    if (!selectedConceptId) return;

    setLoading(true);
    setIsFinished(false);
    setCurrentIdx(0);
    setFeedback(null);
    setSelectedOption('');
    setSessionScore({ correct: 0, total: 0 });

    Promise.all([
      getConcept(selectedConceptId),
      getPracticeQuestions(selectedConceptId)
    ])
      .then(([cRes, qRes]) => {
        setConceptInfo(cRes.data);
        setQuestions(qRes.data || []);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [selectedConceptId]);

  const handleOptionSelect = (label) => {
    if (!feedback) {
      setSelectedOption(label);
    }
  };

  const handleCheckAnswer = async () => {
    if (!selectedOption || feedback) return;

    const q = questions[currentIdx];
    setSubmitting(true);

    try {
      const res = await submitPractice({
        question_id: q.id,
        answer: selectedOption,
        concept_id: selectedConceptId
      });

      setFeedback(res.data);
      setSessionScore(prev => ({
        correct: prev.correct + (res.data.is_correct ? 1 : 0),
        total: prev.total + 1
      }));

      // Update concept info mastery
      if (res.data.new_mastery_score !== undefined) {
        setConceptInfo(prev => ({
          ...prev,
          mastery_score: res.data.new_mastery_score,
          mastery_status: res.data.new_status
        }));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
      setSelectedOption('');
      setFeedback(null);
    } else {
      setIsFinished(true);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header with Concept Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div>
          <span className="text-xs font-bold uppercase text-blue-600 tracking-wider">Targeted Practice</span>
          <h1 className="text-xl font-bold text-gray-900 mt-1">{conceptInfo?.name || "Practice Session"}</h1>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedConceptId || ''}
            onChange={(e) => {
              const newId = parseInt(e.target.value);
              setSelectedConceptId(newId);
              setSearchParams({ concept: newId });
            }}
            className="text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none font-medium"
          >
            {conceptsList.map(c => (
              <option key={c.id} value={c.id}>
                {c.name} ({Math.round(c.score || 0)}%)
              </option>
            ))}
          </select>
          {conceptInfo && <ConceptStatusBadge status={conceptInfo.mastery_status} />}
        </div>
      </div>

      {!isFinished ? (
        questions.length > 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 space-y-6">
            {/* Progress & Difficulty Bar */}
            <div className="flex items-center justify-between text-sm text-gray-500 pb-4 border-b border-gray-100">
              <span className="font-semibold text-gray-700">Question {currentIdx + 1} of {questions.length}</span>
              <div className="flex items-center gap-2">
                <span>Difficulty:</span>
                <span className="px-2 py-0.5 bg-blue-50 text-blue-700 font-bold rounded text-xs">
                  Level {questions[currentIdx]?.difficulty}/5
                </span>
              </div>
            </div>

            {/* Question Text */}
            <div className="text-lg font-medium text-gray-900 leading-relaxed">
              {questions[currentIdx]?.text}
            </div>

            {/* Options */}
            <div className="space-y-3">
              {questions[currentIdx]?.options?.map((opt) => {
                const isSelected = selectedOption === opt.label;
                let optionStyle = "border-gray-200 hover:border-blue-400 hover:bg-blue-50/40";
                
                if (feedback) {
                  if (opt.label === feedback.correct_answer) {
                    optionStyle = "border-green-500 bg-green-50 text-green-900 font-semibold";
                  } else if (isSelected && !feedback.is_correct) {
                    optionStyle = "border-red-500 bg-red-50 text-red-900";
                  } else {
                    optionStyle = "border-gray-200 opacity-60";
                  }
                } else if (isSelected) {
                  optionStyle = "border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20";
                }

                return (
                  <button
                    key={opt.id}
                    onClick={() => handleOptionSelect(opt.label)}
                    disabled={!!feedback}
                    className={`w-full text-left p-4 rounded-xl border-2 transition flex items-center gap-4 ${optionStyle}`}
                  >
                    <span className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shrink-0 ${
                      isSelected ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {opt.label}
                    </span>
                    <span className="flex-1 text-base">{opt.text}</span>
                  </button>
                );
              })}
            </div>

            {/* Feedback / Step-by-Step Explanation Card */}
            {feedback && (
              <div className={`p-5 rounded-xl border ${
                feedback.is_correct ? 'bg-green-50/70 border-green-200' : 'bg-red-50/70 border-red-200'
              } space-y-3 animate-fadeIn`}>
                <div className="flex items-center gap-2 font-bold text-base">
                  {feedback.is_correct ? (
                    <>
                      <CheckCircle2 className="text-green-600" />
                      <span className="text-green-900">Correct! Excellent problem solving.</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="text-red-600" />
                      <span className="text-red-900">Incorrect. The correct answer is ({feedback.correct_answer}).</span>
                    </>
                  )}
                </div>

                <div className="text-sm text-gray-700 pt-2 border-t border-gray-200/60 flex items-start gap-2">
                  <Lightbulb size={18} className="text-yellow-600 shrink-0 mt-0.5" />
                  <div>
                    <strong className="block text-gray-900 mb-1">Step-by-Step Explanation:</strong>
                    <p className="leading-relaxed">{feedback.explanation}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Bottom Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
              <Link
                to={`/learning/concept/${selectedConceptId}`}
                className="text-sm font-medium text-gray-500 hover:text-blue-600 flex items-center gap-1.5"
              >
                <BookOpen size={16} /> Review Learning Material
              </Link>

              {!feedback ? (
                <button
                  onClick={handleCheckAnswer}
                  disabled={!selectedOption || submitting}
                  className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition"
                >
                  {submitting ? 'Checking...' : 'Check Answer'}
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 flex items-center gap-2 transition"
                >
                  {currentIdx < questions.length - 1 ? 'Next Question' : 'Finish Practice'}
                  <ArrowRight size={16} />
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center">
            <p className="text-gray-500">No practice questions available for this concept yet.</p>
          </div>
        )
      ) : (
        /* Summary Card */
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center space-y-6">
          <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto">
            <Award size={36} />
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900">Practice Session Complete!</h2>
            <p className="text-gray-600 mt-1">
              You answered <span className="font-bold text-blue-600">{sessionScore.correct}</span> out of{' '}
              <span className="font-bold text-gray-800">{sessionScore.total}</span> questions correctly.
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 inline-block text-left min-w-[280px]">
            <div className="text-xs text-gray-500 font-bold uppercase mb-1">Updated Mastery for {conceptInfo?.name}</div>
            <div className="flex items-center justify-between">
              <span className="text-2xl font-extrabold text-blue-600">{Math.round(conceptInfo?.mastery_score || 0)}%</span>
              <ConceptStatusBadge status={conceptInfo?.mastery_status} />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <button
              onClick={() => {
                setCurrentIdx(0);
                setSelectedOption('');
                setFeedback(null);
                setIsFinished(false);
                setSessionScore({ correct: 0, total: 0 });
              }}
              className="flex items-center justify-center gap-2 px-6 py-2.5 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
            >
              <RotateCcw size={16} /> Practice Again
            </button>
            <Link
              to="/reassessment"
              className="flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700"
            >
              Take Reassessment
            </Link>
            <Link
              to="/learning/path"
              className="flex items-center justify-center gap-2 bg-gray-100 text-gray-800 px-6 py-2.5 rounded-lg font-medium hover:bg-gray-200"
            >
              Back to Learning Path
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
