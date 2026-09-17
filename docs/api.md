# GapWise AI — API Documentation

## Base URL

- **Local**: `http://localhost:8000/api`
- **Production**: `https://your-backend.onrender.com/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

---

## Auth Endpoints

### POST `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "student"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### POST `/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### GET `/auth/me`

🔒 **Requires Authentication**

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student"
}
```

---

## Student Endpoints

### GET `/student/dashboard`

🔒 **Requires Authentication** (Student only)

Returns comprehensive dashboard data.

**Response (200):**
```json
{
  "user": { "name": "John Doe", "email": "john@example.com" },
  "overall_mastery": 62.5,
  "concepts_mastered": 4,
  "concepts_developing": 3,
  "concepts_needs_attention": 2,
  "has_taken_assessment": true,
  "recent_assessment": {
    "id": 1,
    "date": "2026-08-31T10:30:00Z",
    "score": 64.0
  },
  "recommended_topic": {
    "id": 5,
    "name": "Factorisation",
    "reason": "Root prerequisite gap for Quadratic Equations"
  },
  "mastery_data": [
    { "concept_id": 1, "concept_name": "Number Systems", "score": 85.0, "status": "mastered" },
    { "concept_id": 5, "concept_name": "Factorisation", "score": 30.0, "status": "needs_attention" }
  ]
}
```

### GET `/student/mastery`

🔒 **Requires Authentication** (Student only)

Returns concept mastery breakdown.

### GET `/student/progress`

🔒 **Requires Authentication** (Student only)

Returns mastery history over time.

---

## Assessment Endpoints

### POST `/assessment/start`

🔒 **Requires Authentication** (Student only)

Starts a new diagnostic assessment.

**Response (200):**
```json
{
  "assessment_id": 1,
  "questions": [
    {
      "id": 1,
      "text": "Simplify: (a + b)² - (a - b)²",
      "type": "mcq",
      "concept_name": "Algebraic Identities",
      "difficulty": 2,
      "options": [
        { "id": 1, "label": "A", "text": "4ab" },
        { "id": 2, "label": "B", "text": "2ab" },
        { "id": 3, "label": "C", "text": "2a²" },
        { "id": 4, "label": "D", "text": "4a²" }
      ]
    }
  ]
}
```

### POST `/assessment/{id}/submit`

🔒 **Requires Authentication** (Student only)

Submit assessment answers and get AI analysis.

**Request Body:**
```json
{
  "responses": [
    { "question_id": 1, "answer": "A" },
    { "question_id": 2, "answer": "B" }
  ]
}
```

**Response (200):**
```json
{
  "assessment_id": 1,
  "score": 64.0,
  "total_questions": 25,
  "correct_answers": 16,
  "concept_mastery": [
    {
      "concept_id": 5,
      "concept_name": "Factorisation",
      "score": 30.0,
      "status": "needs_attention",
      "questions_correct": 0,
      "questions_total": 3
    }
  ],
  "root_cause_analysis": [
    {
      "concept_name": "Quadratic Equations",
      "status": "needs_attention",
      "root_gap": "Factorisation",
      "explanation": "Your performance on Factorisation questions suggests it is a root contributing gap for Quadratic Equations.",
      "prerequisite_chain": ["Basic Algebra", "Algebraic Identities", "Factorisation", "Quadratic Equations"]
    }
  ],
  "learning_path_generated": true
}
```

### GET `/assessment/{id}/report`

🔒 **Requires Authentication** (Student only)

Get the full report for a completed assessment (same format as submit response).

### GET `/assessment/history`

🔒 **Requires Authentication** (Student only)

Returns list of past assessments.

---

## Learning Endpoints

### GET `/learning/path`

🔒 **Requires Authentication** (Student only)

Get the active personalized learning path.

**Response (200):**
```json
{
  "path_id": 1,
  "items": [
    {
      "concept_id": 5,
      "concept_name": "Factorisation",
      "order": 1,
      "status": "needs_attention",
      "reason": "Root prerequisite gap — strengthen before progressing",
      "is_locked": false
    },
    {
      "concept_id": 6,
      "concept_name": "Quadratic Equations",
      "order": 2,
      "status": "needs_attention",
      "reason": "Requires Factorisation mastery",
      "is_locked": true
    }
  ]
}
```

### GET `/learning/concept/{id}`

🔒 **Requires Authentication** (Student only)

Get concept details with learning resources.

### GET `/learning/concept/{id}/practice`

🔒 **Requires Authentication** (Student only)

Get practice questions for a specific concept.

### POST `/learning/practice/submit`

🔒 **Requires Authentication** (Student only)

Submit practice answers.

**Request Body:**
```json
{
  "concept_id": 5,
  "responses": [
    { "question_id": 10, "answer": "B" }
  ]
}
```

---

## Reassessment Endpoints

### POST `/reassessment/start`

🔒 **Requires Authentication** (Student only)

Start a reassessment targeting weak concepts.

### POST `/reassessment/{id}/submit`

🔒 **Requires Authentication** (Student only)

Submit reassessment and get before/after comparison.

**Response (200):**
```json
{
  "comparison": [
    {
      "concept_name": "Factorisation",
      "before_score": 30.0,
      "after_score": 65.0,
      "before_status": "needs_attention",
      "after_status": "developing",
      "improved": true
    }
  ],
  "overall_improvement": 15.0
}
```

---

## Teacher Endpoints

### GET `/teacher/dashboard`

🔒 **Requires Authentication** (Teacher only)

Class-level analytics.

### GET `/teacher/students`

🔒 **Requires Authentication** (Teacher only)

List all students with mastery summaries.

### GET `/teacher/student/{id}`

🔒 **Requires Authentication** (Teacher only)

Individual student deep-dive with mastery, gaps, and recommendations.

---

## AI Mentor

### POST `/ai/mentor`

🔒 **Requires Authentication** (Student only)

**Request Body:**
```json
{
  "message": "Why am I struggling with quadratic equations?",
  "concept_id": 6
}
```

**Response (200):**
```json
{
  "response": "Based on your recent assessment, I can see that Factorisation is currently a challenge for you...",
  "suggested_concept": { "id": 5, "name": "Factorisation" },
  "context_used": ["Factorisation explanation", "Quadratic Equations prerequisites"]
}
```

---

## Knowledge Graph

### GET `/graph/concepts`

**Response (200):**
```json
{
  "concepts": [
    { "id": 1, "name": "Number Systems", "description": "...", "difficulty": 1, "mastery_score": 85.0, "mastery_status": "mastered" }
  ],
  "prerequisites": [
    { "source_id": 2, "target_id": 1 }
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

| Status Code | Meaning |
|------------|---------|
| 400 | Bad Request — Invalid input |
| 401 | Unauthorized — Missing or invalid token |
| 403 | Forbidden — Wrong role |
| 404 | Not Found — Resource doesn't exist |
| 422 | Validation Error — Invalid request body |
| 500 | Internal Server Error |
