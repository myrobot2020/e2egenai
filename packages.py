import sys
print("Running in:", sys.executable)
import os
os.chdir("C:/Users/ADMIN/Desktop/env6")
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import os
import pdfplumber
import langchain_community
from langchain_community.vectorstores import PGVector

from langchain_huggingface import HuggingFaceEmbeddings

from langchain.schema.document import Document
import psycopg2

openai.api_key = os.getenv("OPENAI_API_KEY")
import json
pdf_path = "fusion.pdf"
pdf_path = "pranathiss_knowledge_base.pdf"

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationalRetrievalChain


conn = psycopg2.connect(
    dbname="db5",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

#conn.rollback()  # ❗ Clear the broken transaction state
