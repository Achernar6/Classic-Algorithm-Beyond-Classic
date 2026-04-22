# visualization_guide.md

# Pathspace Lab visualization guide

This document defines what each MVP figure shows, what it means, and what it must not imply.

The central rule:

> The same canvas does not mean the same mechanism.

Hard DP, Soft-DP, and QA can all be projected onto a layer-node heatmap, but their hidden objects are different.

---

## 1. Shared visual canvas

The MVP uses a layer-node canvas.

Horizontal axis:

\[
\ell=0,1,\dots,L-1
\]

Vertical axis:

\[
v=0,1,\dots,W-1
\]

A visible cell is:

\[
(\ell,v).
\]

The plotting code may use array shape:

```python
cell_heat.shape == (L, W)
```

and transpose it for display so that layers run left to right.

---

## 2. Problem graph plot

### Shows

- The layered DAG.
- Node positions \((\ell,v)\).
- Optional node cost.
- Optional edge cost.
- Optional highlighted paths, such as gold path and decoy path.

### Purpose

Introduce the problem before showing algorithms.

### Recommended narrative

> A solution is one path through the layers. The planted gold path is globally best, while the decoy path looks attractive early but becomes costly later.

### Do not imply

- That the graph layout is the quantum configuration space.
- That QA current flows along these edges.

---

## 3. Hard DP value heatmap

### Data source

Hard DP trace.

### Heat value

Raw DP value:

\[
D(\ell,v).
\]

For visual brightness, use normalized goodness:

\[
G(\ell,v)=\frac{\max D-D(\ell,v)}{\max D-\min D+\epsilon}.
\]

### Meaning

A bright cell means:

> The best partial path ending here has relatively low cost.

### Purpose

Show deterministic min-plus message passing and compression of histories into local scalar values.

### Do not imply

- DP values are probabilities.
- Bright cells represent all likely final solutions.
- The DP table stores all paths.

### Useful overlays

- Frontier marker for current layer.
- Backpointer arrows.
- Final traceback path.

---

## 4. Soft-DP marginal heatmap

### Data source

Soft-DP trace.

### Heat value

\[
M^{\text{soft}}_{\ell,v}(\beta)
=\sum_{p:p_\ell=v}P_\beta(p).
\]

where:

\[
P_\beta(p)=\frac{e^{-\beta E(p)}}{Z_\beta}.
\]

### Meaning

A bright cell means:

> Under the classical thermal path distribution at this beta, many probable complete paths pass through this cell.

### Purpose

Show probability condensation without quantum phases or interference.

### Expected behavior

- At \(\beta=0\), each layer is roughly uniform over nodes if all paths are structurally symmetric.
- As \(\beta\) grows, mass concentrates around low-energy paths.

### Do not imply

- This is quantum.
- This is a DP value table.
- This distribution has memory of a physical time evolution.

---

## 5. QA marginal heatmap

### Data source

Feasible-subspace QA trace.

### Heat value

\[
M^{\text{QA}}_{\ell,v}(s)
=\sum_{p:p_\ell=v}|\psi_p(s)|^2.
\]

### Meaning

A bright cell means:

> If we measured the current quantum state as a full path, the observed path would likely use this cell.

### Purpose

Show how a wavefunction over complete paths projects onto the DP canvas.

### Expected behavior

- At \(s=0\), the feasible path distribution is uniform.
- During evolution, mass may move non-monotonically.
- Near the end, mass may concentrate on low-energy paths, depending on total time and gap structure.

### Do not imply

- QA is filling the DP table left to right.
- QA probability literally flows along original graph edges.
- The final state must be exactly optimal for finite runtime.

---

## 6. Side-by-side Soft-DP vs QA heatmaps

### Shows

Two heatmaps on the same canvas:

- Soft-DP cell marginal,
- QA cell marginal.

### Alignment modes

#### Progress alignment

Compare:

\[
r=\beta/\beta_{\max}
\]

with:

\[
r=s.
\]

Use this for simple animation and storytelling.

#### Entropy alignment

Compare frames with similar distribution entropy:

\[
S=-\sum_pP(p)\log P(p).
\]

Use this for a fairer comparison of concentration level.

### Purpose

Show whether QA is merely following a thermal path distribution or doing something dynamically different.

### Do not imply

- \(\beta\) and \(s\) are physically the same parameter.
- Similar entropy means identical mechanisms.

---

## 7. Top-k path probability stream

### Data source

Path probabilities from Soft-DP or QA.

### Y value

Soft-DP:

\[
P_\beta(p_i).
\]

QA:

\[
|\psi_{p_i}(s)|^2.
\]

### Which paths to show

Choose a stable set of paths:

- gold path,
- decoy path,
- second-best path,
- a few other low-energy paths,
- optionally one medium-energy reference path.

### Purpose

Show probability competition between complete solutions.

### Expected contrast

Soft-DP path ratios are determined only by energy:

\[
\frac{P_\beta(p_i)}{P_\beta(p_j)}=e^{-\beta(E_i-E_j)}.
\]

QA path probabilities can be non-monotonic because amplitudes evolve with phases and driver-induced mixing.

