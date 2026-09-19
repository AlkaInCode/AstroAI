-- Enables pgvector for the RAG knowledge-base embeddings (PRD S17).
-- Only possible here because the pgvector/pgvector Docker image ships the
-- extension precompiled; installing it natively on Windows needs C++ build
-- tools this project doesn't otherwise require.
CREATE EXTENSION IF NOT EXISTS vector;
