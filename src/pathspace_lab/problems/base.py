"""Shared problem protocol for path-DP examples."""

from __future__ import annotations

from typing import Any, Protocol

import networkx as nx

State = Any
"""A problem state, such as a layer-node pair or artificial source/sink."""

Path = tuple[State, ...]
"""A complete feasible solution represented as an ordered tuple of states."""


class PathDPProblem(Protocol):
    """Protocol consumed by solvers, observables, and visualizers.

    A path-DP problem exposes a directed problem graph, a finite set of complete
    feasible paths, path energies, and a projection from states/paths onto a
    notebook heatmap canvas.
    """

    name: str
    """Human-readable problem name used in traces and figure titles."""

    def graph(self) -> nx.DiGraph:
        """Return the directed problem graph."""
        ...

    def source(self) -> State:
        """Return the artificial or real source state."""
        ...

    def sink(self) -> State:
        """Return the artificial or real sink state."""
        ...

    def states(self) -> list[State]:
        """Return all graph states, including source/sink when present."""
        ...

    def edges(self) -> list[tuple[State, State, float]]:
        """Return weighted directed edges as ``(u, v, weight)`` tuples."""
        ...

    def topological_order(self) -> list[State]:
        """Return a topological ordering for one forward DP pass."""
        ...

    def enumerate_paths(self, max_paths: int | None = None) -> list[Path]:
        """Return complete feasible paths, optionally capped by ``max_paths``."""
        ...

    def path_energy(self, path: Path) -> float:
        """Return the total energy/cost of one complete path."""
        ...

    def state_coord(self, state: State) -> tuple[float, float]:
        """Return plotting coordinates for a graph state."""
        ...

    def state_cell(self, state: State) -> tuple[int, int] | None:
        """Return the visible heatmap cell for a state, or ``None`` if hidden."""
        ...

    def canvas_shape(self) -> tuple[int, int]:
        """Return heatmap shape as ``(num_layers, nodes_per_layer)``."""
        ...

    def path_cells(self, path: Path) -> list[tuple[int, int]]:
        """Return visible heatmap cells visited by a complete path."""
        ...
