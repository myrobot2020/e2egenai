#!pip install pdfplumber
import pdfplumber
from openai import OpenAI

# Set your OpenAI API key
openai.api_key = 'sk-IHYciM2Ez9Vk945zWCA00PQwyxdRv4zynau66ZRUDcT3BlbkFJEZ8CVWRiPunrL64cQDzVwcrSA6a_HaDpAnB3S4idgA'

# Define the PDF path
pdf_path = "fusion.pdf"

# Extract text directly from the PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Define the system prompt
system_prompt = """
You are analyzing a PDF of nuclear physics.
"""

# Create the message payload
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": pdf_text},
    {"role": "user", "content": "what are the 3 conditions for fusion."},
    {"role": "user", "content": "LICF and MCF both have their own advantages."}

]

# Generate a response using the OpenAI API
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

# Print the response
print(response.choices[0].message.content)
