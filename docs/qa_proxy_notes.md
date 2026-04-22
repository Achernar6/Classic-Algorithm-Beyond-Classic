# qa_proxy_notes.md

# Feasible-subspace QA proxy notes

This document explains what the MVP quantum model is, what it preserves from quantum annealing, and what it deliberately does not claim.

The goal is to help readers with a computer science background understand the quantum side without pretending that the MVP is a hardware simulator.

---

## 1. One-sentence description

The MVP implements a **feasible-subspace quantum annealing proxy**: a continuous Hamiltonian evolution from a uniform superposition over valid paths to a diagonal energy function whose ground states are optimal paths.

It is a teaching model for QA-like dynamics over DP solutions.

It is not a direct simulation of a D-Wave QPU.

---

## 2. What quantum annealing tries to do

Quantum annealing encodes an optimization problem into an energy function. The best solution is the lowest-energy state.

The general structure is:

\[
H(s)=A(s)H_{\text{initial}}+B(s)H_{\text{problem}},\quad s\in[0,1].
\]

At the start:

- \(A(s)\) is large,
- \(B(s)\) is small,
- the ground state of \(H_{\text{initial}}\) is easy to prepare.

At the end:

- \(A(s)\) is small,
- \(B(s)\) is large,
- the ground states of \(H_{\text{problem}}\) are the desired solutions.

D-Wave describes QA in this same high-level form: the system begins in the ground state of an initial Hamiltonian, then the problem Hamiltonian is introduced while the initial Hamiltonian is reduced. It also uses an anneal fraction \(s\in[0,1]\) for the annealing schedule.

References:

- https://docs.dwavequantum.com/en/latest/quantum_research/quantum_annealing_intro.html
- https://docs.dwavequantum.com/en/latest/quantum_research/annealing.html

---

## 3. What the MVP preserves

The MVP preserves the conceptual QA kernel:

| QA concept | MVP version |
|---|---|
| Easy initial ground state | Uniform superposition over feasible paths |
| Problem ground state | Minimum-energy path or paths |
| Continuous interpolation | \(H(s)=A(s)H_D+B(s)H_P\) |
| Anneal progress | \(s=t/T\) |
| Quantum state | Complex amplitudes over feasible paths |
| Measurement distribution | \(|\psi_p(s)|^2\) |
| Spectral gap | Gap of instantaneous \(H(s)\) |

This is enough to show why QA is not just recursive search and not just a thermal distribution.

---

## 4. What the MVP changes

Standard transverse-field Ising QA usually uses bitstring basis states:

\[
|z_1,z_2,\dots,z_n\rangle.
\]

A common initial driver is:

\[
-\sum_i X_i,
\]

and a common problem Hamiltonian uses \(Z_i\) and \(Z_iZ_j\) terms.

The MVP does not use that representation. Instead:

| Standard transverse-field Ising QA | MVP feasible-subspace QA |
|---|---|
| Basis = all bitstrings | Basis = valid complete paths |
| Invalid assignments exist and need penalties | Every basis state is feasible |
| Driver often \(-\sum_i X_i\) | Driver is a configuration-graph Laplacian |
| Natural fit for QUBO/Ising hardware | Natural fit for DP/path visualization |
| More hardware-adjacent | More pedagogically transparent |

The MVP is therefore a proxy, not a hardware-equivalent model.

---

## 5. Why use a feasible path basis?

A path-DP problem has a natural set of complete valid solutions:

\[
\mathcal P=\{p_1,p_2,\dots,p_N\}.
\]

Using these paths as basis states gives three benefits.

### 5.1 All states are valid

There is no need for one-hot constraints or penalty terms. This keeps the first notebook focused on mechanism rather than QUBO bookkeeping.

### 5.2 The initial distribution is exactly uniform over valid solutions

This matches the desired teaching intuition:

> Start with every valid path equally possible, then watch probability concentrate.

### 5.3 The distribution can be projected back onto the DP canvas

For each cell \((\ell,v)\):

\[
M^{\text{QA}}_{\ell,v}(s)=\sum_{p:p_\ell=v}|\psi_p(s)|^2.
\]

This lets the notebook show QA on the same layer-node heatmap as Soft-DP.

---

## 6. Why use a Laplacian driver?

The MVP builds a configuration graph:

- node = one feasible path,
- edge = two paths differ by one local choice.

Let its adjacency matrix be \(A\) and degree matrix be \(D\). The driver is:

\[
H_D=L_{\text{cfg}}=D-A.
\]

For a connected undirected graph, the graph Laplacian has the constant vector as a ground state:

\[
|\psi_0\rangle=\frac{1}{\sqrt N}(1,1,\dots,1)^T.
\]

That gives a uniform starting state over feasible paths.

