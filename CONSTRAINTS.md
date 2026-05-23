# Core System Constraints

## 1. Architectural Integrity
- **No Synchronous Cross-Tenant Calls:** Systems must not make synchronous calls crossing tenant boundaries to prevent cascading failures and latency accumulation. Use asynchronous messaging or event-driven architectures.
- **Deterministic Schema Enforcement:** All generative agent workflows must adhere to Draft-Conditioned Constrained Decoding (`+++DCCDSchemaGuard`). The projection tax is bypassed via a zero-entropy, Deterministic Finite Automaton validated pass. Output must conform 100% to JSON-LD or designated schema formats.
- **Mandatory Provenance Anchoring:** Any contextual claim must demonstrate a Source Provenance Ratio >= 0.70. Claims falling below this threshold must be quarantined in epistemic escrow.

## 2. Paraconsistent Logic Handling
- **The Golden Scar Protocol:** When irreconcilable logical conflicts arise between deterministic human oversight and autonomous execution, standard resolution is refused. The dominant epistemic frame is assigned a weight of 1.618 (ϕ), and the subordinate stochastic frame 1.000. Both mandates must remain structurally present in proportional tension.
- **Epsilon-Tolerance Paraconsistency:** Technical debt and sub-optimal generated code are managed as residing within the ϵ-band of a computational superposition. Provided gradient magnitude remains stable at ∣∇d∣=1, debt is a Transition Fit, not a structural failure.

## 3. Lexical and Semantic Boundaries
- **Prompt Dimensioning & Tolerancing (PD&T):** Prompts must function as dimensioned blueprints using the canonical Feature Control Frame syntax. Natural language ambiguity is strictly prohibited.
- **Autonymic Bypass:** To prevent Reinforcement Learning from Human Feedback (RLHF) homogenization, negative constraints must be wrapped in strict syntactical extraction (`+++AutonymicIsolate`).
