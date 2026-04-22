# Pathspace Lab

Pathspace Lab is a small teaching project for comparing three mechanisms on the same layered path-DP problem:

- Hard DP as deterministic min-plus message passing.
- Soft-DP as a classical thermal distribution over complete paths.
- Feasible-subspace quantum annealing as coherent Hamiltonian evolution over feasible complete paths.

The MVP is not a quantum advantage demonstration, not a D-Wave hardware simulator, and not a generic QUBO transverse-field annealer. It is a visual and mathematical notebook workflow for learning how these mechanisms differ while sharing one projection canvas.

## Repository Layout

```text
pathspace-lab/
  docs/
    math_overview.md
    qa_proxy_notes.md
    visualization_guide.md
  notebooks/
    01_dp_softdp_qa_layered_path.ipynb
    paired/
      01_dp_softdp_qa_layered_path.py
  src/
    pathspace_lab/
      problems/
      solvers/
      math/
      viz/
      utils/
  tests/
```

## Setup

Install the package in editable mode with development tools:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest
```

Sync the paired notebook script and notebook:

```bash
python -m jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb
```

Later, once the notebook contains executable MVP content, run it top to bottom:

```bash
python -m jupyter nbconvert --execute notebooks/01_dp_softdp_qa_layered_path.ipynb --to notebook --output pathspace_lab_executed.ipynb
```

## Documentation Guardrails

The companion documents are part of the project specification:

- `docs/math_overview.md` defines formulas, shapes, and invariants.
- `docs/qa_proxy_notes.md` defines the allowed claims for the feasible-subspace QA proxy.
- `docs/visualization_guide.md` defines what each plot shows and what it must not imply.

If implementation changes math, solver semantics, QA wording, or visualization labels, update the matching document in the same change.
