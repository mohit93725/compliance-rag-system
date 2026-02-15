import os
from dotenv import load_dotenv
import psycopg2
from sentence_transformers import SentenceTransformer
from groq import Groq

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not all([DB_HOST, DB_USER, DB_PASSWORD, GROQ_API_KEY]):
    raise ValueError("Missing required environment variables.")

# -----------------------------
# INITIALIZE MODELS
# -----------------------------
embedder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )


# -----------------------------
# RETRIEVE CHUNKS
# -----------------------------
def retrieve_chunks(question, top_k=3):

    query_embedding = embedder.encode(question).tolist()
    embedding_str = str(query_embedding)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT content,
               (1 - (embedding <-> %s::vector)) AS semantic_score,
               ts_rank(content_tsv, plainto_tsquery(%s)) AS keyword_score
        FROM documents
        ORDER BY
            (0.7 * (1 - (embedding <-> %s::vector)) +
             0.3 * ts_rank(content_tsv, plainto_tsquery(%s))) DESC
        LIMIT %s
    """, (embedding_str, question, embedding_str, question, top_k))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return [r[0] for r in results]


# -----------------------------
# GENERATE ANSWER
# -----------------------------
def generate_answer(question, context_chunks):

    context_text = "\n\n---\n\n".join(context_chunks)

    prompt = f"""
You are a regulatory compliance assistant.
Answer strictly using the provided context.
If the answer is not explicitly present, say:
"Not found in provided document."

Context:
{context_text}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer strictly using provided regulatory text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    question = input("Ask your question: ")

    chunks = retrieve_chunks(question)
    answer = generate_answer(question, chunks)

    print("\n--- ANSWER ---\n")
    print(answer)
