import psycopg2
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

query = "What is the minimum capital adequacy ratio required for NBFC?"

query_embedding = model.encode(query).tolist()

conn = psycopg2.connect(
    host="SUPABASE_ID",
    database="postgres",
    user="postgres",
    password="PASSWORD",
    port="5432",
    sslmode="require"
)

cur = conn.cursor()

cur.execute("""
    SELECT content
    FROM documents
    ORDER BY embedding <-> %s::vector
    LIMIT 3
""", (query_embedding,))

results = cur.fetchall()

for i, row in enumerate(results):
    print(f"\nResult {i+1}:\n")
    print(row[0][:1000])  # print first 1000 chars

cur.close()
conn.close()
