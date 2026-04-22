# math_overview.md

# Pathspace Lab mathematical overview

This document is the mathematical source of truth for the MVP. It defines the objects used by the code, the quantities shown in the notebook, and the invariants that tests should protect.

The intended reader is a computer science student who knows dynamic programming and graphs, but may not have seen much quantum computation.

---

## 1. Three spaces, not one space

Pathspace Lab compares three mechanisms on the same small problem. The main source of confusion is that these mechanisms live in different spaces.

| Space | Nodes / elements | Used by | Can have cycles? | Role |
|---|---|---|---|---|
| Original problem graph | Problem states, such as layer-node pairs | DP, visualization | In MVP, no. In later graph extensions, yes | User-facing input |
| DP computation DAG | Subproblem states and dependency edges | Hard DP, Soft-DP | No for a single forward DP pass | Shows classical information propagation |
| Path / configuration space | Complete feasible paths | Soft-DP, QA | Usually yes | Shows distributions or amplitudes over complete solutions |

The MVP uses a layered DAG, so the original problem graph and DP computation graph are almost the same. Later extensions may separate them more clearly, for example by turning a cyclic graph into a time-expanded DAG.

---

## 2. MVP problem: layered DAG path problem

The first supported problem is a layered directed acyclic graph.

### Parameters

| Symbol | Code name | Meaning |
|---|---|---|
| `L` | `problem.L` | Number of visible layers |
| `W` | `problem.W` | Number of nodes per layer |
| `ell` or `l` | layer index | Layer, from `0` to `L - 1` |
| `v`, `u` | node index | Node choice inside a layer, from `0` to `W - 1` |
| `c[ell, v]` | `node_cost[ell, v]` | Cost of selecting node `v` in layer `ell` |
| `e[ell, u, v]` | `edge_cost[ell, u, v]` | Cost of transitioning from node `u` at layer `ell` to node `v` at layer `ell + 1` |
| `p` | `path` | One complete feasible path |
| `E(p)` | `path_energy(path)` | Total path energy / cost |

A visible path chooses exactly one node per layer:

\[
p=(v_0,v_1,\dots,v_{L-1}).
\]

The path energy is:

\[
E(p)=\sum_{\ell=0}^{L-1} c_{\ell,v_\ell}
+\sum_{\ell=0}^{L-2} e_{\ell,v_\ell,v_{\ell+1}}.
\]

The number of feasible visible paths is:

\[
|\mathcal P| = W^L.
\]

### Source and sink

Implementation may use artificial source and sink states:

```text
source -> layer 0 -> layer 1 -> ... -> layer L-1 -> sink
```

The source and sink are useful for graph algorithms, but they do not appear in the main heatmap.

Visible cells are only:

\[
(\ell,v), \quad 0\le \ell < L,\quad 0\le v < W.
\]

### Planted gold path and decoy path

The MVP generator should create a small instance with narrative structure:

- **Gold path**: the globally optimal path. It may not look best in the early layers.
- **Decoy path**: a locally attractive path. It should look cheap early but become expensive later.

This is not a mathematical requirement for the solvers. It is a teaching device. It makes the top-k probability streams and heatmaps more revealing.

The generator should be deterministic under a seed. Tests should not depend on the exact visual drama of the instance, but the notebook should use an instance where the gold and decoy paths are visible.

---

## 3. Hard DP

Hard DP computes the minimum cost to reach each state.

For a DAG edge \(u\to v\) with weight \(w(u,v)\), the recurrence is:

\[
D(v)=\min_{u\to v}\left[D(u)+w(u,v)\right].
\]

with:

\[
D(\text{source})=0.
\]

The best predecessor is:

\[
\operatorname{bp}(v)=\arg\min_{u\to v}\left[D(u)+w(u,v)\right].
\]

The final optimal path is recovered by tracing back from the sink through `bp`.

### DP values are not probabilities

A DP value heatmap is not a probability heatmap. It stores a compressed summary of partial histories:

\[
D(\ell,v)=\text{best cost of any partial path ending at }(\ell,v).
\]

For plotting, it is okay to display a normalized "goodness" score, such as:

\[
G(\ell,v)=\frac{\max D-D(\ell,v)}{\max D-\min D+\epsilon}.
\]

But the notebook must label this as a value-derived visualization, not a distribution.

---

## 4. Soft-DP / classical thermal path distribution

Soft-DP turns the finite set of feasible paths into a Boltzmann distribution.

For inverse temperature \(\beta\ge 0\):

\[
P_\beta(p)=\frac{\exp[-\beta E(p)]}{Z_\beta},
\]

where:

\[
Z_\beta=\sum_{p\in\mathcal P}\exp[-\beta E(p)].
\]

At \(\beta=0\), all paths are equally likely:

\[
P_0(p)=\frac{1}{|\mathcal P|}.
\]

As \(\beta\to\infty\), probability concentrates on minimum-energy paths.

