"""Shared trace dataclasses used by solvers and visualizers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from pathspace_lab.problems.base import Path


@dataclass(slots=True)
class Frame:
    """One solver snapshot at a comparable progress value.

    Attributes:
        progress: Normalized progress coordinate. For example, DP layer
            progress, Soft-DP beta progress, or QA anneal fraction.
        label: Short human-readable label for tables and figure titles.
        cell_heat: Projected layer-node probabilities or other cell scores with
            shape ``(L, W)``. Soft-DP and QA use this for cell marginals.
        value_heat: DP-oriented value table with shape ``(L, W)``. These values
            are not probabilities.
        path_probs: Probability distribution over complete paths, used by
            Soft-DP and by QA after converting amplitudes to probabilities.
        amplitudes: Complex QA amplitudes over complete paths.
        edge_heat: Optional edge-indexed quantities such as projected flow.
        observables: Scalar diagnostics such as energy, entropy, success
            probability, norm, or spectral gap.
        metadata: Method-specific details that should not become required API.
    """

    progress: float
    label: str
    cell_heat: np.ndarray | None = None
    value_heat: np.ndarray | None = None
    path_probs: np.ndarray | None = None
    amplitudes: np.ndarray | None = None
    edge_heat: dict[Any, float] | None = None
    observables: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SolverTrace:
    """A method trace made of ordered frames for one problem instance.

    Attributes:
        method: Solver or visualization source, such as ``"hard_dp"``,
            ``"soft_dp"``, or ``"feasible_qa"``.
        problem_name: Human-readable name of the problem instance.
        frames: Ordered sequence of snapshots.
        paths: Optional path ordering shared by ``path_probs`` and
            ``amplitudes``.
        energies: Optional energy array aligned with ``paths``.
        metadata: Extra method-level context, such as solver parameters.
    """

    method: str
    problem_name: str
    frames: list[Frame]
    paths: list[Path] | None = None
    energies: np.ndarray | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
