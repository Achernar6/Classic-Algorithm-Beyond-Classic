# DEVELOPMENT_ROADMAP.md

# Pathspace Lab MVP Development Roadmap

This roadmap is designed for incremental development with a human reviewer and an AI coding agent. Each issue includes goals, todo items, non-goals, implementation notes, acceptance criteria for humans, acceptance criteria for AI, and validation expectations.

The MVP builds one clean, runnable notebook that compares:

1. **Hard DP** as deterministic min-plus message passing.
2. **Soft-DP** as a classical thermal distribution over feasible paths.
3. **Feasible-subspace Quantum Annealing** as continuous Hamiltonian evolution over feasible complete paths.

The first supported problem is a **layered DAG shortest-path / Viterbi-style path problem**. A solution is a complete path through the layers. All three methods are projected onto the same layer-node visualization canvas.

---

## 0. Required companion documents

These documents are part of the MVP spec, not optional essays.

```text
docs/math_overview.md
docs/qa_proxy_notes.md
docs/visualization_guide.md
```

Use them as follows:

| Document | Purpose | When to update |
|---|---|---|
| `docs/math_overview.md` | Defines variables, formulas, shape conventions, and invariants | Any time a mathematical object, solver formula, observable, or normalization changes |
| `docs/qa_proxy_notes.md` | Defines what the feasible-subspace QA proxy claims and does not claim | Any time the QA Hamiltonian, driver, schedule, simulation method, or quantum wording changes |
| `docs/visualization_guide.md` | Defines what every plot means and what it must not imply | Any time a visualization, axis, heat value, comparison mode, or plot label changes |

### Spec synchronization rule

If an implementation PR changes the main logic, it must update the corresponding spec document in the same PR.

Examples:

- Change `path_energy` formula -> update `docs/math_overview.md`.
- Change Laplacian driver -> update `docs/qa_proxy_notes.md`.
- Change heatmap quantity or normalization -> update `docs/visualization_guide.md`.
- Add a new plot -> update `docs/visualization_guide.md`.
- Change notebook narrative claims -> check `docs/qa_proxy_notes.md` for consistency.

This rule is the project’s scientific lint roller. Use it often. 🧹

---

## 1. Guiding principles

### 1.1 Project philosophy

The MVP is not a quantum advantage demo. It is a visual and mathematical teaching tool.

Central claim:

> Hard DP compresses histories into local values. Soft-DP assigns classical probabilities to complete paths. Feasible-subspace QA evolves complex amplitudes over complete paths. All three can be projected onto the same DP canvas, but their hidden dynamics are different.

This claim must remain consistent with:

- `docs/math_overview.md`
- `docs/qa_proxy_notes.md`
- `docs/visualization_guide.md`

### 1.2 Engineering philosophy

Keep implementation logic outside the notebook.

The notebook should:

- introduce the problem,
- call functions from `src/`,
- display figures,
- explain what the figures mean,
- point readers to the three spec docs for details.

The notebook should not:

- define large classes,
- contain solver internals,
- contain long plotting utilities,
- become the source of truth.

### 1.3 Scientific integrity rules

The MVP quantum model must be described as:

> a feasible-subspace quantum annealing proxy.

It must not be described as:

- a direct simulation of D-Wave hardware,
- a proof of quantum advantage,
- a generic QUBO transverse-field annealer.

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

The model differs from standard transverse-field Ising QA because the Hilbert-space basis is feasible paths rather than all bitstrings, and the driver is a configuration-graph Laplacian rather than \(-\sum_i X_i\).

Reference: `docs/qa_proxy_notes.md`.

---

## 2. Project linking strategy

### 2.1 Recommended structure

Use a standard Python package under `src/`, with a paired notebook workflow.

```text
pathspace-lab/
  README.md
  DEVELOPMENT_ROADMAP.md
  pyproject.toml
  .gitignore
  .pre-commit-config.yaml             # optional
  jupytext.toml                       # optional but recommended
  docs/
    math_overview.md
    qa_proxy_notes.md
    visualization_guide.md
  notebooks/
    01_dp_softdp_qa_layered_path.ipynb
    paired/
      01_dp_softdp_qa_layered_path.py # paired script, percent format
  src/
    pathspace_lab/
      __init__.py
      problems/
        __init__.py
        base.py
        layered_dag.py
      solvers/
        __init__.py
        hard_dp.py
        soft_dp.py
        qa_feasible.py
      math/
        __init__.py
        observables.py
        schedules.py
        hamiltonians.py
        normalization.py
      viz/
        __init__.py
        problem_plot.py
        heatmaps.py
        streams.py
        dashboard.py
        currents.py
      utils/
        __init__.py
        typing.py
        paths.py
        logging.py
  tests/
    conftest.py
    test_layered_dag.py
    test_hard_dp.py
    test_soft_dp.py
    test_qa_feasible.py
    test_observables.py
  scripts/
    sync_notebooks.sh
    execute_notebook.sh
```

### 2.2 Notebook pairing policy

Use Jupytext pairing:

- `.ipynb` is the user-facing notebook.
- `.py:percent` is the diff-friendly paired source.

