"""Deterministic min-plus dynamic programming over a path-DP DAG."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from pathspace_lab.problems.base import Path, PathDPProblem, State
from pathspace_lab.utils.typing import Frame, SolverTrace


def solve_hard_dp(problem: PathDPProblem) -> SolverTrace:
    """Solve a DAG shortest-path problem with min-plus message passing.

    The solver consumes the shared ``PathDPProblem`` graph interface instead of
    any concrete problem arrays. Edge weights must be stored under the
    ``"weight"`` attribute, matching ``PathDPProblem.edges()``.
    """

    graph = problem.graph()
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("hard DP requires a directed acyclic graph")

    source = problem.source()
    sink = problem.sink()
    topo_order = problem.topological_order()
    if source not in graph:
        raise ValueError("problem source is not in graph")
    if sink not in graph:
        raise ValueError("problem sink is not in graph")

    distances: dict[State, float] = {state: np.inf for state in graph.nodes}
    predecessors: dict[State, State] = {}
    distances[source] = 0.0

    layer_counts = _visible_layer_counts(problem, topo_order)
    processed_layer_counts = {layer: 0 for layer in layer_counts}
    frames: list[Frame] = []

    for state in topo_order:
        state_distance = distances[state]
        if np.isfinite(state_distance):
            for successor in graph.successors(state):
                weight = _edge_weight(graph, state, successor)
                candidate = state_distance + weight
                if candidate < distances[successor]:
                    distances[successor] = float(candidate)
                    predecessors[successor] = state

        cell = problem.state_cell(state)
        if cell is None:
            continue

        layer, _ = cell
        processed_layer_counts[layer] += 1
        if processed_layer_counts[layer] == layer_counts[layer]:
            frames.append(
                Frame(
                    progress=(layer + 1) / max(1, len(layer_counts)),
                    label=f"layer {layer}",
                    value_heat=_value_heat(problem, distances),
                    observables={
                        "processed_layer": float(layer),
                        "best_value": float(distances[sink]),
                    },
                    metadata={"processed_state": state},
                )
            )

    best_value = float(distances[sink])
    if not np.isfinite(best_value):
        raise ValueError("sink is unreachable from source")

    if not frames:
        frames.append(
            Frame(
                progress=1.0,
                label="final",
                value_heat=_value_heat(problem, distances),
                observables={"best_value": best_value},
            )
        )

    frames[-1].observables["best_value"] = best_value

    return SolverTrace(
        method="hard_dp",
        problem_name=problem.name,
        frames=frames,
        metadata={
            "distances": distances,
            "predecessors": predecessors,
            "best_value": best_value,
            "source": source,
            "sink": sink,
        },
    )


def traceback_best_path(problem: PathDPProblem, trace: SolverTrace) -> Path:
    """Recover the visible best path from a Hard-DP trace."""

    if trace.method != "hard_dp":
        raise ValueError("traceback_best_path expects a hard_dp trace")

    predecessors = trace.metadata.get("predecessors")
    if not isinstance(predecessors, dict):
        raise ValueError("hard_dp trace is missing predecessor metadata")

    source = trace.metadata.get("source", problem.source())
    sink = trace.metadata.get("sink", problem.sink())
    if sink not in predecessors:
        raise ValueError("hard_dp trace does not contain a sink predecessor")

    reversed_states: list[State] = []
    state = sink
    while state != source:
        reversed_states.append(state)
        if state not in predecessors:
            raise ValueError(f"missing predecessor while tracing from {state!r}")
        state = predecessors[state]

    visible_path = tuple(
        state
        for state in reversed(reversed_states)
        if problem.state_cell(state) is not None
    )
    return visible_path


def _edge_weight(graph: nx.DiGraph, source: State, target: State) -> float:
    data: dict[str, Any] = graph.edges[source, target]
    if "weight" not in data:
        raise ValueError(f"edge {(source, target)!r} is missing a weight")
    weight = float(data["weight"])
    if not np.isfinite(weight):
        raise ValueError(f"edge {(source, target)!r} has a non-finite weight")
    return weight


def _visible_layer_counts(
    problem: PathDPProblem,
    topo_order: list[State],
) -> dict[int, int]:
    counts: dict[int, int] = {}
    for state in topo_order:
        cell = problem.state_cell(state)
        if cell is None:
            continue
        layer, _ = cell
        counts[layer] = counts.get(layer, 0) + 1
    return counts


def _value_heat(problem: PathDPProblem, distances: dict[State, float]) -> np.ndarray:
    heat = np.full(problem.canvas_shape(), np.nan, dtype=float)
    for state, value in distances.items():
        cell = problem.state_cell(state)
        if cell is None or not np.isfinite(value):
            continue
        heat[cell] = float(value)
    return heat


__all__ = ["solve_hard_dp", "traceback_best_path"]
