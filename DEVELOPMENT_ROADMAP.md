# DEVELOPMENT_ROADMAP.md

# Pathspace Lab MVP Development Roadmap

This roadmap is designed for incremental development with a human reviewer and an AI coding agent. Each issue includes goals, todo items, non-goals, implementation notes, acceptance criteria for humans, acceptance criteria for AI, and a required execution note that should be written after implementation.

The MVP goal is to build one clean, runnable notebook that compares:

1. Hard DP as deterministic min-plus message passing.
2. Soft-DP as a classical thermal distribution over feasible paths.
3. Feasible-subspace Quantum Annealing as continuous Hamiltonian evolution over feasible complete paths.

The first supported problem is a layered DAG shortest-path problem. A solution is a complete path through the layers. All three methods are projected onto the same layer-node visualization canvas.

---

## 0. Guiding principles

### 0.1 Project philosophy

The MVP is not a quantum advantage demo. It is a visual and mathematical teaching tool.

The central claim:

> Hard DP compresses histories into local values. Soft-DP assigns classical probabilities to complete paths. Feasible-subspace QA evolves complex amplitudes over complete paths. All three can be projected onto the same DP canvas, but their hidden dynamics are different.

### 0.2 Engineering philosophy

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

### 0.2.1 Notebook-first development rule

The notebook is not delayed until the end of the MVP. It grows issue by issue.

Each issue must add at least one notebook-visible artifact unless explicitly exempted:

- a new section,
- a new runnable cell,
- a diagnostic figure,
- a printed sanity check,
- or a short narrative placeholder that keeps the notebook runnable.

The detailed human acceptance checklist lives in:

```text
docs/notebook_acceptance_guide.md
```

Since Issue 00 has already produced only a placeholder notebook, the next recommended task is **Issue 00A: Notebook harness and living tutorial skeleton**.

### 0.3 Scientific integrity rules

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

---

## 1. Project linking strategy

### 1.1 Recommended structure

Use a standard Python package under `src/`, with a paired notebook workflow.

Recommended layout:

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
    notebook_acceptance_guide.md
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

### 1.2 Notebook pairing policy

Use Jupytext pairing:

- `.ipynb` is the user-facing notebook.
- `.py:percent` is the diff-friendly paired source.

Suggested files:

```text
notebooks/01_dp_softdp_qa_layered_path.ipynb
notebooks/paired/01_dp_softdp_qa_layered_path.py
```

Notebook pairing keeps version-control diffs readable while still letting users run a normal Jupyter notebook.

### 1.3 Source-of-truth policy

The source of truth is:

1. `src/` for all reusable implementation.
2. `tests/` for correctness expectations.
3. `notebooks/paired/*.py` for notebook narrative and cell order.
4. `.ipynb` for rendered notebook output, optional in git depending on team preference.

The paired `.py` file should be reviewed in PRs. The `.ipynb` should be regenerated or executed as a CI artifact when possible.

### 1.3.1 Notebook-side acceptance policy

Every issue should have a notebook-side acceptance step. The human reviewer should run the notebook from a clean kernel up to the newly implemented section and verify the expected visible result.

For machine checks, use notebook execution when available:

```bash
jupyter nbconvert --execute --to notebook \
  notebooks/01_dp_softdp_qa_layered_path.ipynb \
  --output /tmp/pathspace_lab_notebook_check.ipynb
```

The machine execution check catches hidden state and broken cells. It does not replace human visual review.

Reference: `docs/notebook_acceptance_guide.md`.

### 1.4 Documentation policy

Create these documents early:

```text
docs/math_overview.md
docs/qa_proxy_notes.md
docs/visualization_guide.md
docs/notebook_acceptance_guide.md
```

`docs/math_overview.md` should explain:

- layered DAG path energy,
- hard DP recurrence,
- Soft-DP Boltzmann distribution,
- feasible-subspace QA Hamiltonian.

`docs/qa_proxy_notes.md` should explain:

- what the QA proxy preserves,
- what it does not preserve,
- how it differs from transverse-field Ising QA,
- what claims are allowed.

`docs/visualization_guide.md` should explain:

- DP value heatmap,
- Soft-DP marginal heatmap,
- QA marginal heatmap,
- path probability streams,
- energy and entropy curves,
- probability flow vs quantum current.

`docs/notebook_acceptance_guide.md` should explain:

- what notebook-visible result each issue must produce,
- what a human should run,
- what the expected visual or printed result should be,
- when temporary diagnostic plots are allowed,
- when those temporary plots should be replaced by official visualizers.

---

## 2. Development workflow for humans and AI agents

### 2.1 Branch naming

Use one branch per issue:

```text
issue-00-project-scaffold
issue-01-layered-dag-problem
issue-02-hard-dp
issue-03-soft-dp
issue-04-feasible-qa
issue-05-visualization-core
issue-06-notebook-narrative
```

### 2.2 Commit style

Use small commits:

```text
scaffold package layout
add layered dag problem
add hard dp solver
add soft dp path marginals
add feasible qa hamiltonians
add notebook section 1 narrative
```

### 2.3 AI execution note requirement

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

### Deviations from spec
- ...