### Do not imply

- Top-k paths are the only paths carrying probability.
- Non-monotonic QA curves alone prove quantum advantage.

---

## 8. Energy / entropy / success dashboard

### Curves shared by Soft-DP and QA

Expected energy:

\[
\mathbb E[E]=\sum_pP(p)E(p).
\]

Residual energy:

\[
E_{\text{res}}=\mathbb E[E]-E^*.
\]

Success probability:

\[
P_{\text{success}}=\sum_{p:E(p)=E^*}P(p).
\]

Entropy:

\[
S=-\sum_pP(p)\log P(p).
\]

Effective number of paths:

\[
N_{\text{eff}}=e^S.
\]

### QA-only curve

Spectral gap:

\[
\Delta(s)=\lambda_1(s)-\lambda_0(s).
\]

### Purpose

Give global diagnostics beyond the heatmaps.

### Do not imply

- Entropy decrease is always monotonic for QA.
- A small gap is the only reason QA can struggle.
- Success probability from a tiny toy system predicts hardware behavior.

---

## 9. Soft-DP edge flow on the original DAG

### Data source

Soft-DP path probabilities.

### Edge heat

For edge \((\ell,u)\to(\ell+1,v)\):

\[
F^{\text{soft}}_{\ell,u,v}(\beta)
=\sum_{p:p_\ell=u,\,p_{\ell+1}=v}P_\beta(p).
\]

### Meaning

A thick edge means:

> Many probable thermal paths use this transition.

### Purpose

This is the cleanest classical probability-flow picture.

### Do not imply

- Hard DP stores this flow.
- QA current is the same kind of object.

---

## 10. QA path-space current

### Data source

QA amplitudes and instantaneous Hamiltonian.

### Graph

This is not the original DAG.

- Node = complete path.
- Edge = two paths differ by one local choice.

### Current

\[
J_{q\to p}(s)=2\operatorname{Im}\left[\psi_p^*(s)H_{pq}(s)\psi_q(s)\right].
\]

### Meaning

A signed arrow indicates instantaneous probability current between complete paths.

### Purpose

Show that QA moves through configuration space, not through the original DP graph.

### Do not imply

- Current is always nonnegative.
- Current follows the direction of the original DAG.
- Current is the same as probability mass or edge occupancy.

### Practical plotting notes

For readability:

- show only top probability paths,
- threshold tiny currents,
- use fixed layout for animation,
- label gold and decoy paths.

---

## 11. QA occupancy projected onto original DAG

### Data source

QA path probabilities.

### Edge occupancy

\[
O^{\text{QA}}_{\ell,u,v}(s)
=\sum_{p:p_\ell=u,\,p_{\ell+1}=v}|\psi_p(s)|^2.
\]

### Meaning

A thick edge means:

> Measured paths are likely to use this original graph edge.

### Purpose

This can be compared directly with Soft-DP edge marginals.

### Important distinction

Occupancy is not current.

- Occupancy is unsigned probability mass projected onto original edges.
- Current is signed instantaneous motion in path space.

---

## 12. Suggested notebook figure order

Use this order in the MVP notebook:

1. Problem graph with gold and decoy paths.
2. Hard DP value heatmap and backpointers.
3. Soft-DP marginal heatmap animation.
4. QA marginal heatmap animation.
5. Soft-DP vs QA side-by-side by progress.
6. Soft-DP vs QA side-by-side by entropy.
7. Top-k path probability streams.
8. Energy / entropy / success dashboard.
9. QA spectral gap.
10. Soft-DP edge flow.
11. QA path-space current.
12. Final summary panel.

This order moves from familiar DP to probabilistic classical bridge to quantum proxy.

---

## 13. Visual integrity rules

1. Label every heatmap by quantity, not just by method.
2. Never compare DP value heat directly to probability heat without explanation.
3. Use the phrase “projection” for Soft-DP and QA cell heatmaps.
4. Keep source and sink out of the main heatmap.
5. Keep gold path and decoy path labels consistent across plots.
6. If using normalized values, state the normalization.
7. Do not use QA current arrows on the original problem graph unless explicitly labeled as projected occupancy instead.
8. Distinguish progress alignment from entropy alignment.
9. Keep toy problem size small enough that all paths can be inspected.
10. When a plot is pedagogical rather than diagnostic, say so.

---

## 14. Minimal API expected by visualizers

Visualizers should consume `SolverTrace` and `Frame` objects.

Expected fields:

```python
Frame.progress       # float
Frame.label          # str
Frame.cell_heat      # np.ndarray or None
Frame.value_heat     # np.ndarray or None
Frame.path_probs     # np.ndarray or None
Frame.amplitudes     # np.ndarray or None
Frame.edge_heat      # dict or None
Frame.observables    # dict[str, float]
```

Visualizers should not recompute solver internals unless the computation is explicitly a plotting transformation, such as selecting top-k paths.

---

## 15. References

- `math_overview.md` for formulas and invariants.
- `qa_proxy_notes.md` for quantum-model boundaries.
- D-Wave QA introduction: https://docs.dwavequantum.com/en/latest/quantum_research/quantum_annealing_intro.html
