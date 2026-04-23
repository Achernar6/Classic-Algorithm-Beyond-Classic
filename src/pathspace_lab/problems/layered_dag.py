"""Layered DAG path problem and planted teaching instances."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Any

import networkx as nx
import numpy as np

from pathspace_lab.problems.base import Path, State

SOURCE: str = "__source__"
SINK: str = "__sink__"


@dataclass(slots=True)
class LayeredDAGProblem:
    """Fully connected layered DAG with one visible choice per layer.

    A visible path is represented as ``((0, v0), (1, v1), ..., (L-1, vL))``.
    The graph also contains artificial source and sink states for DP-style
    algorithms; those hidden states are omitted from the heatmap canvas.
    """

    node_cost: np.ndarray
    edge_cost: np.ndarray
    name: str = "layered_dag"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.node_cost = np.asarray(self.node_cost, dtype=float)
        self.edge_cost = np.asarray(self.edge_cost, dtype=float)

        if self.node_cost.ndim != 2:
            raise ValueError("node_cost must have shape (L, W)")
        if self.edge_cost.ndim != 3:
            raise ValueError("edge_cost must have shape (L - 1, W, W)")

        expected_edge_shape = (self.L - 1, self.W, self.W)
        if self.edge_cost.shape != expected_edge_shape:
            raise ValueError(
                "edge_cost must have shape "
                f"{expected_edge_shape}, got {self.edge_cost.shape}"
            )

    @property
    def L(self) -> int:
        """Number of visible layers."""

        return int(self.node_cost.shape[0])

    @property
    def W(self) -> int:
        """Number of visible nodes per layer."""

        return int(self.node_cost.shape[1])

    def graph(self) -> nx.DiGraph:
        """Return the weighted layered DAG including source and sink."""

        graph = nx.DiGraph()
        graph.add_node(self.source())
        graph.add_node(self.sink())

        for ell in range(self.L):
            for v in range(self.W):
                graph.add_node((ell, v))

        for v in range(self.W):
            graph.add_edge(self.source(), (0, v), weight=float(self.node_cost[0, v]))

        for ell in range(self.L - 1):
            for u in range(self.W):
                for v in range(self.W):
                    graph.add_edge(
                        (ell, u),
                        (ell + 1, v),
                        weight=float(self.edge_cost[ell, u, v] + self.node_cost[ell + 1, v]),
                    )

        for v in range(self.W):
            graph.add_edge((self.L - 1, v), self.sink(), weight=0.0)

        return graph

    def source(self) -> State:
        """Return the artificial source state."""

        return SOURCE

    def sink(self) -> State:
        """Return the artificial sink state."""

        return SINK

    def states(self) -> list[State]:
        """Return all states, including hidden source and sink."""

        return [self.source(), *self._visible_states(), self.sink()]

    def edges(self) -> list[tuple[State, State, float]]:
        """Return weighted directed edges as ``(u, v, weight)`` tuples."""

        return [
            (u, v, float(data["weight"]))
            for u, v, data in self.graph().edges(data=True)
        ]

    def topological_order(self) -> list[State]:
        """Return a source-to-sink topological order."""

        return list(nx.topological_sort(self.graph()))

    def enumerate_paths(self, max_paths: int | None = None) -> list[Path]:
        """Enumerate visible complete paths in deterministic lexicographic order."""

        if max_paths is not None and max_paths < 0:
            raise ValueError("max_paths must be nonnegative or None")
        if max_paths == 0:
            return []

        paths: list[Path] = []
        for choices in product(range(self.W), repeat=self.L):
            paths.append(tuple((ell, int(v)) for ell, v in enumerate(choices)))
            if max_paths is not None and len(paths) >= max_paths:
                break
        return paths

    def path_energy(self, path: Path) -> float:
        """Return node-plus-transition energy for one visible path."""

        visible = self._visible_path(path)
        if len(visible) != self.L:
            raise ValueError(f"path must visit exactly {self.L} visible states")

        energy = 0.0
        for ell, v in visible:
            energy += float(self.node_cost[ell, v])
        for (ell, u), (next_ell, v) in zip(visible, visible[1:]):
            if next_ell != ell + 1:
                raise ValueError("path layers must increase by one")
            energy += float(self.edge_cost[ell, u, v])
        return energy

    def state_coord(self, state: State) -> tuple[float, float]:
        """Return plotting coordinates with visible layers on the x-axis."""

        if state == self.source():
            return (-1.0, (self.W - 1) / 2.0)
        if state == self.sink():
            return (float(self.L), (self.W - 1) / 2.0)

        ell, v = self._validate_visible_state(state)
        return (float(ell), float(v))

    def state_cell(self, state: State) -> tuple[int, int] | None:
        """Return the visible heatmap cell, omitting source and sink."""

        if state in {self.source(), self.sink()}:
            return None

        ell, v = self._validate_visible_state(state)
        return (ell, v)

    def canvas_shape(self) -> tuple[int, int]:
        """Return heatmap shape as ``(L, W)``."""

        return (self.L, self.W)

    def path_cells(self, path: Path) -> list[tuple[int, int]]:
        """Return the visible cells visited by ``path``."""

        return [self.state_cell(state) for state in self._visible_path(path)]  # type: ignore[list-item]

    def _visible_states(self) -> list[tuple[int, int]]:
        return [(ell, v) for ell in range(self.L) for v in range(self.W)]

    def _visible_path(self, path: Path) -> list[tuple[int, int]]:
        visible: list[tuple[int, int]] = []
        for state in path:
            if state in {self.source(), self.sink()}:
                continue
            visible.append(self._validate_visible_state(state))
        return visible

    def _validate_visible_state(self, state: State) -> tuple[int, int]:
        if (
            not isinstance(state, tuple)
            or len(state) != 2
            or not isinstance(state[0], int)
            or not isinstance(state[1], int)
        ):
            raise ValueError(f"invalid visible state: {state!r}")

        ell, v = state
        if not (0 <= ell < self.L and 0 <= v < self.W):
            raise ValueError(f"visible state out of bounds: {state!r}")
        return (ell, v)


def make_planted_layered_problem(
    L: int = 5,
    W: int = 3,
    seed: int | None = 7,
    name: str = "planted_layered_dag",
) -> LayeredDAGProblem:
    """Create a deterministic planted instance with a gold path and a decoy path.

    The decoy is deliberately cheap in the early prefix but pays a late trap
    transition. The gold path has a less attractive prefix but the best total
    energy. This creates useful structure for later DP, Soft-DP, and QA views.
    """

    if L < 2:
        raise ValueError("L must be at least 2")
    if W < 2:
        raise ValueError("W must be at least 2")

    rng = np.random.default_rng(seed)
    node_cost = 4.0 + rng.uniform(0.0, 0.4, size=(L, W))
    edge_cost = 3.0 + rng.uniform(0.0, 0.5, size=(L - 1, W, W))

    gold_nodes = tuple(int(v) for v in rng.integers(0, W, size=L))
    decoy_nodes = tuple((v + 1) % W for v in gold_nodes)
    trap_layer = max(1, min(L - 2, L // 2))

    for ell, v in enumerate(gold_nodes):
        node_cost[ell, v] = 1.35 if ell < trap_layer else 0.85
    for ell in range(L - 1):
        edge_cost[ell, gold_nodes[ell], gold_nodes[ell + 1]] = 0.18

    for ell, v in enumerate(decoy_nodes):
        if ell <= trap_layer:
            node_cost[ell, v] = 0.35
        else:
            node_cost[ell, v] = 1.25

    for ell in range(L - 1):
        if ell < trap_layer:
            edge_cost[ell, decoy_nodes[ell], decoy_nodes[ell + 1]] = 0.08
        elif ell == trap_layer:
            edge_cost[ell, decoy_nodes[ell], decoy_nodes[ell + 1]] = 4.50
        else:
            edge_cost[ell, decoy_nodes[ell], decoy_nodes[ell + 1]] = 0.25

    gold_path: Path = tuple((ell, v) for ell, v in enumerate(gold_nodes))
    decoy_path: Path = tuple((ell, v) for ell, v in enumerate(decoy_nodes))

    metadata: dict[str, Any] = {
        "seed": seed,
        "gold_nodes": gold_nodes,
        "decoy_nodes": decoy_nodes,
        "gold_path": gold_path,
        "decoy_path": decoy_path,
        "trap_layer": trap_layer,
        "design_note": (
            "Decoy has the cheaper early prefix; gold has the lower complete "
            "energy because the decoy pays a late transition penalty."
        ),
        "source_sink_edge_policy": (
            "source-to-first edges include first-layer node cost; layer edges "
            "include transition plus target node cost; sink edges have zero cost."
        ),
    }
    problem = LayeredDAGProblem(
        node_cost=node_cost,
        edge_cost=edge_cost,
        name=name,
        metadata=metadata,
    )

    metadata["gold_energy"] = problem.path_energy(gold_path)
    metadata["decoy_energy"] = problem.path_energy(decoy_path)
    metadata["gold_prefix_energy"] = _prefix_energy(problem, gold_path, trap_layer)
    metadata["decoy_prefix_energy"] = _prefix_energy(problem, decoy_path, trap_layer)

    return problem


def _prefix_energy(problem: LayeredDAGProblem, path: Path, stop_layer: int) -> float:
    """Energy of the visible prefix through ``stop_layer`` inclusive."""

    prefix = tuple(path[: stop_layer + 1])
    energy = 0.0
    for ell, v in prefix:
        energy += float(problem.node_cost[ell, v])
    for (ell, u), (_, v) in zip(prefix, prefix[1:]):
        energy += float(problem.edge_cost[ell, u, v])
    return energy


__all__ = [
    "LayeredDAGProblem",
    "SINK",
    "SOURCE",
    "make_planted_layered_problem",
]
