**Compliance RAG System**

A Hybrid Retrieval-Augmented Generation (RAG) system designed for RBI regulatory and compliance documents.
This system enables intelligent question answering over complex financial regulations using vector search, hybrid retrieval, and LLM-based answer generation.

**Key Features**

  PDF parsing and structured section-aware chunking
  
  pgvector-based semantic search using PostgreSQL (Supabase)
  
  Hybrid retrieval (Vector + keyword search)
  
  Groq LLaMA 3.1 integration
  
  Retrieval evaluation (Precision, Recall, MRR)
  
  FastAPI deployment with Swagger UI
  
  Source grounding with retrieved chunks

**Run API**

	uvicorn app.main:app --reload
