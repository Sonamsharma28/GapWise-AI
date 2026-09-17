import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { sendMessage } from '../api/ai';
import { getDashboard } from '../api/student';
import { useAuth } from '../context/AuthContext';
import WrongQuestionExplainer from '../components/WrongQuestionExplainer';
import { Send, User, Bot, Sparkles, AlertCircle, RefreshCw, GraduationCap, ChevronRight, BookOpen } from 'lucide-react';

export default function AIMentor() {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const qIdParam = searchParams.get('questionId');
  const qNumParam = searchParams.get('questionNum');

  const [incorrectList, setIncorrectList] = useState([]);
  const [dashLoaded, setDashLoaded] = useState(false);

  // Active question explainer panel (shown alongside or before chat)
  const [activeExplainerQId, setActiveExplainerQId] = useState(null);
  const [activeExplainerQNum, setActiveExplainerQNum] = useState(null);
  const [activeExplainerConceptId, setActiveExplainerConceptId] = useState(null);
  const [activeExplainerConceptName, setActiveExplainerConceptName] = useState(null);

  const [messages, setMessages] = useState([]); // greeting built after dashboard loads
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const initialTriggered = useRef(false);

  // 1. Load dashboard to get wrong questions list + build personalised greeting
  useEffect(() => {
    getDashboard()
      .then(res => {
        const wrongQs = res.data?.recent_incorrect_questions || [];
        setIncorrectList(wrongQs);
        setDashLoaded(true);

        // Build dynamic greeting listing the wrong question numbers
        let greetingText = `Hello ${user?.name || 'there'}! 👋 I am your **Personalized GapWise AI Math Teacher**.\n\nI have full access to your diagnostic assessment results, your concept mastery profile, and your prerequisite gaps.\n\n`;

        if (wrongQs.length > 0) {
          const qNums = wrongQs.map(q => `Q#${q.question_num} (${q.concept_name})`).join(', ');
          greetingText += `📊 **From your latest assessment, you missed:** ${qNums}.\n\n`;
          greetingText += `👆 **Click any button below** to get a full personalized step-by-step explanation for that question — I will break down exactly why your answer was wrong and teach you the correct approach so clearly that you won't need any other teacher!\n\n`;
          greetingText += `You can also type any question or concept name below and I will help you master it. Let's go! 🚀`;
        } else {
          greetingText += `Ask me to break down any concept, explain a question, or guide your next study step. I know your full learning profile!`;
        }

        setMessages([{ role: 'ai', text: greetingText }]);
      })
      .catch(err => {
        console.error(err);
        setDashLoaded(true);
        setMessages([{
          role: 'ai',
          text: `Hello ${user?.name || 'there'}! 👋 I am your **Personalized AI Math Teacher**.\n\nAsk me to explain any question you got wrong, or any concept you want to understand better!`
        }]);
      });
  }, []);

  // 2. If arriving with a questionId URL param, open structured explainer + auto-send chat message
  useEffect(() => {
    if (qIdParam && dashLoaded && !initialTriggered.current) {
      initialTriggered.current = true;
      const qNum = qNumParam ? parseInt(qNumParam) : null;
      const qId = parseInt(qIdParam);

      // Find metadata from incorrect list (may or may not be loaded yet)
      const qInfo = incorrectList.find(q => q.question_id === qId);

      setActiveExplainerQId(qId);
      setActiveExplainerQNum(qNum);
      setActiveExplainerConceptId(qInfo?.concept_id || null);
      setActiveExplainerConceptName(qInfo?.concept_name || null);

      // Also send a chat message
      const qNumText = qNum ? `Question #${qNum}` : 'this question';
      const prompt = `Please also give me a short summary of why I got ${qNumText} wrong and what I should remember.`;
      handleAutoSend(prompt, qId, qNum);
    }
  }, [dashLoaded, qIdParam, qNumParam]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleAutoSend = async (userMsg, targetQId, targetQNum) => {
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setLoading(true);
    try {
      const res = await sendMessage({
        message: userMsg,
        question_id: targetQId,
        question_num: targetQNum
      });
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          text: res.data.response,
          suggestedConcept: res.data.suggested_concept
        }
      ]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I had trouble processing that. Please try asking again!' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setLoading(true);
    try {
      const res = await sendMessage({ message: userMsg });
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          text: res.data.response,
          suggestedConcept: res.data.suggested_concept
        }
      ]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I am having trouble connecting right now. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handlePillClick = (q) => {
    // Open structured explainer panel
    setActiveExplainerQId(q.question_id);
    setActiveExplainerQNum(q.question_num);
    setActiveExplainerConceptId(q.concept_id);
    setActiveExplainerConceptName(q.concept_name);
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleGeneralPill = (text) => {
    setInput(text);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* ── AI Teacher Header Card ── */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-2xl text-white p-6 flex items-center justify-between shadow-md">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center">
            <GraduationCap size={28} />
          </div>
          <div>
            <h2 className="text-xl font-black flex items-center gap-2">
              GapWise AI Math Teacher
              <span className="bg-emerald-400/20 text-emerald-300 text-xs px-2 py-0.5 rounded-full border border-emerald-400/30">
                Online 24/7
              </span>
            </h2>
            <p className="text-blue-100 text-sm mt-0.5">
              Personalized for <strong>{user?.name || 'Student'}</strong> • Grounded in your Assessment & Prerequisite Profile
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-xs bg-white/10 px-3 py-2 rounded-xl border border-white/15">
          <Sparkles size={14} className="text-amber-300" />
          <span>Prerequisite-Aware Teaching</span>
        </div>
      </div>

      {/* ── Wrong Questions Quick-Select Bar ── */}
      {incorrectList.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-sm mb-3">
            <AlertCircle size={16} className="text-amber-600" />
            <span>Questions you missed — click any to get a full AI explanation:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {incorrectList.map((q) => (
              <button
                key={q.question_id}
                onClick={() => handlePillClick(q)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition border shadow-xs ${
                  activeExplainerQId === q.question_id
                    ? 'bg-indigo-600 text-white border-indigo-700'
                    : 'bg-white hover:bg-indigo-50 text-amber-900 border-amber-200 hover:border-indigo-300'
                }`}
              >
                <span className="bg-red-100 text-red-700 px-1.5 py-0.5 rounded font-black text-xs">Q#{q.question_num}</span>
                {q.concept_name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Inline WrongQuestionExplainer Panel (when a question is selected) ── */}
      {activeExplainerQId && (
        <WrongQuestionExplainer
          questionId={activeExplainerQId}
          questionNum={activeExplainerQNum}
          conceptId={activeExplainerConceptId}
          conceptName={activeExplainerConceptName}
          onClose={() => {
            setActiveExplainerQId(null);
            setActiveExplainerQNum(null);
          }}
        />
      )}

      {/* ── Chat Area ── */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden flex flex-col" style={{ minHeight: '480px' }}>
        {/* Chat Messages */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6 bg-slate-50/50" style={{ maxHeight: '520px' }}>
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 max-w-[92%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-xs ${
                msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white'
              }`}>
                {msg.role === 'user' ? <User size={18} /> : <Bot size={20} />}
              </div>

              <div className={`p-4 sm:p-5 rounded-2xl shadow-xs text-sm sm:text-base leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-none'
                  : 'bg-white text-gray-800 border border-gray-200/80 rounded-tl-none'
              }`}>
                <FormattedMessage text={msg.text} isUser={msg.role === 'user'} />

                {/* Practice link if AI suggested a concept */}
                {msg.role === 'ai' && msg.suggestedConcept && (
                  <div className="mt-3 pt-3 border-t border-gray-100 flex flex-wrap gap-2">
                    <Link
                      to="/practice"
                      className="flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-2.5 py-1.5 rounded-lg transition"
                    >
                      <ChevronRight size={13} /> Practice {msg.suggestedConcept}
                    </Link>
                    <Link
                      to="/learning/path"
                      className="flex items-center gap-1 text-xs font-bold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 px-2.5 py-1.5 rounded-lg transition"
                    >
                      <BookOpen size={13} /> Open Learning Path
                    </Link>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 text-white flex items-center justify-center shrink-0 shadow-xs">
                <Bot size={20} />
              </div>
              <div className="p-4 bg-white rounded-2xl rounded-tl-none border border-gray-200 text-gray-500 text-sm flex items-center gap-2 shadow-xs">
                <RefreshCw size={16} className="animate-spin text-blue-600" />
                <span>AI Teacher is preparing your personalised explanation...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* General Quick Prompts */}
        <div className="px-4 py-2.5 bg-gray-50 border-t border-gray-100 flex flex-wrap gap-2 text-xs">
          <button
            onClick={() => handleGeneralPill("Why am I finding Quadratic Equations difficult?")}
            className="bg-white hover:bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
          >
            🔍 Why is Quadratics hard for me?
          </button>
          <button
            onClick={() => handleGeneralPill("Explain how to factorise quadratic equations in 3 easy steps")}
            className="bg-white hover:bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
          >
            💡 3-Step Factoring Method
          </button>
          <button
            onClick={() => handleGeneralPill("Give me a simple practice question to test my understanding")}
            className="bg-white hover:bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
          >
            ✍️ Give me a test question
          </button>
          <button
            onClick={() => handleGeneralPill("What should I study next based on my gaps?")}
            className="bg-white hover:bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full border border-gray-200 transition"
          >
            🗺️ What should I study next?
          </button>
        </div>

        {/* Chat Input */}
        <form onSubmit={handleSend} className="p-4 bg-white border-t border-gray-200 flex gap-2 items-center">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask a doubt or type: 'Explain Question #3' or 'How do I solve quadratics?'..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm bg-gray-50 focus:bg-white transition"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl disabled:opacity-40 font-bold transition shadow-sm flex items-center gap-1.5 shrink-0"
          >
            <Send size={16} />
            <span className="hidden sm:inline">Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}

function FormattedMessage({ text, isUser }) {
  if (isUser) return <span>{text}</span>;

  const lines = text.split('\n');
  return (
    <div className="space-y-2">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (trimmed.startsWith('### ')) {
          return <h3 key={idx} className="font-bold text-gray-900 text-base mt-2 mb-1">{trimmed.replace('### ', '')}</h3>;
        }
        if (trimmed.startsWith('#### ')) {
          return <h4 key={idx} className="font-bold text-gray-800 text-sm mt-2 mb-1">{trimmed.replace('#### ', '')}</h4>;
        }
        if (trimmed.startsWith('> ')) {
          return (
            <blockquote key={idx} className="border-l-4 border-blue-500 pl-3 py-1 my-1.5 bg-blue-50/50 rounded-r text-gray-800 text-xs sm:text-sm font-medium">
              {trimmed.replace('> ', '')}
            </blockquote>
          );
        }
        if (trimmed.startsWith('---')) {
          return <hr key={idx} className="my-2 border-gray-200" />;
        }
        if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          return <li key={idx} className="ml-4 list-disc text-gray-700 text-xs sm:text-sm">{trimmed.substring(2)}</li>;
        }
        if (!trimmed) {
          return <div key={idx} className="h-1" />;
        }
        // Handle **bold** inline
        const parts = trimmed.split(/(\*\*[^*]+\*\*)/g);
        return (
          <p key={idx} className="text-gray-800 text-xs sm:text-sm">
            {parts.map((part, j) =>
              part.startsWith('**') && part.endsWith('**')
                ? <strong key={j}>{part.slice(2, -2)}</strong>
                : part
            )}
          </p>
        );
      })}
    </div>
  );
}
