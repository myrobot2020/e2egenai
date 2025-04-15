from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

def save_chunks_with_tfidf(cur, chunks, table="tfidf4", max_features=384):
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(chunks)
    tfidf_array = tfidf_matrix.toarray()

    for i, chunk in enumerate(chunks):
        tfidf_vector = json.dumps(tfidf_array[i].tolist())
        cur.execute(f"INSERT INTO {table} (chunk, tfidf_vector) VALUES (%s, %s)", (chunk, tfidf_vector))

    return vectorizer  # Return vectorizer to be reused for queries

def query_tfidf_chunks(cur, query, vectorizer, table="tfidf4", top_k=20):
    query_vector = vectorizer.transform([query]).toarray()
    cur.execute(f"SELECT id, chunk, tfidf_vector FROM {table}")
    rows = cur.fetchall()

    results = sorted(
        [
            (id, chunk, cosine_similarity(query_vector, [np.array(json.loads(tfidf))])[0][0])
            for id, chunk, tfidf in rows
        ],
        key=lambda x: x[2],
        reverse=True
    )[:top_k]

    return results
