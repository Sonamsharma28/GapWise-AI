import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import {
  Brain,
  Target,
  LineChart,
  BookOpen,
  Layers,
  Users,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  GitBranch,
  RotateCw,
  ShieldAlert,
  GraduationCap
} from 'lucide-react';

export default function Landing() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative pt-12 pb-20 md:py-24 overflow-hidden">
        <div className="max-w-5xl mx-auto text-center px-4 space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200/80 px-4 py-1.5 rounded-full text-blue-700 text-xs font-semibold shadow-sm">
            <Sparkles size={14} className="text-blue-600" />
            Smart India Hackathon 2026 • Problem Statement SIH027
          </div>

          {/* Heading */}
          <h1 className="text-4xl sm:text-6xl font-extrabold text-gray-900 tracking-tight leading-tight">
            Don't just detect what students got wrong.{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
              Discover why.
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            An AI-powered learning diagnosis system that identifies conceptual and prerequisite gaps,
            generates topological learning paths, and continuously adapts through closed-loop reassessment.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <Link
              to="/register"
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3.5 rounded-xl font-bold text-base transition shadow-lg hover:shadow-xl hover:-translate-y-0.5"
            >
              Start Diagnostic Assessment <ArrowRight size={18} />
            </Link>
            <Link
              to="/knowledge-graph"
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-white hover:bg-gray-50 text-gray-800 border border-gray-200 px-8 py-3.5 rounded-xl font-semibold text-base transition shadow-sm"
            >
              Explore Knowledge Graph
            </Link>
          </div>

          {/* Demo Login Credentials Callout for Judges */}
          <div className="bg-blue-50/80 border border-blue-100 rounded-xl p-4 max-w-xl mx-auto text-left shadow-sm">
            <div className="text-xs font-bold uppercase tracking-wider text-blue-900 mb-2 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span> SIH Quick Demo Access:
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-blue-950 font-mono">
              <div className="bg-white/90 p-2 rounded border border-blue-100">
                <strong>Student:</strong> student@gapwise.ai<br />
                <strong>Pass:</strong> demo123
              </div>
              <div className="bg-white/90 p-2 rounded border border-blue-100">
                <strong>Teacher:</strong> teacher@gapwise.ai<br />
                <strong>Pass:</strong> demo123
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* The Core Problem vs GapWise AI */}
      <section className="py-16 bg-white border-y border-gray-100">
        <div className="max-w-5xl mx-auto px-4 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-3xl font-bold text-gray-900">Why Traditional EdTech Fails</h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-sm sm:text-base">
              Standard testing platforms provide surface-level scores without identifying the underlying root cause.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="p-6 rounded-2xl bg-red-50/60 border border-red-100 space-y-4">
              <div className="flex items-center gap-2 font-bold text-red-900">
                <ShieldAlert className="text-red-600" /> Traditional Assessment
              </div>
              <ul className="space-y-3 text-sm text-red-800">
                <li className="flex items-start gap-2">
                  <span className="text-red-500 font-bold">✕</span>
                  <span>Shows only binary outcomes: "Quadratic Equations = 40% (Weak)".</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-500 font-bold">✕</span>
                  <span>Forces students to re-read quadratic chapters when the actual gap is in basic factoring.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-500 font-bold">✕</span>
                  <span>Static, one-size-fits-all practice without prerequisite backtracking.</span>
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-2xl bg-green-50/60 border border-green-100 space-y-4">
              <div className="flex items-center gap-2 font-bold text-green-900">
                <Brain className="text-green-600" /> GapWise AI Engine
              </div>
              <ul className="space-y-3 text-sm text-green-900">
                <li className="flex items-start gap-2">
                  <CheckCircle2 size={18} className="text-green-600 shrink-0 mt-0.5" />
                  <span>Traces concept graph: <em>Basic Algebra → Algebraic Identities → Factorisation → Quadratic Equations</em>.</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 size={18} className="text-green-600 shrink-0 mt-0.5" />
                  <span>Pinpoints root gap: "Struggling with Quadratics because <strong>Factorisation</strong> is weak."</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 size={18} className="text-green-600 shrink-0 mt-0.5" />
                  <span>Generates topological path unlocking topics only when prerequisites are mastered.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* The 6-Step Adaptive Learning Loop */}
      <section id="how-it-works" className="py-20">
        <div className="max-w-5xl mx-auto px-4 space-y-12">
          <div className="text-center space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
              Continuous Adaptive Pipeline
            </span>
            <h2 className="text-3xl font-bold text-gray-900">How GapWise AI Works</h2>
            <p className="text-gray-500 text-sm sm:text-base max-w-xl mx-auto">
              From diagnostic testing to measurable mastery improvement in 6 steps.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <StepCard
              step="1"
              icon={<Target className="text-blue-600" />}
              title="Diagnostic Assessment"
              desc="Comprehensive multi-concept assessment mapped to difficulty and prerequisite metadata."
            />
            <StepCard
              step="2"
              icon={<Brain className="text-purple-600" />}
              title="AI Gap Detection"
              desc="Evaluates difficulty-weighted correctness and classifies each topic into Mastered, Developing, or Needs Attention."
            />
            <StepCard
              step="3"
              icon={<GitBranch className="text-red-600" />}
              title="Root-Cause Analysis"
              desc="Traverses the prerequisite graph backward to discover the exact foundational topic causing difficulty."
            />
            <StepCard
              step="4"
              icon={<Layers className="text-indigo-600" />}
              title="Personalized Path"
              desc="Generates an ordered roadmap prioritizing foundational root gaps before unlocking higher concepts."
            />
            <StepCard
              step="5"
              icon={<BookOpen className="text-emerald-600" />}
              title="Learn & Practice"
              desc="Study curriculum explanations, step-by-step worked examples, and solve adaptive practice questions."
            />
            <StepCard
              step="6"
              icon={<RotateCw className="text-amber-600" />}
              title="Reassess & Adapt"
              desc="Take targeted reassessments to verify mastery growth and compare Before vs. After score benchmarks."
            />
          </div>
        </div>
      </section>

      {/* Key Role Features (Student vs Teacher) */}
      <section className="py-16 bg-white border-t border-gray-100">
        <div className="max-w-5xl mx-auto px-4 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-3xl font-bold text-gray-900">Built for Students & Educators</h2>
            <p className="text-gray-500 text-sm sm:text-base">
              Dual-role architecture with secure role-based access control and granular analytics.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Student Feature Box */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-blue-50/50 to-white border border-blue-100 shadow-sm space-y-6">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-blue-600 text-white rounded-xl">
                  <GraduationCap size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">For Students</h3>
                  <p className="text-xs text-gray-500">Autonomous, explainable learning journey</p>
                </div>
              </div>

              <ul className="space-y-3 text-sm text-gray-700">
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-blue-600" />
                  <span>Explainable learning gap diagnosis with root-cause insights.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-blue-600" />
                  <span>Interactive 12-concept prerequisite knowledge graph.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-blue-600" />
                  <span>Context-aware AI Learning Mentor available 24/7.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-blue-600" />
                  <span>Real-time practice feedback with step-by-step mathematical reasoning.</span>
                </li>
              </ul>
            </div>

            {/* Teacher Feature Box */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-indigo-50/50 to-white border border-indigo-100 shadow-sm space-y-6">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-indigo-600 text-white rounded-xl">
                  <Users size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">For Teachers</h3>
                  <p className="text-xs text-gray-500">Actionable class & student-level diagnostics</p>
                </div>
              </div>

              <ul className="space-y-3 text-sm text-gray-700">
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  <span>Class-wide concept performance and struggling student counts.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  <span>Student deep-dive profiles showing historical mastery and learning gaps.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  <span>Targeted pedagogical intervention recommendations.</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  <span>Assessment completion rates and class mastery distribution.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className="py-16 bg-gradient-to-br from-blue-600 to-indigo-800 text-white text-center">
        <div className="max-w-3xl mx-auto px-4 space-y-6">
          <h2 className="text-3xl font-extrabold">Ready to Discover Your Learning Gaps?</h2>
          <p className="text-blue-100 text-base">
            Take the Class 9–10 Mathematics diagnostic assessment and experience AI root-cause analysis in action.
          </p>
          <div className="flex justify-center gap-4 pt-2">
            <Link
              to="/register"
              className="bg-white text-blue-700 hover:bg-blue-50 px-8 py-3.5 rounded-xl font-bold text-base transition shadow-lg"
            >
              Get Started Free
            </Link>
            <Link
              to="/login"
              className="bg-blue-700/60 hover:bg-blue-700 text-white border border-white/20 px-8 py-3.5 rounded-xl font-bold text-base transition"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* SIH Footer Note */}
      <footer className="bg-slate-900 text-slate-400 py-8 text-center text-xs space-y-2">
        <div className="font-semibold text-slate-200">
          GAPWISE AI — Built for Smart India Hackathon 2026 (SIH027)
        </div>
        <div>
          Theme: EdTech & Adaptive Learning • Team: HexaMind • Category: Software
        </div>
      </footer>
    </Layout>
  );
}

function StepCard({ step, icon, title, desc }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition space-y-3 relative group">
      <div className="flex items-center justify-between">
        <div className="p-3 bg-gray-50 rounded-xl group-hover:scale-105 transition">{icon}</div>
        <span className="text-3xl font-black text-gray-200 group-hover:text-blue-200 transition font-mono">
          0{step}
        </span>
      </div>
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>
      <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}
