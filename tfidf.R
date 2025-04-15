from sklearn.feature_extraction.text import TfidfVectorizer
import psycopg2
import numpy as np

# Step 1: Create TF-IDF vectors
vectorizer = TfidfVectorizer(max_features=500)  # You can tweak max_features
tfidf_matrix = vectorizer.fit_transform(chunks)

# Step 3: Insert TF-IDF vectors into the table
for i, chunk in enumerate(chunks):
  tfidf_array = tfidf_matrix[i].toarray()[0]  # Convert sparse to dense
cur.execute("""
        INSERT INTO documents_tfidf (content, tfidf_vector)
        VALUES (%s, %s);
    """, (chunk, list(tfidf_array)))

conn.commit()
