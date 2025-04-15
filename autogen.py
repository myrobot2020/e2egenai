for chunk in chunks:
    embedding = model.encode(chunk).tolist()
    cur.execute(
        "INSERT INTO documents12 (content, embedding) VALUES (%s, %s)",
        (chunk, embedding)
    )

conn.commit()

query_embedding = model.encode(query).tolist()

cur.execute("""
    SELECT id, content
    FROM documents12
    ORDER BY embedding <-> CAST(%s AS vector)
    LIMIT 40;
""", (query_embedding,))

minilmresults = cur.fetchall()



client = openai.OpenAI()  # uses API key from environment or config

embedding_model = OpenAIEmbeddings()  # Replace with your actual embedding class

connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5433/db5"

pgvector_connection = PGVector(
    collection_name="documents12",
    connection_string=connection_string,
    embedding_function=embedding_model,
)

retriever = pgvector_connection.as_retriever(search_kwargs={"k": 10})


llm = ChatOpenAI(model="gpt-4", temperature=0)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True  # Set to False if you don’t need context returned
)
