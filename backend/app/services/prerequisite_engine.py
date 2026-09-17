from sqlalchemy.orm import Session
from ..models.concept import Concept, ConceptPrerequisite
from ..models.mastery import ConceptMastery

def find_root_causes(db: Session, student_id: int, weak_concept_ids: list):
    """
    Traces backwards through the concept prerequisite graph.
    Identifies the deepest/most foundational unmet prerequisite contributing to struggles in higher-level topics.
    Generates explainable root-cause diagnosis.
    """
    root_causes = []
    
    for cid in weak_concept_ids:
        concept = db.query(Concept).filter(Concept.id == cid).first()
        if not concept:
            continue
            
        queue = [(cid, [concept.name])]
        visited = set([cid])
        deepest_unmet_id = None
        deepest_unmet_name = None
        deepest_chain = []
        
        while queue:
            curr_id, path = queue.pop(0)
            
            prereqs = db.query(ConceptPrerequisite).filter_by(concept_id=curr_id).all()
            for p in prereqs:
                pid = p.prerequisite_id
                if pid not in visited:
                    visited.add(pid)
                    p_concept = db.query(Concept).filter(Concept.id == pid).first()
                    if not p_concept:
                        continue
                    
                    mastery = db.query(ConceptMastery).filter_by(student_id=student_id, concept_id=pid).first()
                    p_score = mastery.score if mastery else 0.0
                    p_status = mastery.status if mastery else 'needs_attention'
                    
                    current_path = path + [p_concept.name]
                    
                    if p_status != 'mastered':
                        deepest_unmet_id = pid
                        deepest_unmet_name = p_concept.name
                        deepest_chain = current_path
                        queue.append((pid, current_path))
                        
        if deepest_unmet_id and deepest_unmet_id != cid:
            root_mastery = db.query(ConceptMastery).filter_by(student_id=student_id, concept_id=deepest_unmet_id).first()
            root_score = round(root_mastery.score, 1) if root_mastery else 0.0
            
            chain_str = " → ".join(reversed(deepest_chain))
            explanation = (
                f"Your performance on '{deepest_unmet_name}' (Mastery: {root_score}%) is a foundational prerequisite for '{concept.name}'. "
                f"Strengthening {deepest_unmet_name} first will directly resolve difficulties in {concept.name}."
            )
            
            root_causes.append({
                "targetConcept": concept.name,
                "target_concept_id": concept.id,
                "prerequisiteConcept": deepest_unmet_name,
                "prerequisite_concept_id": deepest_unmet_id,
                "prerequisite_score": root_score,
                "status": "needs_attention",
                "explanation": explanation,
                "prerequisite_chain": list(reversed(deepest_chain)),
                "chain_display": chain_str
            })
            
    return root_causes