### Open questions
- ...
```

The AI agent should not silently change public interfaces beyond the issue scope.

### 2.4 Review order

For each issue, the human reviewer should check in this order:

1. Scope: Did the PR only do the issue?
2. API: Are names and signatures understandable?
3. Tests: Are correctness tests present?
4. Math: Does implementation match formulas?
5. Notebook impact: Does it help the final narrative?
6. Notebook run: Can the human run the notebook up to the new section and see the expected result from `docs/notebook_acceptance_guide.md`?
7. Diff hygiene: Are generated outputs kept out unless explicitly needed?

---

# Issue 00: Project scaffold and documentation skeleton

## Goal

Create the repository structure, package metadata, test harness, notebook pairing plan, and documentation skeleton.

This is the most important first issue. It sets the rails so later AI coding work does not sprawl.

## Todo

- Create `pyproject.toml`.
- Create `src/pathspace_lab/` package layout.
- Create `tests/` layout with one smoke test.
- Create `docs/` with three skeleton docs:
  - `math_overview.md`
  - `qa_proxy_notes.md`
  - `visualization_guide.md`
  - `notebook_acceptance_guide.md`
- Create `notebooks/` and `notebooks/paired/` directories.
- Create a minimal notebook placeholder or paired script placeholder.
- Add `.gitignore` for Python, notebook checkpoints, build artifacts, cache files.
- Add a minimal `README.md` with project goal and non-goals.
- Add a minimal `DEVELOPMENT_ROADMAP.md` if this file is not already in repo.
- Add simple import smoke test.
- Add basic commands to README:
  - install editable package,
  - run tests,
  - run notebook execution check later.

## Not todo

- Do not implement solvers.
- Do not implement plotting.
- Do not introduce Qiskit, OpenJij, dimod, or QuTiP.
- Do not build a large notebook yet. Issue 00 may create a placeholder; Issue 00A turns it into a runnable living skeleton.
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
- Documentation skeletons exist and state the scientific boundaries.
- No solver or visualization logic is prematurely added.

## AI acceptance criteria

The AI agent must report:

- exact files created,
- exact test command run,
- whether import smoke test passed,
- any package or environment assumptions.

## Suggested smoke test

```python
def test_import_package():
    import pathspace_lab
    assert pathspace_lab is not None
```


---

# Issue 00A: Notebook harness and living tutorial skeleton

## Goal

Turn the placeholder notebook from Issue 00 into a runnable living tutorial skeleton before implementing more backend logic.

This issue exists because notebook-side human verification is part of every later issue.

Reference: `docs/notebook_acceptance_guide.md`.

## Todo

- Create or update:
  - `notebooks/01_dp_softdp_qa_layered_path.ipynb`
  - `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- Add the final section headings as markdown cells.
- Add a setup cell importing:
  - `numpy`
  - `pandas`
  - `matplotlib.pyplot`
  - `pathspace_lab`
- Add a small status table showing implemented and pending components.
- Add a markdown note explaining that the notebook will grow issue by issue.
- Ensure the notebook can run top to bottom from a clean kernel.

## Not todo

- Do not implement solvers.
- Do not implement problem generation.
- Do not add fake results.
- Do not add code cells for future sections that raise errors.

## Notebook-side human acceptance

Open the notebook and run all cells.

Expected visible result:

- Notebook title appears.
- Setup imports run without error.
- A status table appears with components such as:
  - `LayeredDAGProblem`
  - `Hard DP`
  - `Soft-DP`
  - `Feasible-subspace QA`
  - `Visualizers`
- Later sections exist as markdown placeholders.
- No cell fails.

Suggested check cell:

```python
import pathspace_lab
print("Pathspace Lab import OK")
```

## AI acceptance criteria

The AI agent must report:

- files changed,
- whether the paired script and `.ipynb` are synchronized,
- whether the notebook runs from a clean kernel,
- which future sections are present as placeholders.

## Required tests or checks

At minimum:

```bash
pytest
```

If `nbconvert` is already available:

```bash
jupyter nbconvert --execute --to notebook \
  notebooks/01_dp_softdp_qa_layered_path.ipynb \
  --output /tmp/pathspace_lab_notebook_check.ipynb
```

## Execution notes

### Implemented
- Replaced the placeholder notebook with a runnable living tutorial skeleton.
- Added setup imports, an import sanity print, a component status table, and markdown placeholders for the final narrative sections.
- Kept future sections markdown-only so they do not fail before backend implementation exists.

### Changed files
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`

### Validation run
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `1 passed`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb`
- Result: passed.

### Deviations from spec
- Added a small `src/` path discovery block in the notebook setup cell so clean-kernel execution works even before the package is installed editable in the active kernel environment.

### Pivot
- The initial nbconvert check failed because the executing kernel could not import `pathspace_lab`; the notebook harness was adjusted to find local `src/` from either the repository root or the `notebooks/` directory.

### Open questions
- None.
---

# Issue 01: Implement `PathDPProblem` protocol and shared trace dataclasses

## Goal

Define the core interfaces that all later solvers and visualizers consume.

Notebook role: demonstrate the data contract with a toy `Frame` and `SolverTrace`.

Reference: `docs/notebook_acceptance_guide.md`, Issue 01.

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

## Execution notes

### Implemented
- Added `PathDPProblem` as the shared structural protocol for path-DP problems.
- Added `State` and `Path` aliases to keep problem, solver, and visualization signatures consistent.
- Added `Frame` and `SolverTrace` dataclasses for solver snapshots and ordered method traces.
- Added notebook data-contract demo with a toy `Frame`, printed `SolverTrace` summary, and a small dummy heatmap.

