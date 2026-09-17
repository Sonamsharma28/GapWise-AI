import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .config import settings
from .routers import auth, student, assessment, learning, reassessment, teacher, ai, graph
from .models import user, concept, question, assessment as model_assessment, mastery, learning as model_learning, practice, ai_interaction, teacher_student
from .seed.seeder import seed_database

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed database on boot
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title="GapWise AI API",
    description="AI-Based Learning Gap Detection & Personalized Learning System (SIH 2026)",
    version="1.0.0"
)

# Robust CORS configuration
cors_origins_list = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
if not cors_origins_list:
    cors_origins_list = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in cors_origins_list else cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(assessment.router)
app.include_router(learning.router)
app.include_router(reassessment.router)
app.include_router(teacher.router)
app.include_router(ai.router)
app.include_router(graph.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GapWise AI Backend",
        "version": "1.0.0"
    }

@app.get("/download-pdf")
@app.get("/api/download-pdf")
def download_pdf():
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "GapWise_AI_SIH2026_Pitch_and_Architecture.pdf"))
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="GapWise_AI_SIH2026_Pitch_and_Architecture.pdf"
        )
    return {"error": "PDF file not found"}

@app.get("/")
def root():
    return {
        "message": "Welcome to GapWise AI API",
        "docs": "/docs",
        "health": "/api/health",
        "download_pdf": "/download-pdf"
    }
