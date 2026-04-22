# Notebook Acceptance Guide

This guide makes the MVP notebook a first-class deliverable from the beginning of development.

The project should not wait until all solvers are implemented before the notebook becomes useful. Each issue should add a small runnable notebook section, a visible output, or a narrative checkpoint.

## Core policy

1. The notebook is a living tutorial, not a final wrapper.
2. Each issue must include notebook-side work unless the issue explicitly says otherwise.
3. Notebook code should import reusable logic from `src/pathspace_lab/`.
4. Notebook cells may use tiny one-off diagnostic plotting code before official visualizers exist, but those cells should be replaced by `pathspace_lab.viz` functions once Issue 08 and later plotting issues land.
5. Future sections may appear as markdown placeholders, but they must not contain runnable code that fails.
6. A human reviewer should be able to run the notebook up to the current implemented section and see a concrete result.
7. The paired script is the review source. The `.ipynb` is the user-facing artifact.

## Paired notebook workflow

Recommended files:

```text
notebooks/01_dp_softdp_qa_layered_path.ipynb
notebooks/paired/01_dp_softdp_qa_layered_path.py
```

Use Jupytext percent format, where cells are represented with `# %%` and markdown cells with `# %% [markdown]`.

Recommended human workflow:

```bash
# After editing the paired script, sync to ipynb if needed.
jupytext --sync notebooks/01_dp_softdp_qa_layered_path.ipynb

# Execute the notebook as a machine check.
jupyter nbconvert --execute --to notebook \
  notebooks/01_dp_softdp_qa_layered_path.ipynb \
  --output /tmp/pathspace_lab_notebook_check.ipynb
```

Interactive human review is still required because the MVP is visual and educational.

## Notebook structure over time

The final notebook should contain these sections:

1. Introduction and mental model
2. Setup and reproducibility
3. Create a planted layered path problem
4. Hard DP as deterministic message passing
5. Soft-DP as classical thermal condensation
6. Feasible-subspace QA
7. Same projection, different dynamics
8. Observable dashboard
9. Flow vs current
10. Summary, limitations, and roadmap

Early in development, later sections should be markdown placeholders saying `Pending implementation` rather than broken code.

## Human acceptance by issue

### Issue 00A: Notebook harness after scaffold

This issue should be done immediately after the current Issue 00 scaffold, because the current notebook is only a placeholder.

Notebook changes:

- Create the paired notebook script with all final section headings.
- Add a setup cell that imports standard dependencies and `pathspace_lab`.
- Add a status table showing which MVP components are implemented or pending.
- Add markdown explaining that the notebook will grow issue by issue.

Human should run:

```python
import pathspace_lab
print("Pathspace Lab import OK")
```

Expected visible result:

- A notebook title.
- A short introduction.
- A status table with rows such as `LayeredDAGProblem`, `Hard DP`, `Soft-DP`, `QA`, `Visualizers`.
- No errors from a clean kernel.

Acceptance:

- The notebook is no longer an empty placeholder.
- Future sections are present as markdown only.
- The notebook can run top to bottom even though most sections are pending.

---

### Issue 01: Interfaces and trace dataclasses

Notebook changes:

- Add a small section called `The data contract`.
- Import `Frame` and `SolverTrace`.
- Construct a toy `Frame` with a small `cell_heat` array.
- Display the toy heatmap with direct `matplotlib` code.

Human should run:

```python
from pathspace_lab.utils.typing import Frame, SolverTrace
import numpy as np

frame = Frame(progress=0.0, label="toy", cell_heat=np.ones((2, 3)) / 3)
trace = SolverTrace(method="toy", problem_name="toy", frames=[frame])
print(trace.method, len(trace.frames), trace.frames[0].cell_heat.shape)
```

Expected visible result:

- Printed output like `toy 1 (2, 3)`.
- A tiny 2 by 3 heatmap.
- Markdown explaining that future DP, Soft-DP, and QA solvers will all return this trace shape.

Acceptance:

- The notebook demonstrates the interface contract before any real solver exists.
- The heatmap is explicitly labeled as a dummy data-contract example.

---

### Issue 02: LayeredDAGProblem and planted generator

Notebook changes:

- Add a problem construction section.
- Create a seeded `LayeredDAGProblem` with small default size, e.g. `L=5`, `W=3` or `L=6`, `W=4`.
- Enumerate paths and compute energies.
- Display a compact summary table.
- Display node-cost heatmap with layers on the x-axis and nodes on the y-axis.
- Print the brute-force optimal path and energy.
- Print or display the planted gold path and decoy path if metadata is available.

Human should run:

```python
from pathspace_lab.problems.layered_dag import make_planted_layered_problem

problem = make_planted_layered_problem(L=5, W=3, seed=7)
paths = problem.enumerate_paths()
energies = np.array([problem.path_energy(p) for p in paths])

print("num paths:", len(paths))
print("expected:", problem.W ** problem.L)
print("best energy:", energies.min())
print("best path:", paths[int(energies.argmin())])
print("metadata:", getattr(problem, "metadata", {}))
```

Expected visible result:

- `num paths` equals `W ** L`.
- A node-cost heatmap appears.
- The optimal path and energy are printed.
- The planted gold and decoy paths are visible in metadata or printed notes.

Acceptance:

- A human can tell what problem instance is being solved.
- The notebook explains that each complete path is one feasible solution.
- Source and sink do not appear in the main heatmap.

---

### Issue 03: Observables and marginals

Notebook changes:

- Add a section called `From paths to probabilities`.
- Build two toy distributions over paths:
  - uniform distribution,
  - delta distribution on the optimal path.
- Compute entropy, effective path count, expected energy, success probability, and cell marginals.
- Plot uniform and optimal-path marginal heatmaps side by side.

Human should run:

```python
from pathspace_lab.math.observables import (
    path_entropy,
    effective_num_paths,
    expected_energy,
    success_probability,
    cell_marginals,
)

N = len(paths)
uniform = np.ones(N) / N
opt = np.zeros(N)
opt[int(energies.argmin())] = 1.0

print("uniform entropy:", path_entropy(uniform))
print("log N:", np.log(N))
print("uniform effective paths:", effective_num_paths(uniform))
print("uniform marginal sum:", cell_marginals(problem, paths, uniform).sum())
print("optimal marginal sum:", cell_marginals(problem, paths, opt).sum())
```

Expected visible result:

- Uniform entropy is close to `log(N)`.
- Uniform effective paths is close to `N`.
- Cell marginal sums equal `L`.
- Uniform marginal heatmap looks evenly spread across choices.
- Optimal marginal heatmap looks like a single bright path through the canvas.

Acceptance:

- The notebook makes clear that marginals are projections of path distributions.
- The reader sees the exact visual quantity later used by Soft-DP and QA.

---

### Issue 04: Hard DP solver

Notebook changes:

- Add or activate the `Hard DP` section.
- Run `solve_hard_dp(problem)`.
- Print DP best value and brute-force best value.
- Print the traceback path.
- Plot the final DP value heatmap with direct matplotlib code if official heatmap visualizers are not implemented yet.

Human should run:

```python
from pathspace_lab.solvers.hard_dp import solve_hard_dp, traceback_best_path

dp_trace = solve_hard_dp(problem)
dp_path = traceback_best_path(problem, dp_trace)
print("DP path:", dp_path)
print("DP energy:", problem.path_energy(dp_path))
print("Brute force optimum:", energies.min())
```

Expected visible result:

- DP energy equals brute-force optimum.
- A DP value heatmap appears.
- Markdown states that DP values are not probabilities.

Acceptance:

- The notebook demonstrates deterministic message passing.
- The human can verify that DP solves the planted instance.
- The notebook warns that `value_heat` and probability heatmaps have different meanings.

---

### Issue 05: Soft-DP solver

Notebook changes:

- Activate the `Soft-DP` section.
- Run `solve_soft_dp(problem, betas, paths=paths)`.
- Show marginal heatmaps at beta = 0, middle beta, and max beta.
- Plot entropy and success probability versus beta progress.
- Plot or print top path probabilities for optimal and decoy paths.