Suggested files:

```text
notebooks/01_dp_softdp_qa_layered_path.ipynb
notebooks/paired/01_dp_softdp_qa_layered_path.py
```

Notebook pairing keeps version-control diffs readable while still letting users run a normal Jupyter notebook. Jupytext documents the percent format as scripts where notebook cells are delimited by `# %%`.

Reference: https://jupytext.readthedocs.io/en/latest/formats-scripts.html

### 2.3 Source-of-truth policy

The source of truth is:

1. `docs/*.md` for math, QA claims, and visualization semantics.
2. `src/` for reusable implementation.
3. `tests/` for correctness expectations.
4. `notebooks/paired/*.py` for notebook narrative and cell order.
5. `.ipynb` for the rendered notebook artifact.

The paired `.py` file should be reviewed in PRs. The `.ipynb` can be regenerated or executed as a CI artifact.

---

## 3. Development workflow for humans and AI agents

### 3.1 Branch naming

Use one branch per issue:

```text
issue-00-project-scaffold
issue-01-core-interfaces
issue-02-layered-dag-problem
issue-03-observables
issue-04-hard-dp
issue-05-soft-dp
issue-06-qa-hamiltonians
issue-07-qa-evolution
issue-08-heatmaps
issue-09-problem-plot
issue-10-streams-dashboard
issue-11-flow-current
issue-12-notebook-narrative
issue-13-notebook-execution
issue-14-doc-guardrails
issue-15-mvp-polish
```

### 3.2 Commit style

Use small commits:

```text
scaffold package layout
add math overview skeleton
add layered dag problem
add planted gold and decoy generator
add hard dp solver
add soft dp path marginals
add qa laplacian driver
add notebook section 1 narrative
```

### 3.3 AI execution note requirement

After each issue, the AI agent must add a short note to the issue or PR description:

```markdown
## Execution notes

### Implemented
- ...

### Changed files
- ...

### Validation run
- Command: `pytest ...`
- Result: ...

### Spec docs checked or updated
- `docs/math_overview.md`: checked / updated / not applicable
- `docs/qa_proxy_notes.md`: checked / updated / not applicable
- `docs/visualization_guide.md`: checked / updated / not applicable

### Deviations from roadmap
- ...

### Open questions
- ...
```

The AI agent must not silently change public interfaces beyond the issue scope.

### 3.4 Review order

For each issue, the human reviewer should check in this order:

1. Scope: Did the PR only do the issue?
2. Spec sync: Were the companion docs checked or updated?
3. API: Are names and signatures understandable?
4. Tests: Are correctness tests present?
5. Math: Does implementation match formulas in `docs/math_overview.md`?
6. QA claims: Does text match `docs/qa_proxy_notes.md`?
7. Visualization semantics: Do figures match `docs/visualization_guide.md`?
8. Notebook impact: Does it help the final narrative?
9. Diff hygiene: Are generated outputs kept out unless explicitly needed?

---

# Issue 00: Project scaffold and documentation skeleton

## Goal

Create the repository structure, package metadata, test harness, notebook pairing plan, and documentation skeleton.

This is the most important first issue. It sets the rails so later AI coding work does not sprawl.

## Todo

- Create `pyproject.toml`.
- Create `src/pathspace_lab/` package layout.
- Create `tests/` layout with one smoke test.
- Create `docs/` and add the three spec documents:
  - `math_overview.md`
  - `qa_proxy_notes.md`
  - `visualization_guide.md`
- Create `notebooks/` and `notebooks/paired/` directories.
- Create a minimal notebook placeholder or paired script placeholder.
- Add `.gitignore` for Python, notebook checkpoints, build artifacts, cache files.
- Add a minimal `README.md` with project goal and non-goals.
- Add or copy `DEVELOPMENT_ROADMAP.md`.
- Add simple import smoke test.
- Add basic commands to README:
  - install editable package,
  - run tests,
  - sync paired notebook,
  - execute notebook later.

## Not todo

- Do not implement solvers.
- Do not implement plotting.
- Do not introduce Qiskit, OpenJij, dimod, or QuTiP.
- Do not build a large notebook yet.
- Do not add generated notebook outputs.

## Suggested `pyproject.toml`

```toml
[project]
name = "pathspace-lab"
version = "0.1.0"
description = "Visual comparison of DP, Soft-DP, and feasible-subspace quantum annealing on path-DP problems."
requires-python = ">=3.10"
dependencies = [
  "numpy",
  "scipy",
  "networkx",
  "matplotlib",
  "ipywidgets",
  "pandas",
]

[project.optional-dependencies]
dev = [
  "pytest",
  "jupytext",
  "nbconvert",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

Pytest recommends using isolated environments and project configuration such as `pyproject.toml` for development workflows.

Reference: https://docs.pytest.org/en/stable/explanation/goodpractices.html

## Human acceptance criteria

- A new contributor can run:

```bash
pip install -e ".[dev]"
pytest
```

- The package imports:

```python
import pathspace_lab
```

- The directory layout matches the intended architecture.
- The three docs exist and contain substantive guardrails, not just placeholders.
- No solver or visualization logic is prematurely added.

## AI acceptance criteria

The AI agent must report:

- exact files created,
- exact test command run,
- whether import smoke test passed,
- whether the three spec documents were created,
- any package or environment assumptions.

## Required tests

```python
def test_import_package():
    import pathspace_lab
    assert pathspace_lab is not None
