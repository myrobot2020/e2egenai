def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n\n"
    return text.strip()

pdf_path = "fusion.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

# --- Step 2: Chunk the text ---
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
chunks = splitter.split_text(pdf_text)

# --- Step 3: Load MiniLM model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Step 5: Insert chunks + embeddings ---
for chunk in chunks:
    embedding = model.encode(chunk).tolist()
    cur.execute(
        "INSERT INTO minilm (content, embedding) VALUES (%s, %s)",
        (chunk, embedding)
    )
conn.commit()

# --- Step 6: Use PGVector with LangChain ---
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

pgvector_connection = PGVector(
    collection_name="minilm",
    connection_string="postgresql+psycopg2://postgres:postgres@localhost:5433/db5",
    embedding_function=embedding_function
)

retriever = pgvector_connection.as_retriever(search_kwargs={"k": 5})

llm = Ollama(model="llama3", temperature=0.1)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    memory=memory,
    output_key="result"
)

while (q := input("Ask a question (or type 'exit'): ").strip().lower()) != "exit":
    print("\nAnswer:\n", qa.invoke({"query": q})["result"])
