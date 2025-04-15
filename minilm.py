for chunk in chunks:
    embedding = model.encode(chunk).tolist()
    cur.execute(
        "INSERT INTO minilm (content, embedding) VALUES (%s, %s)",
        (chunk, embedding)
    )

conn.commit()

query_embedding = model.encode(query).tolist()

cur.execute("""
    SELECT id, content
    FROM minilm
    ORDER BY embedding <-> CAST(%s AS vector)
    LIMIT 10;
""", (query_embedding,))

minilmresults = cur.fetchall()
1
create_minilm_table = """
CREATE TABLE IF NOT EXISTS minilm (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);
"""
