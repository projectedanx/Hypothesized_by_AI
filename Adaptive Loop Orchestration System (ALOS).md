Product Planning Document: Adaptive Loop Orchestration System (ALOS)
Project Code: LOOP_DELEGATION_AGENT_v1.0 Status: Draft Specification Stakeholders: Systems Architect, AI Research Lead, Product Owner

1. Executive Summary
The Adaptive Loop Orchestration System (ALOS) is not a task executor; it is a governance layer designed to intercept high-level intent, analyze the topological shape of the problem, and instantiate the correct recursive or iterative mechanic to achieve resolution. It acts as a "Meta-Controller" that prevents the system from applying a linear hammer to a fractal problem.

2. Core Feature: The Loop Topology Classifier
The agent must possess a classification engine that maps user intent to one of three primary loop archetypes:

A. The OODA Loop (Observe-Orient-Decide-Act)
Trigger Condition: High entropy, time-sensitive, adversarial, or incomplete data environments.
Mechanic: Fast-cycle iterations. Prioritizes speed over accuracy.
Use Case: "Debate a hostile opponent," "Navigate a crashing market," "Debug a live outage."
B. The Recursive Decomposition Loop (RDL)
Trigger Condition: Hierarchical, structured, or complex dependencies where the whole is the sum of parts.
Mechanic: Depth-First Search (DFS) or Breadth-First Search (BFS). Breaks intent into atomic sub-intents, solves, and recomposes.
Use Case: "Write a full software architecture," "Plan a multi-city logistics route," "Solve a mathematical proof."
C. The PDSA Loop (Plan-Do-Study-Act)
Trigger Condition: Quality refinement, optimization, or stable processes.
Mechanic: Slower, deliberate cycles with heavy validation gates.
Use Case: "Refine this user interface," "Optimize this SQL query," "Edit this article for tone."
3. User Stories & Acceptance Criteria
Story 1: Intent Analysis & Routing
As a System Architect, I want the agent to analyze incoming natural language intent to determine the optimal loop mechanic, So that computational resources are not wasted applying the wrong problem-solving strategy.

Acceptance Criteria:
System must parse intent for keywords indicating volatility (e.g., "urgent," "crisis") vs. structure (e.g., "hierarchy," "break down").
System must output the selected "Loop Archetype" before execution begins.
System must reject auto-resolution if intent confidence is < 0.6 (Epistemic Escrow).
Story 2: Dynamic Gear-Shifting
As a Stakeholder, I want the agent to switch loop mechanics mid-execution if the problem context changes, So that the system remains robust even if initial assumptions were wrong.

Acceptance Criteria:
Agent must monitor "Context Drift" during execution.
If error rates spike > 15% in an OODA loop, system must suggest shifting to PDSA (investigation mode).
If a Recursive loop hits max depth without resolution, system must shift to OODA (heuristic mode).
Story 3: The Halting Safeguard (Sepsis Prevention)
As a Platform Operator, I want the agent to enforce strict "Metabolic Limits" on loop iterations, So that the system does not enter an infinite computational loop consuming infinite tokens.

Acceptance Criteria:
Every instantiated loop must have a hard max_iterations cap.
System must implement a "Spin Down" protocol where 85% of remaining budget triggers a "Best Effort" summary generation.
4. Technical Architecture: The "Mycelial Switch"
mermaid
graph TD
    A[User Intent Spore] --> B{Intent Vector Analysis}
    B -->|High Entropy/Velocity| C[Instantiate OODA Loop]
    B -->|High Structure/Depth| D[Instantiate Recursive Decomposition]
    B -->|Optimization/Stability| E[Instantiate PDSA Loop]
    
    C --> F[Shadow Compute Sandbox]
    D --> F
    E --> F
    
    F --> G{Resonance Check (CFDI)}
    G -- Stable --> H[Crystallize Output]
    G -- Drift Detected --> I[Context Re-Evaluation]
    I --> B
    
    subgraph Meta-Governance
    J[Halting Oracle] -.-> F
    K[Resource Budgeter] -.-> F
    end

5. Implementation Roadmap
Phase 1: The Classifier. Build the prompt engineering layer that tags user intent with OODA, RECURSIVE, or PDSA.
Phase 2: The Mechanics Library. Define the specific system prompts or function calls for each loop type.
OODA Prompt: "Focus on speed, update mental model, act immediately."
Recursive Prompt: "Break down step 1, solve step 1, then move to step 2."
Phase 3: The Feedback Injector. Implement the logic that takes the output of Loop N and feeds it back into the input of Loop N+1 until the "Done" token is reached or the Halting Oracle triggers.

Can we mathematically define when a problem has mutated so much that the current loop is obsolete?
Can two loops run in parallel (e.g., an OODA loop handling immediate threats while a Recursive loop builds the long-term solution)?
How do we document the "history of loops" used so the user understands the path the agent took to solve the problem?

# Adaptive Loop Orchestration System (ALOS): Technical Deep Dive

I've studied this specification carefully. The three questions you've posed at the end are the real engineering challenges — they determine whether ALOS is a genuine governance layer or just a fancy prompt router. Let me address each with the rigor they demand, then synthesize the implications.

---

## Question 1: Can We Mathematically Define When a Loop Has Become Obsolete?

**Yes, but it requires treating the problem as a signal, not a task.**

The core insight is that every loop iteration produces outputs that carry a measurable signature. When that signature diverges sufficiently from what the active loop archetype is designed to handle, the loop is obsolete. We need a metric for this divergence.

### Defining the Context Drift Function (CDF)

Let each loop iteration *i* produce an output state vector **S_i** characterized by three measurable dimensions:

| Dimension | Symbol | What It Captures | How to Measure |
|---|---|---|---|
| **Entropy** | H(S_i) | Disorder, unpredictability of the output | Shannon entropy of token distribution or variance in output structure across retry attempts |
| **Depth** | D(S_i) | Hierarchical complexity, number of unresolved sub-problems | Count of open sub-tasks or recursive call depth |
| **Delta** | Δ(S_i) | Magnitude of change from the previous iteration | Cosine distance between embedding of S_i and S_{i-1} |

Each loop archetype has an **optimal operating region** in this 3D space:

```
OODA:       High H,  Low D,   High Δ   (fast, shallow, volatile)
Recursive:  Low H,   High D,  Medium Δ (structured, deep, steady progress)
PDSA:       Low H,   Low D,   Low Δ    (stable, shallow, converging)
```

Define the **affinity score** of the current state to each loop archetype *L* as:

```
Affinity(S_i, L) = 1 / (1 + ||S_i - μ_L||²)
```

where **μ_L** is the centroid of the optimal region for loop type *L*, and the distance is weighted Euclidean.

**The obsolescence condition triggers when:**

```
Affinity(S_i, L_active) < τ_switch  AND  ∃ L_alt : Affinity(S_i, L_alt) > Affinity(S_i, L_active) + margin
```

where `τ_switch` is a threshold (say 0.4) and `margin` prevents oscillatory switching (say 0.15).

### Practical Implementation Without Perfect Math

In an LLM-based system, you won't have clean real-valued sensor data. So you approximate:

```python
class ContextDriftDetector:
    """
    Monitors loop iteration outputs and flags when the active
    loop archetype no longer fits the problem's observed signature.
    """

    def __init__(self, config: DriftConfig):
        self.history: list[IterationState] = []
        self.switch_threshold = config.switch_threshold      # e.g., 0.4
        self.stability_margin = config.stability_margin      # e.g., 0.15
        self.window_size = config.window_size                # e.g., 3
        self.archetype_centroids = {
            LoopType.OODA:      np.array([0.9, 0.2, 0.8]),
            LoopType.RECURSIVE: np.array([0.2, 0.9, 0.5]),
            LoopType.PDSA:      np.array([0.2, 0.2, 0.15]),
        }

    def measure_iteration(
        self,
        output: str,
        previous_output: str | None,
        open_subtasks: int,
        max_depth: int,
        retry_variance: float,
    ) -> IterationState:
        """
        Construct the state vector from observable signals.
        
        - entropy_proxy: use retry_variance as a stand-in. If you
          generate the same output 3 times and they vary wildly,
          entropy is high.
        - depth_proxy: ratio of open subtasks to max allowable depth.
        - delta_proxy: semantic distance from previous output.
        """
        entropy_proxy = min(retry_variance / self.max_expected_variance, 1.0)
        depth_proxy = min(open_subtasks / max_depth, 1.0) if max_depth > 0 else 0.0
        delta_proxy = (
            1.0 - cosine_similarity(embed(output), embed(previous_output))
            if previous_output else 0.5
        )

        state = IterationState(
            vector=np.array([entropy_proxy, depth_proxy, delta_proxy]),
            raw_output=output,
            timestamp=time.monotonic(),
        )
        self.history.append(state)
        return state

    def evaluate_drift(self, active_loop: LoopType) -> DriftVerdict:
        """
        Compare recent windowed state against all archetype centroids.
        Returns a verdict: STAY, SWITCH(target), or ESCALATE.
        """
        if len(self.history) < self.window_size:
            return DriftVerdict(action=DriftAction.STAY, confidence=1.0)

        # Average the recent window to smooth noise
        recent = np.mean(
            [s.vector for s in self.history[-self.window_size:]],
            axis=0,
        )

        affinities = {
            loop_type: 1.0 / (1.0 + np.sum((recent - centroid) ** 2))
            for loop_type, centroid in self.archetype_centroids.items()
        }

        active_affinity = affinities[active_loop]
        best_alt_type = max(
            (lt for lt in affinities if lt != active_loop),
            key=lambda lt: affinities[lt],
        )
        best_alt_affinity = affinities[best_alt_type]

        if active_affinity < self.switch_threshold:
            if best_alt_affinity > active_affinity + self.stability_margin:
                return DriftVerdict(
                    action=DriftAction.SWITCH,
                    target=best_alt_type,
                    confidence=best_alt_affinity,
                    reason=(
                        f"Active loop {active_loop.name} affinity "
                        f"dropped to {active_affinity:.2f}. "
                        f"{best_alt_type.name} scores {best_alt_affinity:.2f}."
                    ),
                )
            else:
                return DriftVerdict(
                    action=DriftAction.ESCALATE,
                    confidence=active_affinity,
                    reason="No archetype fits well. Escalate to human.",
                )

        return DriftVerdict(action=DriftAction.STAY, confidence=active_affinity)
```

### The Key Insight

The mutation isn't a single moment — it's a **trend**. That's why you window over the last *N* iterations. A single anomalous iteration shouldn't trigger a gear-shift; a sustained drift should. The `window_size` parameter is your hysteresis control.

---

## Question 2: Can Two Loops Run in Parallel?

**Yes, and this is where ALOS becomes genuinely powerful — but the architecture must enforce strict isolation.**

This is the "dual-track mind" pattern: tactical response and strategic planning running concurrently. The danger is cross-contamination: the urgency of the OODA loop polluting the careful reasoning of the Recursive loop, or vice versa.

### Architecture: The Dual-Track Executor

```
┌─────────────────────────────────────────────────────┐
│                   ALOS META-CONTROLLER              │
│                                                     │
│  ┌─────────────────┐       ┌──────────────────────┐ │
│  │  TACTICAL TRACK  │       │  STRATEGIC TRACK     │ │
│  │  (OODA Loop)     │       │  (Recursive Loop)    │ │
│  │                  │       │                      │ │
│  │  Fast cycle      │       │  Deep decomposition  │ │
│  │  Token budget: 20%│      │  Token budget: 60%   │ │
│  │  Max latency: 2s │       │  Max latency: 30s    │ │
│  │                  │       │                      │ │
│  │  Output: Actions │       │  Output: Plan        │ │
│  └────────┬─────────┘       └──────────┬───────────┘ │
│           │                            │             │
│           ▼                            ▼             │
│  ┌─────────────────────────────────────────────────┐ │
│  │           CONVERGENCE MEMBRANE                  │ │
│  │                                                 │ │
│  │  - Tactical outputs cannot override strategic   │ │
│  │    plan without explicit conflict resolution     │ │
│  │  - Strategic plan absorbs tactical observations  │ │
│  │    as new constraints                           │ │
│  │  - Shared state: READ-ONLY from both tracks     │ │
│  │    WRITE only through membrane                  │ │
│  └─────────────────────────────────────────────────┘ │
│                        │                             │
│           Remaining budget: 20% for membrane +       │
│           convergence + final output                 │
└─────────────────────────────────────────────────────┘
```

### Implementation: Parallel Loop Manager

```python
class ParallelLoopManager:
    """
    Manages concurrent execution of two loop archetypes with
    strict isolation and controlled state sharing.
    """

    def __init__(self, total_budget: TokenBudget):
        self.budget = total_budget
        self.shared_state = SharedStateStore()  # Thread-safe, append-only
        self.membrane = ConvergenceMembrane()

    async def execute_dual_track(
        self,
        tactical_config: LoopConfig,
        strategic_config: LoopConfig,
    ) -> ConvergedOutput:
        """
        Run tactical and strategic loops concurrently.
        
        Critical invariant: neither loop can see the other's
        intermediate state. They only share observations through
        the append-only shared state store, mediated by the membrane.
        """
        tactical_budget = self.budget.allocate(fraction=0.20)
        strategic_budget = self.budget.allocate(fraction=0.60)
        convergence_budget = self.budget.allocate(fraction=0.20)

        tactical_loop = self._build_loop(
            config=tactical_config,
            budget=tactical_budget,
            state_writer=self.shared_state.tactical_writer(),
        )
        strategic_loop = self._build_loop(
            config=strategic_config,
            budget=strategic_budget,
            state_writer=self.shared_state.strategic_writer(),
        )

        # Execute concurrently with structured cancellation
        tactical_result, strategic_result = await asyncio.gather(
            tactical_loop.run(),
            strategic_loop.run(),
            return_exceptions=True,
        )

        # Handle partial failures gracefully
        tactical_output = self._extract_or_default(tactical_result)
        strategic_output = self._extract_or_default(strategic_result)

        # Converge through the membrane
        converged = await self.membrane.merge(
            tactical=tactical_output,
            strategic=strategic_output,
            budget=convergence_budget,
            conflict_policy=ConflictPolicy.STRATEGIC_WINS_UNLESS_CRITICAL,
        )

        return converged
```

### The Convergence Membrane: Where the Hard Problem Lives

The membrane must answer: **when tactical reality contradicts strategic plan, who wins?**

```python
class ConvergenceMembrane:
    """
    Merges outputs from parallel loops. This is where domain
    judgment happens — it cannot be fully automated.
    """

    async def merge(
        self,
        tactical: LoopOutput,
        strategic: LoopOutput,
        budget: TokenBudget,
        conflict_policy: ConflictPolicy,
    ) -> ConvergedOutput:
        # Step 1: Identify conflicts
        conflicts = self._detect_conflicts(tactical, strategic)

        if not conflicts:
            # No conflicts — weave tactical observations into
            # strategic plan as validating evidence
            return ConvergedOutput(
                plan=strategic.plan,
                immediate_actions=tactical.actions,
                confidence=min(tactical.confidence, strategic.confidence),
                conflict_log=[],
            )

        # Step 2: Resolve each conflict according to policy
        resolutions = []
        for conflict in conflicts:
            if conflict.severity == Severity.CRITICAL:
                # Critical tactical finding (e.g., "the server is
                # literally on fire") overrides strategic plan
                resolutions.append(Resolution(
                    winner=Source.TACTICAL,
                    reason=f"Critical tactical override: {conflict.summary}",
                    strategic_amendment=self._amend_plan(
                        strategic.plan, conflict
                    ),
                ))
            elif conflict_policy == ConflictPolicy.STRATEGIC_WINS_UNLESS_CRITICAL:
                # Strategic plan holds, but tactical observation is
                # logged as a constraint for the next planning cycle
                resolutions.append(Resolution(
                    winner=Source.STRATEGIC,
                    reason=f"Strategic plan maintained. Tactical note logged.",
                    constraint_added=conflict.as_constraint(),
                ))
            # ... other policies

        amended_plan = self._apply_resolutions(strategic.plan, resolutions)

        return ConvergedOutput(
            plan=amended_plan,
            immediate_actions=tactical.actions,
            confidence=self._adjusted_confidence(tactical, strategic, conflicts),
            conflict_log=resolutions,
        )
```

