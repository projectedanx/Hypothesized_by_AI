# Decentralized Orchestration Engine — Architecture Specification

> **Constraint compliance note:** The three source mechanics are mapped to
> concrete distributed-systems primitives. The schema below uses no biological
> vocabulary — "spawning" → *demand-driven instantiation*, "stigmergic" →
> *shared-substrate indirect coordination*, "apoptosis" → *threshold-triggered
> deallocation*.

---

## 0. System Overview

A control-plane-free execution fabric. There is **no scheduler, no static
routing table, and no service registry**. Work organizes itself through a single
shared data structure — the **Latent Coordination Substrate (LCS)** — and a
population of short-lived, single-purpose **Task Workers (TW)** that read from
and write to it.

```
                 ┌──────────────────────────────────────────────┐
                 │        Latent Coordination Substrate (LCS)      │
                 │   append-only vector store + decay accumulator  │
                 │   key:  marker_id  →  {vec, weight, ts, refs}   │
                 └───────▲───────────────────────────▲────────────┘
        read/observe     │                           │   deposit/decay
                 ┌───────┴────────┐          ┌────────┴────────┐
   ingest ──►    │  Density Probe  │  spawn   │   Task Workers   │
   stream        │  (instantiator) │ ───────► │  (ephemeral,     │
                 └────────────────┘          │   isolated, 1:1)  │
                                             └──────────────────┘
                                                       │
                                                       ▼
                                              emit results → LCS
                                              (new markers) → DAG grows
```

The execution history forms a **Directed Acyclic Graph (DAG)** that is *derived,
never declared*: every marker a worker reads becomes an in-edge; every marker it
writes becomes an out-edge. The DAG is the audit trail, not the program.

---

## 1. Mechanic A → Demand-Driven Node Instantiation

**Source principle:** initialize ephemeral, single-task nodes in response to
incoming semantic density; no pre-defined static routing table.

### 1.1 Semantic density, defined computationally

Incoming payloads are embedded into a fixed-dimension vector
`e ∈ ℝ^d`. *Semantic density* at a point is the local mass of the substrate:

```
ρ(e) = Σ_{m ∈ LCS}  w_m · K(e, m.vec)        # kernel-weighted neighbor mass
       where K(a,b) = exp(−‖a − b‖² / 2σ²)   # Gaussian similarity kernel
             w_m    = current decay weight of marker m
```

A **Density Probe** (a thin, stateless instantiator — not a router) scans new
input and computes `ρ`. Instantiation is purely local and rule-driven:

| Condition on incoming embedding `e` | Action |
|---|---|
| `ρ(e) ≥ θ_hot` (dense region, hot topic) | spawn `⌈ρ(e)/θ_hot⌉` parallel workers, sharded by sub-cluster |
| `θ_cold ≤ ρ(e) < θ_hot` | spawn exactly 1 worker |
| `ρ(e) < θ_cold` (novel/sparse) | spawn 1 *explorer* worker with widened σ |

There is **no routing table**: the probe never decides *which* worker class
handles the payload. It only decides *how many* isolated environments to bring
up. Worker behavior is selected at runtime by what markers the worker finds
once it reads the substrate (§2).

### 1.2 Worker = isolated, single-task execution environment

Each worker is a **single-shot, sandboxed runtime** (container / microVM /
WASM instance — implementation-agnostic). Contract:

```python
class TaskWorker:
    """Single-task, isolated, ephemeral. No inbound network listeners."""
    worker_id:    UUID                 # ephemeral, never reused
    token_buffer: VectorBuffer         # bounded ring buffer, RAM-only
    focus:        Embedding            # the one marker region it serves
    deadline:     Monotonic            # hard wall-clock ceiling (failsafe)

    def run(self, lcs: Substrate) -> None:
        ctx = lcs.read_region(self.focus, radius=σ)   # pull, never pushed-to
        out = self.execute_single_task(ctx)           # exactly one unit of work
        lcs.deposit(self.derive_markers(out))         # write results as markers
        # control returns to lifecycle manager (§3)
```

Properties enforced by the platform, not by convention:
- **No shared mutable memory** between workers — only the LCS is shared.
- **No point-to-point endpoints** — workers expose no API surface (§2).
- **One task per lifetime** — the runtime is destroyed after `run()`; reuse is
  impossible because `worker_id` is single-use.

