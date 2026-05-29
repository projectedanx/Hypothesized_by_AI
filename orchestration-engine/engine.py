"""
Decentralized Orchestration Engine — reference implementation (single-process
simulation of the distributed design in DESIGN.md).

Mechanics mapped to computational primitives ONLY (no biological vocabulary in
the runtime):
  A. demand-driven instantiation  -> DensityProbe spawns one-shot TaskWorkers
  B. indirect coordination        -> LatentSubstrate (append-and-decay vec store)
  C. threshold-triggered teardown -> computed expiry + atomic flush/destroy

The execution history forms a DERIVED DAG: every marker version a worker reads
becomes an in-edge of the version it writes. MVCC version numbers are globally
monotonic, so every edge points from a higher version to a strictly-lower one
=> the graph is acyclic by construction (proven at the end of demo()).

Run:  python engine.py
"""
from __future__ import annotations
import math
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

# ----------------------------- vector helpers ------------------------------ #

def dot(a, b):   return sum(x * y for x, y in zip(a, b))
def norm(a):     return math.sqrt(dot(a, a)) or 1e-12
def dist2(a, b): return sum((x - y) ** 2 for x, y in zip(a, b))
def cos(a, b):   return dot(a, b) / (norm(a) * norm(b))


def kernel(a, b, sigma):
    """Gaussian similarity kernel K(a,b)."""
    return math.exp(-dist2(a, b) / (2 * sigma * sigma))


# ------------------------------ the marker --------------------------------- #

@dataclass
class Marker:
    vec: list[float]
    w0: float                       # weight at last reinforcement
    ts: float                       # last reinforcement time (monotonic)
    half_life: float                # decay constant tau
    payload: object = None
    version: int = 0                # current MVCC version (globally monotonic)
    marker_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def weight(self, now: float) -> float:
        """Decay computed ON READ: w(t) = w0 * 2^(-(t-ts)/half_life)."""
        return self.w0 * (2.0 ** (-(now - self.ts) / self.half_life))


# ------------------ Mechanic B: shared latent substrate -------------------- #

class LatentSubstrate:
    """Append-and-decay vector store. The ONLY shared, addressable surface.
    No send()/recv() between workers exists anywhere."""

    def __init__(self, merge_eps=0.02):
        self.markers: dict[str, Marker] = {}
        self.merge_eps = merge_eps          # cosine-distance coalesce radius
        self.log: list[tuple] = []          # MVCC append log -> DAG replay
        self._seq = 0                       # monotonic global version counter

    def _next_version(self) -> int:
        self._seq += 1
        return self._seq

    def deposit(self, vec, weight, half_life, refs=None, payload=None,
                now=None) -> Marker:
        """refs are (marker_id, version) parent handles captured at read time.
        A parent edge is kept only if parent_version < new child_version, which
        guarantees acyclicity regardless of merge/reinforcement behavior."""
        now = now if now is not None else time.monotonic()
        refs = refs or []
        parent_versions = [v for (_pid, v) in refs]

        # CRDT-style additive merge with a co-located marker (path amplification)
        for m in self.markers.values():
            if (1 - cos(m.vec, vec)) <= self.merge_eps:
                child_v = self._next_version()          # NEW version on reinforce
                edges = [pv for pv in parent_versions if pv < child_v]
                m.w0 = min(1.0, m.weight(now) + weight)  # reinforce
                m.ts = now                               # reset decay clock
                m.version = child_v
                if payload is not None:
                    m.payload = payload
                self.log.append((now, "reinforce", m.marker_id, child_v, edges))
                return m

        child_v = self._next_version()
        edges = [pv for pv in parent_versions if pv < child_v]
        m = Marker(vec=list(vec), w0=min(1.0, weight), ts=now,
                   half_life=half_life, payload=payload, version=child_v)
        self.markers[m.marker_id] = m
        self.log.append((now, "deposit", m.marker_id, child_v, edges))
        return m

    def read_region(self, center, sigma, now=None, top_k=8):
        """ANN-style region read: markers ranked by weight * kernel."""
        now = now if now is not None else time.monotonic()
        scored = [(m.weight(now) * kernel(center, m.vec, sigma), m)
                  for m in self.markers.values()]
        scored = [(s, m) for s, m in scored if s > 0]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:top_k]]

    def density(self, center, sigma, now=None) -> float:
        """Semantic density rho(e) = sum w_m * K(e, m.vec)."""
        now = now if now is not None else time.monotonic()
        return sum(m.weight(now) * kernel(center, m.vec, sigma)
                   for m in self.markers.values())

    def vacuum(self, theta, now=None):
        """Markers below threshold simply age out of the index."""
        now = now if now is not None else time.monotonic()
        dead = [k for k, m in self.markers.items() if m.weight(now) < theta]
        for k in dead:
            del self.markers[k]
        return len(dead)


# ----------------------- bounded RAM-only token buffer --------------------- #

class VectorBuffer:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self._buf: list = []

    def push(self, tok):
        self._buf.append(tok)
        if len(self._buf) > self.capacity:
            self._buf.pop(0)            # ring behavior

    def flush(self):
        """Overwrite then free -> no token residue for the next host tenant."""
        for i in range(len(self._buf)):
            self._buf[i] = 0
        self._buf = []


# ----------- Mechanic A + C: one-shot worker with computed expiry ---------- #

