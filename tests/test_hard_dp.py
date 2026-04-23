import numpy as np

from pathspace_lab.problems.layered_dag import make_planted_layered_problem
from pathspace_lab.solvers.hard_dp import solve_hard_dp, traceback_best_path


def test_hard_dp_matches_bruteforce():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    paths = problem.enumerate_paths()
    energies = np.array([problem.path_energy(path) for path in paths])

    trace = solve_hard_dp(problem)

    assert np.isclose(trace.metadata["best_value"], float(energies.min()))


def test_traceback_path_is_valid():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_hard_dp(problem)

    path = traceback_best_path(problem, trace)

    assert len(path) == problem.L
    assert path in problem.enumerate_paths()
    assert problem.path_cells(path) == list(path)


def test_traceback_energy_equals_dp_value():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_hard_dp(problem)

    path = traceback_best_path(problem, trace)

    assert np.isclose(problem.path_energy(path), trace.metadata["best_value"])


def test_hard_dp_frames_have_value_heat():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)

    trace = solve_hard_dp(problem)

    assert len(trace.frames) == problem.L
    for frame in trace.frames:
        assert frame.value_heat is not None
        assert frame.value_heat.shape == problem.canvas_shape()
        assert frame.cell_heat is None

    final_heat = trace.frames[-1].value_heat
    assert final_heat is not None
    assert np.all(np.isfinite(final_heat))
