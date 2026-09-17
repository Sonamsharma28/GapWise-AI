from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..models.concept import Concept, ConceptPrerequisite
from ..models.mastery import ConceptMastery
from ..models.learning import LearningPath, LearningPathItem

def generate_personalized_learning_path(db: Session, student_id: int):
    """
    Generates a personalized learning path based on the student's mastery and prerequisite graph.
    - Root-cause prerequisites are placed first.
    - Unlocked if prerequisites are mastered (or have no prerequisites).
    - Locked if prerequisites are not yet mastered.
    """
    # Deactivate previous active learning paths
    old_paths = db.query(LearningPath).filter_by(student_id=student_id, is_active=True).all()
    for p in old_paths:
        p.is_active = False

    new_path = LearningPath(
        student_id=student_id,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_path)
    db.commit()
    db.refresh(new_path)

    # Fetch all concepts and masteries
    concepts = db.query(Concept).all()
    masteries = {m.concept_id: m for m in db.query(ConceptMastery).filter_by(student_id=student_id).all()}
    prereqs = db.query(ConceptPrerequisite).all()

    # Build graph
    # prereq_map: concept_id -> list of prerequisite_ids
    prereq_map = {}
    for p in prereqs:
        if p.concept_id not in prereq_map:
            prereq_map[p.concept_id] = []
        prereq_map[p.concept_id].append(p.prerequisite_id)

    # Filter concepts that need improvement (or all if new student)
    # Order: Topological sort or difficulty/dependency based
    # Calculate in-degree based on prerequisites
    ordered_concepts = []
    visited = set()

    def visit(cid):
        if cid in visited:
            return
        # Visit prerequisites first
        for pid in prereq_map.get(cid, []):
            visit(pid)
        visited.add(cid)
        ordered_concepts.append(cid)

    for c in sorted(concepts, key=lambda x: x.difficulty):
        visit(c.id)

    # Build path items
    path_items = []
    order_idx = 1

    for cid in ordered_concepts:
        concept = db.query(Concept).filter_by(id=cid).first()
        m = masteries.get(cid)
        score = m.score if m else 0.0
        status = m.status if m else 'needs_attention'

        # Check if all prerequisites are mastered
        c_prereqs = prereq_map.get(cid, [])
        all_prereqs_mastered = True
        unmet_prereq_names = []

        for pid in c_prereqs:
            pm = masteries.get(pid)
            if not pm or pm.status != 'mastered':
                all_prereqs_mastered = False
                p_obj = db.query(Concept).filter_by(id=pid).first()
                if p_obj:
                    unmet_prereq_names.append(p_obj.name)

        is_locked = not all_prereqs_mastered if c_prereqs else False

        # If already mastered, it is unlocked and completed
        if status == 'mastered':
            reason = "Concept mastered! Review anytime to maintain proficiency."
            is_locked = False
        elif not is_locked:
            if c_prereqs:
                reason = "Prerequisites satisfied! Recommended priority to build foundations."
            else:
                reason = "Foundational topic — master this first to unlock subsequent modules."
        else:
            reason = f"Prerequisite pending: Master {', '.join(unmet_prereq_names)} to unlock."

        item = LearningPathItem(
            path_id=new_path.id,
            concept_id=cid,
            order=order_idx,
            status=status,
            reason=reason,
            is_locked=is_locked
        )
        db.add(item)
        order_idx += 1

        path_items.append({
            "id": cid,
            "concept_id": cid,
            "name": concept.name,
            "description": concept.description,
            "difficulty": concept.difficulty,
            "grade": concept.grade,
            "status": status,
            "score": score,
            "reason": reason,
            "locked": is_locked,
            "is_locked": is_locked,
            "order": order_idx - 1
        })

    db.commit()
    return path_items