```

---

# Issue 01: Implement `PathDPProblem` protocol and shared trace dataclasses

## Goal

Define the core interfaces that all later solvers and visualizers consume.

Reference:

- `docs/math_overview.md`, sections “Three spaces” and “Shape and normalization conventions”.

## Todo

- Add `src/pathspace_lab/problems/base.py`.
- Add `PathDPProblem` protocol.
- Add type aliases:
  - `State`
  - `Path`
- Add `src/pathspace_lab/utils/typing.py`.
- Add dataclasses:
  - `Frame`
  - `SolverTrace`
- Add docstrings explaining fields.
- Add tests verifying dataclasses can be constructed.

## Not todo

- Do not implement `LayeredDAGProblem` yet.
- Do not implement any solver.
- Do not add plotting.
- Do not add complicated generics unless needed.

## Interface sketch

```python
from typing import Any, Protocol
import numpy as np
import networkx as nx

State = Any
Path = tuple[State, ...]

class PathDPProblem(Protocol):
    name: str
    def graph(self) -> nx.DiGraph: ...
    def source(self) -> State: ...
    def sink(self) -> State: ...
    def states(self) -> list[State]: ...
    def edges(self) -> list[tuple[State, State, float]]: ...
    def topological_order(self) -> list[State]: ...
    def enumerate_paths(self, max_paths: int | None = None) -> list[Path]: ...
    def path_energy(self, path: Path) -> float: ...
    def state_coord(self, state: State) -> tuple[float, float]: ...
    def state_cell(self, state: State) -> tuple[int, int] | None: ...
    def canvas_shape(self) -> tuple[int, int]: ...
    def path_cells(self, path: Path) -> list[tuple[int, int]]: ...
