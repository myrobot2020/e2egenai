create_table_query = """
CREATE TABLE IF NOT EXISTS tfidf4 (
    id SERIAL PRIMARY KEY,
    chunk TEXT,
    tfidf_vector TEXT  -- Store the vector as a serialized JSON string
);
"""
cur.execute("""
    SELECT id, content
    FROM documents12
    ORDER BY embedding <-> CAST(%s AS vector)
    LIMIT 10;
""", (query_embedding,))


create_minilm_table = """
CREATE TABLE IF NOT EXISTS minilm (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);
"""

cur.execute("""
CREATE TABLE IF NOT EXISTS chat_memory (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);
""")


connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5433/db5"

pgvector = PGVector(
    collection_name="minilm",
    connection_string=connection_string,
    embedding_function=embedding_model,
)

# 3. Setup retriever
retriever = pgvector.as_retriever(search_kwargs={"k": 5})

# 4. Set up the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 5. Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # or "map_reduce" / "refine"
    retriever=retriever,
    return_source_documents=True
)


def chat():
    print("Ask me anything about the PDF (type 'exit' to quit):")
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            break
        result = qa.invoke({"query": query})
        print("\n🤖:", result['result'])