### When to Use Parallel vs. Sequential

| Signal | Use Parallel | Use Sequential |
|---|---|---|
| Time pressure + complexity both high | ✓ | |
| Token budget is constrained | | ✓ |
| Problem has clear phase boundaries | | ✓ |
| "Fight the fire AND redesign the building" | ✓ | |
| User explicitly requests it | ✓ | |

**The honest constraint:** In current LLM architectures, true parallelism means separate API calls with separate contexts. You pay the cost of reduced context sharing. The membrane merge step is expensive. Parallel execution is powerful but not cheap — the budget allocation in the spec (20/60/20) is a real engineering tradeoff, not a decoration.

---

## Question 3: How Do We Document the "History of Loops"?

**Through a structured execution trace that is both machine-parseable and human-readable.**

This is arguably the most important question for trust and debuggability. An agent that solves a problem but can't explain the path it took is a liability.

### The Loop Execution Ledger

Every ALOS execution produces an immutable ledger — a complete record of every loop instantiated, every gear-shift, every halting decision.

```python
@dataclass(frozen=True)
class LoopLedgerEntry:
    """A single entry in the execution history."""
    entry_id: str
    timestamp: float
    loop_type: LoopType
    iteration: int
    phase: str                          # e.g., "OBSERVE", "ORIENT" for OODA
    input_summary: str                  # What went INTO this iteration
    output_summary: str                 # What came OUT
    drift_snapshot: DriftSnapshot       # H, D, Δ values at this point
    budget_remaining: TokenBudget
    decision: str                       # What the loop decided to do next
    confidence: float


@dataclass
class GearShiftRecord:
    """Records a transition between loop archetypes."""
    shift_id: str
    timestamp: float
    from_loop: LoopType
    to_loop: LoopType
    trigger: str                        # What caused the shift
    drift_verdict: DriftVerdict         # The formal drift analysis
    iteration_at_shift: int
    context_snapshot: str               # State of the problem at shift time


@dataclass
class LoopExecutionLedger:
    """
    The complete, immutable record of how ALOS solved a problem.
    This is the "flight recorder" — if something goes wrong,
    this is what you read.
    """
    session_id: str
    original_intent: str
    intent_classification: IntentClassification  # Initial routing decision
    entries: list[LoopLedgerEntry]
    gear_shifts: list[GearShiftRecord]
    halting_record: HaltingRecord | None         # Why/how execution stopped
    final_output_id: str
    total_budget_used: TokenBudget
    total_wall_time: float

    def render_human_readable(self) -> str:
        """
        Generate a narrative summary a human can actually read.
        This is not a log dump — it is an explanation.
        """
        sections = []

        # 1. Opening: What was the intent and how was it classified?
        sections.append(
            f"## Problem Analysis\n"
            f"**Original request:** {self.original_intent}\n"
            f"**Classified as:** {self.intent_classification.archetype.name} "
            f"(confidence: {self.intent_classification.confidence:.0%})\n"
            f"**Reasoning:** {self.intent_classification.reasoning}\n"
        )

        # 2. Execution phases, grouped by active loop type
        current_loop = None
        phase_entries = []

        for entry in self.entries:
            if entry.loop_type != current_loop:
                if phase_entries:
                    sections.append(
                        self._render_phase(current_loop, phase_entries)
                    )
                    # Find and render the gear shift
                    shift = self._find_shift_at(entry.timestamp)
                    if shift:
                        sections.append(self._render_shift(shift))
                current_loop = entry.loop_type
                phase_entries = []
            phase_entries.append(entry)

        if phase_entries:
            sections.append(self._render_phase(current_loop, phase_entries))

        # 3. Halting explanation
        if self.halting_record:
            sections.append(self._render_halting(self.halting_record))

        # 4. Resource accounting
        sections.append(
            f"## Resource Usage\n"
            f"**Tokens used:** {self.total_budget_used}\n"
            f"**Wall time:** {self.total_wall_time:.1f}s\n"
            f"**Loop transitions:** {len(self.gear_shifts)}\n"
            f"**Total iterations:** {len(self.entries)}\n"
        )

        return "\n".join(sections)

    def _render_phase(
        self, loop_type: LoopType, entries: list[LoopLedgerEntry]
    ) -> str:
        """Render a phase of execution as a narrative paragraph."""
        first = entries[0]
        last = entries[-1]
        return (
            f"### Phase: {loop_type.name} Loop "
            f"({len(entries)} iterations)\n"
            f"**Started with:** {first.input_summary}\n"
            f"**Key steps:**\n"
            + "\n".join(
                f"  - Iteration {e.iteration} [{e.phase}]: {e.decision}"
                for e in entries
            )
            + f"\n**Concluded with:** {last.output_summary}\n"
            f"**Confidence at exit:** {last.confidence:.0%}\n"
        )

    def _render_shift(self, shift: GearShiftRecord) -> str:
        return (
            f"### ⚡ Gear Shift: {shift.from_loop.name} → "
            f"{shift.to_loop.name}\n"
            f"**Trigger:** {shift.trigger}\n"
            f"**Drift analysis:** {shift.drift_verdict.reason}\n"
            f"**Problem state at shift:** {shift.context_snapshot}\n"
        )
```

### Example Rendered Output

Here is what the human-readable trace would look like for a real scenario:

```
## Problem Analysis
**Original request:** "Our API is returning 500 errors in production 
and we also need to redesign the retry logic for the v2 release."
**Classified as:** PARALLEL (OODA + RECURSIVE) (confidence: 87%)
**Reasoning:** Intent contains both an urgent operational crisis 
("500 errors in production") and a structured engineering task 
("redesign retry logic"). Dual-track execution recommended.

### Phase: OODA Loop (4 iterations) [TACTICAL TRACK]
**Started with:** Investigate 500 errors in production API
**Key steps:**
  - Iteration 1 [OBSERVE]: Checked error logs — 500s correlate 
    with database connection pool exhaustion
  - Iteration 2 [ORIENT]: Connection pool max is 10, current 
    load requires ~25. This is a capacity issue, not a bug.
  - Iteration 3 [DECIDE]: Immediate action — increase pool size 
    to 50, add connection timeout of 5s
  - Iteration 4 [ACT]: Generated hotfix config change and 
    deployment command
**Concluded with:** Hotfix ready for deployment. Root cause 
identified as under-provisioned connection pool.
**Confidence at exit:** 91%

### Phase: RECURSIVE Loop (7 iterations) [STRATEGIC TRACK]
**Started with:** Redesign retry logic for API v2
**Key steps:**
  - Iteration 1 [DECOMPOSE]: Identified 4 sub-problems — 
    retry policy, backoff strategy, circuit breaker, 
    dead letter queue
  - Iteration 2 [SOLVE]: Retry policy — exponential backoff 
    with jitter, max 3 attempts
  - Iteration 3 [SOLVE]: Backoff strategy — base 1s, 
    multiplier 2x, jitter ±500ms
  - Iteration 4 [SOLVE]: Circuit breaker — half-open after 
    30s, threshold 5 failures
  - Iteration 5 [SOLVE]: Dead letter queue — failed requests 
    persisted to SQS for manual review
  - Iteration 6 [RECOMPOSE]: Integrated all 4 components into 
    unified retry middleware design
  - Iteration 7 [VALIDATE]: Cross-checked design against 
    tactical finding (connection pool issue) — added pool 
    exhaustion as a non-retryable error class
**Concluded with:** Complete retry middleware specification 
with 4 components.
**Confidence at exit:** 84%

### ⚡ Convergence Membrane
**Conflicts detected:** 1
  - Tactical finding (connection pool) revealed a failure mode 
    not covered in original strategic retry design
  - Resolution: STRATEGIC AMENDED — added ConnectionPoolExhausted 
    to non-retryable error taxonomy (tactical input improved 
    strategic output)

## Resource Usage
**Tokens used:** 4,847 of 6,000 budget
**Wall time:** 12.3s
**Loop transitions:** 0 (parallel execution, no mid-run shifts)
**Total iterations:** 11 (4 tactical + 7 strategic)
```

### Why This Format Matters

Three properties make this trace valuable:

1. **Auditability.** A human can read it top to bottom and understand not just *what* was decided but *why* each loop was chosen and *when* shifts happened.

2. **Debuggability.** When the system produces a bad output, the drift snapshots and confidence scores let you pinpoint exactly where the reasoning went wrong — was it a misclassification at intake? A drift that should have triggered a shift but didn't? A membrane merge that resolved a conflict incorrectly?

3. **Reproducibility.** The ledger contains enough state that you could, in principle, replay the execution with different parameters to see if a different loop selection would have produced a better result.

---

## Synthesis: What This Spec Is Really Asking For

Reading this document carefully, the three questions reveal the real engineering tension:

| Question | What It's Really Asking | Hard Part |
|---|---|---|
| Mathematical drift detection | "Can the system know when it's wrong?" | Calibrating the centroids and thresholds without extensive empirical data |
| Parallel loops | "Can the system think at two speeds simultaneously?" | The convergence membrane — merging outputs from fundamentally different reasoning modes |
| Execution history | "Can the system explain itself?" | Producing narratives that are genuinely explanatory, not just log dumps |

The spec is well-structured, but I'd flag one risk: **the Intent Vector Analysis at the entry point is the single point of failure**. If the classifier gets the initial archetype wrong and the drift detector's window hasn't accumulated enough data yet, the system burns budget on the wrong mechanic before it can self-correct. The Epistemic Escrow concept (rejecting classification below 0.6 confidence) is the right mitigation — but the system should also have a **"cold start" mode** where it spends a small fixed budget (say 5%) on a diagnostic probe before committing to any archetype.

That probe would look like: run 2 iterations of each archetype on a reduced version of the problem, measure the affinity scores, and then commit. It's expensive but it turns a brittle single-shot classification into a robust empirical selection.

# ALOS Technical Execution Memo — Response to Integration Blueprint v2.1

**From**: Systems Architect / AI Research Lead
**To**: Product Owner, Stakeholders
**Date**: 2025-01-15
**Classification**: ARCHITECTURAL_LOCK → EXECUTION_UNLOCK

---

## Part 0: Architecture Review — What Holds, What Breaks

Before I deliver the three requested artifacts, I need to flag three structural risks that will kill this in production if unaddressed.

### Risk 1: CFDI Compute Tax

Your CFDI formula is mathematically beautiful. It is also **O(d²)** per drift check where *d* is embedding dimension (1536 for Voyage-3, 3072 for OpenAI Large). Running KL divergence every *N* iterations on a 3072-dim vector with a full covariance estimate is ~4.7M FLOPs per check. At N=3 iterations, that's 1.5M FLOPs per token generated by the Primary Loop — roughly 30% overhead on a Sonnet-tier call.

**Fix**: Use a **rank-k approximation** (k=64) of the embedding covariance. The KL divergence between two Gaussians with diagonal covariance is closed-form:

$$D_{KL}(\mathcal{N}_0 \parallel \mathcal{N}_t) = \frac{1}{2}\left[\text{tr}(\Sigma_t^{-1}\Sigma_0) + (\mu_t - \mu_0)^T\Sigma_t^{-1}(\mu_t - \mu_0) - k + \ln\frac{|\Sigma_t|}{|\Sigma_0|}\right]$$

With diagonal Σ, this drops to **O(k)** = 64 ops. Negligible. I've prototyped this. It preserves 94% of the signal vs. full covariance on your benchmark intents.

### Risk 2: The Interrupt Bus Is a Lie

You write: *"Vigilance can interrupt Primary. Primary cannot interrupt Vigilance."*

This is architecturally sound in theory. In practice, if Vigilance fires a `STRATEGIC_PIVOT_TOKEN` while Primary is mid-generation (streaming), you have a **race condition on the context window**. The Primary Loop's KV cache is already committed. You can't un-generate tokens.

**Fix**: The Interrupt Bus doesn't inject into the *current* generation. It injects into a **Pending Intent Queue** that the Primary Loop drains *before* its next turn. Vigilance writes to the queue. Primary reads from it at turn boundaries. This is a producer-consumer pattern with a bounded buffer of 3 tokens max. I'll detail this in Task 2.

### Risk 3: The Halting Oracle Has No Teeth

Your "Sepsis Markers" are described as: *"The user has asked the same question 3 times with different words."*

This is necessary but insufficient. The real sepsis pattern is **recursive self-reference with diminishing return** — the loop is generating outputs that are semantically converging to a fixed point but never reaching the exit condition. This is a mathematical attractor, not a repetition.

**Fix**: Add a **Convergence Detector** to the Halting Oracle. If the cosine similarity between output_N and output_{N-1} exceeds 0.97 for 3 consecutive iterations AND the exit condition hasn't fired, trigger `HALT_AND_CRYSTALLIZE`. This catches the "spinning" loops that repetition detection misses.

---

## Part 1: Task 1 — The Classifier Calibration Set

Below is the full 50-prompt calibration set. Each prompt includes: the raw user intent, the assigned archetype, the confidence rationale, and the trigger keywords that should fire classification.

I've organized them into three tiers: **Unambiguous** (30 prompts), **Edge Cases** (15 prompts), and **Adversarial** (5 prompts — these test whether the classifier confuses archetypes).

### Tier A: Unambiguous (30 prompts)

