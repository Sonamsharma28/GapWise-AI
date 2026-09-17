from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..models.assessment import Assessment, AssessmentResponse
from ..models.question import Question
from ..models.concept import Concept
from ..models.mastery import ConceptMastery

def analyze_assessment(db: Session, assessment_id: int, student_id: int):
    """
    Analyzes student assessment responses.
    Calculates difficulty-weighted mastery score per concept:
    - Difficulty 1: weight 1.0
    - Difficulty 2: weight 1.5
    - Difficulty 3+: weight 2.0
    Classifies mastery into:
    - >= 75%: 'mastered'
    - 40% - 74%: 'developing'
    - < 40%: 'needs_attention'
    Updates or creates ConceptMastery records.
    """
    responses = db.query(AssessmentResponse).filter(AssessmentResponse.assessment_id == assessment_id).all()
    concept_stats = {}
    
    for r in responses:
        q = db.query(Question).filter(Question.id == r.question_id).first()
        if not q:
            continue
        cid = q.concept_id
        if cid not in concept_stats:
            concept_stats[cid] = {
                "correct": 0,
                "total": 0,
                "weighted_score": 0.0,
                "max_weighted": 0.0
            }
            
        weight = 1.0
        if q.difficulty == 2:
            weight = 1.5
        elif q.difficulty >= 3:
            weight = 2.0
            
        concept_stats[cid]["total"] += 1
        concept_stats[cid]["max_weighted"] += weight
        if r.is_correct:
            concept_stats[cid]["correct"] += 1
            concept_stats[cid]["weighted_score"] += weight

    results = []
    for cid, stats in concept_stats.items():
        concept = db.query(Concept).filter(Concept.id == cid).first()
        if not concept:
            continue

        if stats["max_weighted"] > 0:
            score = (stats["weighted_score"] / stats["max_weighted"]) * 100.0
        else:
            score = 0.0
            
        if score >= 75.0:
            status = 'mastered'
        elif score >= 40.0:
            status = 'developing'
        else:
            status = 'needs_attention'
            
        mastery = db.query(ConceptMastery).filter_by(student_id=student_id, concept_id=cid).first()
        if not mastery:
            mastery = ConceptMastery(
                student_id=student_id,
                concept_id=cid,
                score=score,
                status=status,
                attempts=1,
                last_assessed=datetime.now(timezone.utc)
            )
            db.add(mastery)
        else:
            mastery.score = score
            mastery.status = status
            mastery.attempts += 1
            mastery.last_assessed = datetime.now(timezone.utc)

        results.append({
            "concept_id": cid,
            "id": cid,
            "name": concept.name,
            "score": round(score, 1),
            "status": status,
            "correct_count": stats["correct"],
            "total_count": stats["total"]
        })
        
    db.commit()
    return results
