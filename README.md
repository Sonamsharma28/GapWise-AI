# 🎯 GapWise AI

### AI-Based Learning Gap Detection & Personalized Learning System

> **"Don't just detect what students got wrong. Discover why."**

Built for **Smart India Hackathon 2026** | Problem Statement: SIH027 | Team: HexaMind

---

## 🌟 Overview

GapWise AI is an intelligent EdTech platform that goes beyond simple quiz scores. It identifies **what** a student doesn't understand and, more importantly, **why** they are struggling — by tracing learning gaps to their prerequisite root causes.

### Core Pipeline

```
STUDENT → ASSESSMENT → AI ANALYSIS → LEARNING GAP DETECTION
→ ROOT-CAUSE / PREREQUISITE ANALYSIS → PERSONALIZED LEARNING PATH
→ TARGETED LEARNING → PRACTICE → REASSESSMENT → IMPROVED MASTERY
```

### Key Differentiator

Instead of showing:
> "Quadratic Equations = Weak"

GapWise AI reasons through prerequisite concepts:
> "Quadratic Equations needs attention. Your responses suggest that **Factorisation** is the root contributing gap because it is a prerequisite for solving these problems."

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **AI Learning Gap Detection** | Analyzes assessment responses to identify conceptual weaknesses |
| **Prerequisite Root-Cause Analysis** | Traces learning gaps to their deepest prerequisite cause |
| **Knowledge Graph** | Visual concept dependency map color-coded by mastery |
| **Personalized Learning Paths** | Dynamically generated, ordered by prerequisite dependencies |
| **Educational Content** | Original explanations, worked examples, and common mistakes |
| **Adaptive Practice** | Concept-targeted practice with immediate feedback |
| **Continuous Reassessment** | Before/after mastery comparison with improvement tracking |
| **AI Learning Mentor** | Context-aware chat assistant that knows your learning profile |
| **Teacher Dashboard** | Class-level analytics, concept gaps, student-level insights |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, React Router, Recharts |
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL (Neon for production) |
| Auth | JWT (python-jose + bcrypt) |
| AI/LLM | OpenAI API (optional) + deterministic fallback |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Database Hosting | Neon PostgreSQL |

---

## 📂 Project Structure

```
gapwise-ai/
├── frontend/               # React application
│   ├── src/
│   │   ├── api/           # API client and endpoint functions
│   │   ├── context/       # Auth context provider
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # All page components
│   │   └── utils/         # Helper functions
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── models/        # SQLAlchemy database models
│   │   ├── schemas/       # Pydantic validation schemas
│   │   ├── routers/       # API route handlers
│   │   ├── services/      # Business logic (AI, gap detection)
│   │   ├── middleware/    # Auth and error handling
│   │   └── seed/          # Database seed data
│   ├── requirements.txt
│   ├── Dockerfile
│   └── render.yaml
├── docs/                   # Documentation
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Student** | `student@gapwise.ai` | `demo123` |
| **Teacher** | `teacher@gapwise.ai` | `demo123` |

---

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use a free Neon database)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd gapwise-ai
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your database URL and other settings

# Start the server (auto-creates tables and seeds data)
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the backend.

---

## 🌐 Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `SECRET_KEY` | JWT signing secret (change in production!) | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry (default: 1440) | ❌ |
| `OPENAI_API_KEY` | OpenAI API key for AI Mentor | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins, comma-separated | ✅ |

### Frontend (`.env` or Vercel env vars)

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_BASE_URL` | Backend API URL (e.g., `https://your-api.onrender.com/api`) | ✅ |

---

## 🚀 Production Deployment

### Database (Neon)
1. Create a free account at [neon.tech](https://neon.tech)
2. Create a new project and database
3. Copy the connection string

### Backend (Render)
1. Create a free account at [render.com](https://render.com)
2. Create a new Web Service from your GitHub repo
3. Set root directory to `backend`
4. Set environment variables:
   - `DATABASE_URL` = your Neon connection string
   - `SECRET_KEY` = a secure random string
   - `CORS_ORIGINS` = your Vercel frontend URL
   - `OPENAI_API_KEY` = (optional) your OpenAI key
5. Deploy

### Frontend (Vercel)
1. Create a free account at [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Set root directory to `frontend`
4. Set environment variable:
   - `VITE_API_BASE_URL` = your Render backend URL + `/api`
5. Deploy

---

## 📋 API Documentation

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT |
| GET | `/api/auth/me` | Get current user profile |

### Student
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/student/dashboard` | Full student dashboard data |
| GET | `/api/student/mastery` | Concept mastery breakdown |
| GET | `/api/student/progress` | Progress history |

### Assessment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/assessment/start` | Start diagnostic assessment |
| POST | `/api/assessment/{id}/submit` | Submit answers + AI analysis |
| GET | `/api/assessment/{id}/report` | Get assessment report |
| GET | `/api/assessment/history` | Assessment history |

### Learning
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/learning/path` | Active learning path |
| GET | `/api/learning/concept/{id}` | Concept details + resources |
| GET | `/api/learning/concept/{id}/practice` | Practice questions |
| POST | `/api/learning/practice/submit` | Submit practice answers |

### Reassessment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reassessment/start` | Start reassessment |
| POST | `/api/reassessment/{id}/submit` | Submit + compare |
| GET | `/api/reassessment/{id}/comparison` | Before/after comparison |

### Teacher
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teacher/dashboard` | Class-level analytics |
| GET | `/api/teacher/students` | All students |
| GET | `/api/teacher/student/{id}` | Individual student profile |

### AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/mentor` | Chat with AI mentor |

### Graph
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/graph/concepts` | Knowledge graph data |

---

## 🧪 Testing the SIH Demo Scenario

1. **Login** as demo student (`student@gapwise.ai` / `demo123`)
2. **Start** Mathematics Diagnostic Assessment from dashboard
3. **Answer** questions (mix correct and incorrect answers)
4. **Submit** assessment → AI analyzes responses
5. **View** concept mastery map + root-cause analysis
6. **Open** personalized learning path
7. **Study** recommended concept content
8. **Practice** concept-specific questions
9. **Take** reassessment
10. **Compare** before vs. after mastery
11. **See** dashboard improvement
12. **Login** as teacher (`teacher@gapwise.ai` / `demo123`)
13. **View** class-level learning gaps
14. **Open** student profile for detailed analytics

---

## 🧠 How the AI Works

### Gap Detection
- Analyzes all assessment responses per concept
- Calculates weighted mastery score (difficulty-adjusted)
- Classifies: **MASTERED** (≥75%), **DEVELOPING** (40-74%), **NEEDS_ATTENTION** (<40%)

### Prerequisite Root-Cause Analysis
- Traverses the concept prerequisite graph (BFS)
- For each weak concept, checks prerequisite mastery
- Identifies the deepest weak prerequisite as root cause
- Generates human-readable explanations

### Personalized Learning Path
- Topological sort of weak concepts respecting prerequisites
- Root-cause concepts ordered first
- Advanced concepts locked until prerequisites improve

### AI Mentor
- Context-aware responses using student's mastery profile
- RAG retrieval from educational content database
- Optional LLM integration (OpenAI) for richer explanations
- Deterministic fallback ensures functionality without API key

---

## 📄 License

This project was developed for the Smart India Hackathon 2026 by Team HexaMind.

---

## 👥 Team HexaMind

Built with ❤️ for SIH 2026 | Problem Statement SIH027 | Theme: EdTech & Adaptive Learning
