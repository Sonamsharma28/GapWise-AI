# GapWise AI — SIH Demo Script

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Student | `student@gapwise.ai` | `demo123` |
| Teacher | `teacher@gapwise.ai` | `demo123` |

---

## Demo Flow (10-15 minutes)

### Act 1: The Problem (1 min)

**Show the Landing Page.**

> "Traditional assessment systems tell you WHAT a student got wrong, but not WHY. GapWise AI uses AI-powered prerequisite analysis to discover the root cause of learning gaps."

### Act 2: Student Assessment (3 min)

1. **Login** as Demo Student
2. **Click** "Start Diagnostic Assessment"
3. **Answer** the mathematics questions
   - Get most Algebra and Identities questions **correct**
   - Get Factorisation questions **wrong**
   - Get Quadratic Equations questions **wrong**
   - Get Geometry questions **correct**
4. **Submit** the assessment

> "The AI is now analyzing not just what the student got wrong, but tracing through the prerequisite graph to understand WHY."

### Act 3: AI Gap Analysis (3 min)

5. **Show** the Assessment Report:
   - Concept mastery map with color-coded status
   - Overall score

6. **Highlight** the Root-Cause Analysis:
   > "The system didn't just say 'Quadratic Equations is weak.' It traced back through prerequisites and identified that Factorisation is the root gap. The student needs to strengthen Factorisation BEFORE attempting Quadratic Equations."

7. **Show** the Knowledge Graph:
   - Visual concept map with prerequisite arrows
   - Color-coded by mastery status

### Act 4: Personalized Learning (2 min)

8. **Open** the Personalized Learning Path:
   > "The system has generated a personalized path that prioritizes root-cause concepts first. Factorisation is recommended before Quadratic Equations."

9. **Open** the Factorisation learning module:
   - Show explanation, key ideas, worked examples
   > "Each concept has original educational content tailored to the student's needs."

### Act 5: Practice & Reassessment (2 min)

10. **Do** practice questions for Factorisation
11. **Start** a Reassessment
12. **Answer** Factorisation questions correctly this time
13. **Show** the Before/After comparison:
    > "The student's mastery of Factorisation improved from 'Needs Attention' to 'Developing.' The system adapts and updates the learning path accordingly."

### Act 6: AI Mentor (1 min)

14. **Open** the AI Mentor
15. **Ask**: "Why am I struggling with quadratic equations?"
16. **Show** the context-aware response:
    > "The AI Mentor knows the student's learning profile. It doesn't just answer the question — it guides the student toward the right prerequisite concept."

### Act 7: Teacher View (2 min)

17. **Logout** and **Login** as Teacher
18. **Show** the Teacher Dashboard:
    - Class-level concept gaps
    - Students needing attention
19. **Click** on the student profile:
    - Individual mastery, gaps, assessment history
    > "Teachers get actionable insights — not just grades, but specific concepts where each student needs support."

### Closing (1 min)

> "GapWise AI creates a continuous improvement loop:
> ASSESS → DETECT → DIAGNOSE → PERSONALIZE → LEARN → PRACTICE → REASSESS → IMPROVE
>
> This is not a quiz app. It's an intelligent learning diagnosis platform."

---

## Key Talking Points

1. **Root-Cause Analysis**: "We don't just find weak topics. We trace prerequisites to find WHY."
2. **Explainability**: "Every recommendation comes with a clear explanation."
3. **Continuous Loop**: "Assessment → Learning → Reassessment creates measurable improvement."
4. **Works Without AI API**: "Core functionality works offline — the AI mentor enhances but isn't required."
5. **Extensible**: "Built for Math MVP, but architecture supports any subject."

---

## Questions the Judges Might Ask

**Q: How is this different from existing quiz platforms?**
> Unlike quiz platforms that only show scores, GapWise AI traces learning gaps through a prerequisite dependency graph to identify root causes. It explains WHY a student is struggling, not just WHAT they got wrong.

**Q: How does the AI analysis work?**
> We calculate weighted mastery scores per concept (considering difficulty and correctness), then traverse the prerequisite graph using BFS to find the deepest weak prerequisite for each struggling concept. This is the "root cause."

**Q: What if there's no internet/API?**
> The core gap detection and prerequisite analysis work entirely on our own logic — no external API needed. The AI Mentor has a deterministic fallback that uses the student's profile data.

**Q: Can this scale to other subjects?**
> Yes. The architecture uses a generic concept-prerequisite graph. Adding a new subject means adding concepts, prerequisites, questions, and resources. No code changes needed.

**Q: How do you handle data privacy?**
> JWT authentication, password hashing (bcrypt), role-based access control. Students only see their own data. Teachers only see their assigned students.
