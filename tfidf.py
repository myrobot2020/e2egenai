vectorizer = TfidfVectorizer(max_features=384)  # You can adjust `max_features` as needed

# Fit the vectorizer to the chunks (this generates the TF-IDF matrix)
tfidf_matrix = vectorizer.fit_transform(chunks)

# Convert the TF-IDF matrix to an array (optional, for easier access later)
tfidf_array = tfidf_matrix.toarray()

# Insert chunks and their corresponding TF-IDF vectors into the database
for i, chunk in enumerate(chunks):
    # Convert the TF-IDF vector to a JSON string
    tfidf_vector = json.dumps(tfidf_array[i].tolist())  # Convert numpy array to list, then to JSON string

    # Insert the chunk and corresponding TF-IDF vector into the database
    cur.execute(
        "INSERT INTO tfidf4 (chunk, tfidf_vector) VALUES (%s, %s)",
        (chunk, tfidf_vector),
    )

query_tfidf_vector = vectorizer.transform([query]).toarray()

cur.execute("SELECT id, chunk, tfidf_vector FROM tfidf4")
rows = cur.fetchall()

results = []

for row in rows:
    id, chunk, tfidf_vector_json = row
    tfidf_vector = np.array(json.loads(tfidf_vector_json))
    similarity = cosine_similarity(query_tfidf_vector, [tfidf_vector])[0][0]
    results.append((id, chunk, similarity))

# Sort by similarity descending
results.sort(key=lambda x: x[2], reverse=True)

# Display top results
top_k = 20
for i in range(min(top_k, len(results))):
    print(f"ID: {results[i][0]}, Similarity: {results[i][2]:.4f}")
    print(f"Chunk: {results[i][1]}\n")
    
    
top_k = 20
top_tfidf_results = results[:top_k]    
    
