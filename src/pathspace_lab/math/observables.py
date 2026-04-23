"""Common probability observables and path marginal utilities."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from pathspace_lab.problems.base import Path, PathDPProblem, State


def normalize_probs(probs: Sequence[float] | np.ndarray, *, eps: float = 1e-15) -> np.ndarray:
    """Return a normalized one-dimensional probability vector.

    Tiny negative values within ``eps`` are treated as roundoff and clipped to
    zero. Larger negative values and all-zero inputs are rejected because they
    are not probability weights.
    """

    values = np.asarray(probs, dtype=float)
    if values.ndim != 1:
        raise ValueError("probs must be a one-dimensional array")
    if values.size == 0:
        raise ValueError("probs must not be empty")
    if not np.all(np.isfinite(values)):
        raise ValueError("probs must contain only finite values")
    if np.any(values < -eps):
        raise ValueError("probs must be nonnegative")

    clipped = np.where(values < eps, 0.0, values)
    total = float(clipped.sum())
    if total <= eps:
        raise ValueError("probability weights must have positive total mass")
    return clipped / total


def path_entropy(probs: Sequence[float] | np.ndarray, *, eps: float = 1e-15) -> float:
    """Return Shannon entropy ``-sum_p P(p) log P(p)`` for path probabilities."""

    normalized = normalize_probs(probs, eps=eps)
    positive = normalized[normalized > 0.0]
    return float(-np.sum(positive * np.log(positive)))


def effective_num_paths(probs: Sequence[float] | np.ndarray, *, eps: float = 1e-15) -> float:
    """Return the entropy effective path count ``exp(S)``."""

    return float(np.exp(path_entropy(probs, eps=eps)))


def expected_energy(
    probs: Sequence[float] | np.ndarray,
    energies: Sequence[float] | np.ndarray,
    *,
    eps: float = 1e-15,
) -> float:
    """Return expected path energy ``sum_p P(p) E(p)``."""

    normalized = normalize_probs(probs, eps=eps)
    energy_values = _validate_aligned_vector(energies, normalized, name="energies")
    return float(np.dot(normalized, energy_values))


def success_probability(
    probs: Sequence[float] | np.ndarray,
    energies: Sequence[float] | np.ndarray,
    *,
    optimum_energy: float | None = None,
    atol: float = 1e-9,
    eps: float = 1e-15,
) -> float:
    """Return total probability assigned to minimum-energy paths."""

    normalized = normalize_probs(probs, eps=eps)
    energy_values = _validate_aligned_vector(energies, normalized, name="energies")
    target = float(np.min(energy_values) if optimum_energy is None else optimum_energy)
    optimal = np.isclose(energy_values, target, rtol=0.0, atol=atol)
    return float(normalized[optimal].sum())


def cell_marginals(
    problem: PathDPProblem,
    paths: Sequence[Path],
    probs: Sequence[float] | np.ndarray,
    *,
    eps: float = 1e-15,
) -> np.ndarray:
    """Project complete-path probabilities onto visible problem cells."""

    normalized = _validate_path_probs(paths, probs, eps=eps)
    marginals = np.zeros(problem.canvas_shape(), dtype=float)

    for path, probability in zip(paths, normalized):
        for ell, v in problem.path_cells(path):
            marginals[ell, v] += float(probability)

    return marginals


def edge_marginals_from_paths(
    problem: PathDPProblem,
    paths: Sequence[Path],
    probs: Sequence[float] | np.ndarray,
    *,
    eps: float = 1e-15,
) -> dict[tuple[State, State], float]:
    """Project complete-path probabilities onto visible consecutive edges.

    Artificial source and sink states are omitted. The returned dictionary uses
    visible problem states as keys, for example ``((ell, u), (ell + 1, v))`` for
    the MVP layered DAG.
    """

    normalized = _validate_path_probs(paths, probs, eps=eps)
    marginals: dict[tuple[State, State], float] = {}

    for path, probability in zip(paths, normalized):
        visible_states = [state for state in path if problem.state_cell(state) is not None]
        for edge in zip(visible_states, visible_states[1:]):
            marginals[edge] = marginals.get(edge, 0.0) + float(probability)

    return marginals


def _validate_aligned_vector(
    values: Sequence[float] | np.ndarray,
    reference: np.ndarray,
    *,
    name: str,
) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional array")
    if array.shape != reference.shape:
        raise ValueError(f"{name} must have shape {reference.shape}, got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def _validate_path_probs(
    paths: Sequence[Path],
    probs: Sequence[float] | np.ndarray,
    *,
    eps: float,
) -> np.ndarray:
    normalized = normalize_probs(probs, eps=eps)
    if len(paths) != normalized.size:
        raise ValueError(
            f"paths and probs must have the same length, got {len(paths)} and {normalized.size}"
        )
    return normalized


__all__ = [
    "cell_marginals",
    "edge_marginals_from_paths",
    "effective_num_paths",
    "expected_energy",
    "normalize_probs",
    "path_entropy",
    "success_probability",
]
