"""Classical thermal path distribution over feasible complete paths."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from pathspace_lab.math.observables import (
    cell_marginals,
    edge_marginals_from_paths,
    effective_num_paths,
    expected_energy,
    path_entropy,
    success_probability,
)
from pathspace_lab.problems.base import Path, PathDPProblem
from pathspace_lab.utils.typing import Frame, SolverTrace


def solve_soft_dp(
    problem: PathDPProblem,
    betas: Sequence[float] | np.ndarray,
    paths: Sequence[Path] | None = None,
) -> SolverTrace:
    """Compute Boltzmann path distributions and projected marginals.

    This is an enumerative classical thermal baseline, not a forward-backward
    dynamic-programming implementation. It is intentionally small and explicit
    for the MVP notebook.
    """

    beta_values = _validate_betas(betas)
    path_list = list(problem.enumerate_paths() if paths is None else paths)
    if not path_list:
        raise ValueError("Soft-DP requires at least one feasible path")

    energies = np.array([problem.path_energy(path) for path in path_list], dtype=float)
    if not np.all(np.isfinite(energies)):
        raise ValueError("path energies must be finite")

    optimum_energy = float(np.min(energies))
    beta_max = float(np.max(beta_values))
    frames: list[Frame] = []

    for beta in beta_values:
        path_probs, log_z = _boltzmann_probs(energies, float(beta))
        mean_energy = expected_energy(path_probs, energies)
        entropy = path_entropy(path_probs)
        success = success_probability(
            path_probs,
            energies,
            optimum_energy=optimum_energy,
        )

        frames.append(
            Frame(
                progress=0.0 if beta_max == 0.0 else float(beta / beta_max),
                label=f"beta={beta:.3g}",
                cell_heat=cell_marginals(problem, path_list, path_probs),
                path_probs=path_probs,
                edge_heat=edge_marginals_from_paths(problem, path_list, path_probs),
                observables={
                    "beta": float(beta),
                    "log_partition": float(log_z),
                    "expected_energy": mean_energy,
                    "residual_energy": mean_energy - optimum_energy,
                    "entropy": entropy,
                    "effective_paths": effective_num_paths(path_probs),
                    "success_probability": success,
                },
            )
        )

    return SolverTrace(
        method="soft_dp",
        problem_name=problem.name,
        frames=frames,
        paths=path_list,
        energies=energies,
        metadata={
            "betas": beta_values,
            "optimum_energy": optimum_energy,
            "implementation": "enumerated_boltzmann_distribution",
        },
    )


def _boltzmann_probs(energies: np.ndarray, beta: float) -> tuple[np.ndarray, float]:
    log_weights = -beta * energies
    log_z = _logsumexp(log_weights)
    probs = np.exp(log_weights - log_z)
    probs /= probs.sum()
    return probs, log_z


def _logsumexp(values: np.ndarray) -> float:
    max_value = float(np.max(values))
    shifted_sum = float(np.sum(np.exp(values - max_value)))
    return max_value + float(np.log(shifted_sum))


def _validate_betas(betas: Sequence[float] | np.ndarray) -> np.ndarray:
    beta_values = np.asarray(betas, dtype=float)
    if beta_values.ndim != 1:
        raise ValueError("betas must be a one-dimensional array")
    if beta_values.size == 0:
        raise ValueError("betas must not be empty")
    if not np.all(np.isfinite(beta_values)):
        raise ValueError("betas must contain only finite values")
    if np.any(beta_values < 0.0):
        raise ValueError("betas must be nonnegative")
    return beta_values


__all__ = ["solve_soft_dp"]
