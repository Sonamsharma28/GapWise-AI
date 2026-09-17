import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getConcept } from '../api/learning';
import { sendMessage } from '../api/ai';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import {
  BookOpen,
  Key,
  CheckSquare,
  AlertTriangle,
  PlayCircle,
  ArrowLeft,
  Lightbulb,
  GraduationCap,
  Sparkles,
  Bot,
  Send,
  HelpCircle,
  Layers,
  CheckCircle2,
  ChevronRight,
  RefreshCw,
  Target
} from 'lucide-react';

export default function ConceptLearning() {
  const { id } = useParams();
  const [concept, setConcept] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'theory', 'formulas', 'examples', 'pitfalls'
  
  // Interactive AI Assistant inside the concept page
  const [aiQuery, setAiQuery] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [aiMessages, setAiMessages] = useState([]);

  useEffect(() => {
    getConcept(id)
      .then(res => {
        setConcept(res.data);
        // Default AI intro message for this concept
        setAiMessages([
          {
            role: 'ai',
            text: `Hi! I am your AI Math Teacher for **${res.data.name}**.\n\nStuck on any step, need another numerical example, or want me to explain this in simpler terms? Just ask below!`
          }
        ]);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  const handleAskAI = async (e, customPrompt = null) => {
    e?.preventDefault();
    const prompt = customPrompt || aiQuery;
    if (!prompt.trim() || aiLoading) return;

    setAiMessages(prev => [...prev, { role: 'user', text: prompt }]);
    if (!customPrompt) setAiQuery('');
    setAiLoading(true);

    try {
      const res = await sendMessage({
        message: prompt,
        concept_id: parseInt(id)
      });
      setAiMessages(prev => [...prev, { role: 'ai', text: res.data.response }]);
    } catch (err) {
      console.error(err);
      setAiMessages(prev => [
        ...prev,
        { role: 'ai', text: "Sorry, I had trouble answering that. Please try asking again!" }
      ]);
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!concept) {
    return (
      <div className="max-w-3xl mx-auto text-center py-16 space-y-4">
        <div className="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto">
          <AlertTriangle size={32} />
        </div>
        <h2 className="text-xl font-bold text-gray-900">Concept Module Not Found</h2>
        <p className="text-gray-500 text-sm">We could not load the learning module for this concept.</p>
        <Link to="/learning/path" className="inline-flex items-center gap-1.5 bg-blue-600 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow-sm hover:bg-blue-700 transition">
          <ArrowLeft size={16} /> Back to Learning Path
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* ── Top Breadcrumb Bar ── */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Link
          to="/learning/path"
          className="inline-flex items-center gap-1.5 text-sm font-bold text-blue-600 hover:text-blue-800 transition"
        >
          <ArrowLeft size={16} /> Back to Personalized Learning Path
        </Link>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-800 px-3 py-1 rounded-full border border-blue-100">
            Class {concept.grade} Mathematics
          </span>
          <span className="text-xs font-bold uppercase tracking-wider bg-purple-50 text-purple-800 px-3 py-1 rounded-full border border-purple-100">
            Difficulty: {concept.difficulty}/5
          </span>
        </div>
      </div>

      {/* ── Hero Banner ── */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-3xl text-white p-6 sm:p-8 shadow-lg relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="flex items-center gap-2 text-blue-200 text-xs font-bold uppercase tracking-wider">
            <GraduationCap size={18} />
            <span>Mastery Learning Module</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-black tracking-tight">{concept.name}</h1>
          <p className="text-blue-100 text-sm sm:text-base leading-relaxed">
            {concept.description}
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <Link
              to={`/practice`}
              className="inline-flex items-center gap-2 bg-white text-indigo-900 font-bold px-5 py-2.5 rounded-xl text-sm shadow-md hover:bg-blue-50 transition"
            >
              <PlayCircle size={18} className="text-indigo-600" /> Start Adaptive Practice
            </Link>
            <a
              href="#ai-teacher-section"
              className="inline-flex items-center gap-2 bg-white/15 hover:bg-white/25 text-white font-bold px-4 py-2.5 rounded-xl text-sm transition border border-white/20"
            >
              <Bot size={18} /> Ask AI Teacher About This
            </a>
          </div>
        </div>
      </div>

      {/* ── Main Layout: Content Grid & Sticky Sidebar ── */}
      <div className="grid lg:grid-cols-3 gap-8 items-start">
        {/* Left Column: Educational Content Sections */}
        <div className="lg:col-span-2 space-y-8">
          {/* Navigation View Switcher */}
          <div className="flex border-b border-gray-200 bg-white p-1.5 rounded-2xl shadow-xs gap-1 overflow-x-auto text-xs sm:text-sm font-bold">
            <button
              onClick={() => setActiveTab('all')}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl transition shrink-0 ${
                activeTab === 'all'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Layers size={16} /> Complete Guide (All-in-One)
            </button>
            <button
              onClick={() => setActiveTab('theory')}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl transition shrink-0 ${
                activeTab === 'theory'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <BookOpen size={16} /> Theory
            </button>
            <button
              onClick={() => setActiveTab('formulas')}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl transition shrink-0 ${
                activeTab === 'formulas'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Key size={16} /> Formulas
            </button>
            <button
              onClick={() => setActiveTab('examples')}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl transition shrink-0 ${
                activeTab === 'examples'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <CheckSquare size={16} /> Numerical Walkthroughs
            </button>
            <button
              onClick={() => setActiveTab('pitfalls')}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl transition shrink-0 ${
                activeTab === 'pitfalls'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <AlertTriangle size={16} /> Common Traps
            </button>
          </div>

          {/* ── SECTION 1: THEORETICAL FOUNDATION ── */}
          {(activeTab === 'all' || activeTab === 'theory') && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 space-y-4">
              <div className="flex items-center gap-2.5 text-blue-900 font-black text-lg border-b border-gray-100 pb-3">
                <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center">
                  <BookOpen size={18} />
                </div>
                <span>1. Theoretical Foundations & Core Concepts</span>
              </div>

              <div className="prose prose-blue max-w-none text-gray-700 leading-relaxed text-sm sm:text-base space-y-4">
                <p className="whitespace-pre-line bg-blue-50/40 p-5 rounded-2xl border border-blue-100/60 font-normal">
                  {concept.explanation || "Comprehensive theoretical explanation is being loaded."}
                </p>
              </div>

              {/* Theory Quick Check */}
              <div className="bg-indigo-50/60 rounded-xl p-4 border border-indigo-100 flex items-start gap-3 text-xs sm:text-sm text-indigo-950">
                <Sparkles size={18} className="text-indigo-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Why this matters: </span>
                  Understanding the theoretical rules first makes solving numerical problems 10x faster because you recognize the structure instantly instead of guessing!
                </div>
              </div>
            </div>
          )}

          {/* ── SECTION 2: FORMULAS & KEY IDEAS ── */}
          {(activeTab === 'all' || activeTab === 'formulas') && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 space-y-4">
              <div className="flex items-center gap-2.5 text-indigo-900 font-black text-lg border-b border-gray-100 pb-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center">
                  <Key size={18} />
                </div>
                <span>2. Key Formulas, Identities & Core Rules</span>
              </div>

              <p className="text-xs sm:text-sm text-gray-500">
                Memorize and understand these essential mathematical principles for Class {concept.grade} exams:
              </p>

              <div className="grid gap-3">
                {concept.keyIdeas?.map((idea, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-blue-50/70 to-indigo-50/50 rounded-xl border border-blue-100 text-sm font-medium text-blue-950 shadow-2xs"
                  >
                    <span className="w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span className="leading-relaxed">{idea}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── SECTION 3: STEP-BY-STEP NUMERICAL WORKED EXAMPLES ── */}
          {(activeTab === 'all' || activeTab === 'examples') && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 space-y-5">
              <div className="flex items-center gap-2.5 text-emerald-900 font-black text-lg border-b border-gray-100 pb-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <CheckSquare size={18} />
                </div>
                <span>3. Step-by-Step Numerical Worked Example</span>
              </div>

              <p className="text-xs sm:text-sm text-gray-500">
                Observe how standard formulas are applied with exact numbers and clear calculations:
              </p>

              <div className="bg-slate-900 text-slate-100 p-6 rounded-2xl font-mono text-xs sm:text-sm leading-relaxed whitespace-pre-line shadow-inner border border-slate-800">
                {concept.workedExample || "Step-by-step worked example walkthrough."}
              </div>

              <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 text-xs sm:text-sm text-emerald-900 flex items-start gap-3">
                <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold">Golden Method:</div>
                  Always write the formula first, substitute values with brackets to prevent sign errors, and verify the final unit or signs.
                </div>
              </div>
            </div>
          )}

          {/* ── SECTION 4: COMMON PITFALLS & EXAM TRAPS ── */}
          {(activeTab === 'all' || activeTab === 'pitfalls') && (
            <div className="bg-white rounded-2xl shadow-sm border border-red-100 p-6 sm:p-8 space-y-4">
              <div className="flex items-center gap-2.5 text-red-900 font-black text-lg border-b border-red-100 pb-3">
                <div className="w-8 h-8 rounded-lg bg-red-100 text-red-700 flex items-center justify-center">
                  <AlertTriangle size={18} />
                </div>
                <span>4. Common Misconceptions & Traps to Avoid</span>
              </div>

              <p className="text-xs sm:text-sm text-red-700">
                These are the top errors students make in this topic. Don't fall into these traps!
              </p>

              <div className="space-y-3">
                {concept.commonMistakes?.map((mistake, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 p-4 bg-red-50/80 rounded-xl border border-red-200 text-sm text-red-900"
                  >
                    <AlertTriangle size={18} className="text-red-500 shrink-0 mt-0.5" />
                    <span className="leading-relaxed font-medium">{mistake}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── SECTION 5: INLINE AI TEACHER TUTOR ── */}
          <div id="ai-teacher-section" className="bg-white rounded-2xl shadow-sm border border-indigo-200 p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2.5 text-indigo-950 font-black text-lg">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center">
                  <Bot size={18} />
                </div>
                <span>Ask AI Teacher About {concept.name}</span>
              </div>
              <span className="bg-indigo-50 text-indigo-700 text-xs font-bold px-2.5 py-1 rounded-full border border-indigo-100">
                Instant Explanations
              </span>
            </div>

            <p className="text-xs sm:text-sm text-gray-600">
              Have a doubt on this topic? Ask the AI Teacher to break down formulas, give another numerical problem, or simplify any difficult step.
            </p>

            {/* Quick Prompt Helper Buttons */}
            <div className="flex flex-wrap gap-2 text-xs">
              <button
                onClick={(e) => handleAskAI(e, `Explain the core concept of ${concept.name} in simple everyday words.`)}
                className="bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
              >
                💡 Explain in simple terms
              </button>
              <button
                onClick={(e) => handleAskAI(e, `Give me another step-by-step numerical problem on ${concept.name} with full working.`)}
                className="bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
              >
                ✍️ Give another worked example
              </button>
              <button
                onClick={(e) => handleAskAI(e, `What are the most common exam questions asked from ${concept.name}?`)}
                className="bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
              >
                🎯 Top exam questions
              </button>
            </div>

            {/* AI Chat History */}
            <div className="space-y-4 max-h-96 overflow-y-auto p-4 bg-slate-50/70 rounded-2xl border border-gray-200/80">
              {aiMessages.map((msg, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white ml-auto max-w-[85%]'
                      : 'bg-white text-gray-800 border border-gray-200/80 mr-auto max-w-[95%] shadow-2xs'
                  }`}
                >
                  <p className="whitespace-pre-line font-medium">{msg.text}</p>
                </div>
              ))}
              {aiLoading && (
                <div className="flex items-center gap-2 p-3 text-xs text-indigo-700 bg-white rounded-xl border border-indigo-100 shadow-2xs">
                  <RefreshCw size={14} className="animate-spin text-indigo-600" />
                  <span>AI Teacher is preparing a clear explanation...</span>
                </div>
              )}
            </div>

            {/* Query Form */}
            <form onSubmit={handleAskAI} className="flex gap-2">
              <input
                type="text"
                value={aiQuery}
                onChange={e => setAiQuery(e.target.value)}
                placeholder={`Ask anything about ${concept.name}...`}
                className="flex-1 px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-xs sm:text-sm bg-gray-50 focus:bg-white transition"
              />
              <button
                type="submit"
                disabled={aiLoading || !aiQuery.trim()}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl font-bold text-xs sm:text-sm transition disabled:opacity-40 flex items-center gap-1.5 shrink-0 shadow-sm"
              >
                <Send size={15} />
                <span>Ask</span>
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: Sticky Status & Next Step Card */}
        <div className="space-y-6 sticky top-6">
          {/* Current Mastery Card */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-gray-900 text-xs uppercase tracking-wider">Your Mastery</h3>
              <ConceptStatusBadge status={concept.mastery_status} />
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-black text-blue-600">{Math.round(concept.mastery_score)}%</span>
              <span className="text-gray-400 text-xs font-semibold">Mastery Level</span>
            </div>

            <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div
                className={`h-2.5 rounded-full transition-all duration-500 ${
                  concept.mastery_score >= 75
                    ? 'bg-green-500'
                    : concept.mastery_score >= 40
                    ? 'bg-amber-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${Math.max(concept.mastery_score, 8)}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500">
              Practice questions to increase your mastery and unlock advanced topics!
            </p>
          </div>

          {/* Action Card: Start Practice */}
          <div className="bg-gradient-to-br from-blue-600 via-indigo-600 to-indigo-700 p-6 rounded-2xl text-white shadow-md space-y-4">
            <div className="flex items-center gap-2 font-bold text-sm">
              <PlayCircle size={20} />
              <span>Ready to Test Yourself?</span>
            </div>
            <p className="text-blue-100 text-xs leading-relaxed">
              Attempt concept-specific practice questions with immediate mathematical feedback to boost your score.
            </p>
            <Link
              to={`/practice`}
              className="flex items-center justify-center gap-2 bg-white text-indigo-900 py-3 px-4 rounded-xl font-bold text-sm hover:bg-blue-50 transition w-full shadow-sm"
            >
              Start Practice Session <ChevronRight size={16} />
            </Link>
          </div>

          {/* AI Mentor Quick Link */}
          <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 space-y-3">
            <div className="flex items-center gap-2 font-bold text-gray-900 text-sm">
              <Bot size={18} className="text-indigo-600" />
              <span>Full AI Mentor Chat</span>
            </div>
            <p className="text-xs text-gray-500 leading-relaxed">
              Want a comprehensive diagnostic review across all 12 concepts?
            </p>
            <Link
              to="/ai-mentor"
              className="flex items-center justify-center gap-1.5 text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 py-2.5 px-3 rounded-xl text-xs font-bold transition w-full"
            >
              Open AI Mentor Room &rarr;
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