### Why not just use \(-A\)?

If the configuration graph is regular, \(-A\) has a uniform ground state. If the graph is not regular, the ground state can overweight high-degree paths.

The Laplacian is more robust for a teaching model because it makes the uniform feasible starting state explicit.

### Is the Laplacian driver still “quantum”?

Yes, in the limited sense that it is part of a Hermitian Hamiltonian driving coherent amplitude evolution. But it is not the same as the hardware-oriented transverse-field driver.

Use this phrasing:

> We use a constraint-preserving Laplacian driver to create a clean feasible-subspace QA proxy.

---

## 7. Problem Hamiltonian

The problem Hamiltonian is diagonal:

\[
H_P=\operatorname{diag}(E(p_1),\dots,E(p_N)).
\]

This means each path has an energy, and no path mixes with another under \(H_P\) alone.

The optimal paths are ground states:

\[
\arg\min_p E(p)=\text{ground states of }H_P.
\]

---

## 8. Evolution and measurement

At each small time step:

\[
|\psi(t+\Delta t)\rangle\approx e^{-iH(s_k)\Delta t}|\psi(t)\rangle.
\]

The vector \(\psi\) contains complex amplitudes, not probabilities. Probabilities come from squared magnitudes:

\[
P(p_i)=|\psi_i|^2.
\]

A useful computer-science analogy:

- Soft-DP stores nonnegative weights over paths.
- QA stores complex amplitudes over paths.
- Complex amplitudes can interfere; probabilities are only visible after taking squared magnitudes.

This is why QA can show non-monotonic path probabilities even when low-energy paths are ultimately preferred.

---

## 9. How this differs from Soft-DP

Soft-DP uses:

\[
P_\beta(p)\propto e^{-\beta E(p)}.
\]

It is determined only by the final path energy and inverse temperature.

QA uses:

\[
|\psi_p(s)|^2,
\]

where \(\psi(s)\) depends on:

- the driver,
- the schedule,
- total anneal time,
- spectral gaps,
- phases and interference.

So Soft-DP is the classical thermal baseline. QA is a coherent dynamical process.

---

## 10. Allowed claims

Use these claims:

- The MVP implements a feasible-subspace QA proxy.
- It preserves the core Hamiltonian interpolation idea of QA.
- It shows amplitude evolution over complete feasible paths.
- It is useful for teaching how QA differs from DP and classical thermal reweighting.
- It is mathematically exact for the toy Hamiltonian it defines.

---

## 11. Disallowed claims

Do not claim:

- This simulates D-Wave hardware.
- This demonstrates quantum speedup.
- This is a generic QUBO transverse-field annealer.
- The QA current flows directly along the original DP graph.
- The final state is guaranteed to be optimal for any finite runtime.
- Soft-DP and QA are the same process with different parameter names.

---

## 12. Recommended wording for README and notebook

Use:

> This notebook implements a feasible-subspace quantum annealing proxy. The basis states are valid paths, the initial driver has a uniform feasible ground state, and the problem Hamiltonian has optimal paths as ground states. This keeps the conceptual annealing kernel visible while avoiding QUBO penalty machinery in the MVP.

Also use:

> The shared heatmap is a projection. DP values, Soft-DP probabilities, and QA amplitudes do not live in the same hidden space.

---

## 13. Tests that protect the QA proxy

The implementation should test:

1. \(H_P\) is diagonal.
2. \(H_D\) is symmetric / Hermitian.
3. \(H_D\mathbf 1=0\) for a connected configuration graph.
4. The uniform vector is normalized.
5. The initial probability over paths is uniform.
6. The state norm remains close to one during evolution.
7. The final problem Hamiltonian ground energy equals the classical optimum.
8. QA cell marginals sum to one per layer.
9. Probability current is only computed from a Hermitian Hamiltonian and normalized state.

---

## 14. Extension path toward more realistic QA

After the MVP, more hardware-adjacent models can be added as separate extensions:

1. QUBO encoding of the layered path problem.
2. Penalty terms for one-hot constraints.
3. Transverse-field bitstring QA simulation.
4. Feasible mass and illegal-state mass plots.
5. OpenJij SA/SQA sampler comparison.
6. Qiskit gate-model Hamiltonian simulation appendix.
7. Noisy or open-system dynamics.

These should be extensions, not replacements for the clean MVP narrative.

---

## 15. References

- D-Wave documentation, “What is Quantum Annealing?”: https://docs.dwavequantum.com/en/latest/quantum_research/quantum_annealing_intro.html
- D-Wave documentation, “Annealing Implementation and Controls”: https://docs.dwavequantum.com/en/latest/quantum_research/annealing.html
- SciPy `expm_multiply`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.expm_multiply.html
- SciPy `eigsh`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html