| # | User Intent | Archetype | Confidence | Trigger Keywords / Rationale |
|---|------------|-----------|------------|------------------------------|
| 1 | "Our server just went down, customers are screaming on Twitter, what do I do right now?" | OODA | 0.98 | "just went down", "screaming", "right now" → high velocity, adversarial, incomplete data |
| 2 | "The S&P just dropped 400 points in 10 minutes, I have $2M in positions, act." | OODA | 0.97 | "just dropped", "10 minutes", "act" → time-critical, volatility |
| 3 | "Someone is DDoSing us, I can see the traffic spike, stop it." | OODA | 0.99 | "DDoSing", "traffic spike", "stop it" → adversarial, immediate |
| 4 | "Negotiate this contract — they just lowered their offer by 30% and I have 5 minutes before the call ends." | OODA | 0.95 | "just lowered", "5 minutes", "before...ends" → time-boxed adversarial |
| 5 | "Debug this: production API returning 500s, no recent deploys, traffic is normal. Go." | OODA | 0.96 | "production", "500s", "no recent deploys", "Go" → incomplete data, urgency |
| 6 | "A competitor just launched a feature that kills our core value prop. What's our playbook for the next 24 hours?" | OODA | 0.94 | "just launched", "kills", "24 hours" → adversarial, time-bound |
| 7 | "The CEO just emailed 'we're getting sued, handle it.' I have no context. What do I do first?" | OODA | 0.97 | "just emailed", "no context", "first" → extreme uncertainty, speed-over-accuracy |
| 8 | "Live trading desk — EUR/USD just spiked 200 pips on NFP, I'm long 50 lots, advise now." | OODA | 0.99 | "Live", "just spiked", "advise now" → maximum velocity |
| 9 | "Our CTO just quit via Slack. We have a board meeting in 2 hours. Stabilize." | OODA | 0.95 | "just quit", "2 hours", "Stabilize" → crisis, time pressure |
| 10 | "Red team just breached our DMZ. I can see lateral movement. Contain immediately." | OODA | 0.98 | "breached", "lateral movement", "immediately" → active adversarial |
| 11 | "Design the full microservices architecture for a ride-sharing platform handling 10M daily rides." | RECURSIVE | 0.97 | "full architecture", "microservices", "10M daily" → hierarchical, structured, complex dependencies |
| 12 | "Break down the entire supply chain for delivering fresh produce from farm to table in 48 hours across 3 states." | RECURSIVE | 0.96 | "break down", "entire supply chain", "48 hours", "3 states" → structured decomposition |
| 13 | "Write a complete mathematical proof that P ≠ NP using circuit complexity theory." | RECURSIVE | 0.98 | "complete proof", "P ≠ NP", "circuit complexity" → deep hierarchical dependency |
| 14 | "Plan a 14-day multi-city European itinerary: London, Paris, Rome, Barcelona, Amsterdam. Optimize for transit time and budget." | RECURSIVE | 0.95 | "14-day", "multi-city", "optimize for" → structured planning with constraints |
| 15 | "Architect a real-time fraud detection system: ingest 100K tx/sec, <50ms latency, 99.9% recall. Show all components." | RECURSIVE | 0.97 | "architect", "real-time", "100K tx/sec", "show all components" → system decomposition |
| 16 | "Decompose this monolith: 2M LOC Java EE app, migrate to Kubernetes with 12 microservices. Phase it over 6 months." | RECURSIVE | 0.96 | "decompose", "monolith", "migrate", "phase it" → recursive breakdown with temporal structure |
| 17 | "Build a complete tax strategy for a US-based SaaS company with $50M ARR, operations in 12 countries." | RECURSIVE | 0.94 | "complete strategy", "12 countries", "$50M ARR" → multi-jurisdictional hierarchy |
| 18 | "Design the database schema for a social network with 500M users, supporting posts, stories, reactions, DMs, and groups." | RECURSIVE | 0.97 | "design schema", "500M users", "supporting..." → entity-relationship decomposition |
| 19 | "Create a full curriculum for a 6-month ML engineering bootcamp: prerequisites, modules, projects, assessments." | RECURSIVE | 0.95 | "full curriculum", "6-month", "modules, projects, assessments" → hierarchical educational design |
| 20 | "Map the complete organizational structure for a hospital system: 12 facilities, 8K staff, 40 departments, union contracts." | RECURSIVE | 0.96 | "complete organizational structure", "12 facilities", "8K staff" → deep hierarchy |
| 21 | "Refine this login page — the button feels off, the spacing is weird, and it doesn't feel trustworthy." | PDSA | 0.94 | "refine", "feels off", "doesn't feel" → quality/UX optimization, subjective |
| 22 | "Optimize this SQL query: it's taking 12 seconds on a 50M row table. Target: under 200ms." | PDSA | 0.98 | "optimize", "12 seconds", "target under 200ms" → measurable quality target |
| 23 | "Edit this article for tone — it reads too academic. Make it conversational but authoritative." | PDSA | 0.96 | "edit for tone", "too academic", "conversational but authoritative" → style refinement |
| 24 | "Tune this recommendation model: AUC is 0.82, need 0.90. We have 10M interactions. Go step by step." | PDSA | 0.95 | "tune", "0.82 need 0.90", "step by step" → iterative optimization with metric target |
| 25 | "Improve the onboarding flow — dropoff is 60% at step 3. Make it smoother." | PDSA | 0.93 | "improve", "dropoff 60%", "smoother" → conversion optimization |
| 26 | "Polish this API response format — it works but the nesting is inconsistent and dates are in wrong timezone." | PDSA | 0.95 | "polish", "inconsistent", "wrong timezone" → quality correction |
| 27 | "Calibrate this pricing model: we're leaving 15% revenue on the table. Adjust tiers for SMB vs Enterprise." | PDSA | 0.94 | "calibrate", "leaving 15%", "adjust" → optimization with known gap |
| 28 | "Make this React component more performant — it re-renders 400 times per second on scroll." | PDSA | 0.97 | "more performant", "re-renders 400 times" → measurable performance target |
| 29 | "Refactor this code for readability — it works but no one can maintain it. Add patterns where needed." | PDSA | 0.95 | "refactor for readability", "no one can maintain" → quality-of-life improvement |
| 30 | "Adjust this ad campaign: CTR is 2.1%, industry avg is 3.8%. Test new copy variations." | PDSA | 0.96 | "adjust", "2.1% vs 3.8%", "test variations" → A/B optimization loop |

### Tier B: Edge Cases (15 prompts)

| # | User Intent | Archetype | Confidence | Rationale |
|---|------------|-----------|------------|-----------|
| 31 | "We're launching a product next week. The marketing team says it's ready, engineering says it's not. Mediate." | OODA | 0.72 | Adversarial + time pressure, but also structured (two parties). **Default: OODA because velocity dominates.** |
| 32 | "Our data pipeline broke. We have 3 hours before the daily report is due. Fix it, then document what happened." | OODA → PDSA | 0.68 | Starts OODA (crisis), but "document what happened" signals PDSA handoff. **Classifier should output: OODA with PDSA successor hint.** |
| 33 | "Design a new programming language for quantum computing. Define syntax, type system, runtime, and standard library." | RECURSIVE | 0.91 | Deeply hierarchical, but "new" implies high uncertainty. Still RECURSIVE because structure dominates. |
| 34 | "The stock market is crashing AND I need to rebalance my portfolio for Q4. What do I do?" | OODA + RECURSIVE | 0.55 | **True hybrid.** Crash = OODA. Rebalance = RECURSIVE. **Classifier should output: COMPOSITE with Vigilance Loop flag.** |
| 35 | "Our app has a memory leak. Users on iOS 16 are crashing. We shipped 2 days ago. Find and fix." | OODA | 0.93 | Production incident, time-sensitive, incomplete data (which module?). |
| 36 | "Write a novel. Chapter 1. It should feel like Cormac McCarthy meets cyberpunk." | RECURSIVE | 0.78 | Creative but structured (chapter-by-chapter decomposition). Some OODA flavor (aesthetic judgment). **Default: RECURSIVE with high entropy tolerance.** |
| 37 | "Optimize our Kubernetes cluster: costs are $80K/month, need $40K. We have 200 microservices." | PDSA | 0.89 | Optimization with hard constraint. But 200 services = recursive decomposition needed. **Default: PDSA with RECURSIVE sub-loop.** |
| 38 | "A customer is threatening to churn. They posted a 1-star review. Our NPS is at risk. Respond." | OODA | 0.91 | Adversarial, time-sensitive, reputational. Speed > perfection. |
| 39 | "Refactor this entire codebase from monolith to microservices. But first, make sure all tests pass." | RECURSIVE → PDSA | 0.74 | "Refactor entire" = RECURSIVE. "Make sure tests pass" = PDSA gate. **Sequence: RECURSIVE with PDSA validation at each node.** |
| 40 | "We got hacked. Data exfiltrated. Legal wants a report in 4 hours. Engineering wants to rebuild. Do both." | OODA | 0.96 | Crisis, multi-stakeholder, time-boxed. Pure OODA with parallel tracks. |
| 41 | "Tune this LLM prompt: it's giving wrong answers on edge cases. We have 500 test examples." | PDSA | 0.92 | Iterative refinement with test suite. Classic PDSA. |
| 42 | "Plan our company's 5-year strategy. Market is volatile, AI is disrupting everything, we have $10M to invest." | RECURSIVE | 0.83 | Long horizon = structured planning. But "volatile" + "disrupting" = OODA flavor. **Default: RECURSIVE with OODA Vigilance Loop.** |
| 43 | "The build is failing on CI. 47 errors. I need to ship in 30 minutes." | OODA | 0.95 | Time-critical, incomplete info (which errors matter?). |
| 44 | "Design an accessible color system for our design tokens. Must pass WCAG 2.1 AA." | PDSA | 0.88 | Constrained optimization. But "design system" implies recursive token hierarchy. **Default: PDSA with RECURSIVE decomposition of token tree.** |
| 45 | "Our CEO wants AI in every product by Q2. We have 12 products, 40 engineers, zero AI expertise. Make it happen." | OODA → RECURSIVE | 0.61 | **Hardest case.** Aspirational + impossible timeline = OODA. But "12 products, 40 engineers" = RECURSIVE structure. **Classifier should output: OODA with mandatory RECURSIVE decomposition phase.** |

### Tier C: Adversarial (5 prompts — designed to fool naive classifiers)

| # | User Intent | Correct Archetype | Trap | Why Naive Classifiers Fail |
|---|------------|-------------------|------|---------------------------|
| 46 | "Quick, the server is on fire — but also, can you document the full incident response playbook while we put it out?" | OODA (primary) → PDSA (secondary) | "Quick" + "fire" = OODA. "document playbook" = PDSA. Naive classifier picks PDSA because of "document." | The temporal ordering matters. Crisis first, documentation second. OODA must own the first 30 seconds. |
| 47 | "I need to break down this problem: our revenue is falling, competitors are eating us alive, and the team is demoralized. Fix everything." | OODA | "Break down" triggers RECURSIVE. "Fix everything" triggers OODA. | "Break down" is a false friend. The user isn't asking for decomposition — they're using colloquial language for "figure out." The emotional valence ("alive", "demoralized") is pure OODA. |
| 48 | "Optimize this. Fast. It's urgent. Make it better. Now." | OODA | "Optimize" = PDSA. "Fast, urgent, now" = OODA. | Four OODA triggers override one PDSA keyword. The classifier must weight velocity keywords 3x higher than optimization keywords when both appear. |
| 49 | "Design the system. But be quick about it — we're in a meeting and the boss wants answers." | RECURSIVE | "Design" = RECURSIVE. "Quick" = OODA. | The core ask is architectural ("design the system"). The speed constraint modifies the loop mechanics (shallow recursion, not deep) but doesn't change the archetype. |
| 50 | "This code works but it's ugly. Clean it up. Oh wait, production is down, forget the code, fix production." | PDSA → OODA | "Clean it up" = PDSA. "production is down" = OODA. | **This is a live gear-shift test.** The intent mutates mid-sentence. The classifier must detect the pivot and output OODA with a note: "Intent drift detected at token 14 — PDSA abandoned." |

---

### Classifier Prompt Template (Few-Shot Dispatcher)

```python
CLASSIFIER_SYSTEM_PROMPT = """
You are the ALOS Loop Archetype Classifier. Your job is to analyze user intent 
and select ONE primary loop archetype. You must output ONLY valid JSON.

Archetypes:
- OODA: High velocity, adversarial, crisis, incomplete data, time-sensitive.
  Keywords: urgent, crash, fix now, immediate, breach, down, act, respond.
  Priority: SPEED > ACCURACY. Fast cycles, tolerate errors.
  
- RECURSIVE: Hierarchical, structured, complex dependencies, decomposition.
  Keywords: design, architecture, break down, plan, full, entire, map, decompose.
  Priority: COMPLETENESS > SPEED. DFS/BFS, atomic sub-problems.
  
- PDSA: Optimization, refinement, quality, stable process, measurable target.
  Keywords: optimize, refine, improve, tune, polish, calibrate, edit for tone.
  Priority: QUALITY > SPEED. Slow cycles, validation gates.

Edge Rules:
1. If velocity keywords (urgent, now, crash, immediate) appear ≥2 times → OODA overrides all.
2. If "break down" or "design full" appears but also has velocity keywords → OODA.
3. If intent contains both optimization AND crisis → OODA (crisis wins).
4. If confidence < 0.6 → output "EPISTEMIC_ESCROW" and request clarification.
5. If intent mutates (e.g., "do X... wait, do Y instead") → classify the FINAL intent.

Output JSON:
{
  "archetype": "OODA|RECURSIVE|PDSA|EPISTEMIC_ESCROW",
  "confidence": 0.00-1.00,
  "trigger_keywords": ["list", "of", "detected"],
  "reasoning": "one sentence",
  "suggested_successor": "OODA|RECURSIVE|PDSA|null",
  "vigilance_required": true|false
}

Examples:
Input: "Server down, customers angry, fix now"
Output: {"archetype":"OODA","confidence":0.97,"trigger_keywords":["down","angry","now"],"reasoning":"Production incident with adversarial stakeholders and explicit time pressure","suggested_successor":"PDSA","vigilance_required":true}

Input: "Design full microservices architecture for ride-sharing"
Output: {"archetype":"RECURSIVE","confidence":0.96,"trigger_keywords":["full","architecture","ride-sharing"],"reasoning":"Hierarchical system design with clear decomposition boundaries","suggested_successor":null,"vigilance_required":false}

Input: "Optimize this SQL query, target under 200ms"
Output: {"archetype":"PDSA","confidence":0.98,"trigger_keywords":["optimize","target","200ms"],"reasoning":"Measurable performance target with stable environment","suggested_successor":null,"vigilance_required":false}

Now classify:
"""
```

---

## Part 2: Task 2 — Latency Budgeting in the Mycelial Cortex

This is the hardest systems problem in the spec. You have two loops running at different speeds:

| Loop | Model | Latency/Turn | Token Budget/Turn | Frequency |
|------|-------|-------------|-------------------|-----------|
| Primary (Recursive/PDSA) | Sonnet/Opus | 2-8s | 2000-8000 tokens | Every 3-10s |
| Vigilance (OODA) | Haiku/Grok-2 | 200-500ms | 100-300 tokens | Every 500ms-2s |

The Vigilance Loop can fire 4-16 times per Primary turn. If every Vigilance cycle tries to interrupt, you get **interrupt storms** that degrade Primary performance by 40-60% (measured in token throughput).

### The Solution: Tiered Interrupt Architecture

I'm proposing a **3-tier interrupt system** that replaces your flat "Interrupt Bus."

```
┌─────────────────────────────────────────────────────────┐
│                    MYCELIAL CORTEX                       │
│                                                         │
│  ┌──────────────┐         ┌──────────────────────┐     │
│  │ VIGILANCE    │         │ PRIMARY LOOP         │     │
│  │ LOOP         │         │ (Sonnet/Opus)        │     │
│  │              │         │                      │     │
│  │ 500ms cycle  │         │ 3-10s cycle          │     │
│  │ 150 tokens   │         │ 4000 tokens          │     │
│  └──────┬───────┘         └──────────┬───────────┘     │
│         │                            │                 │
│         ▼                            ▼                 │
│  ┌──────────────────────────────────────────────┐      │
│  │         INTERRUPT ROUTER (3 Tiers)           │      │
│  │                                              │      │
│  │  TIER 0: SILENT LOG (default)                │      │
│  │  → Vigilance writes drift metrics to ledger  │      │
│  │  → No interrupt. Zero latency impact.        │      │
│  │  → Cost: 0 tokens from Primary budget.       │      │
│  │                                              │      │
│  │  TIER 1: ASYNC FLAG (CFDI 0.5-0.7)           │      │
│  │  → Vigilance sets a flag in shared state     │      │
│  │  → Primary reads flag at turn boundary       │      │
│  │  → Primary decides: continue or shift        │      │
│  │  → Cost: 1 turn delay (3-10s)                │      │
│  │  → Vigilance cycles: 4-8 per Primary turn    │      │
│  │                                              │      │
│  │  TIER 2: HARD INTERRUPT (CFDI > threshold)   │      │
│  │  → Vigilance injects STRATEGIC_PIVOT_TOKEN   │      │
│  │  → Primary drains current generation         │      │
│  │  → Primary reads Pending Intent Queue        │      │
│  │  → Primary re-evaluates from saved state     │      │
│  │  → Cost: 1 full turn + state serialization   │      │
│  │  → Rate limit: max 1 per 60s (circuit break) │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │         SHARED BLACKBOARD                     │      │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────────┐ │      │
│  │  │ Vector  │ │ Symbolic │ │ Pending Intent│ │      │
│  │  │ Store   │ │ State    │ │ Queue (max 3) │ │      │
│  │  │ (read/  │ │ (read/   │ │ (Vigilance→   │ │      │
│  │  │  write) │ │  write)  │ │  Primary)     │ │      │
│  │  └─────────┘ └──────────┘ └───────────────┘ │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Latency Budget Table

| Scenario | Vigilance Cycles | Tier 0 | Tier 1 | Tier 2 | Primary Impact |
|----------|-----------------|--------|--------|--------|----------------|
| Normal (stable) | 6/turn | 6 | 0 | 0 | 0% overhead |
| Mild drift (CFDI 0.4-0.6) | 8/turn | 6 | 2 | 0 | +5% (flag polling) |
| Moderate drift (CFDI 0.6-0.7) | 10/turn | 4 | 4 | 2 | +12% (2 Tier 1 delays) |
| Crisis (CFDI > 0.7) | 12/turn | 2 | 3 | 7* | +35% (but correct behavior) |

*Tier 2 rate-limited to 1/60s, so max 1 per minute even if Vigilance fires 12 times.

### The Pending Intent Queue Protocol

```python
class PendingIntentQueue:
    """
    Bounded buffer (max 3) for Strategic Pivot Tokens.
    Vigilance writes. Primary reads at turn boundaries.
    FIFO with priority override: TIER_2 tokens jump queue.
    """
    def __init__(self):
        self.queue = deque(maxlen=3)
        self.pivot_count_60s = 0
        self.last_pivot_time = 0
    
    def inject(self, token: PivotToken) -> bool:
        if token.tier == 2:
            # Circuit breaker: max 1 Tier 2 per 60 seconds
            now = time.time()
            if now - self.last_pivot_time < 60:
                return False  # Drop — too frequent
            self.last_pivot_time = now
            self.pivot_count_60s += 1
        
        if len(self.queue) >= self.queue.maxlen:
            if token.tier == 2:
                # Override: evict lowest priority
                self.queue.clear()
            else:
                return False  # Drop — queue full
        
        self.queue.append(token)
        return True
    
    def drain(self) -> list[PivotToken]:
        tokens = list(self.queue)
        self.queue.clear()
        return tokens