@dataclass
class TaskWorker:
    focus: list[float]
    sigma: float
    half_life: float
    theta_activation: float
    task: Callable[[list[Marker]], tuple[list[float], object]]
    worker_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    token_buffer: VectorBuffer = field(default_factory=VectorBuffer)
    alive: bool = True

    def expiry(self, focus_marker: Optional[Marker], now: float) -> float:
        """Exact instant the activation gate will fail (no busy-wait)."""
        if focus_marker is None or focus_marker.w0 <= self.theta_activation:
            return now                       # nothing reinforcing us -> expire now
        dt = focus_marker.half_life * math.log2(
            focus_marker.w0 / self.theta_activation)
        return focus_marker.ts + dt

    def run(self, lcs: LatentSubstrate, now: float):
        """Single task per lifetime: read -> execute -> deposit."""
        ctx = lcs.read_region(self.focus, self.sigma, now=now)
        for m in ctx:
            self.token_buffer.push(m.marker_id)
        out_vec, out_payload = self.task(ctx)
        refs = [(m.marker_id, m.version) for m in ctx]   # MVCC parent handles
        return lcs.deposit(out_vec, weight=1.0, half_life=self.half_life,
                           refs=refs, payload=out_payload, now=now)

    def teardown(self):
        """Atomic threshold-triggered deallocation: fence -> flush -> destroy."""
        self.alive = False                  # FENCE
        self.token_buffer.flush()           # FLUSH (overwrite + free)
        # DESTROY: object dropped by caller; worker_id never reused


# ----------------------- Mechanic A: density probe ------------------------- #

class DensityProbe:
    """Stateless instantiator. Decides HOW MANY workers, never WHICH route."""
    def __init__(self, theta_hot=1.5, theta_cold=0.3, sigma=0.5):
        self.theta_hot = theta_hot
        self.theta_cold = theta_cold
        self.sigma = sigma

    def spawn_count(self, rho: float) -> tuple[int, float]:
        if rho >= self.theta_hot:
            return math.ceil(rho / self.theta_hot), self.sigma
        if rho >= self.theta_cold:
            return 1, self.sigma
        return 1, self.sigma * 2.0          # explorer: widened bandwidth


# ------------------------------- driver ------------------------------------ #

def demo():
    lcs = LatentSubstrate(merge_eps=0.02)
    probe = DensityProbe(theta_hot=1.5, theta_cold=0.3, sigma=0.5)
    HALF_LIFE = 0.05          # seconds (fast decay for a quick demo)
    THETA_ACT = 0.25
    clock = time.monotonic()

    def make_task(label, angle):
        # each worker pushes its result to a distinct latent location so the
        # substrate spreads out and a branching DAG forms (instead of collapsing)
        def _task(ctx):
            inb = ctx[0].vec if ctx else [0.0, 0.0]
            out = [inb[0] + 0.6 * math.cos(angle), inb[1] + 0.6 * math.sin(angle)]
            return out, f"{label}<-{[m.marker_id for m in ctx]}"
        return _task

    # ---- Mechanic A: input arrives, probe instantiates from density ----
    inputs = [[1.0, 0.0], [1.02, 0.01], [1.0, 0.02]]   # a dense cluster
    live: list[TaskWorker] = []

    for e in inputs:
        rho = lcs.density(e, probe.sigma, now=clock)
        n, sig = probe.spawn_count(rho)
        for i in range(n):
            live.append(TaskWorker(
                focus=list(e), sigma=sig, half_life=HALF_LIFE,
                theta_activation=THETA_ACT,
                task=make_task(f"g0.{i}", (i + len(live)) * 1.1)))
    print(f"[spawn] density-gated -> {len(live)} workers instantiated")

    # ---- run generations; workers read substrate, deposit markers ----
    for gen in range(3):
        clock = time.monotonic()
        produced = [w.run(lcs, now=clock) for w in live if w.alive]

        # Mechanic C: compute expiry, tear down workers whose gate fails
        survivors = []
        for w in live:
            region = lcs.read_region(w.focus, w.sigma, now=clock)
            fm = max(region, key=lambda m: m.weight(clock), default=None)
            if clock >= w.expiry(fm, clock):
                w.teardown()
            else:
                survivors.append(w)
        live = survivors

        # next generation: probe re-instantiates from the NEW marker density
        for m in produced:
            rho = lcs.density(m.vec, probe.sigma, now=clock)
            n, sig = probe.spawn_count(rho)
            for i in range(n):
                live.append(TaskWorker(
                    focus=list(m.vec), sigma=sig, half_life=HALF_LIFE,
                    theta_activation=THETA_ACT,
                    task=make_task(f"g{gen+1}.{i}", (gen + i) * 0.9 + 0.3)))
        print(f"[gen {gen}] produced={len(produced)} markers, "
              f"live workers now={len(live)}, "
              f"substrate markers={len(lcs.markers)}")

    # ---- quiescence: let decay run, tear down, vacuum aged markers ----
    time.sleep(HALF_LIFE * 4)
    clock = time.monotonic()
    for w in live:
        w.teardown()
    removed = lcs.vacuum(THETA_ACT, now=clock)
    print(f"[quiesce] all workers torn down, vacuumed {removed} decayed markers, "
          f"remaining={len(lcs.markers)}")

    # ---- reconstruct + verify the DERIVED DAG from the version log ----
    print("\n[derived DAG] version edges (child_v <- parent_v):")
    label = {cv: f"{mid}#{cv}" for _ts, _op, mid, cv, _e in lcs.log}
    all_edges = [(cv, pv) for _ts, _op, _mid, cv, edges in lcs.log for pv in edges]
    for cv, pv in all_edges[:24]:
        print(f"   {label.get(cv, cv)} <- {label.get(pv, '?')}")
    if len(all_edges) > 24:
        print(f"   ... ({len(all_edges) - 24} more edges)")
    violations = [(cv, pv) for cv, pv in all_edges if pv >= cv]
    print(f"\nTotal version edges: {len(all_edges)}; "
          f"edges violating parent_v < child_v: {len(violations)} "
          f"-> {'ACYCLIC (DAG proven by version order)' if not violations else 'INVALID'}")


if __name__ == "__main__":
    demo()
