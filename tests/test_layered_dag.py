import networkx as nx
import numpy as np

from pathspace_lab.problems.layered_dag import (
    SINK,
    SOURCE,
    LayeredDAGProblem,
    make_planted_layered_problem,
)


def tiny_problem() -> LayeredDAGProblem:
    node_cost = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]
    )
    edge_cost = np.array(
        [
            [[0.1, 0.2], [0.3, 0.4]],
            [[0.5, 0.6], [0.7, 0.8]],
        ]
    )
    return LayeredDAGProblem(node_cost=node_cost, edge_cost=edge_cost)


def test_layered_graph_is_dag():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)

    assert nx.is_directed_acyclic_graph(problem.graph())
    assert problem.topological_order()[0] == SOURCE
    assert problem.topological_order()[-1] == SINK


def test_path_count_is_w_power_l():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)

    assert len(problem.enumerate_paths()) == problem.W**problem.L
    assert problem.enumerate_paths(max_paths=0) == []
    assert len(problem.enumerate_paths(max_paths=4)) == 4


def test_each_path_visits_one_node_per_layer():
    problem = make_planted_layered_problem(L=4, W=3, seed=11)

    for path in problem.enumerate_paths():
        cells = problem.path_cells(path)
        assert len(cells) == problem.L
        assert [ell for ell, _ in cells] == list(range(problem.L))
        assert all(0 <= v < problem.W for _, v in cells)


def test_path_energy_matches_manual_calculation():
    problem = tiny_problem()
    path = ((0, 1), (1, 0), (2, 1))

    expected = (
        problem.node_cost[0, 1]
        + problem.node_cost[1, 0]
        + problem.node_cost[2, 1]
        + problem.edge_cost[0, 1, 0]
        + problem.edge_cost[1, 0, 1]
    )

    assert problem.path_energy(path) == expected


def test_path_energy_accepts_source_sink_padded_paths():
    problem = tiny_problem()
    visible_path = ((0, 0), (1, 1), (2, 0))
    padded_path = (problem.source(), *visible_path, problem.sink())

    assert problem.path_energy(padded_path) == problem.path_energy(visible_path)


def test_state_cell_omits_source_and_sink():
    problem = tiny_problem()

    assert problem.state_cell(problem.source()) is None
    assert problem.state_cell(problem.sink()) is None
    assert problem.state_cell((1, 0)) == (1, 0)
    assert problem.canvas_shape() == (3, 2)


def test_graph_edge_weights_match_path_energy_policy():
    problem = tiny_problem()
    path = ((0, 1), (1, 0), (2, 1))
    graph_path = (problem.source(), *path, problem.sink())
    graph = problem.graph()
    graph_energy = sum(
        graph.edges[u, v]["weight"] for u, v in zip(graph_path, graph_path[1:])
    )

    assert np.isclose(graph_energy, problem.path_energy(path))


def test_planted_generator_metadata_includes_gold_and_decoy():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)

    assert problem.metadata["gold_path"] != problem.metadata["decoy_path"]
    assert len(problem.metadata["gold_path"]) == problem.L
    assert len(problem.metadata["decoy_path"]) == problem.L
    assert problem.metadata["gold_energy"] < problem.metadata["decoy_energy"]


def test_planted_decoy_prefix_is_cheaper_but_not_globally_best():
    problem = make_planted_layered_problem(L=5, W=3, seed=7)
    paths = problem.enumerate_paths()
    energies = np.array([problem.path_energy(path) for path in paths])
    best_path = paths[int(energies.argmin())]

    assert best_path == problem.metadata["gold_path"]
    assert problem.metadata["decoy_prefix_energy"] < problem.metadata["gold_prefix_energy"]
    assert problem.metadata["gold_energy"] == float(energies.min())