Human should run:

```python
from pathspace_lab.solvers.soft_dp import solve_soft_dp

betas = np.linspace(0.0, 8.0, 81)
soft_trace = solve_soft_dp(problem, betas=betas, paths=paths)

first = soft_trace.frames[0]
last = soft_trace.frames[-1]
print("beta=0 prob sum:", first.path_probs.sum())
print("beta=max prob sum:", last.path_probs.sum())
print("beta=0 entropy:", first.observables["entropy"])
print("beta=max success:", last.observables["success_probability"])
```

Expected visible result:

- beta 0 marginal heatmap is broad or uniform-looking.
- high beta marginal heatmap concentrates around the best path.
- entropy decreases as beta increases.
- success probability increases on the planted instance.

Acceptance:

- The notebook explains Soft-DP as a classical thermal baseline.
- The reader can see probability condensation without any quantum claims.

---

### Issue 06: QA schedules and Hamiltonian builders

Notebook changes:

- Add a section called `Building the QA proxy`.
- Build `H_P`, configuration graph, and Laplacian driver `H_D`.
- Plot schedule curves `A(s)` and `B(s)`.
- Print Hamiltonian shapes, config graph node count, edge count, and connectedness.
- Check and print `||H_D @ uniform||`.
- Show a small matrix visualization or sparsity plot for `H_D` and diagonal of `H_P`.

Human should run:

```python
from pathspace_lab.math.hamiltonians import (
    build_problem_hamiltonian,
    build_path_config_graph,
    build_laplacian_driver,
)

H_P = build_problem_hamiltonian(energies)
G_cfg = build_path_config_graph(problem, paths)
H_D = build_laplacian_driver(G_cfg)

uniform_vec = np.ones(len(paths)) / np.sqrt(len(paths))
print("H_P shape:", H_P.shape)
print("H_D shape:", H_D.shape)
print("config nodes:", G_cfg.number_of_nodes())
print("config edges:", G_cfg.number_of_edges())
print("driver uniform residual:", np.linalg.norm(H_D @ uniform_vec))
```

Expected visible result:

- Shapes are `(N, N)`.
- Config graph has one node per path.
- Driver uniform residual is close to zero.
- Schedule plot shows `A(s)` decreasing and `B(s)` increasing.

Acceptance:

- The notebook explains that the driver acts in path space, not on the original DAG.
- The human can verify the uniform feasible initial state property.

---

### Issue 07: Feasible-subspace QA time evolution

Notebook changes:

- Activate the `Feasible-subspace QA` section.
- Run `solve_feasible_qa` on a small default instance.
- Display QA marginal heatmaps at several anneal fractions.
- Plot norm error, expected energy, entropy, and success probability.
- Show spectral gap if available.

Human should run:

```python
from pathspace_lab.solvers.qa_feasible import solve_feasible_qa, QASimulationConfig

qa_config = QASimulationConfig(total_time=20.0, steps=120, compute_gap=True)
qa_trace = solve_feasible_qa(problem, config=qa_config, paths=paths)

print("initial prob min/max:", qa_trace.frames[0].path_probs.min(), qa_trace.frames[0].path_probs.max())
print("final prob sum:", qa_trace.frames[-1].path_probs.sum())
print("final norm:", qa_trace.frames[-1].observables["state_norm"])
print("final success:", qa_trace.frames[-1].observables["success_probability"])
```

Expected visible result:

- Initial path probabilities are uniform.
- Norm remains approximately 1.
- QA marginal heatmaps evolve over anneal fraction.
- The final success probability is reported, not promised to be 1.

Acceptance:

- The notebook calls this a feasible-subspace QA proxy.
- The notebook does not claim hardware equivalence or quantum advantage.
- The reader sees that QA is a continuous Hamiltonian process over complete paths.

---

### Issue 08: Core heatmap visualizers

Notebook changes:

