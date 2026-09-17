from sqlalchemy.orm import Session
from ..models.learning import LearningResource
from ..models.concept import Concept
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_relevant_content(db: Session, query: str, top_k: int = 3):
    """
    RAG content retriever:
    Retrieves the most semantically relevant learning resources using TF-IDF matching.
    """
    resources = db.query(LearningResource).all()
    if not resources:
        return []

    documents = []
    metadata = []
    
    for r in resources:
        concept = db.query(Concept).filter_by(id=r.concept_id).first()
        c_name = concept.name if concept else "Mathematics"
        doc_text = f"Concept: {c_name}. Title: {r.title}. Type: {r.resource_type}. Content: {r.content}"
        documents.append(doc_text)
        metadata.append({
            "concept_id": r.concept_id,
            "concept_name": c_name,
            "title": r.title,
            "resource_type": r.resource_type,
            "content": r.content
        })

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        top_indices = similarities.argsort()[-top_k:][::-1]
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05:
                results.append(metadata[idx])
        return results
    except Exception as e:
        # Fallback keyword match
        query_lower = query.lower()
        matched = []
        for item in metadata:
            if item["concept_name"].lower() in query_lower or query_lower in item["content"].lower():
                matched.append(item)
                if len(matched) >= top_k:
                    break
        return matched
