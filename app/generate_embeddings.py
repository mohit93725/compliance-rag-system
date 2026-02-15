import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model (768 dimension)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Connect to Supabase
conn = psycopg2.connect(
    host="SUPABASE_ID",
    database="postgres",
    user="postgres",
    password="YOUR PASSWORD",
    port="5432",
    sslmode="require"
)

cur = conn.cursor()

# Fetch rows without embeddings
cur.execute("""
    SELECT id, content 
    FROM documents
    WHERE embedding IS NULL
""")

rows = cur.fetchall()

print(f"Found {len(rows)} chunks without embeddings.")

for doc_id, content in rows:
    embedding = model.encode(content)

    # Convert numpy array to list
    embedding_list = embedding.tolist()

    cur.execute(
        """
        UPDATE documents
        SET embedding = %s
        WHERE id = %s
        """,
        (embedding_list, doc_id)
    )

conn.commit()
cur.close()
conn.close()

print("Embeddings generated and stored.")
