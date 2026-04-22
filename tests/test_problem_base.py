import networkx as nx

from pathspace_lab.problems.base import Path, PathDPProblem, State


class TinyProblem:
    name = "tiny"

    def graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        graph.add_weighted_edges_from([("source", "sink", 1.0)])
        return graph

    def source(self) -> State:
        return "source"

    def sink(self) -> State:
        return "sink"

    def states(self) -> list[State]:
        return ["source", "sink"]

    def edges(self) -> list[tuple[State, State, float]]:
        return [("source", "sink", 1.0)]

    def topological_order(self) -> list[State]:
        return ["source", "sink"]

    def enumerate_paths(self, max_paths: int | None = None) -> list[Path]:
        paths = [("source", "sink")]
        return paths if max_paths is None else paths[:max_paths]

    def path_energy(self, path: Path) -> float:
        assert path == ("source", "sink")
        return 1.0

    def state_coord(self, state: State) -> tuple[float, float]:
        return (0.0, 0.0) if state == "source" else (1.0, 0.0)

    def state_cell(self, state: State) -> tuple[int, int] | None:
        return None

    def canvas_shape(self) -> tuple[int, int]:
        return (0, 0)

    def path_cells(self, path: Path) -> list[tuple[int, int]]:
        return []


def summarize_problem(problem: PathDPProblem) -> tuple[str, int, float]:
    path = problem.enumerate_paths()[0]
    return problem.name, len(problem.states()), problem.path_energy(path)


def test_path_dp_problem_protocol_can_type_structural_problem():
    assert summarize_problem(TinyProblem()) == ("tiny", 2, 1.0)


def test_path_alias_is_tuple_of_states():
    path: Path = ("source", "sink")

    assert path[0] == "source"
    assert path[-1] == "sink"
