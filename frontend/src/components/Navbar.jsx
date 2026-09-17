import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BookOpen, BarChart3, Brain, GraduationCap, Users, LogOut, Menu, X, Network, FileDown } from 'lucide-react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinks = isAuthenticated && user ? (
    user.role === 'teacher' ? (
      <>
        <Link to="/teacher/dashboard" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><BarChart3 size={18}/> Teacher Dashboard</Link>
        <Link to="/knowledge-graph" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><Network size={18}/> Knowledge Graph</Link>
        <a href="/GapWise_AI_SIH2026_Pitch_and_Architecture.pdf" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700 flex items-center gap-1 font-semibold bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200"><FileDown size={16}/> Pitch PDF</a>
      </>
    ) : (
      <>
        <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><BarChart3 size={18}/> Dashboard</Link>
        <Link to="/knowledge-graph" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><Network size={18}/> Knowledge Graph</Link>
        <Link to="/learning/path" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><BookOpen size={18}/> Learning Path</Link>
        <Link to="/practice" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium">Practice</Link>
        <Link to="/progress" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><GraduationCap size={18}/> Progress</Link>
        <Link to="/ai-mentor" className="text-gray-600 hover:text-blue-600 flex items-center gap-1 font-medium"><Brain size={18}/> AI Mentor</Link>
        <a href="/GapWise_AI_SIH2026_Pitch_and_Architecture.pdf" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700 flex items-center gap-1 font-semibold bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200"><FileDown size={16}/> Pitch PDF</a>
      </>
    )
  ) : (
    <>
      <Link to="/knowledge-graph" className="text-gray-600 hover:text-blue-600 font-medium flex items-center gap-1"><Network size={16}/> Knowledge Graph</Link>
      <a href="/GapWise_AI_SIH2026_Pitch_and_Architecture.pdf" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200"><FileDown size={16}/> Pitch PDF</a>
      <Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium">Login</Link>
      <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm">Register</Link>
    </>
  );

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to={isAuthenticated ? (user?.role === 'teacher' ? '/teacher/dashboard' : '/dashboard') : '/'} className="flex items-center gap-2">
              <div className="bg-blue-600 p-1.5 rounded-lg shadow-sm">
                <Brain className="text-white" size={24} />
              </div>
              <span className="text-xl font-bold text-gray-900 tracking-tight">GapWise AI</span>
            </Link>
          </div>
          <div className="hidden md:flex items-center gap-5 text-sm">
            {navLinks}
            {isAuthenticated && (
              <div className="flex items-center gap-4 ml-3 pl-3 border-l border-gray-200">
                <span className="text-xs font-semibold uppercase bg-gray-100 text-gray-700 px-2.5 py-1 rounded">
                  {user.role}
                </span>
                <span className="text-sm text-gray-800 font-medium">{user.name}</span>
                <button
                  onClick={handleLogout}
                  title="Log out"
                  className="text-gray-400 hover:text-red-600 transition"
                >
                  <LogOut size={18} />
                </button>
              </div>
            )}
          </div>
          <div className="flex items-center md:hidden">
            <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-gray-500 hover:text-gray-900">
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white">
          <div className="px-4 pt-2 pb-4 flex flex-col gap-3 text-sm">
            {navLinks}
            {isAuthenticated && (
              <button onClick={handleLogout} className="text-gray-600 hover:text-red-600 flex items-center gap-2 mt-2 pt-2 border-t border-gray-100 font-medium">
                <LogOut size={18} /> Logout ({user.name})
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