---

## 2. Mechanic B → Indirect Coordination via Shared Substrate

**Source principle:** no direct point-to-point APIs; coordinate by depositing
and reading decay-markers in a shared topological latent space.

### 2.1 The marker

```
Marker = {
  marker_id : UUID,
  vec       : float[d],     # position in the latent topology
  weight    : float,        # ∈ (0, 1], current activation strength
  ts        : monotonic_ns, # last reinforcement timestamp
  half_life : float,        # per-marker decay constant τ
  refs      : UUID[],       # producing worker(s) → forms DAG in-edges
  payload   : bytes,        # serialized partial result / instruction
}
```

The LCS is an **append-and-decay vector index** (HNSW/IVF for ANN reads,
backed by an MVCC log for the DAG). Two operations only:

```
deposit(marker)               # additive: reinforces if near-duplicate exists
read_region(center, radius)   # ANN query → markers ordered by weight·K
```

There is **no `send(worker_x, msg)` primitive anywhere in the system.**
Coordination is emergent:

1. Worker W₁ finishes, deposits marker M with `weight = 1.0` at position `vec`.
2. The Density Probe sees raised local density near `vec` → instantiates W₂.
3. W₂ does `read_region(vec)`, finds M, treats it as input/instruction.
4. W₂ deposits M′ slightly displaced → trail forms → guides W₃…

This is **trail-following over a topological field**. Strong, recently
reinforced regions attract more workers (positive feedback / path
amplification); ignored regions fade (§3). The emergent worker chain
`W₁ → W₂ → W₃` *is* a path in the derived DAG.

### 2.2 Decay (the "marker degradation")

Weight is never stored as a live value; it is *computed on read* so decay needs
no background sweeper for correctness:

```
w(t) = w₀ · 2^(−(t − ts) / half_life)        # exponential decay
```

Reinforcement: a `deposit` near an existing marker resets `ts` and bumps `w₀`
(capped at 1.0). This gives:
- **Reinforced paths persist** (repeatedly useful intermediate results).
- **Stale paths vanish** without explicit garbage-collection messaging.

### 2.3 Conflict & ordering

- **Idempotent merges:** deposits within `ε` cosine distance coalesce
  (CRDT-style G-Counter on weight) → no coordinator, no locks.
- **Causality:** `refs` chains give a partial order; the MVCC log linearizes
  for replay. The DAG is acyclic by construction because a marker can only
  reference markers with strictly earlier `ts`.

---

## 3. Mechanic C → Threshold-Triggered Deallocation

**Source principle:** a node self-terminates and flushes its token buffer the
instant its target marker degrades below the activation threshold.

### 3.1 Activation gate

Each worker is bound to a **focus marker** (or focus region). It holds a live
predicate:

```
alive(W) ≡ max_{m ∈ read_region(W.focus, ε)} w(m, now) ≥ θ_activation
```

Because `w` decays continuously and deterministically (§2.2), the worker can
compute the **exact future instant** its gate will fail — no polling jitter:

```
t_expire = ts + half_life · log2( w₀ / θ_activation )
```

The worker arms a high-resolution monotonic timer for `t_expire`. Any
reinforcement event (a `deposit` that raises `w₀` or resets `ts`) re-arms the
timer to a later `t_expire`. This makes the "exact millisecond" termination a
**scheduled, computed event**, not a busy-wait.

### 3.2 Deallocation sequence (ordered, atomic)

When the gate fails (`now ≥ t_expire` and no reinforcement intervened):

```
1. FENCE      stop reading the LCS; reject further work.
2. CHECKPOINT if partial result is above persistence threshold, flush it to
              the LCS as a final low-weight marker (so progress isn't lost);
              otherwise discard.
3. FLUSH      zero and free token_buffer (overwrite, not just drop the ref —
              guarantees no token residue leaks to the next tenant of the host).
4. DETACH     remove worker_id from any marker.refs write-locks.
5. DESTROY    terminate the isolated runtime; release CPU/RAM/quota.
```

Steps 1–5 are atomic w.r.t. the host: a half-terminated worker cannot deposit
new markers. This prevents "ghost" trails from dead workers.