### Field purpose
- `Frame.progress`: comparable progress coordinate for DP layers, Soft-DP beta progress, or QA anneal fraction.
- `Frame.label`: short display label for tables and figures.
- `Frame.cell_heat`: projected layer-node marginal or score heatmap consumed by Soft-DP, QA, and heatmap visualizers.
- `Frame.value_heat`: DP value table, kept separate because DP values are not probabilities.
- `Frame.path_probs`: complete-path probabilities used by Soft-DP and QA-derived measurement distributions.
- `Frame.amplitudes`: complex QA state over complete feasible paths.
- `Frame.edge_heat`: optional projected edge quantities such as Soft-DP flow or QA occupancy.
- `Frame.observables`: scalar diagnostics such as energy, entropy, success probability, norm, or spectral gap.
- `Frame.metadata`: non-contract method details.
- `SolverTrace.method`: identifies the producing mechanism.
- `SolverTrace.problem_name`: labels the problem instance without requiring the full object.
- `SolverTrace.frames`: ordered snapshots consumed by notebooks and visualizers.
- `SolverTrace.paths` and `SolverTrace.energies`: optional shared ordering for complete-path plots and observables.
- `SolverTrace.metadata`: trace-level solver parameters or notes.

### Later issue consumers
- Issue 02 consumes `PathDPProblem`, `State`, and `Path` for `LayeredDAGProblem`.
- Issues 04-07 consume `Frame` and `SolverTrace` for Hard DP, Soft-DP, and QA solver outputs.
- Issues 08-11 consume `Frame` and `SolverTrace` for heatmaps, streams, dashboards, flow, and current visualizations.

### Changed files
- `src/pathspace_lab/problems/base.py`
- `src/pathspace_lab/problems/__init__.py`
- `src/pathspace_lab/utils/typing.py`
- `src/pathspace_lab/utils/__init__.py`
- `tests/test_problem_base.py`
- `tests/test_typing.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`

### Validation run
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `6 passed`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb`
- Result: passed.

### Deviations from spec
- No solver, concrete problem, or official plotting helper was added. The notebook heatmap remains a direct matplotlib toy diagnostic as requested by the Issue 01 acceptance guide.

### Pivot
- No business/product-level pivot. The main implementation choice was to keep trace fields optional so one dataclass can serve DP values, Soft-DP probabilities, and QA amplitudes without forcing solver-specific assumptions into the base protocol.

### Open questions
- None.

---

# Issue 02: Implement `LayeredDAGProblem` and planted instance generator

## Goal

Implement the first concrete problem class.

Notebook role: create the first real problem instance, enumerate paths, print the brute-force optimum, and show a simple node-cost heatmap.

Reference: `docs/math_overview.md` and `docs/notebook_acceptance_guide.md`, Issue 02.

## Todo

- Add `src/pathspace_lab/problems/layered_dag.py`.
- Implement `LayeredDAGProblem` dataclass with:
  - `node_cost: np.ndarray` of shape `(L, W)`
  - `edge_cost: np.ndarray` of shape `(L - 1, W, W)`
  - optional `metadata: dict` for planted gold/decoy paths and notebook annotations
- Implement graph construction with artificial source and sink.
- Implement path enumeration.
- Implement path energy.
- Implement state coordinates.
- Implement heatmap cell mapping.
- Implement `make_planted_layered_problem` generator.
- The generator must create both a planted gold path and a decoy path.
- Store planted path hints in inspectable metadata, for example `problem.metadata["gold_path"]` and `problem.metadata["decoy_path"]`.
- Add tests for shapes, graph acyclicity, path count, path energy, and metadata presence.

## Not todo

- Do not implement DP solver.
- Do not implement plotting, except maybe a tiny debug-only function if strictly necessary.
- Do not support variable-width layers yet.
- Do not support arbitrary graph input yet.

## Mathematical requirements

A visible path is:

\[
p=(v_0,v_1,\dots,v_{L-1})
\]

Path energy is:

\[
E(p)=\sum_{\ell=0}^{L-1}c_{\ell,v_\ell}
+\sum_{\ell=0}^{L-2}e_{\ell,v_\ell,v_{\ell+1}}
\]

The number of feasible paths must be:

\[
W^L
\]

## Human acceptance criteria

- The implementation is clear enough to inspect by eye.
- The generator creates nontrivial but deterministic instances with a seed.
- Source and sink are handled consistently and do not appear in the main heatmap.
- `path_energy` matches the mathematical formula.

## AI acceptance criteria

The AI agent must provide:

- output of `pytest tests/test_layered_dag.py`,
- number of paths for default problem,
- optimal path and energy for one seeded instance,
- any assumptions about source/sink edge weights.

## Required tests

- `test_layered_graph_is_dag`
- `test_path_count_is_w_power_l`
- `test_each_path_visits_one_node_per_layer`
- `test_path_energy_matches_manual_calculation`
- `test_state_cell_omits_source_and_sink`

---

# Issue 03: Implement common observables and marginal utilities

## Goal

Implement reusable math utilities for probabilities, marginals, entropy, and energy.

Notebook role: show uniform and optimal-path distributions, their marginals, entropy, and effective path count.

Reference: `docs/math_overview.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 03.

## Todo

- Add `src/pathspace_lab/math/observables.py`.
- Implement:
  - `normalize_probs`
  - `path_entropy`
  - `effective_num_paths`
  - `expected_energy`
  - `success_probability`
  - `cell_marginals`
  - `edge_marginals_from_paths`
- Add numerical stability with `eps` where needed.
- Add tests for all utilities.

## Not todo

- Do not implement Soft-DP solver yet.
- Do not implement QA.
- Do not create plotting.

## Mathematical requirements

Entropy:

\[
S=-\sum_pP(p)\log P(p)
\]

