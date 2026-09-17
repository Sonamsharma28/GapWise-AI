import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import { LogIn, Sparkles, User, GraduationCap } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLoginSubmit = async (loginEmail, loginPass) => {
    setError('');
    setLoading(true);
    try {
      const loggedUser = await login(loginEmail, loginPass);
      if (loggedUser.role === 'teacher') {
        navigate('/teacher/dashboard');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleLoginSubmit(email, password);
  };

  const handleDemoLogin = (role) => {
    if (role === 'student') {
      setEmail('student@gapwise.ai');
      setPassword('demo123');
      handleLoginSubmit('student@gapwise.ai', 'demo123');
    } else {
      setEmail('teacher@gapwise.ai');
      setPassword('demo123');
      handleLoginSubmit('teacher@gapwise.ai', 'demo123');
    }
  };

  return (
    <Layout>
      <div className="max-w-md mx-auto my-12 bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
        <div className="text-center">
          <div className="bg-blue-50 p-3.5 rounded-2xl inline-block mb-3 text-blue-600">
            <LogIn size={28} />
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Welcome Back to GapWise</h2>
          <p className="text-gray-500 text-sm mt-1">Sign in to your student or teacher account</p>
        </div>

        {/* 1-Click Demo Accounts for Judges */}
        <div className="bg-blue-50/80 p-4 rounded-xl border border-blue-100 space-y-2">
          <div className="text-xs font-bold text-blue-900 flex items-center gap-1.5 uppercase tracking-wider">
            <Sparkles size={14} className="text-blue-600" /> One-Click SIH Demo Access
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleDemoLogin('student')}
              disabled={loading}
              className="flex items-center justify-center gap-1.5 bg-white hover:bg-blue-100/50 text-blue-700 font-semibold py-2 px-3 rounded-lg border border-blue-200 text-xs transition shadow-2xs"
            >
              <User size={14} /> Demo Student
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('teacher')}
              disabled={loading}
              className="flex items-center justify-center gap-1.5 bg-white hover:bg-indigo-100/50 text-indigo-700 font-semibold py-2 px-3 rounded-lg border border-indigo-200 text-xs transition shadow-2xs"
            >
              <GraduationCap size={14} /> Demo Teacher
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-3.5 rounded-xl text-sm border border-red-100 text-center font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. student@gapwise.ai"
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition disabled:opacity-50 shadow-md hover:shadow-lg"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="text-center text-sm text-gray-500 pt-2 border-t border-gray-100">
          Don't have an account?{' '}
          <Link to="/register" className="text-blue-600 font-bold hover:underline">
            Register here
          </Link>
        </div>
      </div>
    </Layout>
  );
}
