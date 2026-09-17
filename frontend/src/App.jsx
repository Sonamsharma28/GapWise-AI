import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import StudentDashboard from './pages/StudentDashboard';
import Assessment from './pages/Assessment';
import AssessmentReport from './pages/AssessmentReport';
import KnowledgeGraph from './pages/KnowledgeGraph';
import LearningPath from './pages/LearningPath';
import ConceptLearning from './pages/ConceptLearning';
import Practice from './pages/Practice';
import Reassessment from './pages/Reassessment';
import Progress from './pages/Progress';
import AIMentor from './pages/AIMentor';
import TeacherDashboard from './pages/TeacherDashboard';
import StudentAnalytics from './pages/StudentAnalytics';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route path="/dashboard" element={<ProtectedRoute role="student"><Layout><StudentDashboard /></Layout></ProtectedRoute>} />
          <Route path="/assessment" element={<ProtectedRoute role="student"><Layout><Assessment /></Layout></ProtectedRoute>} />
          <Route path="/assessment/:id/report" element={<ProtectedRoute role="student"><Layout><AssessmentReport /></Layout></ProtectedRoute>} />
          <Route path="/knowledge-graph" element={<Layout><KnowledgeGraph /></Layout>} />
          <Route path="/learning/path" element={<ProtectedRoute role="student"><Layout><LearningPath /></Layout></ProtectedRoute>} />
          
          {/* Support both /concept/:id and /learning/concept/:id */}
          <Route path="/concept/:id" element={<ProtectedRoute role="student"><Layout><ConceptLearning /></Layout></ProtectedRoute>} />
          <Route path="/learning/concept/:id" element={<ProtectedRoute role="student"><Layout><ConceptLearning /></Layout></ProtectedRoute>} />
          
          <Route path="/practice" element={<ProtectedRoute role="student"><Layout><Practice /></Layout></ProtectedRoute>} />
          <Route path="/reassessment" element={<ProtectedRoute role="student"><Layout><Reassessment /></Layout></ProtectedRoute>} />
          <Route path="/progress" element={<ProtectedRoute role="student"><Layout><Progress /></Layout></ProtectedRoute>} />
          <Route path="/ai-mentor" element={<ProtectedRoute role="student"><Layout><AIMentor /></Layout></ProtectedRoute>} />
          
          <Route path="/teacher/dashboard" element={<ProtectedRoute role="teacher"><Layout><TeacherDashboard /></Layout></ProtectedRoute>} />
          <Route path="/teacher/student/:id" element={<ProtectedRoute role="teacher"><Layout><StudentAnalytics /></Layout></ProtectedRoute>} />

          {/* Fallback to dashboard */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
