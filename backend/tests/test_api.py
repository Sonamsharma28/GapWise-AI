import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.seed.seeder import seed_database

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_demo_login_student():
    res = client.post("/api/auth/login", json={
        "email": "student@gapwise.ai",
        "password": "demo123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["role"] == "student"

def test_demo_login_teacher():
    res = client.post("/api/auth/login", json={
        "email": "teacher@gapwise.ai",
        "password": "demo123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["role"] == "teacher"

def test_knowledge_graph_endpoints():
    res = client.get("/api/graph/concepts")
    assert res.status_code == 200
    data = res.json()
    assert len(data["concepts"]) >= 12
    assert len(data["prerequisites"]) >= 10

def test_student_full_assessment_flow():
    # 1. Login student
    login_res = client.post("/api/auth/login", json={
        "email": "student@gapwise.ai",
        "password": "demo123"
    })
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Start Assessment
    start_res = client.post("/api/assessment/start", headers=headers)
    assert start_res.status_code == 200
    start_data = start_res.json()
    assessment_id = start_data["id"]
    questions = start_data["questions"]
    assert len(questions) > 0

    # 3. Submit answers (deliberately make factorisation and quadratics weak for SIH root-cause demo)
    answers = {}
    for q in questions:
        if q["concept_name"] in ["Factorisation", "Quadratic Equations"]:
            # Intentionally pick wrong answer
            answers[q["id"]] = "D" if q["options"][0]["label"] != "D" else "A"
        else:
            # Pick first option
            answers[q["id"]] = q["options"][0]["label"]

    submit_res = client.post(f"/api/assessment/{assessment_id}/submit", headers=headers, json={"answers": answers})
    assert submit_res.status_code == 200
    report_data = submit_res.json()
    assert "concepts" in report_data
    assert "rootCauses" in report_data

    # 4. Check Student Dashboard
    dash_res = client.get("/api/student/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["hasAssessment"] is True
    assert "counts" in dash_data

    # 5. Check Learning Path
    path_res = client.get("/api/learning/path", headers=headers)
    assert path_res.status_code == 200
    path_data = path_res.json()
    assert len(path_data["path"]) > 0

    # 6. Check Concept Detail
    first_cid = path_data["path"][0]["id"]
    concept_res = client.get(f"/api/learning/concept/{first_cid}", headers=headers)
    assert concept_res.status_code == 200
    c_data = concept_res.json()
    assert "explanation" in c_data
    assert len(c_data["keyIdeas"]) > 0

    # 7. Practice Submission
    q_res = client.get(f"/api/learning/concept/{first_cid}/practice", headers=headers)
    assert q_res.status_code == 200
    p_questions = q_res.json()
    if p_questions:
        p_q = p_questions[0]
        practice_sub = client.post("/api/learning/practice/submit", headers=headers, json={
            "question_id": p_q["id"],
            "answer": "A",
            "concept_id": first_cid
        })
        assert practice_sub.status_code == 200
        assert "is_correct" in practice_sub.json()

    # 8. Reassessment Flow
    reassess_start = client.post("/api/reassessment/start", headers=headers)
    assert reassess_start.status_code == 200
    reassess_data = reassess_start.json()
    reassess_id = reassess_data["id"]

    r_answers = {q["id"]: "B" for q in reassess_data["questions"]}
    reassess_sub = client.post(f"/api/reassessment/{reassess_id}/submit", headers=headers, json={"answers": r_answers})
    assert reassess_sub.status_code == 200
    assert "comparison" in reassess_sub.json()

    # 9. AI Mentor Chat
    mentor_res = client.post("/api/ai/mentor", headers=headers, json={
        "message": "Why am I finding Quadratic Equations difficult?"
    })
    assert mentor_res.status_code == 200
    assert "response" in mentor_res.json()
    assert len(mentor_res.json()["response"]) > 20

def test_teacher_dashboard_and_analytics():
    # 1. Login Teacher
    login_res = client.post("/api/auth/login", json={
        "email": "teacher@gapwise.ai",
        "password": "demo123"
    })
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Teacher Dashboard
    dash_res = client.get("/api/teacher/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert "stats" in dash_data
    assert dash_data["stats"]["totalStudents"] >= 1
    assert len(dash_data["conceptPerformance"]) >= 12

    # 3. Student Analytics drilldown
    students_res = client.get("/api/teacher/students", headers=headers)
    assert students_res.status_code == 200
    s_list = students_res.json()
    assert len(s_list) >= 1
    student_id = s_list[0]["id"]

    student_drilldown = client.get(f"/api/teacher/student/{student_id}", headers=headers)
    assert student_drilldown.status_code == 200
    drill_data = student_drilldown.json()
    assert drill_data["id"] == student_id
    assert "concepts" in drill_data
    assert "learningGaps" in drill_data