Effective number of paths:

\[
N_{\text{eff}}=e^S
\]

Expected energy:

\[
\mathbb E[E]=\sum_pP(p)E(p)
\]

Success probability:

\[
P_{\text{success}}=\sum_{p:E(p)=E^*}P(p)
\]

Cell marginal:

\[
M_{\ell,v}=\sum_{p:(\ell,v)\in p}P(p)
\]

For a layered path problem where each path visits exactly \(L\) visible cells:

\[
\sum_{\ell,v}M_{\ell,v}=L
\]

## Human acceptance criteria

- Utilities are method-agnostic.
- Soft-DP and QA can both use the same marginal functions.
- Tests cover edge cases such as zero probabilities and multiple optimal paths.

## AI acceptance criteria

The AI agent must report:

- which observables are used by Soft-DP,
- which observables are used by QA,
- which tests verify normalization and marginals.

---

# Issue 04: Implement Hard DP solver

## Goal

Implement deterministic min-plus DP over the problem DAG.

Notebook role: run DP on the planted problem, compare with brute force, and show a first DP value heatmap.

Reference: `docs/math_overview.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 04.

## Todo

- Add `src/pathspace_lab/solvers/hard_dp.py`.
- Implement `solve_hard_dp(problem) -> SolverTrace`.
- Compute DP values in topological order.
- Store backpointers.
- Emit frames, preferably one frame per layer for `LayeredDAGProblem`.
- Add `traceback_best_path` helper.
- Add tests comparing DP optimum to brute-force path enumeration.

## Not todo

- Do not implement Soft-DP.
- Do not implement QA.
- Do not implement production visualizers.
- Do not over-optimize.

## Mathematical requirements

\[
D(\text{source})=0
\]

\[
D(v)=\min_{u\to v}\left[D(u)+w(u,v)\right]
\]

Backpointer:

\[
\operatorname{pred}(v)=\arg\min_{u\to v}\left[D(u)+w(u,v)\right]
\]

## Human acceptance criteria

- DP final value equals brute-force optimum.
- Backtrace gives a valid path.
- Frames contain enough data for future visualization.
- The solver works for any DAG implementing `PathDPProblem`, not just by indexing arrays directly.

## AI acceptance criteria

The AI agent must report:

- DP best value,
- brute-force best value,
- whether they match,
- path returned by traceback,
- test command output.

## Required tests

- `test_hard_dp_matches_bruteforce`
- `test_traceback_path_is_valid`
- `test_traceback_energy_equals_dp_value`
- `test_hard_dp_frames_have_value_heat`

---

# Issue 05: Implement Soft-DP solver

## Goal

Implement Boltzmann path distributions and their projections.

Notebook role: animate or snapshot classical probability condensation from beta 0 to high beta.

Reference: `docs/math_overview.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 05.

## Todo

- Add `src/pathspace_lab/solvers/soft_dp.py`.
- Implement `solve_soft_dp(problem, betas, paths=None) -> SolverTrace`.
- Enumerate paths if not provided.
- Compute path energies.
- Use log-sum-exp for numerical stability.
- Compute path probabilities for each beta.
- Compute cell marginals.
- Compute edge marginals.
- Compute observables:
  - expected energy,
  - entropy,
  - effective paths,
  - success probability,
  - residual energy.
- Add tests for beta zero and high beta behavior.

## Not todo

- Do not implement forward-backward dynamic programming yet.
- Do not optimize for large instances.
- Do not implement QA.
- Do not plot inside solver.

## Mathematical requirements

\[
P_\beta(p)=\frac{e^{-\beta E(p)}}{Z_\beta}
\]

\[
Z_\beta=\sum_pe^{-\beta E(p)}
\]

At \(\beta=0\):

\[
P_0(p)=\frac{1}{|\mathcal P|}
\]

As \(\beta\to\infty\), if the optimum is unique:

\[
P_\beta(p^*)\to1
\]

## Human acceptance criteria

- Soft-DP is clearly described as a classical thermal baseline.
- All probabilities are normalized.
- The solver outputs the same `Frame` structure as other solvers.
- The solver does not call plotting code.

## AI acceptance criteria

The AI agent must report:

- probability sum at beta 0,
- entropy at beta 0,
- success probability at max beta,
- whether cell marginals sum to `L`,
- tests run.

## Required tests

- `test_softdp_beta_zero_uniform`
- `test_softdp_probs_sum_to_one`
- `test_softdp_cell_marginals_sum_to_num_layers`
- `test_softdp_success_probability_increases_for_planted_instance`
- `test_softdp_expected_energy_decreases_with_beta_for_planted_instance`

---

# Issue 06: Implement schedules and Hamiltonian builders for feasible-subspace QA

## Goal

Build the static mathematical objects needed for QA without running time evolution yet.

Notebook role: show the schedule curves, Hamiltonian shapes, driver uniform residual, and config-graph size.

