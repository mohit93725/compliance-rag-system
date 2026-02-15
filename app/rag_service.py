from sentence_transformers import SentenceTransformer
from groq import Groq
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )

def retrieve_chunks(question, top_k=3):
    query_embedding = embedder.encode(question).tolist()
    embedding_str = str(query_embedding)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT content
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """, (embedding_str, top_k))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return [r[0] for r in results]

def generate_answer(question, chunks):

    context = "\n\n---\n\n".join(chunks)

    prompt = f"""
Answer strictly using the provided context.
If not found, say "Not found in provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You answer based only on regulatory text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()
