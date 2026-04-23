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