### 3.3 Why this terminates the whole graph cleanly

- A worker only stays alive while its focus region is *being reinforced by
  downstream demand*.
- When a branch of work completes (or is abandoned), its markers stop being
  reinforced → weights decay → dependent workers hit `t_expire` → they
  deallocate → they stop reinforcing *their* upstream markers → cascade.
- The cascade is **back-pressure-free and message-free**: it is driven entirely
  by the absence of reinforcement, i.e., by decay reaching `θ_activation`.

The system reaches quiescence (zero live workers, all markers decayed below
threshold) automatically once input stops — no shutdown coordinator required.

---

## 4. End-to-End Lifecycle (worked sequence)

```
t0  Input embedding e arrives.
t1  Density Probe computes ρ(e)=0.2 (sparse) → spawns 1 explorer W_A.
t2  W_A reads region(e): empty. Executes task → deposits M1 (w=1.0) at v1.
t3  W_A's focus (e) has no reinforcement → t_expire passes → W_A deallocates,
    flushes buffer. (DAG node A is now terminal-with-output.)
t4  Probe notices density spike near v1 (from M1) → spawns W_B, W_C
    (ρ high, 2 sub-clusters).
t5  W_B reads M1 → produces M2; W_C reads M1 → produces M3.
    M1.refs ← {}, M2.refs ← {A}, M3.refs ← {A}.   # DAG edges form
t6  No worker reinforces M1 anymore → M1 decays below θ → workers focused on
    v1 (none left) → M1 simply ages out of ANN results.
t7  Chain continues until inputs near a region stop arriving; all weights
    decay < θ_activation; last workers deallocate. System quiescent.
```

Resulting **derived DAG**: `A → {B, C} → …`, reconstructable purely from
`marker.refs` in the MVCC log. Nobody declared this graph; it is the fossil
record of which markers fed which workers.

---

## 5. Component / Primitive Mapping (the schema)

| Source mechanic | Computational primitive | Concrete tech |
|---|---|---|
| Demand-driven instantiation | Stateless density evaluator + on-demand sandbox launch | k-NN density estimate → microVM/WASM cold-start pool |
| No static routing table | Behavior bound at read-time from substrate, not pre-wired | ANN region read selects task profile |
| Single-task ephemeral node | One-shot isolated runtime, single-use ID | Firecracker / gVisor / WASM instance |
| Indirect coordination | Shared append-and-decay vector index | HNSW/IVF index + MVCC log |
| Decay-markers | TTL-less exponential-weight vectors | `w(t)=w₀·2^(−Δt/τ)` computed on read |
| Reinforcement / path amplification | CRDT additive merge on co-located deposits | G-Counter on weight |
| Threshold deallocation | Pre-computed expiry timer + atomic teardown | monotonic timer → fenced flush/destroy |
| Buffer flush | Overwrite-then-free token ring buffer | zeroized RAM-only `VectorBuffer` |
| Coordination graph | Derived DAG from `marker.refs` | linearizable MVCC replay |

---

## 6. Properties & Guarantees

- **No central scheduler / SPOF:** only the LCS is shared; it is a replicable
  CRDT-backed store.
- **Acyclicity:** markers reference strictly-earlier markers → DAG cannot cycle.
- **Self-cleaning:** deterministic decay + computed expiry ⇒ no leaked workers,
  no orphan state, automatic quiescence.
- **Isolation/security:** no inbound endpoints on workers; token buffers are
  overwritten on teardown ⇒ no cross-tenant token residue.
- **Backpressure:** density-gated instantiation throttles itself when `ρ` is low;
  hot regions scale out via the `⌈ρ/θ_hot⌉` rule.

## 7. Key Tunables

| Symbol | Meaning | Effect of increase |
|---|---|---|
| `σ` | similarity kernel bandwidth | broader trail-following, fewer/larger clusters |
| `θ_hot`, `θ_cold` | spawn thresholds | controls parallelism vs. cost |
| `θ_activation` | termination floor | higher → workers die sooner, cheaper, less context retention |
| `half_life (τ)` | per-marker decay constant | longer-lived trails, more memory pressure |
| `ε` | merge/coalesce radius | dedup aggressiveness |
```
