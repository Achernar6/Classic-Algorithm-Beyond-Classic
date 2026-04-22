import numpy as np

from pathspace_lab.utils.typing import Frame, SolverTrace


def test_frame_can_hold_cell_heat_and_observables():
    cell_heat = np.ones((2, 3)) / 3
    frame = Frame(
        progress=0.0,
        label="toy",
        cell_heat=cell_heat,
        observables={"entropy": float(np.log(6))},
    )

    assert frame.progress == 0.0
    assert frame.label == "toy"
    assert frame.cell_heat is cell_heat
    assert frame.value_heat is None
    assert frame.observables["entropy"] == float(np.log(6))


def test_solver_trace_can_hold_ordered_frames_paths_and_energies():
    frame = Frame(progress=1.0, label="final", path_probs=np.array([1.0]))
    trace = SolverTrace(
        method="toy",
        problem_name="tiny",
        frames=[frame],
        paths=[("source", "sink")],
        energies=np.array([1.0]),
        metadata={"note": "contract check"},
    )

    assert trace.method == "toy"
    assert trace.problem_name == "tiny"
    assert len(trace.frames) == 1
    assert trace.paths == [("source", "sink")]
    assert trace.energies is not None
    assert trace.energies.tolist() == [1.0]
    assert trace.metadata["note"] == "contract check"


def test_frame_default_dicts_are_independent():
    first = Frame(progress=0.0, label="first")
    second = Frame(progress=0.0, label="second")

    first.observables["x"] = 1.0

    assert second.observables == {}
