import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getConcepts } from '../api/graph';
import LoadingSpinner from '../components/LoadingSpinner';
import ConceptStatusBadge from '../components/ConceptStatusBadge';
import { Network, BookOpen, CheckCircle, AlertTriangle, XCircle, ArrowRight, Info } from 'lucide-react';

export default function KnowledgeGraph() {
  const [data, setData] = useState({ concepts: [], prerequisites: [] });
  const [loading, setLoading] = useState(true);
  const [selectedConcept, setSelectedConcept] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    getConcepts()
      .then(res => {
        setData(res.data);
        if (res.data.concepts?.length > 0) {
          setSelectedConcept(res.data.concepts[0]);
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  // Node position layout for DAG visualization (X, Y in SVG coordinates)
  const nodePositions = {
    1: { x: 120, y: 100 },   // Number Systems
    2: { x: 300, y: 100 },   // Basic Algebra
    3: { x: 480, y: 70 },    // Linear Equations
    4: { x: 480, y: 160 },   // Algebraic Identities
    5: { x: 660, y: 160 },   // Factorisation
    6: { x: 840, y: 120 },   // Quadratic Equations
    7: { x: 1020, y: 120 },  // Polynomials
    8: { x: 300, y: 320 },   // Triangles
    9: { x: 660, y: 320 },   // Coordinate Geometry
    10: { x: 480, y: 440 },  // Trigonometry Basics
    11: { x: 720, y: 440 },  // Trigonometry Applications
    12: { x: 480, y: 260 }   // Mensuration
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'mastered':
        return { fill: '#22c55e', border: '#16a34a', bg: 'bg-green-100 text-green-800' };
      case 'developing':
        return { fill: '#eab308', border: '#ca8a04', bg: 'bg-yellow-100 text-yellow-800' };
      case 'needs_attention':
        return { fill: '#ef4444', border: '#dc2626', bg: 'bg-red-100 text-red-800' };
      default:
        return { fill: '#94a3b8', border: '#64748b', bg: 'bg-gray-100 text-gray-700' };
    }
  };

  const filteredConcepts = data.concepts.filter(c => {
    if (filter === 'all') return true;
    return c.status === filter;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Network className="text-blue-600" /> Mathematics Knowledge & Prerequisite Graph
          </h1>
          <p className="text-gray-500 text-sm">
            Interactive map of Class 9–10 concept dependencies. Click on any node to view prerequisites and diagnostics.
          </p>
        </div>
        
        {/* Filter Pills */}
        <div className="flex items-center gap-2 bg-white p-1 rounded-lg border border-gray-200 shadow-sm text-xs font-medium">
          <button 
            onClick={() => setFilter('all')} 
            className={`px-3 py-1.5 rounded-md transition ${filter === 'all' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            All Topics ({data.concepts.length})
          </button>
          <button 
            onClick={() => setFilter('mastered')} 
            className={`px-3 py-1.5 rounded-md transition ${filter === 'mastered' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Mastered
          </button>
          <button 
            onClick={() => setFilter('developing')} 
            className={`px-3 py-1.5 rounded-md transition ${filter === 'developing' ? 'bg-yellow-500 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Developing
          </button>
          <button 
            onClick={() => setFilter('needs_attention')} 
            className={`px-3 py-1.5 rounded-md transition ${filter === 'needs_attention' ? 'bg-red-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Needs Attention
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Visual Graph Canvas */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-4 overflow-x-auto relative">
          <div className="text-xs text-gray-400 font-semibold mb-2 flex items-center gap-2">
            <Info size={14} /> Arrow direction: A → B means "A is a Prerequisite for B"
          </div>
          
          <svg viewBox="0 0 1150 540" className="w-full h-auto min-w-[750px] select-none">
            <defs>
              <marker
                id="arrowhead"
                markerWidth="8"
                markerHeight="6"
                refX="26"
                refY="3"
                orient="auto"
              >
                <polygon points="0 0, 8 3, 0 6" fill="#94a3b8" />
              </marker>
              <marker
                id="arrowhead-active"
                markerWidth="8"
                markerHeight="6"
                refX="26"
                refY="3"
                orient="auto"
              >
                <polygon points="0 0, 8 3, 0 6" fill="#2563eb" />
              </marker>
            </defs>

            {/* Render Prerequisite Edges */}
            {data.prerequisites?.map((edge, i) => {
              const from = nodePositions[edge.source];
              const to = nodePositions[edge.target];
              if (!from || !to) return null;

              const isConnected = selectedConcept && (selectedConcept.id === edge.source || selectedConcept.id === edge.target);

              // Curved bezier path
              const dx = to.x - from.x;
              const dy = to.y - from.y;
              const cx1 = from.x + dx * 0.5;
              const cy1 = from.y;
              const cx2 = from.x + dx * 0.5;
              const cy2 = to.y;

              return (
                <path
                  key={i}
                  d={`M ${from.x} ${from.y} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${to.x} ${to.y}`}
                  fill="none"
                  stroke={isConnected ? '#2563eb' : '#cbd5e1'}
                  strokeWidth={isConnected ? 2.5 : 1.5}
                  strokeDasharray={isConnected ? 'none' : 'none'}
                  markerEnd={isConnected ? 'url(#arrowhead-active)' : 'url(#arrowhead)'}
                  className="transition-all duration-300"
                />
              );
            })}

            {/* Render Concept Nodes */}
            {data.concepts?.map((c) => {
              const pos = nodePositions[c.id] || { x: 100, y: 100 };
              const colors = getStatusColor(c.status);
              const isSelected = selectedConcept?.id === c.id;

              return (
                <g
                  key={c.id}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() => setSelectedConcept(c)}
                  className="cursor-pointer group"
                >
                  {/* Outer pulse when selected */}
                  {isSelected && (
                    <circle
                      r="32"
                      fill="none"
                      stroke="#3b82f6"
                      strokeWidth="3"
                      strokeDasharray="4 2"
                      className="animate-spin"
                    />
                  )}

                  {/* Main Node Circle */}
                  <circle
                    r="24"
                    fill={isSelected ? '#1e40af' : colors.fill}
                    stroke="#ffffff"
                    strokeWidth="3"
                    className="transition-all duration-200 group-hover:scale-110 shadow-lg"
                  />

                  {/* Icon / Difficulty text */}
                  <text
                    textAnchor="middle"
                    dy="5"
                    fill="#ffffff"
                    fontSize="11"
                    fontWeight="bold"
                  >
                    L{c.difficulty}
                  </text>

                  {/* Label Text */}
                  <text
                    textAnchor="middle"
                    dy="42"
                    fill={isSelected ? '#1e3a8a' : '#1e293b'}
                    fontSize="11"
                    fontWeight={isSelected ? 'bold' : '600'}
                    className="drop-shadow-sm"
                  >
                    {c.name}
                  </text>

                  {/* Score Pill */}
                  <text
                    textAnchor="middle"
                    dy="56"
                    fill="#64748b"
                    fontSize="9"
                    fontWeight="500"
                  >
                    {c.status !== 'unassessed' ? `${Math.round(c.score)}%` : 'Class ' + c.grade}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Graph Legend */}
          <div className="flex flex-wrap items-center justify-center gap-6 mt-4 pt-4 border-t border-gray-100 text-xs text-gray-600">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-green-500"></span> Mastered (≥75%)
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-yellow-500"></span> Developing (40-74%)
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-red-500"></span> Needs Attention (&lt;40%)
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-slate-400"></span> Unassessed
            </div>
          </div>
        </div>

        {/* Node Inspector Sidebar */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
          {selectedConcept ? (
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded">
                    Grade {selectedConcept.grade} • Difficulty {selectedConcept.difficulty}/5
                  </span>
                  <ConceptStatusBadge status={selectedConcept.status} />
                </div>
                <h2 className="text-xl font-bold text-gray-900 mt-2">{selectedConcept.name}</h2>
                <p className="text-gray-600 text-sm mt-2">{selectedConcept.description}</p>
              </div>

              {/* Mastery Stats */}
              <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 font-medium">Your Mastery Score:</span>
                  <span className="font-bold text-gray-900">{Math.round(selectedConcept.score || 0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      selectedConcept.score >= 75 ? 'bg-green-500' : selectedConcept.score >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${selectedConcept.score || 0}%` }}
                  ></div>
                </div>
              </div>

              {/* Prerequisites for this concept */}
              <div>
                <h3 className="text-xs font-bold uppercase text-gray-400 tracking-wider mb-2">
                  Direct Prerequisites
                </h3>
                {data.prerequisites?.filter(p => p.target === selectedConcept.id).length > 0 ? (
                  <div className="space-y-2">
                    {data.prerequisites
                      .filter(p => p.target === selectedConcept.id)
                      .map((p, i) => (
                        <div key={i} className="flex items-center justify-between bg-blue-50/60 p-2.5 rounded-lg text-sm border border-blue-100/50">
                          <span className="font-medium text-blue-900">{p.source_name}</span>
                          <span className="text-xs text-blue-600 font-semibold">Required First</span>
                        </div>
                      ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 italic bg-gray-50 p-3 rounded-lg">
                    This is a foundational topic (No prerequisites required).
                  </p>
                )}
              </div>

              {/* Concepts Unlocked by this */}
              <div>
                <h3 className="text-xs font-bold uppercase text-gray-400 tracking-wider mb-2">
                  Unlocks Next
                </h3>
                {data.prerequisites?.filter(p => p.source === selectedConcept.id).length > 0 ? (
                  <div className="space-y-2">
                    {data.prerequisites
                      .filter(p => p.source === selectedConcept.id)
                      .map((p, i) => (
                        <div key={i} className="flex items-center justify-between bg-gray-50 p-2.5 rounded-lg text-sm">
                          <span className="font-medium text-gray-800">{p.target_name}</span>
                          <ArrowRight size={14} className="text-gray-400" />
                        </div>
                      ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 italic">Advanced terminal topic in this module.</p>
                )}
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">Select any concept to inspect details</div>
          )}

          {/* Action CTAs */}
          {selectedConcept && (
            <div className="pt-6 border-t border-gray-100 flex flex-col gap-2">
              <Link
                to={`/learning/concept/${selectedConcept.id}`}
                className="flex items-center justify-center gap-2 bg-blue-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-blue-700 transition"
              >
                <BookOpen size={18} /> Learn Concept
              </Link>
              <Link
                to={`/practice?concept=${selectedConcept.id}`}
                className="flex items-center justify-center gap-2 bg-white text-blue-600 border border-blue-200 py-2.5 px-4 rounded-lg font-medium hover:bg-blue-50 transition"
              >
                Practice Questions
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
