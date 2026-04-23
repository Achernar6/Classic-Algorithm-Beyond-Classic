import numpy as np
import pytest

from pathspace_lab.problems.layered_dag import make_planted_layered_problem
from pathspace_lab.solvers.soft_dp import solve_soft_dp


def test_softdp_beta_zero_uniform():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    paths = problem.enumerate_paths()

    trace = solve_soft_dp(problem, betas=[0.0], paths=paths)
    probs = trace.frames[0].path_probs

    assert probs is not None
    assert np.allclose(probs, np.ones(len(paths)) / len(paths))
    assert np.isclose(trace.frames[0].observables["entropy"], np.log(len(paths)))


def test_softdp_probs_sum_to_one():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_soft_dp(problem, betas=np.linspace(0.0, 8.0, 9))

    for frame in trace.frames:
        assert frame.path_probs is not None
        assert np.isclose(frame.path_probs.sum(), 1.0)
        assert np.all(frame.path_probs >= 0.0)


def test_softdp_cell_marginals_sum_to_num_layers():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_soft_dp(problem, betas=[0.0, 2.0, 8.0])

    for frame in trace.frames:
        assert frame.cell_heat is not None
        assert frame.cell_heat.shape == problem.canvas_shape()
        assert np.allclose(frame.cell_heat.sum(axis=1), np.ones(problem.L))
        assert np.isclose(frame.cell_heat.sum(), problem.L)


def test_softdp_success_probability_increases_for_planted_instance():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_soft_dp(problem, betas=np.linspace(0.0, 8.0, 17))
    success = np.array(
        [frame.observables["success_probability"] for frame in trace.frames]
    )

    assert success[-1] > success[0]
    assert np.all(np.diff(success) >= -1e-12)


def test_softdp_expected_energy_decreases_with_beta_for_planted_instance():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_soft_dp(problem, betas=np.linspace(0.0, 8.0, 17))
    expected = np.array(
        [frame.observables["expected_energy"] for frame in trace.frames]
    )

    assert expected[-1] < expected[0]
    assert np.all(np.diff(expected) <= 1e-12)


def test_softdp_edge_marginals_sum_to_visible_edges_per_path():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    trace = solve_soft_dp(problem, betas=[0.0, 8.0])

    for frame in trace.frames:
        assert frame.edge_heat is not None
        assert np.isclose(sum(frame.edge_heat.values()), problem.L - 1)


def test_softdp_rejects_invalid_betas():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)

    with pytest.raises(ValueError, match="nonnegative"):
        solve_soft_dp(problem, betas=[-1.0])

    with pytest.raises(ValueError, match="must not be empty"):
        solve_soft_dp(problem, betas=[])
