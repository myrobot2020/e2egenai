with pdfplumber.open("fusion.pdf") as pdf:
    text = "\n\n".join(p.extract_text() for p in pdf.pages if p.extract_text())

chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80).split_text(text)
model = SentenceTransformer("all-MiniLM-L6-v2")

conn = psycopg2.connect(dbname="db5", user="postgres", password="postgres", host="localhost", port="5433")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS minilm (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
)
""")
conn.commit()

for chunk in chunks:
    cur.execute("INSERT INTO minilm (content, embedding) VALUES (%s, %s)", (chunk, model.encode(chunk).tolist()))
conn.commit()

retriever = PGVector(
    collection_name="minilm",
    connection_string="postgresql+psycopg2://postgres:postgres@localhost:5433/db5",
    embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
).as_retriever(search_kwargs={"k": 5})

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"  # this is required!
)

qa = ConversationalRetrievalChain.from_llm(
    llm=Ollama(model="llama3", temperature=0.1),
    retriever=retriever,  # <- this should be a valid retriever
    memory=memory,
    return_source_documents=True,
    output_key="answer"  # also IMPORTANT!
)

print("\nAnswer:\n", qa.invoke({"question": q})["answer"])

while (q := input("Ask a question (or type 'exit'): ").strip().lower()) != "exit":
    print("\nAnswer:\n", qa.invoke({"query": q})["result"])