- Replace temporary heatmap snippets with `pathspace_lab.viz.heatmaps` functions.
- Add side-by-side Soft-DP vs QA marginal comparisons by progress and by entropy.

Expected visible result:

- DP value heatmap has clear value labeling.
- Soft-DP and QA marginal heatmaps use probability labeling.
- Comparison plots make clear that the same canvas does not mean the same mechanism.

Acceptance:

- Notebook visuals are cleaner than temporary diagnostics.
- Axis and colorbar labels match `docs/visualization_guide.md`.

---

### Issue 09: Problem graph plot

Notebook changes:

- Replace or supplement the cost heatmap with a graph plot.
- Highlight the optimal path.
- If generator metadata contains a decoy path, optionally highlight it with a distinct style.

Expected visible result:

- A layered DAG with source, layers, and sink.
- The gold path is visually obvious.
- The decoy path is visible or described.

Acceptance:

- A human can understand the input graph before reading solver sections.

---

### Issue 10: Top-k streams and dashboard

Notebook changes:

- Add top-k path probability plot for Soft-DP and QA.
- Add observable dashboard.
- Include expected energy, entropy, effective paths, success probability, and QA gap when available.

Expected visible result:

- The optimal path and decoy path can be tracked over progress.
- Soft-DP curves look like thermal reweighting.
- QA curves may be non-monotonic or otherwise visibly different.

Acceptance:

- The notebook uses curves to clarify, not to claim speedup.
- Missing observables are skipped gracefully.

---

### Issue 11: Flow and current visualization

Notebook changes:

- Add `Flow vs current` section.
- Plot Soft-DP edge flow on the original DAG.
- Plot QA current on a truncated path-space graph.

Expected visible result:

- Soft-DP flow is shown on the original DAG.
- QA current is shown on the graph of complete paths.
- Captions explicitly state that these are different hidden spaces.

Acceptance:

- No plot implies QA current flows through original DP cells.
- This section becomes the conceptual centerpiece for information-transfer differences.

---

### Issue 12: Notebook narrative consolidation

By this point the notebook should already exist and contain working partial sections. Issue 12 is not the first notebook issue. It is the consolidation pass.

Notebook changes:

- Remove outdated temporary diagnostic code or clearly label it as diagnostic.
- Ensure every section has before-figure and after-figure text.
- Ensure claims align with `docs/math_overview.md`, `docs/qa_proxy_notes.md`, and `docs/visualization_guide.md`.
- Ensure the notebook reads as a coherent tutorial.

Expected visible result:

- A clean, educational notebook from top to bottom.
- No placeholder sections except future roadmap notes.

Acceptance:

- A reader can understand the MVP without opening source code.
- The notebook is scientifically bounded and visually coherent.

---

### Issue 13: Notebook execution checks

Notebook changes:

- Add no new conceptual content unless needed to make execution robust.
- Add or validate `scripts/execute_notebook.sh`.

Human should run:

```bash
bash scripts/execute_notebook.sh
```

Expected visible result:

- A completed executed notebook artifact or success message.
- No hidden state assumptions.

Acceptance:

- Clean-kernel execution succeeds.
- Runtime is acceptable for MVP parameters.

---

### Issue 14: Documentation and scientific guardrails

Notebook changes:

- Add links from notebook to:
  - `docs/math_overview.md`
  - `docs/qa_proxy_notes.md`
  - `docs/visualization_guide.md`
- Add limitations section.
- Ensure terminology matches docs.

Expected visible result:

- Notebook clearly states what is shown and what is not claimed.

Acceptance:

- No hardware-equivalence or quantum-speedup overclaim appears.

---

### Issue 15: MVP polish

Notebook changes:

- Final execution.
- Final visual readability pass.
- Optional thumbnail or example output images.

Human should check:

- Does every figure have a caption or nearby explanation?
- Can a reader distinguish values, probabilities, flows, and currents?
- Are gold path and decoy path used in the story?
- Does the notebook run top to bottom from a clean kernel?

Acceptance:

- The notebook is the MVP artifact, not just a demo script.
