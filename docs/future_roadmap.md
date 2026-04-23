# Future Roadmap Beyond MVP

This document collects future directions that should not distract the MVP roadmap. The MVP remains focused on one clean layered DAG notebook comparing Hard DP, Soft-DP, and feasible-subspace QA.

## Phase 1: Add Second Path-DAG Problem

Candidates:

- grid path,
- edit-distance-style alignment,
- sequence alignment.

Goal:

Show that the pipeline is not hardcoded to layered Viterbi paths.

## Phase 2: Add Time-Expanded Cyclic Graph Support

Original graphs may have cycles. Lift them into a DAG:

\[
(t,v)
\]

This supports:

- fixed-horizon graph walks,
- Bellman-Ford-style shortest paths,
- finite-horizon MDPs.

## Phase 3: Add QUBO Transverse-Field QA Extension

Add optional QUBO encoding with one-hot variables and penalty terms.

Visualize:

- feasible mass,
- invalid state mass,
- penalty energy,
- comparison with feasible-subspace QA.

## Phase 4: Add OpenJij SA/SQA Sampler Comparison

Use samplers for final distribution and benchmark-style plots.

Visualize:

- final energy histogram,
- success probability,
- residual energy.

## Phase 5: Add Qiskit Gate-Model Appendix

Show Hamiltonian simulation and Trotterized evolution as a gate-model counterpart.

## Phase 6: Add Hypergraph DP

Support DP where one subproblem depends on multiple subproblems:

\[
u \to (v_1, v_2, \dots, v_k)
\]

Needed for:

- matrix-chain multiplication,
- CKY parsing,
- interval DP,
- tree DP.

## Phase 7: Add Open-System QA Experiments

Explore:

- thermal effects,
- dephasing,
- Lindblad dynamics,
- freeze-out,
- schedule pauses,
- reverse annealing.
