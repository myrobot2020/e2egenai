# Extract text directly from the PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:  # Check if text extraction was successful
                text += extracted + "\n\n"
    return text.strip()

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
chunks = splitter.split_text(pdf_text)
model = SentenceTransformer("all-MiniLM-L6-v2")
####################
query="funding"
#####################

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

