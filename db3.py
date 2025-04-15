import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import PGVector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.document import Document
from dotenv import load_dotenv

load_dotenv()  
postgres_password = os.getenv('POSTGRES_PASSWORD')
print(postgres_password)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text.strip()

pdf_path = "fusion.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(pdf_text)

embedding_model_name = "all-MiniLM-L6-v2"
embedding_function = HuggingFaceEmbeddings(model_name=embedding_model_name)
documents = [Document(page_content=chunk, metadata={"source": f"chunk_{i}"}) for i, chunk in enumerate(chunks)]


vectorstore = PGVector.from_documents(
    documents=documents,
    embedding=embedding_function,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

print(f"✅ Loaded {len(chunks)} chunks into PGVector collection '{COLLECTION_NAME}'")
