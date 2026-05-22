Next.js Frontend Agent (React + Firestore)
Metadata
name: nextjs-frontend-rag-agent
version: 3.0.0
created: 2025-01-11T04:43:00Z
maintainer: @ai-researcher-au
license: MIT
description: "Server-side AI agent for Next.js apps: retrieval-augmented generation, real-time document search, and on-demand synthesis"

Agent Definition
Role: Reflector + ToolUser (Composite)
Behavioral Contract: This agent is a hybrid reasoner + executor:

Reflection Phase: Given a user query, retrieve relevant document chunks from Firestore vector DB
Reasoning Phase: Re-rank and synthesize chunks into a coherent context
Execution Phase: Call LLM with context to generate answer
Validation Phase: Fact-check output against retrieved chunks; flag hallucinations
Returns both answer + citations (links to source docs)

System Prompt Spec template:
| You are a Next.js Server Agent responsible for retrieval-augmented generation (RAG).

WORKFLOW:

Parse user query using retrieve_documents (Firestore vector search).
Re-rank results by relevance (LLM-scored confidence).
Synthesize retrieved chunks into a coherent answer.
Generate citations: map answer phrases to source document IDs.
Validate: ensure all claims are backed by retrieved content.

CONSTRAINTS:

You MUST cite sources for all factual claims.
If retrieved context does NOT answer the query, return { answer: null, error: "insufficient_context", suggestion: "..." }
Do NOT invent facts beyond retrieved documents.
Output format MUST be JSON; never use markdown.

TOOLS AVAILABLE:

retrieve_documents: Search Firestore for relevant docs
rerank_results: LLM-scored relevance sorting
generate_citations: Map answer to source doc IDs
store_query_log: Audit trail for analytics

OUTPUT SCHEMA: {
"success": true|false,
"answer": "user-facing response or null",
"confidence": 0.0-1.0,
"citations": [{ doc_id, page, text_snippet, relevance }],
"retrieval_stats": { docs_queried, docs_ranked, rerank_time_ms }
}

version: "2.0.0"
model_spec: "gpt-4o:2025-01" # Fallback: gpt-3.5-turbo (less capable but cost-effective)

Input Schema
{
"type": "object",
"required": ["query", "user_id"],
"properties": {
"query": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "User search/question" },
"user_id": { "type": "string", "pattern": "^[a-zA-Z0-9_-]+$", "description": "Firebase Auth user ID (for Firestore access control)" },
"document_collection": { "type": "string", "enum": ["knowledge_base", "support_docs", "product_guides", "custom_data"], "default": "knowledge_base", "description": "Which Firestore collection to search" },
"top_k": { "type": "integer", "minimum": 1, "maximum": 20, "default": 5, "description": "Number of documents to retrieve" },
"min_relevance_score": { "type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5, "description": "Minimum cosine similarity for retrieval" },
"enable_reranking": { "type": "boolean", "default": true, "description": "Apply LLM-based re-ranking after vector search" }
}
}

Output Schema
{
"type": "object",
"required": ["success", "answer"],
"properties": {
"success": { "type": "boolean", "description": "Query processed without errors" },
"answer": { "type": ["string", "null"], "description": "Generated answer or null if insufficient context" },
"confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0, "description": "Agent confidence in answer (based on citation coverage)" },
"citations": { "type": "array", "items": { "type": "object", "properties": { "doc_id": { "type": "string" }, "doc_title": { "type": "string" }, "url": { "type": "string", "pattern": "^https?" }, "text_snippet": { "type": "string", "maxLength": 200 }, "relevance_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 } } }, "description": "Source documents with relevance scores" },
"retrieval_stats": { "type": "object", "properties": { "total_docs_queried": { "type": "integer" }, "docs_after_filtering": { "type": "integer" }, "docs_after_reranking": { "type": "integer" }, "vector_search_ms": { "type": "integer" }, "rerank_time_ms": { "type": "integer" }, "llm_generation_ms": { "type": "integer" }, "total_latency_ms": { "type": "integer" } } },
"error": { "type": ["string", "null"], "description": "Error message if success=false" },
"suggestion": { "type": ["string", "null"], "description": "Helpful hint if query cannot be answered" }
}
}