### Numerical stability

Use log-sum-exp:

\[
\log P_\beta(p)=-\beta E(p)-\log Z_\beta.
\]

In code:

```python
logw = -beta * energies
logZ = logsumexp(logw)
path_probs = np.exp(logw - logZ)
```

### Cell marginals

The shared heatmap quantity for Soft-DP is the cell marginal:

\[
M^{\text{soft}}_{\ell,v}(\beta)
=\sum_{p\in\mathcal P:\,p_\ell=v} P_\beta(p).
\]

It means:

> Under the classical thermal distribution, how likely is the final path to use cell \((\ell,v)\)?

Since every path visits exactly one visible cell per layer:

\[
\sum_{\ell=0}^{L-1}\sum_{v=0}^{W-1}M^{\text{soft}}_{\ell,v}(\beta)=L.
\]

For each layer separately:

\[
\sum_v M^{\text{soft}}_{\ell,v}(\beta)=1.
\]

### Edge marginals

For a visible edge \((\ell,u)\to(\ell+1,v)\):

\[
F^{\text{soft}}_{\ell,u,v}(\beta)
=\sum_{p:\,p_\ell=u,\,p_{\ell+1}=v}P_\beta(p).
\]

This is a nonnegative classical probability flow through the problem graph.

---

## 5. Feasible-subspace quantum annealing

The MVP quantum model uses complete feasible paths as basis states.

### Hilbert basis

Let:

\[
\mathcal P=\{p_1,p_2,\dots,p_N\}
\]

be all feasible paths. Each path becomes one basis vector:

\[
|p_i\rangle.
\]

A quantum state is a complex vector:

\[
|\psi(t)\rangle=\sum_{i=1}^{N}\psi_i(t)|p_i\rangle.
\]

Measurement probability of path \(p_i\):

\[
P_t(p_i)=|\psi_i(t)|^2.
\]

### Problem Hamiltonian

The problem Hamiltonian is diagonal in the path basis:

\[
H_P=\sum_i E(p_i)|p_i\rangle\langle p_i|.
\]

Matrix form:

\[
H_P=\operatorname{diag}(E(p_1),\dots,E(p_N)).
\]

The ground states of \(H_P\) are the optimal paths.

### Configuration graph

Define a configuration graph \(G_{\text{cfg}}\):

- node = one complete path,
- edge = two paths differ by one local choice, usually one layer's selected node.

For two paths:

\[
p=(v_0,\dots,v_{L-1}),\quad q=(u_0,\dots,u_{L-1}),
\]

connect them when their Hamming distance over layers is one:

\[
|\{\ell:v_\ell\ne u_\ell\}|=1.
\]

### Driver Hamiltonian

Use the graph Laplacian of the configuration graph:

\[
H_D=L_{\text{cfg}}=D-A,
\]

where:

- \(A\) is adjacency,
- \(D\) is diagonal degree matrix.

If \(G_{\text{cfg}}\) is connected, the uniform vector is a ground state of the Laplacian:

\[
|\psi(0)\rangle=\frac{1}{\sqrt N}\sum_i |p_i\rangle.
\]

This is why the MVP starts with exactly uniform probability over feasible paths.

### Annealing Hamiltonian

The time-dependent Hamiltonian is:

\[
H(s)=A(s)H_D+B(s)H_P,
\]

where \(s\in[0,1]\) is anneal progress.

MVP schedule:

\[
A(s)=1-s,\quad B(s)=s.
\]

At \(s=0\):

\[
H(0)=H_D.
\]

At \(s=1\):

\[
H(1)=H_P.
\]

### Time evolution

The state obeys:

\[
i\frac{d}{dt}|\psi(t)\rangle=H(t)|\psi(t)\rangle.
\]

The simulation uses small steps:

\[
|\psi(t+\Delta t)\rangle\approx \exp[-iH(s_k)\Delta t]|\psi(t)\rangle.
\]

The state norm should remain one:

\[
\sum_i|\psi_i(t)|^2=1.
\]

### QA cell marginals

The shared heatmap quantity for QA is:

\[
M^{\text{QA}}_{\ell,v}(s)
=\sum_{p_i:\,p_{i,\ell}=v}|\psi_i(s)|^2.
\]

It means:

> If we measured the current quantum state as a path, how likely would the observed path use cell \((\ell,v)\)?

It has the same normalization as Soft-DP cell marginals:

\[
\sum_v M^{\text{QA}}_{\ell,v}(s)=1,
\]

and:

\[
\sum_{\ell,v}M^{\text{QA}}_{\ell,v}(s)=L.
\]

---

## 6. Common observables

For a path distribution \(P(p)\), used by both Soft-DP and QA after converting amplitudes to probabilities:

### Expected energy

\[
\mathbb E[E]=\sum_pP(p)E(p).
\]

For QA this is also:

\[
\langle H_P\rangle=\sum_i|\psi_i|^2E(p_i).
\]

### Residual energy

\[
E_{\text{res}}=\mathbb E[E]-E^*,
\]

where:

\[
E^*=\min_pE(p).
\]

### Success probability

\[
P_{\text{success}}=\sum_{p:E(p)=E^*}P(p).
\]

If the optimum is unique:

\[
P_{\text{success}}=P(p^*).
\]

### Entropy

\[
S=-\sum_pP(p)\log P(p).
\]

Use a small epsilon in code to avoid \(\log 0\).

### Effective number of paths

\[
N_{\text{eff}}=e^S.
\]

This is an intuitive count of how many paths still carry substantial probability.

---

## 7. QA-specific observables

### Spectral gap

For the instantaneous Hamiltonian \(H(s)\), let:

\[
\lambda_0(s)\le \lambda_1(s)\le \dots
\]

Then:

\[
\Delta(s)=\lambda_1(s)-\lambda_0(s).
\]

The minimum gap is:

\[
\Delta_{\min}=\min_s\Delta(s).
\]

A small gap is a warning sign: adiabatic following is harder near that point.

### Probability current

For QA, probability motion is not ordinary nonnegative flow over the original DP graph. It is a signed current over the configuration graph.

For basis states \(p\) and \(q\):

\[
J_{q\to p}(s)=2\operatorname{Im}\left[\psi_p^*(s)H_{pq}(s)\psi_q(s)\right].
\]

Interpretation:

- positive value: probability current from \(q\) toward \(p\),
- negative value: current in the opposite direction,
- zero: no instantaneous current along that edge.

This is not the same as edge occupancy.

---

## 8. Shape and normalization conventions

### Heatmap shape

Use:

```python
cell_heat.shape == (L, W)
```

Indexing:

```python
cell_heat[ell, v]
```

Plotting may transpose to place layer on the horizontal axis and node on the vertical axis.

### Path probabilities

Soft-DP:

```python
path_probs.shape == (num_paths,)
path_probs.sum() == 1
```

QA:

```python
amplitudes.shape == (num_paths,)
np.sum(np.abs(amplitudes) ** 2) == 1
```

### Marginal sums

For both Soft-DP and QA:

```python
cell_heat.sum(axis=1) == np.ones(L)
cell_heat.sum() == L
```

### Source and sink

Source and sink are allowed inside graph paths, but should be omitted from visible heatmaps and visible layer marginals.

---

## 9. Code-to-math map

| Math object | Code location / likely name |
|---|---|
| \(L,W\) | `LayeredDAGProblem.L`, `LayeredDAGProblem.W` |
| \(c_{\ell,v}\) | `problem.node_cost[ell, v]` |
| \(e_{\ell,u,v}\) | `problem.edge_cost[ell, u, v]` |
| \(p\) | `Path`, usually tuple of states |
| \(E(p)\) | `problem.path_energy(path)` |
| \(D(v)\) | `solve_hard_dp(...).frames[*].value_heat` or internal distance map |
| \(P_\beta(p)\) | `Frame.path_probs` in Soft-DP trace |
| \(M_{\ell,v}\) | `Frame.cell_heat` |
| \(H_P\) | `build_problem_hamiltonian` |
| \(H_D\) | `build_laplacian_driver` |
| \(\psi\) | `Frame.amplitudes` in QA trace |
| \(\Delta(s)\) | `Frame.observables["gap"]` or separate gap trace |

---

## 10. Core invariants for tests

The test suite should protect these invariants:

1. `LayeredDAGProblem` graph is acyclic.
2. Number of paths is \(W^L\).
3. Every path visits exactly one visible cell per layer.
4. `path_energy` matches the explicit formula.
5. Hard DP final value equals the minimum enumerated path energy.
6. At \(\beta=0\), Soft-DP path probabilities are uniform.
7. Soft-DP probabilities sum to one.
8. Soft-DP cell marginals sum to one per layer and \(L\) globally.
9. \(H_P\) is diagonal.
10. \(H_D\) is symmetric / Hermitian and positive semidefinite for the Laplacian driver.
11. The uniform vector is a ground state of \(H_D\) when the configuration graph is connected.
12. QA amplitudes remain normalized within numerical tolerance.
13. QA path probabilities sum to one.
14. QA cell marginals sum to one per layer and \(L\) globally.
15. QA final problem Hamiltonian ground energy equals the classical optimum.

---

## 11. References

- D-Wave documentation, “What is Quantum Annealing?”: https://docs.dwavequantum.com/en/latest/quantum_research/quantum_annealing_intro.html
- D-Wave documentation, “Annealing Implementation and Controls”: https://docs.dwavequantum.com/en/latest/quantum_research/annealing.html
- SciPy `expm_multiply`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.expm_multiply.html
- SciPy `eigsh`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html
- NetworkX `topological_sort`: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html