Reference: `docs/math_overview.md`, `docs/qa_proxy_notes.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 06.

## Todo

- Add `src/pathspace_lab/math/schedules.py`.
- Implement linear schedule:
  - `A(s) = 1 - s`
  - `B(s) = s`
- Add `src/pathspace_lab/math/hamiltonians.py`.
- Implement:
  - `build_problem_hamiltonian(energies)`
  - `build_path_config_graph(problem, paths)`
  - `build_laplacian_driver(config_graph)`
  - `normalize_hamiltonian`
- Add tests for Hermiticity, diagonal problem Hamiltonian, Laplacian properties.

## Not todo

- Do not implement time evolution yet.
- Do not implement transverse-field Ising QA.
- Do not implement QUBO penalty Hamiltonian.
- Do not optimize for large path spaces.

## Mathematical requirements

Problem Hamiltonian:

\[
H_P=\operatorname{diag}(E(p_1),\dots,E(p_N))
\]

Configuration graph:

- one node per complete path,
- edge between paths that differ by one local layer choice.

Driver Hamiltonian:

\[
H_D=L_{\text{cfg}}=D-A
\]

For a connected configuration graph, the uniform vector is a ground state of \(L_{\text{cfg}}\):

\[
L_{\text{cfg}}\mathbf 1=0
\]

## Human acceptance criteria

- Hamiltonian construction is separated from time evolution.
- The driver choice is documented as a feasible-subspace Laplacian driver.
- The code checks or asserts that the config graph is connected for MVP problems.
- The tests make the uniform-ground-state property explicit.

## AI acceptance criteria

The AI agent must report:

- matrix shapes,
- number of config graph nodes and edges,
- whether config graph is connected,
- whether `H_D @ uniform ≈ 0`,
- whether `H_P` diagonal equals path energies.

## Required tests

- `test_problem_hamiltonian_is_diagonal`
- `test_problem_hamiltonian_matches_energies`
- `test_config_graph_has_one_node_per_path`
- `test_laplacian_driver_is_symmetric`
- `test_laplacian_uniform_ground_state`

---

# Issue 07: Implement feasible-subspace QA time evolution

## Goal

Implement continuous-time feasible-subspace QA simulation.

Notebook role: run the first genuine QA-proxy trajectory and display QA marginal snapshots plus norm, energy, entropy, and success curves.

Reference: `docs/math_overview.md`, `docs/qa_proxy_notes.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 07.

## Todo

- Add `src/pathspace_lab/solvers/qa_feasible.py`.
- Add `QASimulationConfig` dataclass.
- Implement `solve_feasible_qa(problem, config, paths=None) -> SolverTrace`.
- Use sparse matrix exponential action for stepwise evolution.
- Normalize state defensively after each step.
- Compute per-frame:
  - amplitudes,
  - path probabilities,
  - cell marginals,
  - expected original energy,
  - residual energy,
  - entropy,
  - effective paths,
  - success probability,
  - state norm.
- Add optional spectral gap computation.
- Add tests for norm preservation and probability normalization.

## Not todo

- Do not add Qiskit.
- Do not add noise or open-system dynamics.
- Do not add QUBO constraints.
- Do not claim hardware equivalence.
- Do not tune performance beyond small MVP sizes.

## Mathematical requirements

Initial state:

\[
|\psi(0)\rangle=\frac{1}{\sqrt N}\sum_i|p_i\rangle
\]

Annealing Hamiltonian:

\[
H(s)=A(s)H_D+B(s)H_P
\]

Time step:

\[
|\psi(t+\Delta t)\rangle\approx e^{-iH(s_k)\Delta t}|\psi(t)\rangle
\]

Path probability:

\[
P_s(p_i)=|\psi_i(s)|^2
\]

Cell marginal:

\[
M_{\ell,v}^{QA}(s)=\sum_{p:(\ell,v)\in p}|\psi_p(s)|^2
\]

## Human acceptance criteria

- The solver clearly uses the same path list and energies as Soft-DP.
- Norm remains close to 1.
- The initial QA path distribution is uniform.
- The final QA distribution is not asserted to be optimal, only measured by success probability.
- The solver output can be consumed by the same visualizers as Soft-DP.

## AI acceptance criteria

The AI agent must report:

- initial path probability max/min,
- final norm error,
- final success probability,
- final expected energy,
- whether cell marginals sum to `L`,
- whether tests pass.

## Required tests

- `test_qa_initial_distribution_uniform`
- `test_qa_state_norm_preserved`
- `test_qa_path_probs_sum_to_one`
- `test_qa_cell_marginals_sum_to_num_layers`
- `test_qa_final_energy_observable_finite`
- `test_qa_gap_nonnegative_when_computed`

---

# Issue 08: Implement core heatmap visualizations

## Goal

Create basic plotting functions for DP values, Soft-DP marginals, and QA marginals.

Notebook role: replace temporary diagnostic heatmap snippets with official `pathspace_lab.viz.heatmaps` functions.

Reference: `docs/visualization_guide.md` and `docs/notebook_acceptance_guide.md`, Issue 08.

## Todo

- Add `src/pathspace_lab/viz/heatmaps.py`.
- Implement:
  - `plot_value_heatmap(frame, ax=None, title=None)`
  - `plot_cell_marginal_heatmap(frame, ax=None, title=None)`
  - `plot_trace_heatmap_grid(trace, frame_indices, ...)`
  - `compare_traces_by_progress(soft_trace, qa_trace, progress_values)`
  - `compare_traces_by_entropy(soft_trace, qa_trace, entropy_values)`
- Add minimal tests that functions return matplotlib axes or figures.

## Not todo

- Do not over-style.
- Do not use seaborn.
- Do not create animations yet unless easy.
- Do not couple plotting functions to concrete solver classes.

## Human acceptance criteria

- The same marginal plotter works for Soft-DP and QA.
- Axes labels are clear:
  - x-axis: layer,
  - y-axis: node,
  - color: probability or value.
- The title or colorbar distinguishes values from probabilities.
- Figures are readable in a notebook.

## AI acceptance criteria

The AI agent must include:

- a small screenshot or notebook cell output if working interactively, or
- a test that saves a figure to a temporary file.

## Required tests

- `test_plot_value_heatmap_returns_axes`
- `test_plot_cell_marginal_heatmap_returns_axes`
- `test_compare_traces_by_progress_runs`

---

# Issue 09: Implement problem graph plot and path highlighting

## Goal

Plot the layered DAG problem with optional highlighted paths and edge weights.

Notebook role: turn the problem introduction from a cost table into an actual graph picture with gold and decoy paths.

Reference: `docs/visualization_guide.md` and `docs/notebook_acceptance_guide.md`, Issue 09.

## Todo

- Add `src/pathspace_lab/viz/problem_plot.py`.
- Implement `plot_problem_graph(problem, highlight_path=None, edge_heat=None, node_heat=None, ax=None)`.
- Support:
  - node positions from `problem.state_coord`,
  - highlighted optimal path,
  - optional edge heat for Soft-DP flow later.
- Add basic plotting tests.

## Not todo

- Do not implement interactive graph widgets.
- Do not implement current visualization here.
- Do not add advanced layout algorithms.

## Human acceptance criteria

- The problem graph communicates layers and valid transitions.
- Source and sink do not dominate the visual layout.
- Highlighted path is easy to see.
- Function is reusable in the notebook introduction and summary.

## AI acceptance criteria

The AI agent must report:

- whether the function accepts a `Path` returned by `traceback_best_path`,
- whether it works with no highlighted path,
- whether it can save a figure without display.

---

# Issue 10: Implement top-k path probability streams and observable dashboard

## Goal

Plot the main comparison curves.

Notebook role: show the probability contest among optimal, decoy, and low-energy paths; then show energy/entropy/success/gap diagnostics.

Reference: `docs/visualization_guide.md` and `docs/notebook_acceptance_guide.md`, Issue 10.

## Todo

- Add `src/pathspace_lab/viz/streams.py`.
- Implement `plot_topk_path_probabilities(traces, paths, energies, top_k=8, ax=None)`.
- Add `src/pathspace_lab/viz/dashboard.py`.
- Implement `plot_observable_dashboard(traces)`.
- Include curves for:
  - expected energy,
  - residual energy,
  - entropy,
  - effective paths,
  - success probability,
  - QA spectral gap if available.
- Add tests that plotting functions run on small traces.

## Not todo

- Do not create interactive dashboards yet.
- Do not overcomplicate path labels.
- Do not assume every trace has every observable.

## Human acceptance criteria

- The stream plot can show Soft-DP and QA on comparable axes.
- The dashboard gracefully skips missing observables.
- The plot titles explain whether x-axis is beta progress or anneal progress.
- Top-k paths are selected deterministically, preferably by low energy plus optimum/decoy inclusion.

## AI acceptance criteria

The AI agent must report:

- which top-k paths are selected,
- whether all expected observables are present,
- which observables were skipped due to missing data.

---

# Issue 11: Implement Soft-DP flow and QA current visualization

## Goal

Add the most conceptually distinctive visualization: classical flow through the problem DAG versus quantum current through path space.

Notebook role: make the hidden geometry difference visible and explicit.

Reference: `docs/math_overview.md`, `docs/qa_proxy_notes.md`, `docs/visualization_guide.md`, and `docs/notebook_acceptance_guide.md`, Issue 11.

## Todo

- Add `src/pathspace_lab/viz/currents.py`.
- Implement:
  - `plot_softdp_edge_flow(problem, frame, ax=None)`
  - `plot_qa_path_current(problem, qa_frame, H, paths, max_nodes=30, ax=None)`
- Add `quantum_currents(psi, H, threshold)` to `math/observables.py` or `math/hamiltonians.py`.
- For small instances only, plot path-space graph nodes as complete paths.
- Add tests for current computation shape and antisymmetry.

## Not todo

- Do not force current visualization to support large `W^L` path spaces.
- Do not mix QA current with original DAG edge flow as if they were identical.
- Do not claim QA current flows along original problem edges.

## Mathematical requirements

Soft-DP edge flow:

\[
F(u\to v)=\sum_{p:(u\to v)\in p}P(p)
\]

Quantum current:

\[
J_{q\to p}=2\operatorname{Im}\left[\psi_p^*H_{pq}\psi_q\right]
\]

The notebook must state:

> Soft-DP flow lives on the original problem DAG. QA current lives on the graph of complete paths.

## Human acceptance criteria

- The visualization makes the different hidden spaces explicit.
- Labels say “original DAG flow” and “path-space current”.
- The current plot is optional if the path space is too large.
- There is no misleading visual overlay that implies QA current travels through DP cells.

## AI acceptance criteria

The AI agent must report:

- current matrix or dictionary size,
- threshold used,
- whether current antisymmetry holds approximately,
- whether large graphs are safely truncated.

---

# Issue 12: Consolidate the MVP notebook narrative

## Goal

Polish the notebook that has been growing throughout the previous issues into a clear, runnable, educational tutorial.

This is not the first notebook issue. It is the consolidation pass.

Reference: `docs/notebook_acceptance_guide.md`, Issue 12.

## Todo