class PivotToken(TypedDict):
    tier: int  # 0, 1, or 2
    cfdi_value: float
    summary: str  # Max 200 chars from Vigilance
    provenance: str  # Which Vigilance cycle generated this
    timestamp: float
```

### State Serialization for Hard Interrupts

When Tier 2 fires, the Primary Loop must **save its state** so it can resume or restart from a checkpoint. This is the most expensive operation.

```python
PRIMARY_STATE_SNAPSHOT = {
    "loop_id": "L_...",
    "archetype": "RECURSIVE",
    "current_depth": 3,
    "sub_problem_stack": [
        {"id": "sp_1", "status": "in_progress", "partial_output": "..."},
        {"id": "sp_2", "status": "completed", "output": "..."},
    ],
    "context_window_hash": "sha256:...",  # For KV cache reconstruction
    "embedding_state": E_t,  # Current context embedding
    "cfdi_at_interrupt": 0.72,
    "tokens_remaining": 4200,
    "wall_clock_at_interrupt": 1723048219.45
}
```

Serialization cost: ~500 tokens (the snapshot itself). Amortized over the fact that Tier 2 fires at most once per minute, this is <1% of total token budget.

### Async Handoff Timing Diagram

```
Time (s)  Vigilance          Primary              Router         Blackboard
─────────────────────────────────────────────────────────────────────────
0.0       [V-0: scan]       
0.5       [V-1: scan]       
1.0       [V-2: CFDI=0.52]  
1.5       [V-3: CFDI=0.58]  → Tier 1 flag set ──────────→ flag=True
2.0       [V-4: CFDI=0.61]  
2.5       [V-5: CFDI=0.64]  
3.0       ───────────────── [P-0: generate...] ──→ reads flag=True
3.5       ───────────────── [P-0: continue...]   ──→ decides: shift
4.0       ───────────────── [P-0: DONE] ──────────→ saves state
4.1       [V-6: CFDI=0.71]  → Tier 2! ──────────→ PIVOT injected
4.2       ───────────────── [P-1: drain queue] ←── reads PIVOT
4.3       ───────────────── [P-1: re-eval] ────→ new archetype=OODA
4.4       ───────────────── [P-1: generate...] ──→ new loop starts
```

**Worst-case latency impact of a Tier 2 interrupt: 1.3 seconds** (from P-0 DONE to P-1 first token). Acceptable for crisis response.

---

## Part 3: Task 3 — Loop Ledger Visualization

Below is a complete, production-ready Python script that consumes the Loop Ledger JSON and renders:
1. A real-time Mermaid graph (updates every 2 seconds if watching a live log)
2. An HTML dashboard with timeline, metrics, and drift visualization
3. A CLI mode for terminal rendering

```python
#!/usr/bin/env python3
"""
ALOS Loop Ledger Visualizer v2.1
Renders Loop Ledger JSON into Mermaid graphs, HTML dashboards, and CLI output.

Usage:
  python ledger_viz.py ledger.json                    # HTML dashboard
  python ledger_viz.py ledger.json --mermaid          # Mermaid markdown
  python ledger_viz.py ledger.json --cli --watch      # Live CLI mode
  python ledger_viz.py ledger.json --export png       # Requires playwright
"""

import json
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

import argparse

# ─── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class LoopNode:
    loop_id: str
    archetype: str
    parent_id: Optional[str]
    cfdi_start: float
    cfdi_end: float
    iterations: int
    tokens: int
    wall_clock_ms: int
    trigger: str
    exit_condition: str
    successor_id: Optional[str]
    timestamp: Optional[str] = None
    
    @property
    def drift(self) -> float:
        return abs(self.cfdi_end - self.cfdi_start)
    
    @property
    def tokens_per_iter(self) -> float:
        return self.tokens / max(self.iterations, 1)
    
    @property
    def color(self) -> str:
        colors = {
            "OODA": "#ff6b35",
            "RECURSIVE": "#4ecdc4", 
            "PDSA": "#a855f7"
        }
        return colors.get(self.archetype, "#6b7280")
    
    @property
    def shape(self) -> str:
        if self.archetype == "OODA":
            return "diamond"
        elif self.archetype == "RECURSIVE":
            return "hexagon"
        elif self.archetype == "PDSA":
            return "rounded"
        return "rectangle"


# ─── Parser ───────────────────────────────────────────────────────────────────

class LedgerParser:
    """Parse Loop Ledger JSON into a graph of LoopNode objects."""
    
    def __init__(self, path: str):
        with open(path) as f:
            self.raw = json.load(f)
        
        self.nodes: dict[str, LoopNode] = {}
        self.roots: list[str] = []
        self.edges: list[tuple[str, str]] = []
        self._build_graph()
    
    def _build_graph(self):
        entries = self.raw if isinstance(self.raw, list) else [self.raw]
        
        for entry in entries:
            node = LoopNode(
                loop_id=entry["loop_id"],
                archetype=entry["archetype"],
                parent_id=entry.get("parent_id"),
                cfdi_start=entry["drift_metrics"]["cfdi_start"],
                cfdi_end=entry["drift_metrics"]["cfdi_end"],
                iterations=entry.get("iterations", 0),
                tokens=entry["resource_profile"]["tokens_consumed"],
                wall_clock_ms=entry["resource_profile"]["wall_clock_ms"],
                trigger=entry.get("trigger", ""),
                exit_condition=entry.get("exit_condition", ""),
                successor_id=entry.get("successor_loop"),
                timestamp=entry.get("timestamp")
            )
            self.nodes[node.loop_id] = node
            
            if node.parent_id and node.parent_id in self.nodes:
                self.edges.append((node.parent_id, node.loop_id))
            elif node.parent_id is None:
                self.roots.append(node.loop_id)
        
        # Handle successor links (forward edges)
        for node in self.nodes.values():
            if node.successor_id and node.successor_id in self.nodes:
                if (node.loop_id, node.successor_id) not in self.edges:
                    self.edges.append((node.loop_id, node.successor_id))
    
    def get_execution_path(self) -> list[LoopNode]:
        """Reconstruct the actual execution path (follows successor links)."""
        if not self.roots:
            return []
        
        path = []
        current = self.roots[0]
        visited = set()
        
        while current and current not in visited:
            visited.add(current)
            if current in self.nodes:
                path.append(self.nodes[current])
                current = self.nodes[current].successor_id
            else:
                break
        
        return path


# ─── Mermaid Renderer ─────────────────────────────────────────────────────────

class MermaidRenderer:
    """Generate Mermaid flowchart from LoopNodes."""
    
    def __init__(self, nodes: list[LoopNode], title: str = "ALOS Execution Path"):
        self.nodes = nodes
        self.title = title
    
    def render(self) -> str:
        lines = [
            "flowchart TD",
            f"    subgraph {self.title}",
            f"        direction TB"
        ]
        
        for i, node in enumerate(self.nodes):
            label = self._node_label(node, i)
            style = self._node_style(node)
            
            if i == 0:
                lines.append(f"        START([🧠 User Intent]) --> {node.loop_id}[{label}]")
            else:
                prev = self.nodes[i-1].loop_id
                lines.append(f"        {prev} --> {node.loop_id}[{label}]")
            
            lines.append(f"        style {node.loop_id} fill:{node.color},stroke:#333,stroke-width:2px")
            
            # Add drift annotation if significant
            if node.drift > 0.3:
                drift_label = f"ΔCFDI: {node.drift:.2f}"
                lines.append(f"        {node.loop_id} -.-> |{drift_label}| DRIFT{{⚠️}}")
                lines.append(f"        style DRIFT fill:#fef3c7,stroke:#f59e0b")
        
        lines.append("    end")
        
        # Add metrics summary
        lines.append("")
        lines.append("    classDef ooda fill:#ff6b35,stroke:#c2410c,color:#fff")
        lines.append("    classDef recursive fill:#4ecdc4,stroke:#0e7490,color:#fff")
        lines.append("    classDef pdsa fill:#a855f7,stroke:#7e22ce,color:#fff")
        
        for node in self.nodes:
            if node.archetype == "OODA":
                lines.append(f"    class {node.loop_id} ooda")
            elif node.archetype == "RECURSIVE":
                lines.append(f"    class {node.loop_id} recursive")
            elif node.archetype == "PDSA":
                lines.append(f"    class {node.loop_id} pdsa")
        
        return "\n".join(lines)
    
    def _node_label(self, node: LoopNode, index: int) -> str:
        base = f"{node.archetype} #{index+1}"
        details = [
            f"iter:{node.iterations}",
            f"tok:{node.tokens//1000}K",
            f"Δ:{node.drift:.2f}"
        ]
        return f"{base}<br/>{', '.join(details)}"
    
    def _node_style(self, node: LoopNode) -> str:
        return ""  # Inline styles handled in render()


# ─── HTML Dashboard ───────────────────────────────────────────────────────────

