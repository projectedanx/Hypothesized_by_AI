---

## Sparse Attention vs Token Pruning vs Sliding-Window

| Aspect | Sparse Attention | Token Pruning | Sliding-Window |
|--------|------------------|---------------|----------------|
| **Core Idea** | Attend to subset of positions via learned/random patterns | Dynamically remove "unimportant" tokens from computation | Limit attention to fixed local window size |
| **Efficiency Gain** | O(n²) → O(n√n) or O(n log n) | Proportional to prune ratio (can be 50%+) | O(n) per layer, constant memory |
| **Context Coverage** | Partial global + local (varies by pattern) | Preserves "important" tokens, loses others | Strictly local, no cross-window info |
| **Implementation** | Complex attention kernels, sparsity masks | Dynamic scoring + masking | Simple, standard in modern libs |

---

### 1. Sparse Attention

**Approaches:**
- **Fixed patterns**: Global + local blocks (BigBird, ETC)
- **Learnable**: Sparse attention heads learn optimal positions (Longformer)
- **Random**: Connect random nodes for global reach (BigBird's random attention)

**Efficiency vs Coverage:**
```
Full attention:     O(n²) — perfect coverage, infeasible at scale
Sparse (k patterns): O(n·k) — each token attends to k << n positions

Example: Longformer with global+local+random
- Local window: captures local structure
- Global tokens: CLS or task tokens maintain "summary"
- Random: provides path for information to propagate across distance
```

**Trade-off:** Better long-range dependency modeling than sliding-window alone, but complexity still superlinear and requires custom kernels.

---

### 2. Token Pruning

**Approaches:**
- **Static**: Remove tokens below certain importance score (e.g., token frequency, entropy)
- **Dynamic**: Learn which tokens to drop mid-computation (FastBERT, DeeBERT)
- **Mixture-of-Experts style**: Route tokens to different "experts" or skip layers

**Efficiency vs Coverage:**
```
Baseline: O(n) tokens per layer
With pruning: O(α·n) where α = kept token ratio (e.g., 0.5)

Key insight: Not all tokens contribute equally
- Redundant "the", "a" tokens → often prunable
- Key nouns/entities → usually kept
```

**Trade-off:** High efficiency gains, but risks losing nuanced information. Requires careful fine-tuning to maintain quality.

---

### 3. Sliding-Window Attention

**Approaches:**
- **Fixed window (W)**: Each token attends to W tokens on each side
- **Multi-head**: Different heads use different window sizes
- **Dilated**: Gaps in window for larger receptive field (Fastformer-style)

**Efficiency vs Coverage:**
```
O(n·W) per layer — linear in sequence length
Memory: O(n·W) instead of O(n²)

Example: Mistral-7B uses 4096 window size
- Local coherence captured well
- Information propagates via layer stacking (tokens in layer 1 influence layer 32)
```

**Trade-off:** Excellent local context, but long-range dependencies emerge only through layer stacking (limited in very deep models).

---

## Visual Trade-off Summary

```
Context Coverage →
                Low ←─────────────────────────→ High
Efficiency ↑     
   High  |  [Sliding-Window]   [Token Pruning]   [Full Attention]
         |   + Simple           + Aggressive        - O(n²) memory
         |   - Limited range    - Information loss  - Only for short seqs
         |
   Medium |                     [Sparse Attention]
         |                       + Flexible patterns
         |                       - Complex implementation
         |
   Low   |   [Dense Attention]  (theoretical baseline)
```

---

## Hybrid Approaches (Modern Models)

Most state-of-the-art models combine these:

```
┌─────────────────────────────────────────────┐
│  Mistral 7B / Llama 3:                       │
│  • Sliding-window (4K) for efficiency        │
│  • Grouped Query Attention (sparse key/value)│
│  • No explicit pruning, but implicit via GQA │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  BigBird / Longformer:                       │
│  • Global tokens (CLS, task markers)         │
│  • Sliding window (512)                      │
│  • Random connections (global propagation)   │
└─────────────────────────────────────────────┘
```

---

## Key Takeaways

| If you need... | Choose... |
|----------------|-----------|
| Long contexts with moderate efficiency | Sparse attention |
| Maximum speed with acceptable quality loss | Token pruning |
| Simple, predictable scaling | Sliding-window |
| Production systems | Hybrid (sliding + sparse + GQA/MQA) |

The field is moving toward **multi-scale attention** — combining local windows for efficiency with occasional global attention for long-range dependencies, often with learned routing between them.