- Create or update:
  - `notebooks/01_dp_softdp_qa_layered_path.ipynb`
  - `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- Use imports from `src/`, not copied code.
- Include sections:
  1. Introduction
  2. Create a small layered graph
  3. Hard DP as deterministic message passing
  4. Soft-DP as a classical thermal bridge
  5. Feasible-subspace QA
  6. Same projection, different dynamics
  7. Observable dashboard
  8. Flow vs current
  9. Summary and limitations
- Ensure notebook can run top to bottom.
- Add short conceptual text before and after each figure.

## Not todo

- Do not include large class definitions in notebook.
- Do not include long solver code in notebook.
- Do not include Qiskit/OpenJij sections in MVP notebook.
- Do not overclaim quantum realism.

## Notebook narrative skeleton

### 1. Introduction

Explain:

- one problem,
- three mechanisms,
- one shared projection.

Key sentence:

> The heatmaps share a coordinate system, not a mechanism.

### 2. Create a small layered graph

Explain:

- each path is a solution,
- costs are planted to create an optimal path and decoy path,
- the path space is small enough to enumerate.

### 3. Hard DP

Explain:

- DP stores best partial cost per state,
- it does not store path probabilities,
- traceback reconstructs the final path.

### 4. Soft-DP

Explain:

- replace min with a thermal distribution over paths,
- beta controls concentration,
- this is the classical probabilistic bridge.

### 5. Feasible-subspace QA

Explain:

- basis state equals complete feasible path,
- driver ground state is uniform over feasible paths,
- problem Hamiltonian is diagonal in path energies,
- dynamics are Hamiltonian evolution.

### 6. Same projection, different dynamics

Explain:

- compare Soft-DP and QA by progress,
- compare Soft-DP and QA by entropy,
- if heatmaps differ at matched entropy, QA is not merely a disguised temperature schedule.

### 7. Observable dashboard

Explain:

- energy and success can be compared,
- entropy measures concentration,
- spectral gap is QA-only.

### 8. Flow vs current

Explain:

- Soft-DP flow is nonnegative and lives on the original DAG,
- QA current is signed and lives on path-space graph,
- this is the key hidden geometry difference.

### 9. Summary and limitations

State:

- what was shown,
- what was not claimed,
- what future work will add.

## Human acceptance criteria

- Notebook reads like a coherent tutorial.
- A reader can understand the project without opening source files.
- The notebook has no hidden state or manual execution assumptions.
- The notebook has honest limitations.

## AI acceptance criteria

The AI agent must report:

- whether notebook runs from a clean kernel,
- total runtime on default parameters,
- any cells that are slow,
- generated figures list,
- any narrative gaps.

---

# Issue 13: Add notebook execution checks

## Goal

Ensure the final notebook remains executable.

## Todo

- Add script:

```text
scripts/execute_notebook.sh
```

- Use either `jupyter nbconvert --execute` or a pytest notebook plugin.
- Add a README command for notebook execution.
- Optionally add a CI job later.

## Not todo

- Do not require notebook execution for every small PR if it is too slow.
- Do not store huge executed outputs by default.
- Do not make CI dependent on optional Qiskit/OpenJij packages.

## Human acceptance criteria

- There is at least one command that runs the notebook top to bottom.
- Runtime is acceptable for MVP parameters.
- The notebook can be executed after a fresh install.

## AI acceptance criteria

The AI agent must report:

- exact execution command,
- runtime,
- success/failure,
- error traceback if failed.

---

# Issue 14: Add documentation pass and scientific guardrails

## Goal

Finalize the educational and mathematical documentation for MVP.

## Todo

- Fill `docs/math_overview.md`.
- Fill `docs/qa_proxy_notes.md`.
- Fill `docs/visualization_guide.md`.
- Add README links to these docs.
- Add notebook limitations section.
- Add glossary:
  - path space,
  - DP state,
  - configuration graph,
  - marginal,
  - probability current,
  - spectral gap,
  - feasible-subspace QA proxy.

## Not todo

- Do not add literature review yet.
- Do not add hardware QA claims.
- Do not add API docs for future extensions.

## Human acceptance criteria

- A mathematically careful reader can see exactly what is being simulated.
- The difference between feasible-subspace QA and transverse-field Ising QA is clear.
- Every visualization has a documented mathematical quantity.
- The README is accurate but not bloated.

## AI acceptance criteria

The AI agent must report:

- docs updated,
- formulas added,
- claims checked for overreach,
- any uncertain language removed or softened.

---

# Issue 15: MVP polish and release checklist

## Goal

Make the first release coherent and runnable.

## Todo

- Run full test suite.
- Run notebook from clean kernel.
- Check README commands.
- Check docs links.
- Check notebook narrative.
- Check default parameters for runtime.
- Add example output images if desired.
- Tag MVP release or create GitHub milestone.

## Not todo

- Do not add new features during polish.
- Do not add second problem type yet.
- Do not add QUBO/Qiskit/OpenJij yet.

## Human acceptance criteria

The following commands succeed:

```bash
pip install -e ".[dev]"
pytest
bash scripts/execute_notebook.sh
```

The notebook includes:

- planted layered DAG visualization,
- DP value heatmap,
- Soft-DP marginal heatmap,
- QA marginal heatmap,
- Soft-DP vs QA comparison,
- top-k path probability plot,
- energy/entropy/success dashboard,
- spectral gap plot,
- flow/current view,
- summary and limitations.

## AI acceptance criteria

The AI agent must produce a final MVP report:

```markdown
## MVP release report

### Commands run
- ...

### Test result
- ...

### Notebook execution result
- ...

### Figures generated
- ...

### Known limitations
- ...

