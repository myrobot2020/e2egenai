# Fix Unicode on Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

# --- Step 1: Extract text from PDF ---
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

# --- Step 4: PostgreSQL connection ---
conn = psycopg2.connect(
    dbname="db5",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS minilm (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
)
""")
conn.commit()

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

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)

        
# --- Step 7: Chat loop ---
print("Ask me anything about the PDF (type 'exit' to quit):")
while True:
    try:
        query = input("Ask a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        result = qa.invoke(query)
        print("\nAnswer:\n", result["result"])
    except Exception as e:
        print("Error:", e)

