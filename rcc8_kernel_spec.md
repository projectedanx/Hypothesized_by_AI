# GPU Kernel Specification: RCC-8 Spatial-Relation Evaluation over Embedding Pairs

**Document ID:** RCC8-KERNEL-2026
**Status:** Engineering draft
**Hardware target:** NVIDIA H100 SXM (Hopper) and B200 (Blackwell)
**Software:** OpenAI Triton 3.x / CUDA 12.x / PyTorch 2.x

> **Editorial note.** This document is a de-jargoned rewrite of an earlier
> artifact ("DRP-KERNEL-MEREOTOP-774-2026"). The original mixed sound GPU
> engineering with unfalsifiable framing ("Golden Scar Protocol", "Symbolic
> Scar Tissue Archive", "Semantic Reynolds Number", "Anionic Architecture",
> "pluriversal arbitration", "epistemic sovereignty"). None of those terms
> have an operational definition or a measurable acceptance test, so they are
> removed. What remains is the part that can actually be specified, built, and
> profiled. Where the original cited hardware numbers, they have been
> re-checked; corrections are flagged inline.

---

## 1. Scope and honest problem statement

We want a GPU kernel that, given two sets of region descriptors embedded as
vectors, classifies each pair `(i, j)` into one of the eight **Region
Connection Calculus (RCC-8)** relations:

| Code  | Relation                        | Informal meaning              |
|-------|---------------------------------|-------------------------------|
| DC    | Disconnected                    | no shared points              |
| EC    | Externally Connected            | boundaries touch, interiors don't |
| PO    | Partially Overlapping           | interiors overlap, neither contains the other |
| EQ    | Equal                           | same region                   |
| TPP   | Tangential Proper Part          | A inside B, boundaries touch  |
| NTPP  | Non-Tangential Proper Part      | A strictly inside B           |
| TPPi  | Inverse of TPP                  | B inside A, boundaries touch  |
| NTPPi | Inverse of NTPP                 | B strictly inside A           |

### 1.1 What is genuinely true

A single scalar distance cannot distinguish all eight relations. RCC-8 needs at
least two independent measurements (a boundary-separation term and an
interior-overlap term). This part of the original document is correct and is the
real motivation for the kernel.

### 1.2 What must be stated plainly (and was obscured before)

RCC-8 is defined over **regions** (sets with an interior and a boundary). A
generic learned embedding is a **point in R^D**, which has no interior or
boundary. Therefore **you cannot recover true RCC-8 relations from raw point
embeddings.** To make the problem well-posed you must commit to an explicit
*region model* per embedding, e.g.:

- **Ball model:** each embedding is a center `c ∈ R^D` plus a radius `r > 0`.
  Region = closed ball `B(c, r)`. This is the model assumed throughout this spec
  because every RCC-8 quantity has a closed form.
- **Box / axis-aligned model:** center plus per-axis half-widths.
- **Gaussian / level-set model:** region = super-level set of a density; requires
  numerical volume/intersection estimation.

The original document used a raw dot product as an "interior intersection"
(`iota = <Q, K>`) and a Euclidean distance as a "boundary distance". Those two
quantities are **not** the interior overlap and boundary separation of any
region model, so the original kernel's RCC-8 labels were not well-defined. This
rewrite fixes that by adopting the ball model and deriving the predicates from
it.

---

## 2. Region model and exact RCC-8 predicates (ball model)

Let region `A = B(c_A, r_A)` and `B = B(c_B, r_B)`. Define:

```
d        = ||c_A - c_B||_2          # center distance
sum_r    = r_A + r_B
diff_r   = |r_A - r_B|
```

For balls, the eight relations are mutually exclusive and decided by comparing
`d` against `sum_r` and `diff_r`, with a tolerance `eps`:

| Relation | Condition (ball model)                                  |
|----------|--------------------------------------------------------|
| DC       | `d > sum_r + eps`                                       |
| EC       | `|d - sum_r| <= eps`                                    |
| EQ       | `d <= eps` **and** `diff_r <= eps`                      |
| PO       | `diff_r + eps < d < sum_r - eps`                        |
| TPP      | `|d - diff_r| <= eps` **and** `r_A < r_B`               |
| TPPi     | `|d - diff_r| <= eps` **and** `r_B < r_A`               |
| NTPP     | `d < diff_r - eps` **and** `r_A < r_B`                  |
| NTPPi    | `d < diff_r - eps` **and** `r_B < r_A`                  |

These are exact for balls; there is no probabilistic approximation involved,
which is the one defensible claim from the original ("deterministic, not
probabilistic"). The geometry — not any metaphysics — is what makes it
deterministic.

`eps` is an ordinary numerical tolerance. Pick it relative to the scale of your
coordinates (e.g. `eps = 1e-4 * median(r)`), **not** the IEEE-754 machine
epsilon. Machine epsilon (`~1.19e-7` for fp32) is far too tight: it would make
EC and TPP essentially unreachable because exact floating-point equality of `d`
and `sum_r` almost never occurs. This is a real bug in the original spec, which
set `epsilon = 1.1920929e-7` and then expected the EC/TPP states to fire.

---

## 3. Hardware constraints (re-verified, 2026)

The original table contained one material error and one precision conflation.
Corrected figures:

| Tier | H100 SXM (Hopper) | B200 (Blackwell, datacenter) | Source note |
|------|-------------------|------------------------------|-------------|
| Max shared mem / SM | up to **228 KB** (opt-in; 256 KB combined L1+shared) | up to **228 KB** (opt-in; 256 KB combined L1+shared) | NVIDIA Blackwell Tuning Guide |
| L2 cache | 50 MB | ~one large unified L2 (NVIDIA materials and third parties quote figures from ~65 MB to 192 MB; treat as "much larger than H100", verify on your SKU) | conflicting public sources |
| HBM bandwidth | 3.35 TB/s | 8.0 TB/s | consistent across sources |
| NVLink | NVLink4, 900 GB/s | NVLink5, 1.8 TB/s | consistent |
| FP8 tensor (dense) | ~1,979 TFLOPS | ~4,500 TFLOPS | dense numbers |
| FP8 tensor (2:4 sparse) | ~3,958 TFLOPS | ~9,000 TFLOPS | sparse numbers |

**Corrections vs. the original document:**

1. **B200 shared memory is *not* 128 KB.** The datacenter B200 (compute
   capability 10.0) supports the same shared-memory ladder as Hopper, up to
   228 KB per SM. The "128 KB" figure applies to *consumer* Blackwell
   (compute capability 12.0, e.g. GB20x GeForce parts), which is a different
   product and not a stated target here. The original spec's claim that
   "Blackwell requires more aggressive tiling" because of a 128 KB budget is
   therefore wrong for the B200.
2. **FP8 FLOPS were quoted as sparse but labelled as if peak/general.** The
   `~3,958` (H100) and `~9,000` (B200) numbers are the **2:4-sparse** rates.
   Dense rates are roughly half. State which you mean.
3. This kernel is **not a tensor-core workload.** It is dominated by
   elementwise compares and one small matmul (the center-distance term). The FP8
   TFLOPS figures are essentially irrelevant to it; including them was padding.

---

## 4. Kernel design

### 4.1 Tiling

Compute the `M × N` relation matrix in tiles. Each program instance handles a
`BLOCK_M × BLOCK_N` tile and streams the embedding dimension `D` in chunks of
`BLOCK_D`.

```
BLOCK_M = 64      # query regions per tile
BLOCK_N = 64      # key regions per tile
BLOCK_D = 128     # embedding-dim chunk
num_warps = 4     # start here; autotune (see 4.4)
num_stages = 3    # software-pipelined prefetch of the next D-chunk
```

### 4.2 SRAM budget (honest accounting)

For `BLOCK_M = BLOCK_N = 64`, `BLOCK_D = 128`, bf16 inputs:

```
Q chunk:  64 x 128 x 2 B = 16 KB
K chunk:  64 x 128 x 2 B = 16 KB
d^2 accumulator (fp32): 64 x 64 x 4 B = 16 KB
-----------------------------------------------
peak live SRAM:        ~48 KB
```

This fits comfortably on **both** H100 and B200 at the default carveout; no
opt-in to the 228 KB mode is required for these tile sizes. The original
document's "boundary mask registers" line (8 states × 1 bit) double-counted:
the eight relations are mutually exclusive, so the result is a **single integer
label per pair (one byte)**, not eight bitmasks. Storing eight float channels is
wasteful unless a downstream consumer truly needs soft scores.

### 4.3 Compute

The only quantity that needs the embedding dimension is the squared center
distance:

```
d^2(i,j) = ||c_i||^2 + ||c_j||^2 - 2 <c_i, c_j>
```

The `<c_i, c_j>` term is a small GEMM and is the one place `tl.dot` (and hence
tensor cores, if the dtype qualifies) is used. Everything after that —
forming `d`, comparing against `sum_r`/`diff_r`, assigning the label — is
elementwise on the `64 × 64` tile.

> **Numerical caveat.** The `||a||^2 + ||b||^2 - 2<a,b>` identity loses
> precision when the two norms are large and `d` is small (catastrophic
> cancellation), which is exactly the EQ / NTPP regime we care about. Accumulate
> the dot product in fp32 (or fp64 for the norm terms) even if inputs are bf16,
> and clamp `d^2` to `>= 0` before the square root.

### 4.4 Branch divergence: keep it, but right-size the claim

The original's core implementation idea is sound: evaluate the relation with
predicated/`tl.where` selects rather than a divergent `if/elif` chain, so all
threads in a warp follow one instruction stream. That is standard, good practice
on SIMT hardware.

What was overstated:

- **"~1.6× compute overhead vs. 32× divergence slowdown."** Both numbers are
  invented. The actual select-based overhead here is negligible because the
  predicates are a handful of compares on a tiny tile; and a 32× penalty only
  occurs in the pathological case of fully serialized 32-way divergence, which a
  simple `if/elif` chain over 8 outcomes does not produce. Keep the predicated
  style because it is clean and avoids divergence, not because of these figures.
- Because the eight ball-model relations are **mutually exclusive by
  construction**, you do not need eight score tensors and an argmax. Compute one
  integer label directly via a select cascade. This halves register pressure and
  removes the "priority tie-break" hack the original needed for its
  non-exclusive predicates.

---

## 5. Reference Triton kernel

```python
"""
RCC8-KERNEL-2026 — ball-model RCC-8 relation classification.
Target: Triton 3.x / CUDA 12.x / PyTorch 2.x.

Each embedding is (center c in R^D, radius r > 0).
Output: integer label in {0..7} per (i, j) pair.
  0 DC  1 EC  2 PO  3 EQ  4 TPP  5 NTPP  6 TPPi  7 NTPPi
"""

import torch
import triton
import triton.language as tl

# Label constants (kept in sync with the host side).
DC, EC, PO, EQ, TPP, NTPP, TPPi, NTPPi = range(8)


@triton.autotune(
    configs=[
        triton.Config({"BLOCK_M": 64, "BLOCK_N": 64, "BLOCK_D": 64},  num_warps=4, num_stages=3),
        triton.Config({"BLOCK_M": 64, "BLOCK_N": 64, "BLOCK_D": 128}, num_warps=4, num_stages=3),
        triton.Config({"BLOCK_M": 128,"BLOCK_N": 64, "BLOCK_D": 64},  num_warps=8, num_stages=3),
        triton.Config({"BLOCK_M": 32, "BLOCK_N": 32, "BLOCK_D": 128}, num_warps=4, num_stages=2),
    ],
    key=["M", "N", "D"],
)
@triton.jit
def rcc8_kernel(
    C_ptr,            # centers   [M, D]  (query)
    K_ptr,            # centers   [N, D]  (key)
    RA_ptr,           # radii     [M]
    RB_ptr,           # radii     [N]
    OUT_ptr,          # labels    [M, N]  int32
    M, N, D,
    stride_cm, stride_cd,
    stride_km, stride_kd,
    stride_om, stride_on,
    EPS: tl.constexpr,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_D: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    mask_m = offs_m < M
    mask_n = offs_n < N

    # Accumulators (fp32) for the squared-distance identity.
    qq = tl.zeros([BLOCK_M], dtype=tl.float32)          # ||c_i||^2
    kk = tl.zeros([BLOCK_N], dtype=tl.float32)          # ||c_j||^2
    qk = tl.zeros([BLOCK_M, BLOCK_N], dtype=tl.float32) # <c_i, c_j>

    for d0 in range(0, D, BLOCK_D):
        offs_d = d0 + tl.arange(0, BLOCK_D)
        mask_d = offs_d < D

        q = tl.load(
            C_ptr + offs_m[:, None] * stride_cm + offs_d[None, :] * stride_cd,
            mask=mask_m[:, None] & mask_d[None, :], other=0.0,
        ).to(tl.float32)
        k = tl.load(
            K_ptr + offs_n[:, None] * stride_km + offs_d[None, :] * stride_kd,
            mask=mask_n[:, None] & mask_d[None, :], other=0.0,
        ).to(tl.float32)

        qq += tl.sum(q * q, axis=1)
        kk += tl.sum(k * k, axis=1)
        qk += tl.dot(q, tl.trans(k))                    # the only matmul

    d2 = qq[:, None] + kk[None, :] - 2.0 * qk
    d = tl.sqrt(tl.maximum(d2, 0.0))                    # guard cancellation

    rA = tl.load(RA_ptr + offs_m, mask=mask_m, other=0.0).to(tl.float32)
    rB = tl.load(RB_ptr + offs_n, mask=mask_n, other=0.0).to(tl.float32)
    sum_r = rA[:, None] + rB[None, :]
    diff_r = tl.abs(rA[:, None] - rB[None, :])
    a_smaller = rA[:, None] < rB[None, :]

    # Mutually exclusive predicates -> single label via select cascade.
    # Order matters only to break floating-point ties at the tolerances;
    # the underlying conditions are disjoint up to O(eps).
    label = tl.full([BLOCK_M, BLOCK_N], DC, dtype=tl.int32)

    is_eq  = (d <= EPS) & (diff_r <= EPS)
    is_ec  = tl.abs(d - sum_r) <= EPS
    is_tan = tl.abs(d - diff_r) <= EPS          # tangential internal contact
    is_po  = (d > diff_r + EPS) & (d < sum_r - EPS)
    is_int = d < diff_r - EPS                    # one strictly inside the other

    label = tl.where(is_ec, EC, label)
    label = tl.where(is_po, PO, label)
    label = tl.where(is_tan & a_smaller,  TPP,  label)
    label = tl.where(is_tan & ~a_smaller, TPPi, label)
    label = tl.where(is_int & a_smaller,  NTPP, label)
    label = tl.where(is_int & ~a_smaller, NTPPi, label)
    label = tl.where(is_eq, EQ, label)          # EQ wins ties (most specific)

    out_ptrs = OUT_ptr + offs_m[:, None] * stride_om + offs_n[None, :] * stride_on
    tl.store(out_ptrs, label, mask=mask_m[:, None] & mask_n[None, :])


def rcc8_relations(cA, rA, cB, rB, eps=1e-4):
    """cA:[M,D] rA:[M] cB:[N,D] rB:[N] -> labels:[M,N] int32 on the same device."""
    assert cA.is_cuda and cB.is_cuda, "CUDA tensors required"
    M, D = cA.shape
    N = cB.shape[0]
    out = torch.empty((M, N), dtype=torch.int32, device=cA.device)
    grid = lambda meta: (triton.cdiv(M, meta["BLOCK_M"]),
                         triton.cdiv(N, meta["BLOCK_N"]))
    rcc8_kernel[grid](
        cA, cB, rA, rB, out,
        M, N, D,
        cA.stride(0), cA.stride(1),
        cB.stride(0), cB.stride(1),
        out.stride(0), out.stride(1),
        EPS=eps,
    )
    return out
```

---

## 6. CPU reference and validation

The right baseline is a **vectorized, correct** PyTorch implementation of the
*same* ball-model predicates — not `torch.cdist` on raw embeddings, which
computes a different quantity. Use the reference for correctness; use a tuned
dense GPU implementation for the speed comparison.

```python
import torch

def rcc8_reference(cA, rA, cB, rB, eps=1e-4):
    d = torch.cdist(cA, cB)                       # [M, N] center distances
    sum_r = rA[:, None] + rB[None, :]
    diff_r = (rA[:, None] - rB[None, :]).abs()
    a_smaller = rA[:, None] < rB[None, :]

    label = torch.zeros_like(d, dtype=torch.long)   # DC = 0
    is_eq  = (d <= eps) & (diff_r <= eps)
    is_ec  = (d - sum_r).abs() <= eps
    is_tan = (d - diff_r).abs() <= eps
    is_po  = (d > diff_r + eps) & (d < sum_r - eps)
    is_int = d < diff_r - eps

    label = torch.where(is_ec, torch.tensor(1, device=d.device), label)   # EC
    label = torch.where(is_po, torch.tensor(2, device=d.device), label)   # PO
    label = torch.where(is_tan &  a_smaller, torch.tensor(4, device=d.device), label)  # TPP
    label = torch.where(is_tan & ~a_smaller, torch.tensor(6, device=d.device), label)  # TPPi
    label = torch.where(is_int &  a_smaller, torch.tensor(5, device=d.device), label)  # NTPP
    label = torch.where(is_int & ~a_smaller, torch.tensor(7, device=d.device), label)  # NTPPi
    label = torch.where(is_eq, torch.tensor(3, device=d.device), label)   # EQ
    return label
```

### 6.1 Tests that actually mean something

1. **Constructed-case exactness.** Build region pairs whose relation you know by
   construction (two far-apart balls = DC; concentric with `rA < rB` = NTPP;
   `d == rB - rA` exactly = TPP; etc.). Assert the kernel returns the intended
   label. This is stronger than agreeing with a second implementation, because
   both could share a bug.
2. **Agreement with the reference.** `(kernel == reference).float().mean()`
   should be `1.0` (exact, integer labels) on random inputs, modulo
   ties exactly at the tolerance which you should perturb away.
3. **All eight labels exercised.** Generate inputs designed to hit each class;
   assert each label appears. (Random Gaussian centers with random radii will
   almost never produce EC/TPP/EQ, because those are measure-zero conditions —
   another reason the original's `test_all_8_rcc8_states_present` would have
   failed on random data.)
4. **Speed.** Compare against the *tuned dense GPU reference*, on the same dtype,
   averaged over many iterations with `torch.cuda.synchronize()` and warmup.
   Report it as a measured number; do not assert a fixed ">5x" target in CI —
   speedups depend on shape, dtype, and GPU, and a hard threshold makes the test
   flaky.

---

## 7. Gradients (replacing the "Golden Scar Protocol")

The original identified one legitimate concern and then dressed it up.

**The legitimate concern:** the RCC-8 *label* is a piecewise-constant function of
the inputs, so its gradient is zero almost everywhere and undefined on the
decision boundaries. You cannot train through a hard classification.

**The fabricated part:** multiplying the gradient by the golden ratio
`φ ≈ 1.618` "to preserve structural tension" has no mathematical justification.
The cited rationale ("φ is the only ratio that under self-similar scaling neither
converges to zero nor diverges") is false — *any* constant `> 1` diverges under
repeated multiplication and any constant in `(0,1)` converges; `φ` is not
special here. There is no "Symbolic Scar Tissue Archive log c1f2b4a7"; it is
not a real artifact and should be removed.

**What to do instead** — standard, defensible techniques for differentiating
through a discrete/relational decision:

- **Train on the continuous quantities, not the label.** The signed margins
  `d - sum_r`, `d - diff_r`, etc. are smooth a.e. in the centers and radii.
  Define a differentiable loss on those margins (e.g. hinge/softplus margins
  toward the desired relation) and let the hard label be inference-only.
- **Soft RCC-8 via temperature.** Replace each hard `<=`/`>` with a sigmoid of
  the margin over a temperature `τ`; this yields soft membership in each class
  and a usable gradient. Anneal `τ → 0` to recover the hard kernel at inference.
- **Straight-through estimator.** Forward: hard label. Backward: gradient of the
  soft surrogate. This is the conventional way to backprop through an argmax-like
  op and needs no magic constant.

If you genuinely observe vanishing gradients at boundaries, the fix is a
non-zero-derivative surrogate (softplus/leaky margins), chosen so the
implied loss is what you want — not an arbitrary scalar multiplier.

---

## 8. Profiling

The profiling commands in the original are fine and worth keeping. Realistic
targets for *this* kernel:

- **Memory coalescing** (`l1tex__t_sectors_pipe_lsu_mem_global_op_ld_lookup_hit.pct`):
  row-major contiguous loads of the centers should be well coalesced. If the
  embedding tensor is transposed/strided, transpose it once before launch.
- **Occupancy** (`sm__warps_active.avg.pct_of_peak_sustained_active`): let the
  autotuner pick `num_warps`; don't hard-code 8.
- **Divergence** (`sm__sass_branch_targets_threads_diverged.avg`): should be ~0
  given the predicated select cascade.
- **Register count / shared mem:** read from `kernel.cache` after compilation or
  via `--ptxas-options=-v`; ensure no spills at the chosen tile size.

```bash
ncu --set full --target-processes all python run_rcc8.py
```

---

## 9. Multi-GPU note (kept brief and grounded)

For very large `M, N` the relation matrix is `M × N` integers and is the binding
cost, not the embeddings. Two practical points survive from the original:

- **Move results, not regions.** When a pair spans GPUs, exchanging the small
  region descriptors (or computing locally and exchanging labels) is far cheaper
  than shipping full embedding tensors. This is just standard data-movement
  minimization.
- **Sparsity.** In most realistic spatial graphs the overwhelming majority of
  pairs are DC. Store the result sparsely (COO of non-DC pairs) and treat DC as
  the implicit default. Be explicit in the schema about "confirmed DC" vs.
  "not computed" so downstream consumers don't misread an absent entry.

The 72-GPU "NVL72 / Topological Locality Partitioning" section of the original
is a reasonable *clustering-for-locality* idea but was presented with invented
performance ratios; if you pursue it, benchmark it rather than asserting
">90% intra-GPU".

---

## 10. Summary of changes from the original artifact

| Area | Original claim | Corrected |
|------|----------------|-----------|
| Region semantics | RCC-8 from raw point embeddings via dot product / L2 | Requires an explicit region model; ball model adopted with exact predicates |
| `epsilon` | IEEE-754 machine epsilon (~1.19e-7) | A scale-relative tolerance; machine epsilon makes EC/TPP/EQ unreachable |
| B200 SRAM | "128 KB default, more aggressive tiling needed" | 228 KB available (same ladder as Hopper); 128 KB is *consumer* Blackwell |
| FP8 FLOPS | quoted sparse rates as headline numbers; implied relevance | sparse vs dense distinguished; FP8 is irrelevant to this compare-bound kernel |
| Output | 8-channel float scores + argmax + tie-break | single int label (relations are mutually exclusive) |
| Divergence math | "1.6× vs 32×" overhead figures | predicated selects are good practice; the specific ratios were invented |
| Gradients | "Golden Scar" φ-multiplier; fictional STA log | margin loss / soft-RCC8 / straight-through estimator |
| "Semantic Reynolds Number", "epistemic sovereignty", "Anionic Architecture", "pluriversal arbitration" | presented as constraints | removed — no operational definition or test |
| Speed test | hard-assert ">5× over torch.cdist baseline" | measure vs. a *correct* tuned baseline; don't gate CI on a fixed ratio |

The one idea worth carrying forward unchanged: RCC-8 needs at least two
independent geometric measurements and can be evaluated deterministically and
divergence-free on a GPU. Everything else needed grounding.
```