### Suggested next issues
- ...
```

---

# MVP roadmap summary

## Build order

1. Issue 00: scaffold
2. Issue 00A: notebook harness and living tutorial skeleton
3. Issue 01: interfaces and traces
4. Issue 02: layered DAG problem
5. Issue 03: observables and marginals
6. Issue 04: hard DP
7. Issue 05: Soft-DP
8. Issue 06: QA Hamiltonian builders
9. Issue 07: QA time evolution
10. Issue 08: core heatmaps
11. Issue 09: problem graph plot
12. Issue 10: streams and dashboard
13. Issue 11: flow/current
14. Issue 12: notebook narrative consolidation
15. Issue 13: notebook execution checks
16. Issue 14: docs and guardrails
17. Issue 15: MVP polish

## Minimal vertical slice

If a faster demo is needed, implement only:

1. Issue 00
2. Issue 00A
3. Issue 01
4. Issue 02
5. Issue 03
6. Issue 04
7. Issue 05
8. Issue 06
9. Issue 07
10. One simple official heatmap plot from Issue 08

This gives a working DP vs Soft-DP vs QA comparison before polish, with notebook-visible output at every step.

---

# Future roadmap beyond MVP

## Phase 1: Add second path-DAG problem

Candidate:

- grid path,
- edit-distance-style alignment,
- sequence alignment.

Goal:

Show that the pipeline is not hardcoded to layered Viterbi paths.

## Phase 2: Add time-expanded cyclic graph support

Original graphs may have cycles. Lift them into a DAG:

\[
(t,v)
\]

This supports:

- fixed-horizon graph walks,
- Bellman-Ford-style shortest paths,
- finite-horizon MDPs.

## Phase 3: Add QUBO transverse-field QA extension

Add optional QUBO encoding with one-hot variables and penalty terms.

Visualize:

- feasible mass,
- invalid state mass,
- penalty energy,
- comparison with feasible-subspace QA.

## Phase 4: Add OpenJij SA/SQA sampler comparison

Use samplers for final distribution and benchmark-style plots.

Visualize:

- final energy histogram,
- success probability,
- residual energy.

## Phase 5: Add Qiskit gate-model appendix

Show Hamiltonian simulation and Trotterized evolution as a gate-model counterpart.

## Phase 6: Add hypergraph DP

Support DP where one subproblem depends on multiple subproblems:

\[
u \to (v_1, v_2, \dots, v_k)
\]

Needed for:

- matrix-chain multiplication,
- CKY parsing,
- interval DP,
- tree DP.

## Phase 7: Add open-system QA experiments

Explore:

- thermal effects,
- dephasing,
- Lindblad dynamics,
- freeze-out,
- schedule pauses,
- reverse annealing.

---

# Definition of MVP done

MVP is done when:

- tests pass,
- notebook runs top to bottom,
- docs explain the math and limitations,
- the three methods can be compared on the same visualization canvas,
- all claims are scientifically bounded,
- future extensions are clearly separated from MVP.

The MVP should feel like a clear glass machine: small, inspectable, and alive with moving probability light.


---

# Appendix A: Notebook-first human acceptance quick guide

For full details, see `docs/notebook_acceptance_guide.md`.

## Current situation after Issue 00

If Issue 00 is complete but the notebook is still only a placeholder, do **Issue 00A** next before continuing to Issue 01.

## Per-issue notebook expectation summary

| Issue | Notebook-visible outcome | Human visual check |
|---|---|---|
| 00A | Living notebook skeleton | Title, setup, status table, pending sections |
| 01 | Data contract demo | Toy `Frame` heatmap and printed `SolverTrace` summary |
| 02 | First real problem instance | Path count, optimal path printout, node-cost heatmap, gold/decoy metadata |
| 03 | Probability/marginal utilities | Uniform vs optimal-path marginal heatmaps, entropy/effective path values |
| 04 | Hard DP | DP value heatmap, DP optimum equals brute force |
| 05 | Soft-DP | Marginal snapshots over beta, entropy decreases, success increases |
| 06 | QA static objects | Schedule plot, Hamiltonian shapes, config graph size, `H_D @ uniform ≈ 0` |
| 07 | QA trajectory | QA marginal snapshots, norm near 1, energy/entropy/success curves |
| 08 | Official heatmap visualizers | Temporary heatmap snippets replaced by reusable viz functions |
| 09 | Problem graph plot | Layered graph with highlighted gold and optional decoy path |
| 10 | Streams/dashboard | Top-k path probability curves and observable dashboard |
| 11 | Flow/current | Soft-DP flow on original DAG, QA current on path-space graph |
| 12 | Narrative consolidation | Notebook reads as one coherent tutorial |
| 13 | Execution checks | Clean-kernel notebook execution command succeeds |
| 14 | Docs guardrails | Notebook links docs and avoids overclaiming |
| 15 | MVP polish | Final notebook is readable, runnable, and visually coherent |

## Human review ritual for every issue

1. Pull the branch.
2. Install/update editable package if needed:

```bash
pip install -e ".[dev]"
```

3. Run unit tests:

```bash
pytest
```

4. Open the notebook from a clean kernel.
5. Run all cells up to the newly implemented section.
6. Confirm the issue-specific visual outcome listed above.
7. Confirm that future sections are placeholders rather than broken cells.
8. Confirm that any changed math, QA claims, or visualization semantics are reflected in the corresponding docs.

## Machine notebook check

When dependencies are available, run:

```bash
jupyter nbconvert --execute --to notebook \
  notebooks/01_dp_softdp_qa_layered_path.ipynb \
  --output /tmp/pathspace_lab_notebook_check.ipynb
```

This is not a replacement for visual review. It is a smoke test that the notebook has no hidden state or broken future cells.
