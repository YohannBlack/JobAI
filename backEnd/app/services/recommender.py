from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(cv_text, job_offers, top_k=5):
    texts = [cv_text] + job_offers
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    sorted_indices = similarities.argsort()[::-1]
    return [job_offers[i] for i in sorted_indices[:top_k]]
