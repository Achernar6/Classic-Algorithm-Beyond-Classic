# Project Philosophy

This document holds the longer project philosophy and scientific guardrails for Pathspace Lab. The roadmap keeps only a short operational summary.

## Teaching Goal

The MVP is not a quantum advantage demo. It is a visual and mathematical teaching tool.

The central claim:

> Hard DP compresses histories into local values. Soft-DP assigns classical probabilities to complete paths. Feasible-subspace QA evolves complex amplitudes over complete paths. All three can be projected onto the same DP canvas, but their hidden dynamics are different.

The first supported problem is deliberately small: a layered DAG shortest-path problem where a complete solution chooses one node per visible layer. The point is not scale. The point is a clear comparison among three mechanisms.

## Engineering Philosophy

Keep implementation logic outside the notebook.

The notebook should:

- introduce the problem,
- call functions from `src/`,
- display figures,
- explain what the figures mean.

The notebook should not:

- define large classes,
- contain solver internals,
- contain long plotting utilities,
- become the single source of truth.

The source of truth should remain:

1. `src/` for reusable implementation.
2. `tests/` for correctness expectations.
3. `notebooks/paired/*.py` for notebook narrative and cell order.
4. `.ipynb` for the user-facing notebook artifact.

## Notebook-First Rule

The notebook is not delayed until the end of the MVP. It grows issue by issue.

Each issue must add at least one notebook-visible artifact unless explicitly exempted:

- a new section,
- a new runnable cell,
- a diagnostic figure,
- a printed sanity check,
- or a short narrative placeholder that keeps the notebook runnable.

The detailed human acceptance checklist lives in `docs/notebook_acceptance_guide.md`.

## Scientific Integrity Rules

The MVP quantum model must be described as:

> a feasible-subspace quantum annealing proxy.

It must not be described as:

> a direct simulation of D-Wave hardware,
> a proof of quantum advantage,
> a generic QUBO transverse-field annealer.

The model preserves the core annealing structure:

\[
H(s)=A(s)H_D+B(s)H_P
\]

where:

- \(H_D\) has an easy known ground state,
- \(H_P\) encodes path energy and has optimal paths as ground states,
- \(A(s)\) decreases,
- \(B(s)\) increases,
- the state evolves according to a time-dependent Hamiltonian.

The model differs from standard transverse-field Ising QA because the Hilbert space basis is feasible paths rather than all bitstrings, and the driver is a configuration-graph Laplacian rather than \(-\sum_i X_i\).

## Design Taste

The MVP should feel like a clear, inspectable teaching machine:

- small enough to enumerate,
- mathematical enough to audit,
- visual enough to build intuition,
- bounded enough not to overclaim.

The heatmaps share a coordinate system, not a mechanism. That sentence should remain close to the center of the project.
