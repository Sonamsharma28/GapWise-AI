from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.concept import Concept, ConceptPrerequisite
from ..models.mastery import ConceptMastery
from ..models.user import User
from ..middleware.auth import verify_token

router = APIRouter(prefix="/api/graph", tags=["graph"])

@router.get("/concepts")
def get_graph(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    current_student_id = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if payload:
            email = payload.get("sub")
            user = db.query(User).filter_by(email=email).first()
            if user:
                current_student_id = user.id

    concepts = db.query(Concept).all()
    prereqs = db.query(ConceptPrerequisite).all()
    
    mastery_map = {}
    if current_student_id:
        masteries = db.query(ConceptMastery).filter_by(student_id=current_student_id).all()
        mastery_map = {m.concept_id: {"score": round(m.score, 1), "status": m.status} for m in masteries}

    concept_nodes = []
    for c in concepts:
        m = mastery_map.get(c.id, {"score": 0.0, "status": "unassessed"})
        concept_nodes.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "difficulty": c.difficulty,
            "grade": c.grade,
            "score": m["score"],
            "status": m["status"]
        })

    edges = []
    for p in prereqs:
        source = db.query(Concept).filter_by(id=p.prerequisite_id).first()
        target = db.query(Concept).filter_by(id=p.concept_id).first()
        if source and target:
            edges.append({
                "id": p.id,
                "source": p.prerequisite_id,
                "target": p.concept_id,
                "source_name": source.name,
                "target_name": target.name
            })

    return {
        "concepts": concept_nodes,
        "prerequisites": edges,
        "edges": edges
    }