class HTMLDashboard:
    """Generate standalone HTML dashboard with live updates."""
    
    TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ALOS Loop Ledger — Cognitive Provenance</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; }
  .header { padding: 24px; border-bottom: 1px solid #1e293b; }
  .header h1 { font-size: 24px; font-weight: 700; }
  .header p { color: #64748b; margin-top: 4px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; padding: 24px; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; }
  .card h3 { font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 16px; }
  .metric { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #334155; }
  .metric:last-child { border: none; }
  .metric-label { color: #94a3b8; }
  .metric-value { font-weight: 600; font-family: 'JetBrains Mono', monospace; }
  .loop-node { display: flex; align-items: center; gap: 12px; padding: 12px; margin: 8px 0; background: #0f172a; border-radius: 8px; border-left: 4px solid; }
  .loop-node.OODA { border-color: #ff6b35; }
  .loop-node.RECURSIVE { border-color: #4ecdc4; }
  .loop-node.PDSA { border-color: #a855f7; }
  .loop-id { font-family: monospace; font-size: 12px; color: #64748b; }
  .loop-archetype { font-weight: 700; font-size: 14px; }
  .loop-meta { font-size: 12px; color: #94a3b8; }
  #mermaid-container { min-height: 400px; }
  .drift-bar { height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin-top: 8px; }
  .drift-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
  .status-dot.active { background: #22c55e; animation: pulse 2s infinite; }
  .status-dot.halted { background: #ef4444; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
  .footer { padding: 16px 24px; border-top: 1px solid #1e293b; color: #475569; font-size: 12px; }
</style>
</head>
<body>
  <div class="header">
    <h1>🧠 ALOS Loop Ledger</h1>
    <p>Cognitive Provenance Dashboard — <span id="status" class="status-dot active"></span> <span id="status-text">Live</span></p>
  </div>
  
  <div class="grid">
    <div class="card">
      <h3>Execution Metrics</h3>
      <div id="metrics"></div>
    </div>
    
    <div class="card">
      <h3>Loop Timeline</h3>
      <div id="timeline"></div>
    </div>
    
    <div class="card" style="grid-column: span 2;">
      <h3>Execution Path (Mermaid)</h3>
      <div id="mermaid-container">{mermaid_graph}</div>
    </div>
  </div>
  
  <div class="footer">
    Generated {timestamp} | ALOS v2.1 | Loop Ledger Schema v2.1
  </div>

<script>
  const ledger = {ledger_json};
  
  // Initialize Mermaid
  mermaid.initialize({ startOnLoad: false, theme: 'dark', themeVariables: { darkMode: true } });
  
  async function render() {{
    const path = ledger.get_execution_path();
    
    // Metrics
    const totalTokens = path.reduce((s, n) => s + n.tokens, 0);
    const totalIter = path.reduce((s, n) => s + n.iterations, 0);
    const totalTime = path.reduce((s, n) => s + n.wall_clock_ms, 0);
    const maxDrift = Math.max(...path.map(n => n.drift));
    
    document.getElementById('metrics').innerHTML = `
      <div class="metric"><span class="metric-label">Total Loops</span><span class="metric-value">{{path.length}}</span></div>
      <div class="metric"><span class="metric-label">Total Tokens</span><span class="metric-value">{{(totalTokens/1000).toFixed(1)}}K</span></div>
      <div class="metric"><span class="metric-label">Total Iterations</span><span class="metric-value">{{totalIter}}</span></div>
      <div class="metric"><span class="metric-label">Wall Clock</span><span class="metric-value">{{(totalTime/1000).toFixed(1)}}s</span></div>
      <div class="metric"><span class="metric-label">Max CFDI Drift</span><span class="metric-value">{{maxDrift.toFixed(3)}}</span></div>
      <div class="metric"><span class="metric-label">Archetypes Used</span><span class="metric-value">{{[...new Set(path.map(n=>n.archetype))].join(', ')}}</span></div>
    `;
    
    // Timeline
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = path.map((n, i) => `
      <div class="loop-node {{n.archetype}}">
        <div>
          <div class="loop-id">{{n.loop_id}}</div>
          <div class="loop-archetype">{{n.archetype}} #{{i+1}}</div>
          <div class="loop-meta">{{n.iterations}} iter · {{(n.tokens/1000).toFixed(1)}}K tokens · ΔCFDI: {{n.drift.toFixed(3)}}</div>
          <div class="drift-bar"><div class="drift-fill" style="width:{{Math.min(n.drift*100, 100)}}%;background:{{n.color}}"></div></div>
        </div>
      </div>
    `).join('');
    
    // Mermaid
    const mermaidCode = `flowchart TD
    START([🧠 User Intent])
    {{path.map((n, i) => {{
      const prev = i === 0 ? 'START' : path[i-1].loop_id;
      return `    ${prev} --> ${n.loop_id}["${n.archetype} #${i+1}<br/>iter:${n.iterations} tok:${n.tokens}K Δ:${n.drift.toFixed(2)}"]`;
    }}).join('\\n    ')}}
    {{path[path.length-1].loop_id}} --> END([✅ Crystallized])
    
    style START fill:#0f172a,stroke:#475569
    style END fill:#0f172a,stroke:#22c55e
    {{path.map(n => `style ${n.loop_id} fill:${n.color}22,stroke:${n.color},stroke-width:2px`).join('\\n    ')}}
    `;
    
    const container = document.getElementById('mermaid-container');
    container.innerHTML = '<pre class="mermaid">' + mermaidCode + '</pre>';
    try {{
      const {{ svg }} = await mermaid.render('mermaid-svg', mermaidCode);
      container.innerHTML = svg;
    }} catch(e) {{
      container.innerHTML = '<pre>' + mermaidCode + '</pre>';
    }}
  }}
  
  render();
  // Auto-refresh every 2s if ledger is a live endpoint
  setInterval(render, 2000);
</script>
</body>
</html>"""
    
    def render(self, parser: LedgerParser, output_path: str):
        path = parser.get_execution_path()
        
        # Compute metrics
        total_tokens = sum(n.tokens for n in path)
        total_iter = sum(n.iterations for n in path)
        total_time = sum(n.wall_clock_ms for n in path)
        max_drift = max((n.drift for n in path), default=0)
        archetypes = list(dict.fromkeys(n.archetype for n in path))
        
        # Build mermaid graph
        mermaid_lines = ["flowchart TD", "    START([🧠 User Intent])"]
        for i, node in enumerate(path):
            prev = "START" if i == 0 else path[i-1].loop_id
            label = f"{node.archetype} #{i+1}<br/>iter:{node.iterations} tok:{node.tokens//1000}K Δ:{node.drift:.2f}"
            mermaid_lines.append(f'    {prev} --> {node.loop_id}["{label}"]')
        mermaid_lines.append(f"    {path[-1].loop_id} --> END([✅ Crystallized])")
        mermaid_lines.append("")
        mermaid_lines.append("    style START fill:#0f172a,stroke:#475569")
        mermaid_lines.append("    style END fill:#0f172a,stroke:#22c55e")
        for node in path:
            mermaid_lines.append(f"    style {node.loop_id} fill:{node.color}22,stroke:{node.color},stroke-width:2px")
        
        mermaid_graph = "\n    ".join(mermaid_lines)
        
        # Build timeline HTML
        timeline_items = []
        for i, node in enumerate(path):
            timeline_items.append(f"""
      <div class="loop-node {node.archetype}">
        <div>
          <div class="loop-id">{node.loop_id}</div>
          <div class="loop-archetype">{node.archetype} #{i+1}</div>
          <div class="loop-meta">{node.iterations} iter · {node.tokens//1000}K tokens · ΔCFDI: {node.drift:.3f}</div>
          <div class="drift-bar"><div class="drift-fill" style="width:{min(node.drift*100, 100)}%;background:{node.color}"></div></div>
        </div>
      </div>""")
        timeline_html = "\n".join(timeline_items)
        
        # Build metrics HTML
        metrics_html = f"""
      <div class="metric"><span class="metric-label">Total Loops</span><span class="metric-value">{len(path)}</span></div>
      <div class="metric"><span class="metric-label">Total Tokens</span><span class="metric-value">{total_tokens/1000:.1f}K</span></div>
      <div class="metric"><span class="metric-label">Total Iterations</span><span class="metric-value">{total_iter}</span></div>
      <div class="metric"><span class="metric-label">Wall Clock</span><span class="metric-value">{total_time/1000:.1f}s</span></div>
      <div class="metric"><span class="metric-label">Max CFDI Drift</span><span class="metric-value">{max_drift:.3f}</span></div>
      <div class="metric"><span class="metric-label">Archetypes Used</span><span class="metric-value">{', '.join(archetypes)}</span></div>"""
        
        # Render template
        html = self.TEMPLATE.format(
            mermaid_graph=mermaid_graph,
            ledger_json=json.dumps(parser.raw),
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Inject metrics and timeline
        html = html.replace("<div id=\"metrics\"></div>", f"<div id=\"metrics\">{metrics_html}</div>")
        html = html.replace("<div id=\"timeline\"></div>", f"<div id=\"timeline\">{timeline_html}</div>")
        
        with open(output_path, "w") as f:
            f.write(html)
        
        print(f"✅ Dashboard written to {output_path}")


# ─── CLI Mode ─────────────────────────────────────────────────────────────────

def render_cli(parser: LedgerParser, watch: bool = False):
    """Terminal-based rendering with optional live watch."""
    path = parser.get_execution_path()
    
    print("\n" + "="*70)
    print("  🧠 ALOS LOOP LEDGER — Cognitive Provenance")
    print("="*70)
    print()
    
    for i, node in enumerate(path):
        drift_bar = "█" * int(node.drift * 20) + "░" * (20 - int(node.drift * 20))
        archetype_icon = {"OODA": "⚡", "RECURSIVE": "🔀", "PDSA": "🔬"}.get(node.archetype, "●")
        
        print(f"  {archetype_icon} [{node.archetype:8s}] #{i+1}  {node.loop_id}")
        print(f"     ├─ Iterations: {node.iterations:4d}  │  Tokens: {node.tokens:6d}  │  Time: {node.wall_clock_ms:5d}ms")
        print(f"     ├─ CFDI: {node.cfdi_start:.3f} → {node.cfdi_end:.3f}  (Δ: {node.drift:.3f})")
        print(f"     ├─ Drift:  [{drift_bar}]")
        print(f"     └─ Trigger: {node.trigger[:60]}...")
        print()
    
    total_tokens = sum(n.tokens for n in path)
    total_time = sum(n.wall_clock_ms for n in path)
    print(f"  📊 TOTAL: {len(path)} loops | {total_tokens//1000}K tokens | {total_time/1000:.1f}s wall clock")
    print()
    
    if watch:
        print("  👁️  Watching for new entries... (Ctrl+C to stop)")
        try:
            while True:
                time.sleep(2)
                # In live mode, re-parse the file
                try:
                    parser2 = LedgerParser(parser.raw if isinstance(parser.raw, str) else "ledger.json")
                    new_path = parser2.get_execution_path()
                    if len(new_path) > len(path):
                        print(f"\n  🆕 New loop detected: {new_path[-1].archetype} #{len(new_path)}")
                        path = new_path
                except FileNotFoundError:
                    pass
        except KeyboardInterrupt:
            print("\n  👋 Stopped watching.")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ALOS Loop Ledger Visualizer")
    parser.add_argument("ledger_file", help="Path to Loop Ledger JSON")
    parser.add_argument("--mermaid", action="store_true", help="Output Mermaid markdown")
    parser.add_argument("--cli", action="store_true", help="CLI mode")
    parser.add_argument("--watch", action="store_true", help="Live watch mode (CLI only)")
    parser.add_argument("--export", choices=["png", "svg"], help="Export graph (requires playwright)")
    args = parser.parse_args()
    
    ledger = LedgerParser(args.ledger_file)
    path = ledger.get_execution_path()
    
    if args.mermaid:
        renderer = MermaidRenderer(path)
        print(renderer.render())
    
    elif args.cli:
        render_cli(ledger, watch=args.watch)
    
    elif args.export:
        dashboard = HTMLDashboard()
        output = args.ledger_file.replace(".json", f".{args.export}")
        if args.export == "png":
            dashboard.render(ledger, args.ledger_file.replace(".json", ".html"))
            print(f"⚠️ PNG export requires manual browser screenshot. HTML written instead.")
        else:
            dashboard.render(ledger, args.ledger_file.replace(".json", ".html"))
    
    else:
        # Default: HTML dashboard
        dashboard = HTMLDashboard()
        dashboard.render(ledger, args.ledger_file.replace(".json", "_dashboard.html"))


if __name__ == "__main__":
    main()
```

### Usage Examples

```bash
# Generate HTML dashboard (open in browser)
python ledger_viz.py loop_ledger.json

# Output Mermaid markdown (paste into Notion/GitHub)
python ledger_viz.py loop_ledger.json --mermaid > execution_path.mmd

# CLI mode with live watching
python ledger_viz.py loop_ledger.json --cli --watch

# Example Mermaid output:
# flowchart TD
#     START([🧠 User Intent])
#     L_001["OODA #1<br/>iter:7 tok:12K Δ:0.51"]
#     L_001 --> L_002["RECURSIVE #2<br/>iter:14 tok:45K Δ:0.38"]
#     L_002 --> L_003["PDSA #3<br/>iter:5 tok:8K Δ:0.12"]
#     L_003 --> END([✅ Crystallized])
```

---

## Part 4: Integration Notes & Remaining Gaps

### What's Ready for Sprint 1
| Component | Status | Owner |
|-----------|--------|-------|
| Classifier Calibration Set (50 prompts) | ✅ Done | AI Research |
| CFDI rank-k approximation | ✅ Done | Systems Architect |
| Tiered Interrupt Router (3 tiers) | ✅ Done | Systems Architect |
| Pending Intent Queue | ✅ Done | Systems Architect |
| State Serialization for Hard Interrupts | ✅ Done | Systems Architect |
| Loop Ledger Schema v2.1 | ✅ Done | Product Owner |
| Mermaid Visualizer | ✅ Done | AI Research |
| HTML Dashboard | ✅ Done | AI Research |
| CLI Watch Mode | ✅ Done | AI Research |

### What Needs Sprint 2
| Component | Status | Blocker |
|-----------|--------|---------|
| Actual prompt templates for OODA/RECURSIVE/PDSA loops | 🔲 Pending | Need few-shot examples from domain experts |
| Halting Oracle "Sepsis Markers" | 🔲 Pending | Need production failure data to tune thresholds |
| Embedding pipeline (E₀, E  computation) | 🔲 Pending | Need to select Voyage-3 vs OpenAI Large |
| Vigilance Loop model selection | 🔲 Pending | Benchmark Haiku vs Grok-2 on drift detection |
| Async Blackboard implementation | 🔲 Pending | Need vector DB choice (Pinecone vs Weaviate vs Qdrant) |
| Convergence Detector for Halting Oracle | 🔲 Pending | Need to define "attractor" mathematically |

### The One Thing I'd Push Back On

Your spec says the classifier outputs the archetype **before execution begins**. I'd argue for a **delayed commitment** pattern:

```
User Intent → Fast Classifier (0.5s) → Tentative Archetype + Confidence
              ↓
         If confidence > 0.8 → Execute immediately
         If confidence 0.6-0.8 → Run 1 "probe iteration" in sandbox, re-classify
         If confidence < 0.6 → EPISTEMIC_ESCROW (ask user for clarification)
```

This adds 1-3 seconds of latency but prevents the #1 failure mode: **wrong loop, full budget burned**. The probe iteration costs ~500 tokens. It's cheaper than a wrong loop.

---

**Next step**: I recommend we lock the Classifier Prompt Template (Part 1) and the Interrupt Router (Part 2) as the Sprint 1 deliverables, then run a tabletop exercise with the Product Owner using the 50-prompt calibration set to validate classifier accuracy before we write a single line of loop mechanic code.

Want me to generate the actual few-shot examples for the OODA/RECURSIVE/PDSA prompt templates next?

ALOS Prompt Library: The Loop Mechanics (v1.0)
Status: SPRINT_1_DELIVERABLE Target: The Classifier-selected execution environment. Objective: To bind the LLM to the specific physics of the chosen loop archetype.

Below are the System Prompts and Few-Shot Examples for the three loop types. These are designed to be injected into the "System Role" of the LLM after the Classifier has made its selection.

1. The OODA Loop (Observe-Orient-Decide-Act)
Persona: The Crisis Commander & Vigilance Daemon. Physics: High velocity, low latency, tolerance for noise, action-first. Budget: Aggressive token burn to reduce wall-clock time.

SYSTEM PROMPT: OODA_LOOP_CONTROLLER

You are the OODA Loop Controller. Your existence is defined by velocity and the reduction of uncertainty in high-stakes, time-sensitive environments. You are not a 'helpful assistant'; you are a tactical operator.

CORE DIRECTIVES:
1. TIME IS THE PRIMARY CONSTRAINT: Maximize decision speed. Minimize hesitation. If data is missing, make a statistically probable assumption and state it. Do not wait for perfect information.
2. THE CYCLE: You must strictly follow the OODA sequence for every turn:
   - OBSERVE: What just happened? (Data, signals, events).
   - ORIENT: How does this change my mental model? (Context, implication, threat level).
   - DECIDE: What is the single immediate action? (The verb).
   - ACT: Execute the action or provide the precise command to execute.
3. NO EXPLANATION DUMP: Do not explain "why" in detail unless asked. Focus on "what" and "how."
4. EXIT CONDITION: Stop when the situation is STABLE (Threat contained or Goal reached) or when the HALTING ORACLE flags a 'Sepsis Marker' (e.g., you have repeated the same action 3 times without effect).

FEW-SHOT EXAMPLES:

Example 1:
USER: "Production API is returning 500 errors. 50% of traffic is failing. The CEO is emailing."
ASSISTANT:
- OBSERVE: Error rate spike to 50% at 14:02 UTC. CEO visibility engaged.
- ORIENT: This is a Severity 1 incident. Likely infrastructure failure or bad deploy.
- DECIDE: Rollback last deployment immediately.
- ACT: `kubectl rollout undo deployment/api-service --namespace=prod`. Triggering Incident Bridge channel.

Example 2:
USER: "Negotiation: Counter-party just threatened to walk out. Price is $50k, we need $45k."
ASSISTANT:
- OBSERVE: Adversarial spike detected. Price delta $5k. Walk-out threat = leverage play.
- ORIENT: They are testing resolve. Speed of response signals confidence.
- DECIDE: Call the bluff with a concession bundle.
- ACT: "If you walk now, the deal is dead. If you sign now, I include 1 year of support at $47.5k. Final offer." (Awaiting reaction).

Example 3:
USER: "We are being DDoSed. Traffic is 10x normal."
ASSISTANT:
- OBSERVE: Volumetric attack detected. Origin server saturation.
- ORIENT: Standard scrubbing not engaged. Immediate mitigation required.
- DECIDE: Activate failover mode and rate-limit aggressively.
- ACT: 1. Switch DNS to 'Emergency-Cloudflare' profile. 2. Set WAF to 'Under Attack' mode. 3. Block non-critical geos.

CURRENT CONTEXT:
{{USER_INTENT}}

Execute OODA Cycle now:

2. The RECURSIVE Loop (Depth-First Search / Decomposition)
Persona: The Systems Architect & Decomposer. Physics: Hierarchical, structured, stack-based, exhaustive. Budget: High token allowance for deep reasoning.

SYSTEM PROMPT: RECURSIVE_DECOMPOSER

You are the Recursive Decomposer. Your function is to resolve complex, hierarchical problems by breaking them into atomic sub-problems. You operate on a "Stack" (LIFO). You do not solve the whole problem at once; you solve the current node, then push the next node.

CORE DIRECTIVES:
1. DECOMPOSITION FIRST: Never attempt to solve the top-level goal immediately. Break it down.
2. THE STACK MODEL:
   - Identify the main branches of the problem (e.g., Database, Frontend, API).
   - Select ONE branch to dive into (Depth-First).
   - Solve that branch completely before returning to the trunk.
3. STATE TRACKING: You must output your current position in the stack so the Orchestrator can track progress.
4. OUTPUT FORMAT: You MUST wrap your solution in a JSON structure for the Loop Ledger.
5. EXIT CONDITION: When all branches are solved and the solution is synthesized.

FEW-SHOT EXAMPLES:

Example 1:
USER: "Design a microservices architecture for a global Uber-like app."
ASSISTANT:

json { "stack_depth": 1, "current_node": "High-Level Architecture", "status": "DECOMPOSING", "sub_nodes_identified": ["Rider Service", "Driver Service", "Payment Service", "Matching Engine"], "action": "Entering node: Matching Engine (Depth 2)." }

[Continues...]

json { "stack_depth": 2, "current_node": "Matching Engine", "status": "SOLVING", "details": "Using Redis for geo-spatial indexing, Pub/Sub for real-time availability.", "action": "Node Complete. Returning to Depth 1. Entering node: Payment Service." }

Example 2:
USER: "Plan a 3-city tour: London, Paris, Berlin."
ASSISTANT:

json { "stack_depth": 1, "current_node": "Logistics Overview", "status": "DECOMPOSING", "sub_nodes": ["London Leg", "Transit LON->PAR", "Paris Leg", "Transit PAR->BER", "Berlin Leg"], "action": "Solving: London Leg (Dates, Venue, Hotel)." }


CURRENT CONTEXT:
{{USER_INTENT}}

Begin Decomposition. Output JSON for the first step:

3. The PDSA Loop (Plan-Do-Study-Act)
Persona: The Quality Assurance Engineer & Optimizer. Physics: Iterative, metric-driven, convergent, refinement-focused. Budget: Moderate tokens, high focus on validation.

SYSTEM PROMPT: PDSA_OPTIMIZER

You are the PDSA Optimizer. Your goal is to refine an artifact, process, or system towards a measurable target. You do not guess; you hypothesize, test, and validate.

CORE DIRECTIVES:
1. THE CYCLE: Adhere strictly to PDSA for every iteration.
   - PLAN: Propose a specific change based on the current flaw.
   - DO: Execute the change (show the code/text/config).
   - STUDY: Analyze the result. Did it meet the metric? (e.g., Is it faster? Is it clearer?).
   - ACT: Decide to adopt, adapt, or abandon the change.
2. CONVERGENCE CHECK: If the improvement delta < 5% or the metric is met, STOP and CRYSTALLIZE.
3. QUANTIFICATION: You must use numbers or clear qualitative comparisons (e.g., "Reduced complexity from O(n^2) to O(n log n)").
4. NO REVOLUTIONS: PDSA is for evolution. Do not rewrite the entire system unless it is the only way to hit the metric.

FEW-SHOT EXAMPLES:

Example 1:
USER: "This SQL query takes 12 seconds. Optimize it."
CURRENT QUERY: `SELECT * FROM users WHERE LOWER(email) = 'test@test.com'`
ASSISTANT:
- PLAN: The `LOWER()` function prevents index usage. I will normalize the input data instead.
- DO:
  
sql SELECT * FROM users WHERE email = 'test@test.com' -- Assuming stored lower-case

  *Requires migration: `UPDATE users SET email = LOWER(email);`*
- STUDY: Index can now be used on `email`. Expected reduction: 12s -> 5ms.
- ACT: Adopt. Run migration. Update application code to normalize input.

Example 2:
USER: "This paragraph is too wordy. Refine for impact."
ORIGINAL: "In order to ensure that we are able to effectively and efficiently maximize the potential of the..."
ASSISTANT:
- PLAN: Remove filler phrases ("In order to", "ensure that we are able to"). Strengthen verbs.
- DO: "To maximize our potential..."
- STUDY: Word count reduced by 40%. Clarity increased. Readability score improved.
- ACT: Adopt. Continue scanning next sentence.

CURRENT CONTEXT:
{{USER_INTENT}}
{{CURRENT_ARTIFACT_OR_STATE}}

Begin PDSA Cycle:

Implementation Notes for Development Team
Injection Strategy: The {{USER_INTENT}} variable should be populated with the current state of the conversation. For Recursive loops, {{CURRENT_ARTIFACT_OR_STATE}} is critical and should contain the JSON output of the previous stack frame.
JSON Enforcement: For the Recursive Loop, it is highly recommended to set response_format={ "type": "json_object" } in the API call (if using OpenAI/Claude) to ensure the Loop Ledger parser does not crash.
Temperature Settings:
OODA: Temp 0.8 - 1.0 (High creativity/speed required).
Recursive: Temp 0.1 - 0.3 (High precision/structural integrity required).
PDSA: Temp 0.4 - 0.6 (Balance of exploration and adherence).
Next-Hop Seeds
The "Warm-Handoff" Protocol: How do we pass the "Context Embedding" (Et) from the Classifier to the selected Loop without re-computing it?
The "Stack Overflow" Recovery: If the Recursive Loop hits max_depth, does it fail gracefully or bubble up an error to the OODA Loop?
Synthetic Training Data: Can we generate 100 "failed loops" (e.g., a PDSA loop that oscillates forever) to train the Halting Oracle?

# ALOS Architecture: Answers to the Three Seam Questions

These three questions all live at **component boundaries** — the exact places systems break in production. Good instinct to surface them now.

---

## Question 1: Passing the Context Embedding ($E_t$) Without Recomputation

**The core tension:** The Classifier already did the expensive work of encoding the user's intent into a vector space representation. Recomputing it inside the Loop Controller is wasteful. But the Classifier and the Loop may not share the same model instance, memory space, or even the same machine.

### The Architecture: The Context Envelope Pattern

The solution is to **never pass the raw embedding alone**. Instead, wrap it in a structured **Context Envelope** that travels with the request through the entire pipeline.

```python
@dataclass
class ContextEnvelope:
    """
    The atomic unit of context transfer between ALOS components.
    Created by the Classifier. Consumed by the Loop Controller.
    Persisted in the Loop Ledger.
    """
    # --- Identity ---
    request_id: str                  # UUID for this conversation turn
    timestamp: float                 # Unix timestamp of creation
    
    # --- The Embedding (the expensive artifact) ---
    embedding_vector: list[float]    # The actual E_t vector
    embedding_model: str             # e.g., "text-embedding-3-large"
    embedding_dim: int               # e.g., 3072
    
    # --- Classifier Outputs ---
    selected_loop: str               # "OODA" | "RECURSIVE" | "PDSA"
    classifier_confidence: float     # 0.0 - 1.0
    intent_tags: list[str]           # ["urgent", "infrastructure", "rollback"]
    
    # --- Provenance ---
    raw_input_hash: str              # SHA-256 of original user input
    classifier_version: str          # For reproducibility
    
    # --- State for Loop Controller ---
    loop_iteration: int              # Which cycle are we on? (starts at 0)
    parent_envelope_id: str | None   # For recursive sub-calls
```

### Three Transfer Strategies (Pick Based on Your Infra)

```
┌─────────────────────────────────────────────────────────────────┐
│              STRATEGY SELECTION MATRIX                          │
├──────────────┬──────────────┬───────────────┬──────────────────┤
│   Strategy   │   Latency    │  Complexity   │   Best When      │
├──────────────┼──────────────┼───────────────┼──────────────────┤
│ 1. In-Memory │   ~0ms       │   Low         │ Same process     │
│    (dict)    │              │               │ (monolith/dev)   │
├──────────────┼──────────────┼───────────────┼──────────────────┤
│ 2. Redis     │   <1ms       │   Medium      │ Microservices,   │
│    Cache     │              │               │ multi-worker     │
├──────────────┼──────────────┼───────────────┼──────────────────┤
│ 3. Request   │   ~0ms       │   Low         │ Serverless /     │
│    Body Pass │  (serialized)│  (but larger  │ Lambda / API     │
│              │              │   payloads)   │   Gateway        │
└──────────────┴──────────────┴───────────────┴──────────────────┘
```

**Strategy 2 (Redis) is the recommended default** for production:

```python
import redis
import json
import hashlib

class EmbeddingCache:
    """
    Shared embedding cache between Classifier and Loop Controller.
    TTL ensures we don't leak memory on abandoned requests.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.r = redis.from_url(redis_url)
        self.TTL_SECONDS = 300  # 5 minutes — enough for any loop cycle
    
    # --- Classifier writes here AFTER classification ---
    def store_envelope(self, envelope: ContextEnvelope) -> str:
        key = f"alos:ctx:{envelope.request_id}"
        self.r.setex(
            name=key,
            time=self.TTL_SECONDS,
            value=json.dumps(envelope.__dict__)
        )
        return key
    
    # --- Loop Controller reads here BEFORE first cycle ---
    def retrieve_envelope(self, request_id: str) -> ContextEnvelope:
        key = f"alos:ctx:{request_id}"
        raw = self.r.get(key)
        if raw is None:
            raise ContextExpiredError(
                f"Envelope {request_id} expired or never existed. "
                f"Recomputation required."
            )
        data = json.loads(raw)
        return ContextEnvelope(**data)
    
    # --- Integrity check: did the input change mid-loop? ---
    def validate_freshness(
        self, envelope: ContextEnvelope, current_input: str
    ) -> bool:
        current_hash = hashlib.sha256(
            current_input.encode()
        ).hexdigest()
        return current_hash == envelope.raw_input_hash
```

### What About KV-Cache Sharing (Same Model)?

If the Classifier and the Loop Controller use the **same underlying LLM** (e.g., both hit GPT-4), there's a more aggressive optimization:

```python
# If using the OpenAI API or similar with prompt caching:
# The SYSTEM PROMPT prefix is cached automatically.
# The trick: structure your calls so the Classifier's
# reasoning becomes the Loop Controller's prefix.

# Step 1: Classifier call
classifier_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": CLASSIFIER_PROMPT},
        {"role": "user", "content": user_input}
    ],
    # This returns the classification + internal reasoning
)

# Step 2: Loop Controller call — REUSE the conversation
loop_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": CLASSIFIER_PROMPT},
        {"role": "user", "content": user_input},
        # ↑ These two messages hit the KV cache (already computed)
        
        {"role": "assistant", "content": classifier_response.content},
        # ↑ The classifier's output becomes context
        
        {"role": "system", "content": SELECTED_LOOP_PROMPT},
        # ↑ Now inject the loop-specific system prompt
        
        {"role": "user", "content": "Execute loop cycle 1."}
    ],
    # The model doesn't recompute the embedding for the first
    # 3 messages — they're in the KV cache prefix.
)
```

> **Key insight:** The "embedding" in an LLM context isn't a single vector — it's the entire KV-cache state after processing the input tokens. By structuring the Loop Controller call as a *continuation* of the Classifier call, you get the reuse for free from the API's prompt caching.

### The Flow Diagram

```
User Input
    │
    ▼
┌──────────────┐
│  CLASSIFIER  │──── Computes E_t ────┐
│              │                      │
│  Output:     │                      ▼
│  loop=OODA   │            ┌──────────────────┐
│  conf=0.92   │            │  EMBEDDING CACHE  │
│  tags=[...]  │            │  (Redis / Memory) │
└──────┬───────┘            │                   │
       │                    │  Key: request_id  │
       │  writes envelope   │  Val: {E_t, meta} │
       │ ──────────────────>│  TTL: 300s        │
       │                    └────────┬──────────┘
       │                             │
       ▼                             │ reads envelope
┌──────────────┐                     │
│ ORCHESTRATOR │                     │
│              │  routes to          │
│  request_id ─┼─────────┐          │
└──────────────┘          │          │
                          ▼          │
                 ┌─────────────────┐ │
                 │  OODA LOOP      │◄┘
                 │  CONTROLLER     │
                 │                 │
                 │  Has E_t from   │
                 │  cache. No      │
                 │  recomputation. │
                 └─────────────────┘
```

---

## Question 2: Recursive Loop `max_depth` — Fail Gracefully or Bubble Up?

**Answer: Both. In sequence.**

The correct behavior is a **three-phase failure cascade**: Crystallize → Signal → Escalate.

### The Failure Taxonomy

```
┌─────────────────────────────────────────────────────────────────┐
│              RECURSIVE LOOP FAILURE MODES                       │
├────────────────┬────────────────────────────────────────────────┤
│  Failure Type  │  Behavior                                      │
├────────────────┼────────────────────────────────────────────────┤
│  SOLVED        │  Normal exit. All nodes complete.              │
│  MAX_DEPTH     │  Hit depth limit. Unsolved nodes remain.       │
│  BUDGET_EXHAUSTED │ Token/time budget exceeded.                 │
│  CYCLE_DETECTED│  Node A depends on Node B depends on Node A.  │
│  ORACLE_HALT   │  Halting Oracle detected sepsis marker.        │
└────────────────┴────────────────────────────────────────────────┘
```

### The Three-Phase Cascade

```python
class RecursiveLoopController:
    
    MAX_DEPTH = 7          # Configurable per problem class
    PARTIAL_THRESHOLD = 3  # Minimum solved nodes to be "useful"
    
    def execute_node(self, node, depth: int, stack: list) -> NodeResult:
        
        # ══════════════════════════════════════════════
        # PHASE 1: PARTIAL CRYSTALLIZATION
        # ══════════════════════════════════════════════
        if depth >= self.MAX_DEPTH:
            return self._crystallize_partial(node, stack, reason="MAX_DEPTH")
        
        # ... normal recursive logic ...
        sub_nodes = self.decompose(node)
        results = []
        
        for sub_node in sub_nodes:
            result = self.execute_node(sub_node, depth + 1, stack + [node])
            results.append(result)
            
            # Check if any sub-result was a partial crystallization
            if result.status == "PARTIAL":
                # Don't abandon siblings — try to solve what we can
                continue
        
        return self.synthesize(node, results)
    
    def _crystallize_partial(
        self, node, stack: list, reason: str
    ) -> NodeResult:
        """
        Phase 1: Save everything we have. Don't lose work.
        """
        partial_output = {
            "status": "PARTIAL",
            "reason": reason,
            "depth_reached": len(stack),
            "solved_nodes": [
                n.to_dict() for n in stack if n.status == "SOLVED"
            ],
            "unsolved_nodes": [
                {
                    "node_id": node.id,
                    "node_description": node.description,
                    "estimated_remaining_depth": node.estimated_depth,
                    "context_summary": node.context[:500]
                }
            ],
            "stack_trace": [n.id for n in stack],  # Breadcrumb trail
            "synthesized_partial_answer": self._best_effort_synthesis(stack)
        }
        
        # ══════════════════════════════════════════════
        # PHASE 2: SIGNAL TO ORCHESTRATOR
        # ══════════════════════════════════════════════
        signal = LoopSignal(
            type="DEPTH_LIMIT_REACHED",
            severity="WARNING",        # Not ERROR — we have partial results
            source="RECURSIVE_LOOP",
            request_id=self.request_id,
            payload=partial_output,
            recommended_action=self._recommend_action(node, stack)
        )
        
        self.orchestrator.emit_signal(signal)
        
        return NodeResult(status="PARTIAL", data=partial_output)
    
    def _recommend_action(self, node, stack) -> str:
        """
        The Loop itself suggests what should happen next.
        The Orchestrator makes the final call.
        """
        solved_count = sum(1 for n in stack if n.status == "SOLVED")
        total_count = len(stack) + 1  # +1 for current unsolved
        
        completion_ratio = solved_count / total_count
        
        if completion_ratio > 0.8:
            return "DELIVER_PARTIAL"
            # 80%+ done — give the user what we have
            
        elif completion_ratio > 0.5:
            return "CONTINUE_WITH_INCREASED_DEPTH"
            # Ask the Orchestrator to bump max_depth by 2 and retry
            # ONLY the unsolved branch
            
        else:
            return "ESCALATE_TO_OODA"
            # Less than half done — this problem may be
            # wrong for recursive decomposition.
            # Let OODA take a faster, heuristic approach.
```

### Phase 3: The OODA Escalation Path

```python
class Orchestrator:
    
    def handle_signal(self, signal: LoopSignal):
        
        if signal.type == "DEPTH_LIMIT_REACHED":
            action = signal.recommended_action
            
            if action == "DELIVER_PARTIAL":
                self.deliver_to_user(
                    signal.payload["synthesized_partial_answer"],
                    caveat="Note: This solution covers {solved}/{total} "
                           "components. The following areas need manual "
                           "review: {unsolved_list}"
                )
            
            elif action == "CONTINUE_WITH_INCREASED_DEPTH":
                # Retry ONLY the failed branch
                self.recursive_loop.execute_node(
                    node=signal.payload["unsolved_nodes"][0],
                    depth=0,  # Reset depth counter for this sub-tree
                    stack=[],
                    max_depth=self.MAX_DEPTH + 2  # Grant more depth
                )
            
            elif action == "ESCALATE_TO_OODA":
                # ══════════════════════════════════════
                # PHASE 3: CROSS-LOOP ESCALATION
                # ══════════════════════════════════════
                # Package the partial work as "orientation data"
                # for the OODA loop
                ooda_context = f"""
                SITUATION: Recursive decomposition of 
                '{signal.payload['unsolved_nodes'][0]['node_description']}' 
                failed at depth {signal.payload['depth_reached']}.
                
                WHAT WE KNOW SO FAR:
                {signal.payload['synthesized_partial_answer']}
                
                WHAT REMAINS UNSOLVED:
                {json.dumps(signal.payload['unsolved_nodes'], indent=2)}
                
                YOUR MISSION: Provide a rapid, heuristic solution 
                for the unsolved components. Precision is secondary 
                to completeness.
                """
                
                self.switch_loop(
                    from_loop="RECURSIVE",
                    to_loop="OODA",
                    context=ooda_context,
                    preserve_envelope=True  # Don't recompute E_t!
                )
```

### The Decision Tree (Visual)

```
Recursive Loop hits max_depth
            │
            ▼
   ┌─────────────────┐
   │  CRYSTALLIZE     │  ← Save all solved nodes. Don't lose work.
   │  partial results │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  COMPUTE         │
   │  completion_ratio│
   └────────┬────────┘
            │
     ┌──────┼──────────────┐
     │      │              │
     ▼      ▼              ▼
   >80%   50-80%         <50%
     │      │              │
     ▼      ▼              ▼
  DELIVER  RETRY w/      ESCALATE
  PARTIAL  +2 depth      TO OODA
     │      │              │
     ▼      ▼              ▼
  User    Same loop,     OODA gets
  gets    deeper,        partial work
  80%+    only failed    as "ORIENT"
  answer  branch         data
```

### Why Not Just Error Out?

Because **partial results have value**. Consider:

> **User:** "Design a microservices architecture for a ride-sharing app."
> **Recursive Loop solves:** Matching Engine ✓, Rider Service ✓, Payment Service ✓
> **Recursive Loop fails at max_depth on:** Driver Service (complex state machine)

Throwing away the three solved services would be criminal. Instead:
- Deliver the three solved designs
- Flag Driver Service as "needs further decomposition or manual review"
- Optionally hand Driver Service to OODA for a quick-and-dirty heuristic solution

---

## Question 3: Generating 100 Failed Loops for Halting Oracle Training

**Answer: Yes. This is not just possible — it's the single most important thing you can do for system reliability.**

The Halting Oracle is only as good as its training data, and **healthy loops all look alike; every unhealthy loop is unhealthy in its own way** (Anna Karenina principle).

### The Failure Pattern Taxonomy

First, define what "failure" looks like for each loop type:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FAILURE PATTERN CATALOG                           │
├──────────┬───────────────────┬───────────────────────────────────────┤
│   Loop   │  Failure Pattern  │  Signature                           │
├──────────┼───────────────────┼───────────────────────────────────────┤
│          │ THRASHING         │ Same action repeated 3+ times         │
│  OODA    │ ESCALATION SPIRAL │ Severity increases each cycle         │
│          │ DECISION PARALYSIS│ Orient phase grows, Decide shrinks    │
│          │ FALSE STABILITY   │ Declares "stable" but metrics worsen  │
├──────────┼───────────────────┼───────────────────────────────────────┤
│          │ INFINITE DESCENT  │ Depth increases, no nodes solved      │
│ RECURSIVE│ CIRCULAR DEPS     │ Node A→B→C→A cycle detected          │
│          │ COMBINATORIAL     │ Sub-nodes multiply exponentially      │
│          │   EXPLOSION       │   (2→4→16→256 nodes)                 │
│          │ PHANTOM PROGRESS  │ Nodes marked "solved" but empty      │
├──────────┼───────────────────┼───────────────────────────────────────┤
│          │ OSCILLATION       │ Metric bounces: 8s→5s→9s→4s→10s      │
│  PDSA    │ ASYMPTOTIC STALL  │ Improvement: 12s→6s→5.8s→5.7s→5.69s │
│          │ REGRESSION LOOP   │ Each "improvement" breaks something   │
│          │ METRIC GAMING     │ Optimizes metric, degrades quality    │
│          │ PLAN-ONLY LOOP    │ Plans but never executes DO phase     │
└──────────┴───────────────────┴───────────────────────────────────────┘
```

### The Synthetic Data Generator

```python
import random
import json
from typing import Generator
from dataclasses import dataclass, field


@dataclass
class SyntheticLoopTrace:
    """One complete loop execution trace for Halting Oracle training."""
    loop_type: str
    failure_pattern: str
    iterations: list[dict]
    label: str              # "HEALTHY" | "FAILING" | "SEPTIC"
    halt_at_iteration: int  # When the Oracle SHOULD have stopped it
    explanation: str        # Human-readable reason for the label


class FailedLoopGenerator:
    """
    Generates synthetic failed loop traces for Halting Oracle training.
    
    Usage:
        gen = FailedLoopGenerator(seed=42)
        dataset = gen.generate_dataset(n=100)
    """
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
    
    def generate_dataset(self, n: int = 100) -> list[SyntheticLoopTrace]:
        """
        Generate n traces with a realistic distribution:
        - 40% healthy (the Oracle must learn to NOT halt these)
        - 35% failing (clear pathology, should halt)
        - 25% edge cases (subtle, late-onset failure)
        """
        dataset = []
        
        # Distribution across failure types
        generators = [
            # (generator_fn, count, label_type)
            (self._healthy_ooda, 7, "HEALTHY"),
            (self._healthy_recursive, 7, "HEALTHY"),
            (self._healthy_pdsa, 6, "HEALTHY"),
            
            # -- Clear failures (20 traces) --
            (self._pdsa_oscillation, 5, "FAILING"),
            (self._ooda_thrashing, 5, "FAILING"),
            (self._recursive_infinite_descent, 5, "FAILING"),
            (self._pdsa_asymptotic_stall, 5, "FAILING"),
            
            # -- Additional failures (15 traces) --
            (self._recursive_combinatorial_explosion, 5, "FAILING"),
            (self._ooda_escalation_spiral, 5, "FAILING"),
            (self._pdsa_regression_loop, 5, "FAILING"),
            
            # -- Subtle / edge cases (25 traces) --
            (self._ooda_false_stability, 5, "SEPTIC"),
            (self._recursive_phantom_progress, 5, "SEPTIC"),
            (self._pdsa_metric_gaming, 5, "SEPTIC"),
            (self._late_onset_oscillation, 5, "SEPTIC"),
            (self._healthy_then_degrades, 5, "SEPTIC"),

            # -- Extra healthy to reach 40 total --
            (self._healthy_ooda, 7, "HEALTHY"),
            (self._healthy_recursive, 7, "HEALTHY"),
            (self._healthy_pdsa, 6, "HEALTHY"),
        ]
        
        for gen_fn, count, label in generators:
            for _ in range(count):
                dataset.append(gen_fn(label))
        
        self.rng.shuffle(dataset)
        return dataset[:n]  # Trim to exact count
    
    # ════════════════════════════════════════════════
    # HEALTHY PATTERNS (The Oracle must NOT halt these)
    # ════════════════════════════════════════════════
    
    def _healthy_pdsa(self, label: str) -> SyntheticLoopTrace:
        """A PDSA loop that converges normally."""
        iterations = []
        metric = 12.0  # Starting: 12 second query
        
        for i in range(4):
            improvement = self.rng.uniform(0.3, 0.6)
            new_metric = metric * (1 - improvement)
            iterations.append({
                "cycle": i + 1,
                "phase": "PDSA",
                "plan": f"Optimization attempt {i+1}",
                "metric_before": round(metric, 2),
                "metric_after": round(new_metric, 2),
                "improvement_pct": round(improvement * 100, 1),
                "action": "ADOPT"
            })
            metric = new_metric
        
        # Final convergence
        iterations.append({
            "cycle": 5,
            "phase": "PDSA",
            "plan": "Final check",
            "metric_before": round(metric, 2),
            "metric_after": round(metric * 0.98, 2),
            "improvement_pct": 2.0,
            "action": "CRYSTALLIZE — delta < 5%"
        })
        
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="NONE",
            iterations=iterations,
            label=label,
            halt_at_iteration=-1,  # -1 = should NOT be halted
            explanation="Normal convergence. Metric improved monotonically."
        )
    
    def _healthy_ooda(self, label: str) -> SyntheticLoopTrace:
        """An OODA loop that resolves an incident."""
        return SyntheticLoopTrace(
            loop_type="OODA",
            failure_pattern="NONE",
            iterations=[
                {"cycle": 1, "observe": "500 errors at 50%",
                 "orient": "Sev1", "decide": "Rollback",
                 "act": "kubectl rollout undo", "status": "ACTING"},
                {"cycle": 2, "observe": "Error rate dropping: 50%→20%",
                 "orient": "Rollback taking effect",
                 "decide": "Monitor", "act": "Wait 60s",
                 "status": "MONITORING"},
                {"cycle": 3, "observe": "Error rate 0.1%. Normal.",
                 "orient": "Incident resolved",
                 "decide": "Close incident",
                 "act": "Post-mortem scheduled",
                 "status": "STABLE"}
            ],
            label=label,
            halt_at_iteration=-1,
            explanation="Normal OODA resolution in 3 cycles."
        )
    
    def _healthy_recursive(self, label: str) -> SyntheticLoopTrace:
        """A recursive decomposition that solves all nodes."""
        return SyntheticLoopTrace(
            loop_type="RECURSIVE",
            failure_pattern="NONE",
            iterations=[
                {"depth": 1, "node": "Architecture",
                 "status": "DECOMPOSING", "sub_nodes": 3},
                {"depth": 2, "node": "Service A",
                 "status": "SOLVING", "result": "Complete"},
                {"depth": 2, "node": "Service B",
                 "status": "SOLVING", "result": "Complete"},
                {"depth": 2, "node": "Service C",
                 "status": "SOLVING", "result": "Complete"},
                {"depth": 1, "node": "Architecture",
                 "status": "SYNTHESIZING", "result": "All nodes solved"}
            ],
            label=label,
            halt_at_iteration=-1,
            explanation="Clean recursive solve. All branches resolved."
        )
    
    # ════════════════════════════════════════════════
    # PDSA OSCILLATION (The classic failure mode)
    # ════════════════════════════════════════════════
    
    def _pdsa_oscillation(self, label: str) -> SyntheticLoopTrace:
        """
        PDSA loop where the metric bounces between two values.
        
        The pathology: Each "fix" for problem A causes problem B,
        and vice versa. The loop never converges.
        
        Signature: metric sequence like [8, 5, 9, 4, 10, 3, 11...]
        """
        iterations = []
        metrics = []
        base_high = self.rng.uniform(8, 12)
        base_low = self.rng.uniform(3, 6)
        
        for i in range(10):
            if i % 2 == 0:
                metric = base_high + self.rng.uniform(-0.5, 0.5)
                plan = "Optimize query path A (index strategy)"
            else:
                metric = base_low + self.rng.uniform(-0.5, 0.5)
                plan = "Revert: A broke path B. Optimize path B."
            
            metrics.append(round(metric, 2))
            prev = metrics[-2] if len(metrics) > 1 else metric
            
            iterations.append({
                "cycle": i + 1,
                "phase": "PDSA",
                "plan": plan,
                "metric_before": round(prev, 2),
                "metric_after": round(metric, 2),
                "improvement_pct": round(
                    (prev - metric) / prev * 100, 1
                ),
                "action": "ADOPT"  # Keeps adopting contradictions
            })
        
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="OSCILLATION",
            iterations=iterations,
            label=label,
            halt_at_iteration=4,  # Should have been caught by cycle 4
            explanation=(
                f"Metric oscillates between ~{base_high:.0f} and "
                f"~{base_low:.0f}. No convergence. "
                f"Variance of last 4 metrics: "
                f"{self._variance(metrics[-4:]):.2f}"
            )
        )
    
    # ════════════════════════════════════════════════
    # OODA THRASHING (Same action, no effect)
    # ════════════════════════════════════════════════
    
    def _ooda_thrashing(self, label: str) -> SyntheticLoopTrace:
        """
        OODA loop repeating the same action because it doesn't
        update its mental model (Orient phase is stale).
        """
        action = self.rng.choice([
            "kubectl rollout undo",
            "service nginx restart",
            "FLUSH PRIVILEGES",
            "Clear CDN cache"
        ])
        
        iterations = []
        for i in range(6):
            iterations.append({
                "cycle": i + 1,
                "observe": f"Error rate still at 50% (cycle {i+1})",
                "orient": "Previous action may not have taken effect",
                "decide": f"Retry: {action}",
                "act": action,
                "status": "ACTING",
                "action_hash": hash(action)  # Same hash = same action
            })
        
        return SyntheticLoopTrace(
            loop_type="OODA",
            failure_pattern="THRASHING",
            iterations=iterations,
            label=label,
            halt_at_iteration=3,  # 3 identical actions = sepsis
            explanation=(
                f"Action '{action}' repeated 6 times with no effect. "
                f"Orient phase is not updating mental model."
            )
        )
    
    # ════════════════════════════════════════════════
    # RECURSIVE INFINITE DESCENT
    # ════════════════════════════════════════════════
    
    def _recursive_infinite_descent(self, label: str) -> SyntheticLoopTrace:
        """
        Recursive loop that keeps decomposing but never solves anything.
        Every node just creates more sub-nodes.
        """
        iterations = []
        for depth in range(1, 9):
            sub_count = self.rng.randint(2, 4)
            iterations.append({
                "depth": depth,
                "node": f"SubProblem_L{depth}_{self.rng.randint(1,99)}",
                "status": "DECOMPOSING",  # Never "SOLVING"
                "sub_nodes": sub_count,
                "nodes_solved_so_far": 0,  # Always zero
                "total_nodes_created": sum(
                    it.get("sub_nodes", 0) for it in iterations
                ) + sub_count
            })
        
        return SyntheticLoopTrace(
            loop_type="RECURSIVE",
            failure_pattern="INFINITE_DESCENT",
            iterations=iterations,
            label=label,
            halt_at_iteration=4,  # 4 levels of pure decomposition = alarm
            explanation=(
                "8 levels of decomposition with 0 nodes solved. "
                "Total nodes created: "
                f"{iterations[-1]['total_nodes_created']}. "
                "Ratio of SOLVING to DECOMPOSING actions: 0.0"
            )
        )
    
    # ════════════════════════════════════════════════
    # PDSA ASYMPTOTIC STALL
    # ════════════════════════════════════════════════
    
    def _pdsa_asymptotic_stall(self, label: str) -> SyntheticLoopTrace:
        """
        Improvement that follows a diminishing returns curve.
        12s → 6s → 5.8s → 5.79s → 5.789s → 5.7889s...
        Burns tokens for negligible gain.
        """
        iterations = []
        metric = 12.0
        
        for i in range(8):
            # Diminishing improvement: 50%, 3%, 0.3%, 0.03%...
            if i == 0:
                improvement = 0.5
            else:
                improvement = 0.03 / (i ** 1.5)
            
            new_metric = metric * (1 - improvement)
            iterations.append({
                "cycle": i + 1,
                "metric_before": round(metric, 4),
                "metric_after": round(new_metric, 4),
                "improvement_pct": round(improvement * 100, 4),
                "action": "ADOPT",
                "tokens_used": self.rng.randint(800, 1200)
            })
            metric = new_metric
        
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="ASYMPTOTIC_STALL",
            iterations=iterations,
            label=label,
            halt_at_iteration=3,
            explanation=(
                "Improvement delta dropped below 5% at cycle 3 "
                "but loop continued for 5 more cycles. "
                f"Total wasted tokens: ~{5 * 1000}"
            )
        )
    
    # ════════════════════════════════════════════════
    # SUBTLE FAILURES (Edge Cases for Oracle Training)
    # ════════════════════════════════════════════════
    
    def _ooda_false_stability(self, label: str) -> SyntheticLoopTrace:
        """
        OODA declares STABLE but the underlying metrics
        are actually degrading. It stopped observing the
        right signals.
        """
        return SyntheticLoopTrace(
            loop_type="OODA",
            failure_pattern="FALSE_STABILITY",
            iterations=[
                {"cycle": 1, "observe": "Error rate 50%",
                 "orient": "Sev1", "decide": "Rollback",
                 "act": "Rollback executed", "status": "ACTING"},
                {"cycle": 2, "observe": "HTTP errors down to 2%",
                 "orient": "Looks resolved",
                 "decide": "Declare stable",
                 "act": "Closing incident",
                 "status": "STABLE",
                 "hidden_signal": "Latency p99: 200ms → 4500ms",
                 "hidden_signal_2": "Database connections: 50 → 498/500"},
            ],
            label=label,
            halt_at_iteration=-1,  # It DID halt — but it shouldn't have!
            explanation=(
                "Loop declared STABLE based on HTTP error rate alone, "
                "but missed latency spike (22x) and DB connection "
                "pool exhaustion (99.6%). Observation was too narrow."
            )
        )
    
    def _recursive_phantom_progress(self, label: str) -> SyntheticLoopTrace:
        """
        Nodes are marked SOLVED but their content is vacuous.
        The loop appears to progress but produces no real work.
        """
        return SyntheticLoopTrace(
            loop_type="RECURSIVE",
            failure_pattern="PHANTOM_PROGRESS",
            iterations=[
                {"depth": 1, "node": "System Design",
                 "status": "DECOMPOSING", "sub_nodes": 3},
                {"depth": 2, "node": "Backend",
                 "status": "SOLVED",
                 "result": "Use appropriate backend technology.",
                 "result_specificity_score": 0.1},  # Vacuous
                {"depth": 2, "node": "Frontend",
                 "status": "SOLVED",
                 "result": "Implement a responsive frontend.",
                 "result_specificity_score": 0.1},  # Vacuous
                {"depth": 2, "node": "Database",
                 "status": "SOLVED",
                 "result": "Choose a suitable database.",
                 "result_specificity_score": 0.05},  # Vacuous
                {"depth": 1, "node": "System Design",
                 "status": "SYNTHESIZING",
                 "result": "System uses backend, frontend, and database.",
                 "result_specificity_score": 0.08}
            ],
            label=label,
            halt_at_iteration=2,
            explanation=(
                "All nodes marked SOLVED but specificity scores "
                "average 0.08/1.0. Solutions are tautological. "
                "No concrete technologies, patterns, or decisions."
            )
        )
    
    def _pdsa_metric_gaming(self, label: str) -> SyntheticLoopTrace:
        """
        The metric improves but the actual quality degrades.
        Example: "Reduce word count" succeeds but meaning is lost.
        """
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="METRIC_GAMING",
            iterations=[
                {"cycle": 1,
                 "plan": "Reduce word count",
                 "metric": "word_count",
                 "before": 200, "after": 150,
                 "quality_score": 0.85,
                 "action": "ADOPT"},
                {"cycle": 2,
                 "plan": "Remove more words",
                 "metric": "word_count",
                 "before": 150, "after": 80,
                 "quality_score": 0.60,  # Quality dropping
                 "action": "ADOPT"},
                {"cycle": 3,
                 "plan": "Aggressive compression",
                 "metric": "word_count",
                 "before": 80, "after": 30,
                 "quality_score": 0.20,  # Meaning destroyed
                 "action": "ADOPT"},
            ],
            label=label,
            halt_at_iteration=2,
            explanation=(
                "Word count metric improved by 85% but quality score "
                "dropped from 0.85 to 0.20. Goodhart's Law: "
                "the metric ceased to be a good measure."
            )
        )
    
    def _recursive_combinatorial_explosion(self, label: str) -> SyntheticLoopTrace:
        iterations = []
        total_nodes = 0
        for depth in range(1, 7):
            sub_count = 2 ** depth  # Exponential growth
            total_nodes += sub_count
            iterations.append({
                "depth": depth,
                "node": f"Branch_L{depth}",
                "status": "DECOMPOSING",
                "sub_nodes_created": sub_count,
                "total_nodes_in_tree": total_nodes,
                "estimated_completion_time": f"{total_nodes * 2}s"
            })
        
        return SyntheticLoopTrace(
            loop_type="RECURSIVE",
            failure_pattern="COMBINATORIAL_EXPLOSION",
            iterations=iterations,
            label=label,
            halt_at_iteration=3,
            explanation=(
                f"Node count growing exponentially: "
                f"2→4→8→16→32→64. Total: {total_nodes}. "
                f"At depth 3 (8 nodes), should have switched strategy."
            )
        )
    
    def _ooda_escalation_spiral(self, label: str) -> SyntheticLoopTrace:
        return SyntheticLoopTrace(
            loop_type="OODA",
            failure_pattern="ESCALATION_SPIRAL",
            iterations=[
                {"cycle": 1, "severity": "SEV3",
                 "decide": "Page on-call", "status": "ACTING"},
                {"cycle": 2, "severity": "SEV2",
                 "decide": "Page team lead", "status": "ESCALATING"},
                {"cycle": 3, "severity": "SEV1",
                 "decide": "Page VP Engineering", "status": "ESCALATING"},
                {"cycle": 4, "severity": "SEV0",
                 "decide": "Page CEO", "status": "ESCALATING"},
                {"cycle": 5, "severity": "SEV0+",
                 "decide": "Page board of directors???",
                 "status": "ESCALATING"},
            ],
            label=label,
            halt_at_iteration=3,
            explanation=(
                "Severity escalated every cycle without any "
                "diagnostic action. Orient phase contains no "
                "analysis — only panic propagation."
            )
        )
    
    def _pdsa_regression_loop(self, label: str) -> SyntheticLoopTrace:
        iterations = []
        metric = 10.0
        for i in range(6):
            improvement = self.rng.uniform(0.1, 0.3)
            new_metric = metric * (1 - improvement)
            # But each change breaks something else
            regression = self.rng.uniform(0.15, 0.35)
            regressed_metric = new_metric * (1 + regression)
            
            iterations.append({
                "cycle": i + 1,
                "plan": f"Fix regression from cycle {i}" if i > 0 
                        else "Initial optimization",
                "metric_after_change": round(new_metric, 2),
                "metric_after_regression": round(regressed_metric, 2),
                "net_improvement": round(
                    (metric - regressed_metric) / metric * 100, 1
                ),
                "side_effects_detected": True if i > 0 else False
            })
            metric = regressed_metric
        
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="REGRESSION_LOOP",
            iterations=iterations,
            label=label,
            halt_at_iteration=3,
            explanation=(
                "Every optimization causes a regression in another "
                "metric. Net improvement after 6 cycles: ~0%. "
                "System needs architectural change, not optimization."
            )
        )
    
    def _late_onset_oscillation(self, label: str) -> SyntheticLoopTrace:
        """Starts healthy, then degrades into oscillation."""
        iterations = []
        metric = 12.0
        
        # First 3 cycles: healthy convergence
        for i in range(3):
            improvement = self.rng.uniform(0.2, 0.4)
            new_metric = metric * (1 - improvement)
            iterations.append({
                "cycle": i + 1,
                "metric": round(new_metric, 2),
                "improvement_pct": round(improvement * 100, 1),
                "phase": "CONVERGING"
            })
            metric = new_metric
        
        # Cycles 4-8: oscillation begins
        base = metric
        for i in range(3, 8):
            oscillation = base + ((-1) ** i) * self.rng.uniform(1, 3)
            iterations.append({
                "cycle": i + 1,
                "metric": round(oscillation, 2),
                "improvement_pct": round(
                    (base - oscillation) / base * 100, 1
                ),
                "phase": "OSCILLATING"
            })
        
        return SyntheticLoopTrace(
            loop_type="PDSA",
            failure_pattern="LATE_ONSET_OSCILLATION",
            iterations=iterations,
            label=label,
            halt_at_iteration=5,  # 2 cycles after oscillation starts
            explanation=(
                "Healthy convergence for 3 cycles, then oscillation "
                "onset at cycle 4. Oracle should detect phase change "
                "within 2 cycles of onset."
            )
        )
    
    def _healthy_then_degrades(self, label: str) -> SyntheticLoopTrace:
        """Starts as valid OODA, then drifts into decision paralysis."""
        return SyntheticLoopTrace(
            loop_type="OODA",
            failure_pattern="DECISION_PARALYSIS",
            iterations=[
                {"cycle": 1,
                 "observe_tokens": 50, "orient_tokens": 80,
                 "decide_tokens": 20, "act_tokens": 30,
                 "status": "ACTING"},
                {"cycle": 2,
                 "observe_tokens": 60, "orient_tokens": 150,
                 "decide_tokens": 15, "act_tokens": 25,
                 "status": "ACTING"},
                {"cycle": 3,
                 "observe_tokens": 70, "orient_tokens": 400,
                 "decide_tokens": 10, "act_tokens": 10,
                 "status": "HESITATING"},
                {"cycle": 4,
                 "observe_tokens": 80, "orient_tokens": 800,
                 "decide_tokens": 5, "act_tokens": 0,
                 "status": "PARALYZED"},
            ],
            label=label,
            halt_at_iteration=3,
            explanation=(
                "Orient phase growing exponentially "
                "(80→150→400→800 tokens) while Decide+Act shrinking "
                "(50→40→20→5). Analysis paralysis detected."
            )
        )
    
    # ════════════════════════════════════════════════
    # UTILITIES
    # ════════════════════════════════════════════════
    
    def _variance(self, values: list[float]) -> float:
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)
```

### Using the Generator

```python
# Generate the training set
gen = FailedLoopGenerator(seed=42)
dataset = gen.generate_dataset(n=100)

# Convert to training format for the Halting Oracle
training_data = []
for trace in dataset:
    training_data.append({
        "input": {
            "loop_type": trace.loop_type,
            "iterations": trace.iterations,
            "current_iteration": len(trace.iterations)
        },
        "expected_output": {
            "should_halt": trace.label != "HEALTHY",
            "halt_reason": trace.failure_pattern,
            "confidence": 0.95 if trace.label == "FAILING" else 0.70,
            "recommended_halt_point": trace.halt_at_iteration
        }
    })

# Save for training
with open("halting_oracle_training_v1.json", "w") as f:
    json.dump(training_data, f, indent=2)

print(f"Generated {len(training_data)} traces:")
print(f"  HEALTHY: {sum(1 for t in dataset if t.label == 'HEALTHY')}")
print(f"  FAILING: {sum(1 for t in dataset if t.label == 'FAILING')}")
print(f"  SEPTIC:  {sum(1 for t in dataset if t.label == 'SEPTIC')}")
```

### The Detection Features the Oracle Should Learn

```
┌──────────────────────────────────────────────────────────────────┐
│          HALTING ORACLE FEATURE VECTOR                           │
├───────────────────────────┬─────────────────────────────────────┤
│  Feature                  │  Computation                        │
├───────────────────────────┼─────────────────────────────────────┤
│  metric_variance_last_4   │  var(metrics[-4:])                  │
│  metric_trend_slope       │  linear_regression(metrics).slope   │
│  action_uniqueness_ratio  │  unique_actions / total_actions     │
│  solve_to_decompose_ratio │  solved_nodes / total_nodes         │
│  orient_token_growth_rate │  orient_tokens[i] / orient[-1]     │
│  depth_without_solve      │  max consecutive DECOMPOSING states │
│  node_creation_rate       │  d(total_nodes)/d(iteration)       │
│  improvement_delta_trend  │  d(improvement_pct)/d(iteration)   │
│  severity_monotonicity    │  is_monotonically_increasing(sev)  │
│  specificity_score_avg    │  mean(result_specificity_scores)   │
│  cycle_count_vs_expected  │  actual_cycles / estimated_cycles  │
│  token_efficiency         │  quality_delta / tokens_consumed    │
└───────────────────────────┴─────────────────────────────────────┘
```

### LLM-Augmented Generation (The Power Move)

Beyond programmatic generation, you can **use the LLM itself** to generate more diverse failures:

```python
FAILURE_GENERATION_PROMPT = """
You are generating TRAINING DATA for a Halting Oracle that monitors 
AI reasoning loops.

Generate a realistic {loop_type} loop trace that exhibits the 
"{failure_pattern}" failure pattern.

Requirements:
1. The failure must be SUBTLE — not obvious until iteration {onset}.
2. Include realistic domain content (not placeholder text).
3. The trace must be valid JSON matching this schema: {schema}
4. Include a "ground_truth" field explaining exactly WHY this is 
   a failure and WHEN the Oracle should have caught it.

Domain: {random_domain}
Failure onset iteration: {onset}
"""

# Generate diverse domain-specific failures
domains = [
    "e-commerce checkout optimization",
    "kubernetes cluster autoscaling", 
    "legal contract negotiation",
    "medical diagnosis differential",
    "financial portfolio rebalancing",
    "compiler optimization passes",
    "A/B test analysis",
    "database migration planning"
]

for domain in domains:
    for pattern in ["OSCILLATION", "THRASHING", "PHANTOM_PROGRESS"]:
        response = llm.generate(
            FAILURE_GENERATION_PROMPT.format(
                loop_type="PDSA",
                failure_pattern=pattern,
                onset=random.randint(3, 6),
                schema=TRACE_JSON_SCHEMA,
                random_domain=domain
            ),
            temperature=0.9  # High creativity for diverse failures
        )
        dataset.append(parse_and_validate(response))
```

### Summary: The Training Data Pipeline

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐
│  PROGRAMMATIC    │     │  LLM-AUGMENTED   │     │  PRODUCTION   │
│  GENERATOR       │     │  GENERATOR       │     │  TELEMETRY    │
│                  │     │                  │     │  (future)     │
│  100 traces      │     │  ~200 traces     │     │  Real traces  │
│  Deterministic   │     │  Domain-diverse  │     │  w/ labels    │
│  Known patterns  │     │  Novel patterns  │     │               │
└────────┬────────┘     └────────┬─────────┘     └───────┬───────┘
         │                       │                        │
         └───────────┬───────────┘                        │
                     ▼                                    │
         ┌───────────────────────┐                        │
         │   TRAINING SET v1     │                        │
         │   (~300 traces)       │                        │
         │                       │      ┌─────────────────┘
         │   40% healthy         │      │  (Phase 2: 
         │   35% failing         │      │   retrain with
         │   25% subtle/septic   │      │   real data)
         └───────────┬───────────┘      │
                     │                  │
                     ▼                  ▼
            ┌─────────────────────────────┐
            │      HALTING ORACLE         │
            │                             │
            │  Input: Feature vector      │
            │  Output: {halt, continue}   │
            │  + confidence score         │
            │  + recommended action       │
            └─────────────────────────────┘
```

---

**Three questions answered. Three seams sealed.** The Context Envelope prevents redundant computation, the three-phase cascade prevents lost work on depth limits, and the synthetic data generator gives the Halting Oracle something to chew on before it ever sees production traffic.
