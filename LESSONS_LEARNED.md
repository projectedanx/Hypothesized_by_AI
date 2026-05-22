# High-Value Lessons Learned

## 1. Navigating Theoretical vs. Functional State
This repository contains advanced theoretical markdown documentation (e.g., Pluriversal Transformer, Paraconsistent Twist-Structured Attention) rather than functional machine learning or traditional backend code. Building an interactive frontend required a mock layer to simulate the complex behaviors described in the text (like continuous concept-token attention and topological expert routing).
**Lesson:** When working with theoretical knowledge graphs, creating realistic mock endpoints that strictly adhere to prescribed schemas (in this case, the Reflector/ToolUser JSON output schema) is critical for demonstrating the *intended* interaction model without requiring the underlying custom CUDA/Triton implementations.

## 2. Strict Schema Adherence in Next.js Route Handlers
The agent definition mandated a strict JSON output schema containing fields like `success`, `answer`, `citations`, and `retrieval_stats`.
**Lesson:** Implementing Next.js App Router API endpoints (`route.ts`) proved highly effective for isolating the mocked retrieval-augmented generation (RAG) logic from the client. By typing the response clearly on the frontend, we ensured that the UI perfectly matches the "Reflector Phase" and "Validation Phase" requirements, specifically handling the dynamic mapping of citations to the exact markdown files present in the repository.

## 3. UI Design for Multi-Agent Contexts
The application needed to support different "agents" based on the repository's context (e.g., PTST Specialist, KCPM Oracle).
**Lesson:** Utilizing a sidebar for agent context switching and maintaining state for `selectedAgent` allowed the chat interface to dynamically adapt its mocked responses. Rendering complex metadata (like `retrieval_stats` with latency and reranking metrics) directly in the chat flow provides immediate, tangible feedback on the agent's "reasoning phase," turning abstract system prompts into a visual, debuggable experience for the user.

## 4. Constraint Management (DCCDSchemaGuard & AdjectivalBound)
Operating under constraints such as `No_Evaluative_Adjectives` and enforcing strict bicameral output required careful wording in the generated artifacts.
**Lesson:** Keeping code and documentation objective and strictly descriptive (avoiding words like "amazing," "perfect," or "innovative") ensures alignment with the rigid, research-oriented persona required by the system constraints.

## 5. Semantic Topography & JSON-RPC 2.0 Mapping
The execution of the VANCE protocol required mapping unstructured theoretical markdown into strict geometric definitions.
**Lesson:** Abstract semantics must be grounded in precise JSON-RPC 2.0 schemas. By extracting AST-equivalent nodes from text and defining strict mereological bounds, we eliminate ambiguity and establish a deterministic topological index for cross-file symbol references, specifically linking `The Paraconsistent Twist-Structured Transformer (PTST).md` to its implementation mock in `frontend/src/app/api/agent/route.ts`.
