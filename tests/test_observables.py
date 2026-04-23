import numpy as np
import pytest

from pathspace_lab.math.observables import (
    cell_marginals,
    edge_marginals_from_paths,
    effective_num_paths,
    expected_energy,
    normalize_probs,
    path_entropy,
    success_probability,
)
from pathspace_lab.problems.layered_dag import LayeredDAGProblem


def tiny_problem() -> LayeredDAGProblem:
    node_cost = np.array(
        [
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ]
    )
    edge_cost = np.zeros((2, 2, 2))
    return LayeredDAGProblem(node_cost=node_cost, edge_cost=edge_cost)


def test_normalize_probs_scales_positive_weights():
    normalized = normalize_probs([2.0, 3.0, 5.0])

    assert np.allclose(normalized, [0.2, 0.3, 0.5])
    assert np.isclose(normalized.sum(), 1.0)


def test_normalize_probs_rejects_invalid_weights():
    with pytest.raises(ValueError, match="nonnegative"):
        normalize_probs([0.5, -0.1])

    with pytest.raises(ValueError, match="positive total"):
        normalize_probs([0.0, 0.0])


def test_entropy_and_effective_paths_are_stable_with_zero_probabilities():
    delta = np.array([1.0, 0.0, 0.0])

    assert np.isclose(path_entropy(delta), 0.0)
    assert np.isclose(effective_num_paths(delta), 1.0)


def test_uniform_entropy_and_effective_paths_match_log_count():
    probs = np.ones(8) / 8

    assert np.isclose(path_entropy(probs), np.log(8))
    assert np.isclose(effective_num_paths(probs), 8.0)


def test_expected_energy_uses_normalized_probabilities():
    probs = np.array([1.0, 1.0, 2.0])
    energies = np.array([2.0, 4.0, 10.0])

    assert np.isclose(expected_energy(probs, energies), 6.5)


def test_success_probability_sums_multiple_optima():
    probs = np.array([0.2, 0.3, 0.5])
    energies = np.array([1.0, 1.0, 2.0])

    assert np.isclose(success_probability(probs, energies), 0.5)


def test_success_probability_accepts_explicit_optimum_tolerance():
    probs = np.array([0.2, 0.3, 0.5])
    energies = np.array([1.0, 1.0 + 5e-10, 2.0])

    assert np.isclose(success_probability(probs, energies, optimum_energy=1.0), 0.5)


def test_cell_marginals_for_uniform_paths_sum_by_layer_and_globally():
    problem = tiny_problem()
    paths = problem.enumerate_paths()
    probs = np.ones(len(paths)) / len(paths)

    marginals = cell_marginals(problem, paths, probs)

    assert marginals.shape == problem.canvas_shape()
    assert np.allclose(marginals.sum(axis=1), np.ones(problem.L))
    assert np.isclose(marginals.sum(), problem.L)
    assert np.allclose(marginals, 0.5)


def test_cell_marginals_for_delta_path_are_one_hot():
    problem = tiny_problem()
    paths = problem.enumerate_paths()
    probs = np.zeros(len(paths))
    target_index = 5
    probs[target_index] = 1.0

    marginals = cell_marginals(problem, paths, probs)

    assert np.isclose(marginals.sum(), problem.L)
    for ell, v in paths[target_index]:
        assert marginals[ell, v] == 1.0
    assert np.count_nonzero(marginals) == problem.L


def test_edge_marginals_from_paths_sum_to_num_visible_edges_per_path():
    problem = tiny_problem()
    paths = problem.enumerate_paths()
    probs = np.ones(len(paths)) / len(paths)

    edge_marginals = edge_marginals_from_paths(problem, paths, probs)

    assert np.isclose(sum(edge_marginals.values()), problem.L - 1)
    assert np.isclose(edge_marginals[((0, 0), (1, 0))], 0.25)
    assert np.isclose(edge_marginals[((1, 1), (2, 1))], 0.25)


def test_edge_marginals_omit_source_and_sink_from_padded_paths():
    problem = tiny_problem()
    visible_paths = problem.enumerate_paths()
    padded_paths = [
        (problem.source(), *path, problem.sink())
        for path in visible_paths
    ]
    probs = np.ones(len(padded_paths)) / len(padded_paths)

    edge_marginals = edge_marginals_from_paths(problem, padded_paths, probs)

    assert all(problem.source() not in edge for edge in edge_marginals)
    assert all(problem.sink() not in edge for edge in edge_marginals)
    assert np.isclose(sum(edge_marginals.values()), problem.L - 1)
