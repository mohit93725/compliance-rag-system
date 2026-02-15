import psycopg2
import json

# --- DATABASE CONNECTION ---
conn = psycopg2.connect(
    host="SUPABASE_ID",
    database="postgres",
    user="postgres",
    password="PASSWORD",
    port="5432",
    sslmode="require"
)

cur = conn.cursor()

CHUNK_FILE = "data/regulations/MD44_chunks.txt"
SOURCE_NAME = "RBI_MD44"

with open(CHUNK_FILE, "r", encoding="utf-8") as f:
    content = f.read()

chunks = content.split("--- CHUNK")

inserted = 0

for chunk in chunks:
    chunk = chunk.strip()
    if len(chunk) < 200:
        continue

    metadata = {
        "document": "MD44",
        "type": "regulation"
    }

    cur.execute(
        """
        INSERT INTO documents (source, content, metadata)
        VALUES (%s, %s, %s::jsonb)
        """,
        (
            SOURCE_NAME,
            chunk,
            json.dumps(metadata)
        )
    )

    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted {inserted} chunks into Supabase.")
