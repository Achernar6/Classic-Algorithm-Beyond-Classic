# Execution Log

This file stores completed issue execution notes that used to live inline in `DEVELOPMENT_ROADMAP.md`. The roadmap keeps issue specifications and short pointers here.

## Issue 00A: Notebook Harness and Living Tutorial Skeleton

### Implemented

- Replaced the placeholder notebook with a runnable living tutorial skeleton.
- Added setup imports, an import sanity print, a component status table, and markdown placeholders for the final narrative sections.
- Kept future sections markdown-only so they do not fail before backend implementation exists.

### Changed Files

- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `1 passed`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb`
- Result: passed.

### Deviations From Spec

- Added a small `src/` path discovery block in the notebook setup cell so clean-kernel execution works even before the package is installed editable in the active kernel environment.

### Pivot

- The initial nbconvert check failed because the executing kernel could not import `pathspace_lab`; the notebook harness was adjusted to find local `src/` from either the repository root or the `notebooks/` directory.

### Open Questions

- None.

## Issue 01: PathDPProblem Protocol and Shared Trace Dataclasses

### Implemented

- Added `PathDPProblem` as the shared structural protocol for path-DP problems.
- Added `State` and `Path` aliases to keep problem, solver, and visualization signatures consistent.
- Added `Frame` and `SolverTrace` dataclasses for solver snapshots and ordered method traces.
- Added notebook data-contract demo with a toy `Frame`, printed `SolverTrace` summary, and a small dummy heatmap.

### Field Purpose

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

### Later Issue Consumers

- Issue 02 consumes `PathDPProblem`, `State`, and `Path` for `LayeredDAGProblem`.
- Issues 04-07 consume `Frame` and `SolverTrace` for Hard DP, Soft-DP, and QA solver outputs.
- Issues 08-11 consume `Frame` and `SolverTrace` for heatmaps, streams, dashboards, flow, and current visualizations.

### Changed Files

- `src/pathspace_lab/problems/base.py`
- `src/pathspace_lab/problems/__init__.py`
- `src/pathspace_lab/utils/typing.py`
- `src/pathspace_lab/utils/__init__.py`
- `tests/test_problem_base.py`
- `tests/test_typing.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `6 passed`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb`
- Result: passed.

### Deviations From Spec

- No solver, concrete problem, or official plotting helper was added. The notebook heatmap remains a direct matplotlib toy diagnostic as requested by the Issue 01 acceptance guide.

### Pivot

- No business/product-level pivot. The main implementation choice was to keep trace fields optional so one dataclass can serve DP values, Soft-DP probabilities, and QA amplitudes without forcing solver-specific assumptions into the base protocol.

### Open Questions

- None.

## Issue 02: LayeredDAGProblem and Planted Instance Generator

### Implemented

- Added `LayeredDAGProblem` with dense fixed-width layer costs, artificial source/sink graph construction, visible-path enumeration, explicit path-energy calculation, coordinate/cell mapping, and source/sink omission from heatmaps.
- Added `make_planted_layered_problem` with deterministic seeded gold and decoy paths. The default instance has a decoy with cheaper early prefix (`1.21` vs gold prefix `3.91`) but worse complete energy (`8.46` vs gold `5.97`), so later probability views can show local attraction versus global optimality.
- Added notebook-visible Issue 02 section with path count, brute-force optimum, gold/decoy metadata, summary table, and a node-cost heatmap marked with `G` and `D`.

### Changed Files

- `src/pathspace_lab/problems/layered_dag.py`
- `src/pathspace_lab/problems/__init__.py`
- `tests/test_layered_dag.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest tests\test_layered_dag.py`
- Result: passed, `9 passed`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `15 passed`.
- Command: `$env:MPLBACKEND='Agg'; & 'C:\Users\ACH\miniconda3\python.exe' notebooks\paired\01_dp_softdp_qa_layered_path.py`
- Result: passed; printed `num paths: 243`, `expected: 243`, best/gold path `((0, 1), (1, 1), (2, 0), (3, 0), (4, 1))`, best/gold energy `5.97`, decoy energy `8.46`.
- Command: `$env:JUPYTER_ALLOW_INSECURE_WRITES='1'; & 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb --output-dir .pytest_cache`
- Result: passed after installing `ipykernel`, registering the `python3` kernel, and installing `pywin32` for Windows Jupyter support.

### Deviations From Spec

- `enumerate_paths()` returns visible paths only, matching the mathematical `W ** L` path space. `path_energy()` also accepts source/sink-padded paths for graph-algorithm compatibility.
- The local Windows environment requires `JUPYTER_ALLOW_INSECURE_WRITES=1` for nbconvert because Jupyter's secure connection-file ACL update receives `SetFileSecurity` access denied.

### Source/Sink Assumptions

- Source-to-first-layer edge weights include the first-layer node cost.
- Layer-to-layer edge weights include transition cost plus the target node cost.
- Sink edges have zero cost.

### Open Questions

- None.

## Issue 03: Common Observables and Marginal Utilities

### Implemented

- Added reusable probability utilities for normalization, entropy, effective path count, expected energy, and success probability.
- Added complete-path projection utilities for visible cell marginals and visible edge marginals.
- Added notebook-visible `From Paths to Probabilities` section using uniform and optimal-path distributions, including entropy, effective path count, expected energy, success probability, and side-by-side marginal heatmaps.
- Kept all reusable logic in `src/pathspace_lab/`; the notebook only calls package functions and displays diagnostics.

### Changed Files

- `src/pathspace_lab/math/observables.py`
- `src/pathspace_lab/math/__init__.py`
- `tests/test_observables.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`
- `docs/execution_log.md`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest tests\test_observables.py`
- Result: passed, `11 passed`.
- Command: `$env:MPLBACKEND='Agg'; & 'C:\Users\ACH\miniconda3\python.exe' notebooks\paired\01_dp_softdp_qa_layered_path.py`
- Result: passed; printed `uniform entropy: 5.493061443340546`, `log N: 5.493061443340548`, `uniform effective paths: 242.9999999999993`, `uniform marginal sum: 4.9999999999999964`, and `optimal marginal sum: 5.0`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb`
- Result: passed.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `26 passed`.
- Command: `$env:JUPYTER_ALLOW_INSECURE_WRITES='1'; & 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb --output-dir .pytest_cache`
- Result: passed; wrote `.pytest_cache\pathspace_lab_notebook_check.ipynb`.

### Deviations From Spec

- None. Edge marginals are returned as a dictionary keyed by visible state edges, which keeps the utility method-agnostic while matching the MVP layered-DAG visible edge semantics.

### Environment Notes

- Running Jupytext sync from the paired `.py` path hit a Windows path pairing mismatch. Syncing from `notebooks/01_dp_softdp_qa_layered_path.ipynb`, as documented in `docs/notebook_acceptance_guide.md`, succeeded.
- The local Windows nbconvert check still requires `JUPYTER_ALLOW_INSECURE_WRITES=1` because Jupyter cannot update some profile ACL permissions.

### Mathematical Sanity Checks

- Uniform entropy matches `log(N)` for `N = 243`.
- Uniform effective path count matches `N` within floating-point tolerance.
- Uniform and optimal-path cell marginal sums both equal `L = 5`.
- Tests cover zero-probability entropy stability, multiple-optimum success probability, normalization, cell marginal sums, and edge marginal sums.

### Downstream Consumers

- Soft-DP will use `normalize_probs`, `path_entropy`, `effective_num_paths`, `expected_energy`, `success_probability`, `cell_marginals`, and `edge_marginals_from_paths` after constructing Boltzmann path probabilities.
- Feasible-subspace QA will use the same observables after converting amplitudes to path probabilities via squared magnitudes.

### Open Questions

- None.

## Issue 04: Hard DP Solver

### Implemented

- Added deterministic min-plus Hard DP solver over the shared `PathDPProblem` DAG interface.
- Stored full distances, backpointers, source/sink, and final best value in `SolverTrace.metadata`.
- Emitted one `Frame` per visible layer with `value_heat` snapshots for future visualization.
- Added `traceback_best_path(problem, trace)` to recover the visible optimal path from backpointers.
- Activated the notebook Hard DP section with DP/brute-force comparison and a temporary direct matplotlib DP value heatmap.

### Changed Files

- `src/pathspace_lab/solvers/hard_dp.py`
- `src/pathspace_lab/solvers/__init__.py`
- `tests/test_hard_dp.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`
- `docs/execution_log.md`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest tests\test_hard_dp.py`
- Result: passed, `4 passed`.
- Command: `$env:MPLBACKEND='Agg'; & 'C:\Users\ACH\miniconda3\python.exe' notebooks\paired\01_dp_softdp_qa_layered_path.py`
- Result: passed; printed DP path `((0, 1), (1, 1), (2, 0), (3, 0), (4, 1))`, DP energy `5.969999999999999`, DP best value `5.970000000000001`, brute-force optimum `5.969999999999999`, and `matches brute force: True`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb`
- Result: passed.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `30 passed`.
- Command: `$env:JUPYTER_ALLOW_INSECURE_WRITES='1'; & 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb --output-dir .pytest_cache`
- Result: passed; wrote `.pytest_cache\pathspace_lab_notebook_check.ipynb`.

### Deviations From Spec

- None. The solver uses the graph/topological/state-cell protocol rather than indexing concrete layered-DAG arrays directly.

### Mathematical Sanity Checks

- `D(source) = 0` in solver initialization.
- Each relaxation uses `D(v) = min_u D(u) + w(u, v)` over outgoing DAG edges in topological order.
- Final DP best value matches brute-force enumeration within floating-point tolerance.
- Traceback path energy equals the DP sink value.
- Final frame `value_heat` is finite over all visible cells for the planted instance.

### Environment Notes

- The local Windows nbconvert check still requires `JUPYTER_ALLOW_INSECURE_WRITES=1` because Jupyter cannot update some profile ACL permissions.

### Open Questions

- None.

## Issue 05: Soft-DP Solver

### Implemented

- Added enumerative Soft-DP solver that turns complete-path energies into Boltzmann probabilities for each beta.
- Used a numerically stable log-sum-exp calculation for path probabilities.
- Reused common observables for expected energy, residual energy, entropy, effective path count, success probability, cell marginals, and edge marginals.
- Returned the shared `SolverTrace`/`Frame` structure with `cell_heat`, `path_probs`, `edge_heat`, aligned `paths`, and aligned `energies`.
- Activated the notebook Soft-DP section with beta snapshots, entropy/success curves, and top low-energy path probabilities including optimal and decoy paths.

### Changed Files

- `src/pathspace_lab/solvers/soft_dp.py`
- `src/pathspace_lab/solvers/__init__.py`
- `tests/test_soft_dp.py`
- `notebooks/paired/01_dp_softdp_qa_layered_path.py`
- `notebooks/01_dp_softdp_qa_layered_path.ipynb`
- `DEVELOPMENT_ROADMAP.md`
- `docs/execution_log.md`

### Validation Run

- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest tests\test_soft_dp.py`
- Result: passed, `7 passed`.
- Command: `$env:MPLBACKEND='Agg'; & 'C:\Users\ACH\miniconda3\python.exe' notebooks\paired\01_dp_softdp_qa_layered_path.py`
- Result: passed; printed `beta=0 prob sum: 1.0`, `beta=max prob sum: 1.0`, `beta=0 entropy: 5.493061443340547`, `beta=max success: 0.9193250609975623`, `beta=max expected energy: 5.994850692655994`, `optimal path probability at beta=max: 0.9193250609975614`, `decoy path probability at beta=max: 2.052688360563381e-09`, and `beta=max marginal sum: 5.0`.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb`
- Result: passed.
- Command: `& 'C:\Users\ACH\miniconda3\python.exe' -m pytest`
- Result: passed, `37 passed`.
- Command: `$env:JUPYTER_ALLOW_INSECURE_WRITES='1'; & 'C:\Users\ACH\miniconda3\python.exe' -m jupyter nbconvert --execute --to notebook notebooks/01_dp_softdp_qa_layered_path.ipynb --output pathspace_lab_notebook_check.ipynb --output-dir .pytest_cache`
- Result: passed; wrote `.pytest_cache\pathspace_lab_notebook_check.ipynb`.

### Deviations From Spec

- None. The solver uses an internal NumPy log-sum-exp helper instead of importing `scipy.special.logsumexp`; the mathematical computation is the same.

### Environment Notes

- Importing `scipy.special.logsumexp` triggered a local SciPy/Numpy `MemoryError` during test collection. To keep Issue 05 stable and lightweight, the solver now uses a small NumPy-only log-sum-exp helper.
- The local Windows nbconvert check still requires `JUPYTER_ALLOW_INSECURE_WRITES=1` because Jupyter cannot update some profile ACL permissions.

### Mathematical Sanity Checks

- At beta `0`, path probabilities are uniform and entropy matches `log(N)` for `N = 243`.
- Every tested Soft-DP frame has path probabilities summing to `1`.
- Cell marginals sum to one per layer and `L = 5` globally.
- Edge marginals sum to `L - 1 = 4`.
- On the planted instance, success probability increases with beta and expected energy decreases with beta.
- At beta `8`, success probability is approximately `0.9193`; the decoy path probability is approximately `2.05e-09`.

### Open Questions

- None.
