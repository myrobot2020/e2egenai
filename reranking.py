tfidf_dict = {item[0]: item[1] for item in top_tfidf_results}
minilm_dict = {item[0]: item[1] for item in minilmresults}

# Intersecting chunk_ids
common_ids = list(set(tfidf_dict.keys()) & set(minilm_dict.keys()))

# Create merged list (id, chunk) for text generation
merged_chunks = [(cid, tfidf_dict[cid]) for cid in common_ids]

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def query_merged_chunks_by_embedding(query, merged_data, model, top_k=3):
    query_embedding = model.encode(query).reshape(1, -1)  # shape: (1, 384)

    results = []
    for cid, chunk, embedding in merged_data:
        chunk_embedding = np.array(embedding).reshape(1, -1)
        similarity = cosine_similarity(query_embedding, chunk_embedding)[0][0]
        results.append((similarity, cid, chunk))

    # Sort by similarity descending
    results.sort(reverse=True)

    return results[:top_k]

merged_chunks_embeddings = []

for cid, chunk in merged_chunks:
    embedding = model.encode(chunk).tolist()
    merged_chunks_embeddings.append((cid, chunk, embedding))

top_results = query_merged_chunks_by_embedding(query, merged_chunks_embeddings, model)

for i, (score, cid, chunk) in enumerate(top_results, 1):
    print(f"{i}. [ID: {cid}] Similarity: {score:.4f}")
    print(chunk[:300] + "\n")