```

## Human acceptance criteria

- Interfaces are small and readable.
- `Frame` and `SolverTrace` are general enough for DP, Soft-DP, and QA.
- No solver-specific assumptions leak into the base problem protocol.

## AI acceptance criteria

- Tests pass.
- The agent explains why each field exists.
- The agent lists which later issue consumes each interface.
- The agent confirms no spec doc update was needed, or updates `docs/math_overview.md` if shape conventions changed.

---

# Issue 02: Implement `LayeredDAGProblem` and planted instance generator

## Goal

Implement the first concrete problem class and a seeded generator with a gold path and a decoy path.

Reference:

- `docs/math_overview.md`, sections “MVP problem”, “Planted gold path and decoy path”.
- `docs/visualization_guide.md`, sections “Problem graph plot” and “Suggested notebook figure order”.

## Todo

- Add `src/pathspace_lab/problems/layered_dag.py`.
- Implement `LayeredDAGProblem` dataclass with:
  - `node_cost: np.ndarray` of shape `(L, W)`
  - `edge_cost: np.ndarray` of shape `(L - 1, W, W)`
- Implement graph construction with artificial source and sink.
- Implement path enumeration.
- Implement path energy.
- Implement state coordinates.
- Implement heatmap cell mapping.
- Implement `make_planted_layered_problem` generator.
- In the generator, support or return metadata for:
  - gold path,
  - decoy path,
  - seed.
- Add tests for shapes, graph acyclicity, path count, path energy, and source/sink omission from heatmaps.

## Not todo

- Do not implement DP solver.
- Do not implement plotting, except maybe a tiny debug-only helper if strictly necessary.
- Do not support variable-width layers yet.
- Do not support arbitrary graph input yet.

## Mathematical requirements

A visible path is:

\[
p=(v_0,v_1,\dots,v_{L-1}).
\]

Path energy is:

\[
E(p)=\sum_{\ell=0}^{L-1}c_{\ell,v_\ell}
+\sum_{\ell=0}^{L-2}e_{\ell,v_\ell,v_{\ell+1}}.
\]

The number of feasible paths must be:

\[
W^L.
\]

## Human acceptance criteria

- The implementation is clear enough to inspect by eye.
- The generator creates nontrivial deterministic instances with a seed.
- The default generated instance has a visible gold path and a visible decoy path.
- Source and sink are handled consistently and do not appear in the main heatmap.
- `path_energy` matches the mathematical formula.

## AI acceptance criteria

The AI agent must provide:

- output of `pytest tests/test_layered_dag.py`,
- number of paths for default problem,
- optimal path and energy for one seeded instance,
- decoy path and energy for one seeded instance,
- any assumptions about source/sink edge weights,
- confirmation that `docs/math_overview.md` remains consistent.

## Required tests

- `test_layered_graph_is_dag`
- `test_path_count_is_w_power_l`
- `test_each_path_visits_one_node_per_layer`
- `test_path_energy_matches_manual_calculation`
- `test_state_cell_omits_source_and_sink`
- `test_planted_problem_is_deterministic_under_seed`

---

# Issue 03: Implement common observables and marginal utilities

## Goal

Implement reusable math utilities for probabilities, marginals, entropy, energy, and success probability.

Reference:

- `docs/math_overview.md`, sections “Common observables”, “Shape and normalization conventions”.

## Todo

- Add `src/pathspace_lab/math/observables.py`.
- Implement:
  - `path_entropy(path_probs)`
  - `effective_num_paths(path_probs)`
  - `expected_energy(path_probs, energies)`
  - `residual_energy(path_probs, energies)`
  - `success_probability(path_probs, energies, tol=...)`
  - `cell_marginals(problem, paths, path_probs)`
  - `edge_marginals_from_paths(paths, path_probs)`
- Add validation for shape mismatches.
- Add tests for normalization and simple known examples.

## Not todo

- Do not implement Soft-DP solver yet.
- Do not implement QA current yet.
- Do not add plotting.

## Human acceptance criteria

- Functions are small and individually testable.
- Probability normalization assumptions are explicit.
- Marginal sums obey the invariants in `docs/math_overview.md`.

## AI acceptance criteria

The AI agent must report:

- tests run,
- at least one simple hand-computed example,
- marginal sum checks,
- whether any doc update was needed.

## Required tests

- `test_entropy_uniform_distribution`
- `test_expected_energy_manual_example`
- `test_success_probability_unique_optimum`
- `test_cell_marginals_sum_to_layers`
- `test_cell_marginals_sum_to_one_per_layer`
- `test_edge_marginals_manual_example`

---

# Issue 04: Implement Hard DP solver

## Goal

Implement deterministic min-plus DP over the problem DAG.

Reference:

- `docs/math_overview.md`, section “Hard DP”.
- `docs/visualization_guide.md`, section “Hard DP value heatmap”.

## Todo

- Add `src/pathspace_lab/solvers/hard_dp.py`.
- Implement `solve_hard_dp(problem) -> SolverTrace`.
- Compute distance values with topological order.
- Compute backpointers.
- Produce frames, preferably one frame per visible layer for `LayeredDAGProblem`.
- Include `value_heat` in frames.
- Include final path and final energy in trace metadata.
- Add tests comparing DP result to enumerated path minimum.

## Not todo

- Do not implement Soft-DP.
- Do not implement plotting.
- Do not implement generic cyclic graph shortest paths.

## Human acceptance criteria

- DP recurrence is recognizable.
- Trace output can drive a value heatmap.
- Final DP value equals enumerated optimum for small instances.
- Backpointer traceback returns a valid path.

## AI acceptance criteria

The AI agent must report:

- final DP path and energy for a seeded problem,
- enumerated optimum and equality check,
- tests run,
- whether `docs/math_overview.md` or visualization docs needed updates.

## Required tests

- `test_hard_dp_matches_enumerated_optimum`
- `test_hard_dp_traceback_is_valid_path`
- `test_hard_dp_value_heat_shape`
- `test_hard_dp_source_sink_not_in_heatmap`

---

# Issue 05: Implement Soft-DP solver

## Goal

Implement the classical thermal path distribution and its projected marginals.

Reference:

- `docs/math_overview.md`, section “Soft-DP / classical thermal path distribution”.
- `docs/visualization_guide.md`, sections “Soft-DP marginal heatmap” and “Top-k path probability stream”.

## Todo

- Add `src/pathspace_lab/solvers/soft_dp.py`.
- Implement `solve_soft_dp(problem, betas, paths=None) -> SolverTrace`.
- Enumerate paths if not provided.
- Compute path energies.
- Use log-sum-exp for numerical stability.
- Produce frames with:
  - `path_probs`,
  - `cell_heat`,
  - optional `edge_heat`,
  - observables: expected energy, residual energy, entropy, effective paths, success probability.
- Add tests for \(\beta=0\), high-beta behavior, marginal sums, and observables.

## Not todo

- Do not implement forward-backward dynamic programming yet.
- Do not implement QA.
- Do not claim Soft-DP is quantum.

## Human acceptance criteria

- At \(\beta=0\), path probabilities are uniform.
- At large \(\beta\), success probability increases on simple unique-optimum cases.
- Marginal heatmaps match the formulas.
- Trace is compatible with visualization tools.

## AI acceptance criteria

The AI agent must report:

- path probability sum checks,
- entropy at \(\beta=0\),
- final success probability on a seeded problem,
- tests run,
- doc sync status.

## Required tests

- `test_soft_dp_beta_zero_uniform`
- `test_soft_dp_probs_sum_to_one`
- `test_soft_dp_cell_marginals_sum_to_layers`
- `test_soft_dp_success_probability_increases_on_simple_case`
- `test_soft_dp_uses_logsumexp_stably`

---

# Issue 06: Implement feasible QA Hamiltonian builders

## Goal

Build the Hamiltonians needed for feasible-subspace QA.

Reference:

- `docs/math_overview.md`, section “Feasible-subspace quantum annealing”.
- `docs/qa_proxy_notes.md`, sections “Why use a feasible path basis?” and “Why use a Laplacian driver?”.

## Todo

- Add or update `src/pathspace_lab/math/hamiltonians.py`.
- Implement path indexing:
  - `paths -> index`
  - `index -> paths`
- Implement problem Hamiltonian:
  - diagonal sparse matrix with path energies.
- Implement configuration graph builder:
  - edge between paths that differ in exactly one visible layer.
- Implement Laplacian driver:
  - `H_D = D - A`.
- Implement optional normalization utilities:
  - normalized problem Hamiltonian,
  - normalized driver Hamiltonian.
- Add tests for diagonal, symmetry, uniform ground state, and dimensions.

## Not todo

- Do not implement time evolution yet.
- Do not implement QUBO or transverse-field Ising QA.
- Do not add Qiskit.

## Human acceptance criteria

- The Hamiltonians match the formulas in `docs/math_overview.md`.
- The Laplacian driver has the uniform vector as a ground state when the configuration graph is connected.
- Matrices are sparse.
- Path indexing is stable.

## AI acceptance criteria

The AI agent must report:

- number of paths and Hamiltonian shape for default instance,
- whether the configuration graph is connected,
- norm of `H_D @ ones`,
- tests run,
- confirmation that QA wording still matches `docs/qa_proxy_notes.md`.

## Required tests

- `test_problem_hamiltonian_is_diagonal`
- `test_problem_hamiltonian_ground_energy_matches_optimum`
- `test_configuration_graph_edges_hamming_one`
- `test_laplacian_driver_is_symmetric`
- `test_laplacian_driver_uniform_ground_state`

---

# Issue 07: Implement feasible-subspace QA time evolution

## Goal

Simulate coherent time evolution under the feasible-subspace QA Hamiltonian.

Reference:

- `docs/math_overview.md`, sections “Time evolution”, “QA-specific observables”.
- `docs/qa_proxy_notes.md`, sections “Evolution and measurement” and “Allowed claims”.

## Todo

- Add `src/pathspace_lab/solvers/qa_feasible.py`.
- Add `QASimulationConfig` dataclass.
- Implement linear schedule by default:
  - `A(s)=1-s`
  - `B(s)=s`
- Simulate:

\[
\psi(t+\Delta t)\approx e^{-iH(s_k)\Delta t}\psi(t).
\]

- Use sparse matrix exponential action, e.g. `scipy.sparse.linalg.expm_multiply`.
- Produce `SolverTrace` frames with:
  - amplitudes,
  - path probabilities,
  - cell marginals,
  - expected energy,
  - residual energy,
  - entropy,
  - effective paths,
  - success probability,
  - state norm.
- Add optional gap computation at selected grid points using sparse eigensolver.
- Add tests for norm preservation, probability sums, heatmap sums, and ground-energy consistency.

## Not todo

- Do not implement noisy dynamics.
- Do not implement QUBO transverse-field QA.
- Do not implement Qiskit circuit simulation.
- Do not claim finite-time evolution guarantees the optimum.

## Human acceptance criteria

- The QA implementation is readable and directly tied to formulas.
- The trace can drive QA heatmaps and dashboards.
- The state norm remains close to 1.
- The model is clearly named as a feasible-subspace proxy.

## AI acceptance criteria

The AI agent must report:

- default `QASimulationConfig`,
- state norm max deviation,
- final success probability on a seeded problem,
- whether gap computation is enabled or skipped,
- tests run,
- doc sync status for `docs/qa_proxy_notes.md`.

## Required tests

- `test_qa_initial_distribution_uniform`
- `test_qa_state_norm_preserved`
- `test_qa_path_probs_sum_to_one`
- `test_qa_cell_marginals_sum_to_layers`
- `test_qa_final_problem_ground_energy_matches_classical_optimum`
- `test_qa_trace_contains_required_observables`

---

# Issue 08: Implement core heatmap visualizations

## Goal

Implement reusable heatmap visualizers for DP values, Soft-DP marginals, and QA marginals.

Reference:

- `docs/visualization_guide.md`, sections 1 through 6.

## Todo

- Add `src/pathspace_lab/viz/heatmaps.py`.
- Implement:
  - `plot_value_heatmap(frame, ...)`
  - `plot_cell_marginal_heatmap(frame, ...)`
  - `plot_trace_heatmap_grid(trace, frame_indices, ...)`
  - `compare_traces_by_progress(soft_trace, qa_trace, ...)`
  - `compare_traces_by_entropy(soft_trace, qa_trace, ...)`
- Label all plots with the quantity being shown.
- Ensure source/sink are not shown in main heatmaps.
- Add lightweight tests for function execution on small traces.

## Not todo

- Do not implement full animation yet unless simple.
- Do not implement graph plotting.
- Do not hardcode `LayeredDAGProblem` assumptions beyond array shape.

## Human acceptance criteria

- Plot titles and labels make it clear whether heat is value, probability marginal, or comparison.
- The visualizer consumes `Frame` and `SolverTrace` rather than recomputing solver internals.
- Entropy-alignment comparison is clearly labeled.

## AI acceptance criteria

The AI agent must report:

- example figures created or smoke-tested,
- whether visual labels match `docs/visualization_guide.md`,
- tests run,
- any plotting limitations.

## Required tests

- `test_plot_value_heatmap_runs`
- `test_plot_cell_marginal_heatmap_runs`
- `test_compare_traces_by_progress_runs`
- `test_compare_traces_by_entropy_selects_frames`

---

# Issue 09: Implement problem graph plot

## Goal

Implement the initial graph visualization, including gold and decoy path highlighting.

Reference:

- `docs/visualization_guide.md`, section “Problem graph plot”.
- `docs/math_overview.md`, section “Planted gold path and decoy path”.

## Todo

- Add `src/pathspace_lab/viz/problem_plot.py`.
- Implement `plot_problem_graph(problem, ...)`.
- Support optional:
  - highlighted gold path,
  - highlighted decoy path,
  - edge heat,
  - node heat,
  - labels.
- Keep plotting readable for small `L,W`.
- Add smoke tests.

## Not todo

- Do not implement path-space current plot here.
- Do not over-design styling.
- Do not require plotly.

## Human acceptance criteria

- The plot explains the problem before any solver runs.
- Gold path and decoy path can be visually distinguished.
- Source/sink are either clearly shown as artificial or omitted with explanation.

## AI acceptance criteria

The AI agent must report:

- a seeded example with gold and decoy metadata,
- whether the plot uses problem coordinates,
- tests run.

---

# Issue 10: Implement top-k streams and observable dashboard

## Goal

Visualize path-level probability competition and global observables.

Reference:

- `docs/visualization_guide.md`, sections “Top-k path probability stream” and “Energy / entropy / success dashboard”.

## Todo

- Add `src/pathspace_lab/viz/streams.py`.
- Implement `plot_topk_path_probabilities(...)`.
- Ensure stable path selection across traces.
- Include gold and decoy paths if provided.
- Add `src/pathspace_lab/viz/dashboard.py`.
- Implement `plot_observable_dashboard(...)`.
- Include:
  - expected energy,
  - residual energy,
  - entropy,
  - effective paths,
  - success probability,
  - QA gap if present.
- Add smoke tests.

## Not todo

- Do not implement flow/current plots yet.
- Do not imply non-monotonic QA probabilities prove quantum advantage.

## Human acceptance criteria

- Top-k streams make gold-vs-decoy competition visible.
- Dashboard separates shared metrics from QA-only metrics.
- Labels make clear whether x-axis is beta progress, anneal fraction, or frame progress.

## AI acceptance criteria

The AI agent must report:

- which paths were selected for top-k plot,
- whether gold/decoy are included,
- tests run,
- any missing observables.

---

# Issue 11: Implement Soft-DP flow and QA current visualizations

## Goal

Implement the most conceptually distinctive visualization: classical probability flow versus quantum current.

Reference:

- `docs/math_overview.md`, sections “Edge marginals” and “Probability current”.
- `docs/visualization_guide.md`, sections “Soft-DP edge flow”, “QA path-space current”, and “QA occupancy projected onto original DAG”.

## Todo

- Add `src/pathspace_lab/viz/currents.py`.
- Implement Soft-DP edge-flow plot on the original DAG.
- Implement QA path-space current computation if not already in math utilities.
- Implement QA path-space current plot for small top-probability subsets.
- Optionally implement QA edge occupancy projection.
- Add tests for current computation on tiny Hermitian matrices.

## Not todo

- Do not draw QA current on the original DAG and label it as literal current.
- Do not require large graph layouts.
- Do not over-optimize for large path spaces.

## Human acceptance criteria

- Soft-DP flow is nonnegative and drawn on original problem edges.
- QA current is signed and drawn on path-space edges.
- The distinction between occupancy and current is explicit.
- The notebook text explains the hidden-space difference.

## AI acceptance criteria

The AI agent must report:

- a tiny current sanity check,
- how many path-space nodes are shown by default,
- whether any currents were thresholded,
- tests run,
- confirmation that visualization claims match `docs/visualization_guide.md`.

---

# Issue 12: Implement notebook narrative

## Goal

Build the MVP notebook narrative using the implemented modules.

Reference:

- `docs/math_overview.md`
- `docs/qa_proxy_notes.md`
- `docs/visualization_guide.md`

## Todo

Create or update:

```text
notebooks/01_dp_softdp_qa_layered_path.ipynb
notebooks/paired/01_dp_softdp_qa_layered_path.py
```

Notebook sections:

1. Introduction: three mechanisms, one projection canvas.
2. Create layered graph with gold and decoy paths.
3. Hard DP as deterministic message passing.
4. Soft-DP as classical thermal bridge.
5. Feasible-subspace QA as continuous Hamiltonian proxy.
6. Same projection, different dynamics.
7. Observable dashboard.
8. Flow versus current.
9. Summary and limitations.

## Not todo

- Do not put solver internals into notebook cells.
- Do not use optional dependencies.
- Do not make the default instance too large.
- Do not overclaim QA realism.

## Narrative requirements

The notebook must include these statements, in natural wording:

- The shared heatmap is a projection, not a shared mechanism.
- DP values are not probabilities.
- Soft-DP is a classical thermal baseline.
- The QA model is a feasible-subspace proxy, not a D-Wave hardware simulator.
- QA current flows in path space, not along original DP graph edges.
- Gold and decoy paths are pedagogical devices used to make probability competition visible.

## Human acceptance criteria

- A reader can follow the story without opening source files.
- The notebook still points to docs for mathematical details.
- Figures appear in a pedagogically logical order.
- Limitations are honest and visible.

## AI acceptance criteria

The AI agent must report:

- notebook sections completed,
- source modules imported,
- whether paired script was updated,
- whether docs were referenced,
- any cells that are placeholders.

---

# Issue 13: Notebook execution checks

## Goal

Ensure the notebook can run top-to-bottom from a clean environment.

Reference:

- `docs/visualization_guide.md` for expected figure order.

## Todo

- Add `scripts/execute_notebook.sh`.
- Add a README command for notebook execution.
- Use `jupyter nbconvert --execute` or equivalent.
- Keep default runtime small.
- Add optional CI note.

## Not todo

- Do not commit large generated outputs unless team decides to.
- Do not add heavy CI matrix.

## Human acceptance criteria

- A contributor can run the notebook without manual cell surgery.
- Runtime is reasonable for a toy MVP.
- Failures are easy to diagnose.

## AI acceptance criteria

The AI agent must report:

- exact execution command,
- runtime,
- whether outputs were generated,
- any failed cells.

Reference: nbconvert can execute notebook input cells and save the result.

https://nbconvert.readthedocs.io/en/latest/execute_api.html

---

# Issue 14: Documentation and scientific guardrails

## Goal

Review and tighten all educational and scientific text.

Reference:

- `docs/math_overview.md`
- `docs/qa_proxy_notes.md`
- `docs/visualization_guide.md`

## Todo

- Review README.
- Review all three docs.
- Review notebook markdown cells.
- Ensure formulas and code names are consistent.
- Ensure all overclaims are removed.
- Ensure gold/decoy story is described as pedagogical.
- Ensure visualizations are not mislabeled.

## Not todo

- Do not add new features.
- Do not rewrite the project structure.
- Do not make prose too verbose.

## Human acceptance criteria

- A skeptical reader can tell what is implemented and what is not.
- A beginner can tell how to read each plot.
- QA proxy claims are precise.

## AI acceptance criteria

The AI agent must report:

- claims changed,
- formulas corrected,
- docs updated,
- any remaining ambiguous wording.

---

# Issue 15: MVP polish and release checklist

## Goal

Prepare the first shareable MVP release.

## Todo

- Run full test suite.
- Execute notebook top-to-bottom.
- Check paired notebook diff.
- Check all docs are linked from README.
- Check default parameters produce readable plots.
- Check no optional dependencies are required.
- Check no generated cache files are committed.
- Add a short “What to try next” section to README.

## Not todo

- Do not add new algorithms.
- Do not start QUBO/Qiskit/OpenJij work in this issue.
- Do not broaden problem support before the first MVP lands.

## Human acceptance criteria

The repo is ready for a first public PR or internal demo.

## AI acceptance criteria

The AI agent must report:

- full test command and result,
- notebook execution command and result,
- files changed,
- final limitations,
- follow-up issue suggestions.

---

## Notebook narrative skeleton

The notebook should be built around this narrative arc.

### Section 0: Introduction

Explain the three mechanisms:

- Hard DP: local values.
- Soft-DP: classical path probabilities.
- QA: amplitudes over complete paths.

Point readers to:

- `docs/math_overview.md`
- `docs/qa_proxy_notes.md`
- `docs/visualization_guide.md`

### Section 1: Create a layered graph

Generate a planted problem with:

- gold path,
- decoy path,
- small `L,W`,
- deterministic seed.

Show the graph.

### Section 2: Hard DP

Show:

- recurrence,
- DP value heatmap,
- backpointers,
- traceback.

Emphasize:

> DP values are compressed partial-history summaries, not probabilities.

### Section 3: Soft-DP

Show:

- Boltzmann path distribution,
- marginal heatmap,
- top-k path stream.

Emphasize:

> Soft-DP is the classical thermal bridge.

### Section 4: Feasible-subspace QA

Show:

- path basis,
- \(H_D\),
- \(H_P\),
- annealing Hamiltonian,
- QA marginal heatmap.

Emphasize:

> This is a feasible-subspace QA proxy, not hardware QA.

### Section 5: Same projection, different dynamics

Compare:

- Soft-DP vs QA by progress.
- Soft-DP vs QA by entropy.

Emphasize:

> Similar concentration does not imply the same mechanism.

### Section 6: Observable dashboard

Show:

- expected energy,
- residual energy,
- entropy,
- effective paths,
- success probability,
- QA gap.

### Section 7: Flow versus current

Show:

- Soft-DP edge flow on the original DAG.
- QA current on path-space graph.

Emphasize:

> Classical probabilistic flow travels through problem edges. QA current travels between complete configurations.

### Section 8: Summary

End with:

> Same canvas, different hidden geometry.

---

## Roadmap after MVP

Do not implement these before the MVP is stable.

### Phase 1: Second path-DAG problem

Add grid path or edit-distance-style alignment.

Goal: show that the interface is not hardcoded to the layered graph.

### Phase 2: Cyclic graph problems via time expansion

Support original graphs with cycles by lifting them into:

\[
(t,v).
\]

The lifted graph is acyclic because time moves forward.

### Phase 3: Standard QUBO / transverse-field QA extension

Add a separate notebook:

```text
02_from_path_dp_to_qubo_qa.ipynb
```

Introduce:

- one-hot variables,
- penalty terms,
- feasible mass,
- illegal-state mass,
- bitstring basis,
- transverse-field driver.

D-Wave’s `dimod` documentation describes Binary Quadratic Models as containing Ising and QUBO models used by samplers.

Reference: https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/

### Phase 4: OpenJij SA/SQA comparison

Add sampler-based comparison.

OpenJij documents `SQASampler` as simulated quantum annealing on a classical computer.

Reference: https://tutorial.openjij.org/en/tutorial/001-openjij_introduction.html

### Phase 5: Qiskit gate-model appendix

Add Hamiltonian simulation or Trotterized evolution appendix.

This should remain separate from the MVP because the clean feasible-path Hamiltonian is not naturally a local Pauli Hamiltonian without encoding work.

### Phase 6: Hypergraph DP

Move from path-DAG to weighted acyclic hypergraphs for:

- matrix-chain multiplication,
- CKY parsing,
- interval DP,
- tree DP.

### Phase 7: More realistic open-system QA

Explore:

- noisy dynamics,
- thermal effects,
- freeze-out,
- nonlinear schedules,
- reverse annealing.

---

## Final MVP definition of done

A fresh clone can run:

```bash
pip install -e ".[dev]"
pytest
jupyter nbconvert --execute notebooks/01_dp_softdp_qa_layered_path.ipynb --to notebook --output /tmp/pathspace_lab_executed.ipynb
```

and the notebook produces:

1. A planted layered DAG visualization.
2. A Hard DP value heatmap.
3. A Soft-DP marginal heatmap.
4. A feasible-subspace QA marginal heatmap.
5. Soft-DP vs QA comparison by progress and entropy.
6. Top-k path probability curves including gold and decoy paths.
7. Energy / entropy / success dashboard.
8. QA spectral gap curve.
9. Soft-DP flow and QA current visualization.
10. A clear written explanation of what is and is not being claimed.

The MVP is done when the small toy universe runs, teaches, and does not overclaim. ✨

## Issue 00 execution notes

### Implemented
- Created Python package metadata and editable-install configuration.
- Created the `src/pathspace_lab` package namespace with planned subpackages.
- Created the `tests` layout with an import smoke test.
- Created the `docs` layout and moved the three companion specification documents into it.
- Created notebook and paired-script placeholders for the future MVP notebook.
- Added `.gitignore`, `jupytext.toml`, and a README with setup, test, notebook sync, and future execution commands.

### Changed files
- `.gitignore`
- `README.md`
- `DEVELOPMENT_ROADMAP.md`
- `docs/math_overview.md`
- `docs/qa_proxy_notes.md`
- `docs/visualization_guide.md`
- `jupytext.toml`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `pyproject.toml`
- `src/pathspace_lab/__init__.py`
- `src/pathspace_lab/problems/__init__.py`
- `src/pathspace_lab/solvers/__init__.py`
- `src/pathspace_lab/math/__init__.py`
- `src/pathspace_lab/viz/__init__.py`
- `src/pathspace_lab/utils/__init__.py`
- `tests/test_import_package.py`

### Validation run
- Command: `pytest`
- Result: pending at note creation; run after scaffold write.

### Spec docs checked or updated
- `docs/math_overview.md`: moved into required location and checked for issue00 consistency.
- `docs/qa_proxy_notes.md`: moved into required location and checked for issue00 consistency.
- `docs/visualization_guide.md`: moved into required location and checked for issue00 consistency.

### Deviations from roadmap
- The three companion documents already existed at the repository root, so they were moved into `docs/` instead of recreated.
- Script files under `scripts/` were left for later notebook execution issues; README commands document the planned workflow.

### Open questions
- None for issue00.

### Issue 00 validation update
- Editable install initially failed because `pyproject.toml` had a UTF-8 BOM from Windows PowerShell output. The file was rewritten as UTF-8 without BOM.
- Added an explicit setuptools build backend and `src` package discovery so editable installs are backend-defined.
### Issue 00 pairing update
- Jupytext configuration was adjusted to pair `notebooks/*.ipynb` with `notebooks/paired/*.py:percent`.
- README commands now use `python -m jupytext` and `python -m jupyter` so the workflow does not depend on Scripts being on PATH.
- Removed the extra paired-directory notebook generated during the first sync check.
### Issue 00 final validation
- Command: `python -m pip install -e ".[dev]"`
- Result: passed.
- Command: `python -m pytest`
- Result: passed, 1 test.
- Command: `python -m jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb`
- Result: passed after using forward slashes in the notebook path on Windows.
- Command: `python -c "import pathspace_lab; print(pathspace_lab.__version__)"`
- Result: passed, printed `0.1.0`.
- Generated validation caches and egg-info were removed after validation.