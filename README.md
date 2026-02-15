Compliance RAG System

Hybrid Retrieval-Augmented Generation (RAG) system for RBI regulatory documents.

This system enables intelligent question answering over complex financial regulations using vector search, hybrid retrieval, and LLM-based answer generation.

🚀 Features

PDF parsing and structured chunking

pgvector-based semantic search (Supabase / PostgreSQL)

Hybrid retrieval (Vector + keyword search)

Groq LLaMA 3.1 integration

Retrieval evaluation (Precision, Recall, MRR)

FastAPI deployment with Swagger UI

Source grounding with retrieved chunks

🧠 Architecture

Document Ingestion

PDF → Clean text

Section-aware chunking

Stored in PostgreSQL

Embedding Layer

sentence-transformers/all-mpnet-base-v2

768-dim vectors stored using pgvector

Retrieval

Vector similarity search

Hybrid search (semantic + keyword)

Generation

LLaMA 3.1 via Groq API

Strict context grounding

Evaluation

Precision@k

Recall@k

MRR

🛠 Tech Stack

FastAPI

PostgreSQL + pgvector (Supabase)

Sentence Transformers

Groq API

Python

Uvicorn

📂 Project Structure
app/
  chunk_document.py
  ingest_chunks.py
  generate_embeddings.py
  rag_query.py
  evaluate_retrieval.py
  main.py

data/
  regulations/

requirements.txt
README.md

🔧 Setup
1. Create virtual environment
python -m venv venv
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Configure Environment Variables

Create .env:

DB_HOST=your_supabase_host
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=postgres
DB_PORT=5432
GROQ_API_KEY=your_groq_key

▶ Run API
uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/docs

📊 Example Query
What is the minimum capital adequacy ratio required for NBFC-MFIs?

📈 Retrieval Metrics (Sample)

Precision@3: 0.33 – 0.42

Recall@3: 1.00

MRR: 0.88 – 1.00
