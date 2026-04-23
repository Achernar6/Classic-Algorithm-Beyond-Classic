# Classic Algorithm Beyond Classic - Round 1
## Dynamic Programming & Quantum Annealing

**Classic Algorithm Beyond Classic** is a self-learning project series about reinterpreting classic algorithms from a quantum view: not to replace the classical story (or prove quantum supremacy), but to look at familiar computational structures through a different state space, geometry, and notion of evolution.

Round 1 starts from a small **layered DAG shortest-path problem**. A solution is a complete path through the layers. The same path problem is then viewed through three related but different mechanisms:

- **Hard DP** compresses partial histories into local min-plus values.
- **Soft-DP** assigns a classical thermal distribution to complete feasible paths.
- **Feasible-subspace quantum annealing** evolves complex amplitudes over complete feasible paths.

The common visual object is a layer-node canvas. Hard DP, Soft-DP, and the quantum annealing proxy can all be projected onto that canvas (but the projection should not erase the difference between their hidden objects: values, probabilities, and amplitudes do not mean the same thing).

For the quantum part, the MVP uses a feasible-subspace proxy with the annealing form

$$
H(s)=A(s)H_D+B(s)H_P.
$$

Here the basis states are valid paths, the driver has a uniform feasible ground state, and the problem Hamiltonian has optimal paths as ground states. I know the current proxy has a clear boundary; later rounds can incorporate a more realistic quantum stack like Qiskit or D-wave and generalize toward richer graph and optimization problems.

The goal is to keep the project runnable, inspectable, and mathematically sound while preserving the original reason I am doing it: to synthesize the vague intuitions about **dynamic programming, thermal relaxation, and quantum evolution** into objects I can compute, visualize, and finally graspe.


It is also a first attempt to make something open in public while being watched by the ... big Other of the internet??

--**Technical part ends, below is some random chat**--

## About Working with AI

The meaning of this README are fully human-written and original (with a little bit paraphrase). The engineering part of the project was developed mainly with Codex, together with a workflow I have been shaping through personal projects (something close to a state machine, and also very close to what people have recently started calling a harness. Cybernetics does enjoy returning under new names.)

I do not want to divide the work with AI by saying, for example, "I designed this data class, the AI wrote that plotting function." **Most of the ideas came while I was learning the principles and the surrounding technical ecosystem**, but the concrete implementation is too entangled for that kind of accounting to feel honest.

So here is the distinction I care about: **the human role is to keep the purpose, and to let that purpose permeate the whole project.**

We live in a typed world. We have semantics. Lambda calculus is a beautiful warning against underestimating reduction: with only abstraction and application, functions can even stand in for data. Relations are astonishingly powerful. But **a project is not only a pile of reducible transformations**. No speed of logical metonymy can turn every entity into relation without remainder. The decision of **what something is for** cannot be automated away.

What does it mean for purpose to permeate a project? AI can now work surprisingly well at the coarsest level of planning and at the finest level of local execution. The difficult part is the mixing layer between them. Coffee and milk are simple before mixing and simple again after mixing, but in the middle the pattern is at its most complex. Building with AI often feels like living in that middle layer: adding small grains of structure, watching where the system wants to avalanche, then nudging it back toward the purpose. Never let it automate you out of the loop.

The analogy I like is the growth of a single-crystal turbine blade. You do not place every atom by hand. You shape the thermal gradient, the selector, and the boundary conditions so that one orientation survives the competition and grows through a complex form. That is close to how I want to work with AI: not as a replacement for intention, and not as a passive tool, but **a wavefront where human can ride and guide the project to cystalize into the ONE** with your desired form.

(This project is one small crystal grown under that condition.)

## Why This Exists

Back in high school, when I was studying chemistry and physics competitions, I only touched the edge of things that stayed with me: physical chemistry and thermodynamics, kinetic versus thermodynamic products, crystals and phase transitions, the Schrodinger equation, special relativity. I did not go very far, but those subjects left behind a particular hunger. I kept wanting to apply them beyond their original territory, toward more general systems: individuals, collectives, choices, histories, the strange ways a human life searches through possibility.

Then, during my undergraduate years, I moved into broad computer science. For a while I stepped away from the scientific view of the world. After that I worked for a year in financial data, which gave me something less romantic but very valuable: a habit of abstraction, and a sense of how general ideas survive contact with engineering practice.

Now, in my master's period, I have somehow returned to quantum questions. Quantum mechanics was one of the few old regions where my intuition had not yet lit up. So this project is a way to combine an older scientific fascination with a newer practical ability: to explore one small edge of how humans traverse the world, using visualization to build intuition and hands-on implementation to learn the texture of the problem.

Before studying the actual principles and limits of quantum annealing carefully, my naive intuition gave it a kind of romance. Compared with ordinary thermal models, it seemed to promise a path toward the global optimum without the undignified panic of reheating again and again, without being trapped forever behind local energy barriers. Compared with hard DP, whose local and deterministic wisdom can feel like "do your assigned work and trust the future," quantum annealing seemed, in my imagination, to listen synchronically to the whispers among different possibilities.

That romance is part of why I was drawn to it.

The hands-on work has also made the limit very clear: this romance does not automatically extend into positive evidence for quantum supremacy. The proxy here is small, controlled, and pedagogical. But I am old enough (not sure) now to appreciate even these fractions of reality. It is already a privilege, an honor to touch a question like this with my own hands.