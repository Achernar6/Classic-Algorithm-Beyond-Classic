# CABC -Round1- Dynamic Programming vs. Quantum Annealing

A notebook project about dynamic programming, thermal relaxation, and quantum annealing as three different ways of moving through a space of possible paths. Round 1 of the series [classic algorithms beyond classic] (if it's lucky enough to have sequels, but at least for now I plan to generalize this to trikier graph scenarios after the MVP works out.)

It is also a first attempt to make something open in public while being watched by the ... big Other of the internet(?) Basically, I am writing it for myself: to leave a trail of how I learn, test metaphors, and gradually replace vague intuition with runnable objects. If someone later finds the trail useful, even only as a starting point for their own intuition, that would already be more than enough.

The planned shape of the project is simple:

- The notebook is the front door. It should feel like a living essay: runnable, visual, and honest about what it does and does not show.
- The math notes keep the claims grounded. They are there to stop a beautiful metaphor from quietly becoming a false statement.
- The visualization notes explain what each picture is allowed to mean. A picture can build intuition, but it can also smuggle in a promise the model never made.
- The source code and tests support the notebook from underneath. They are not the point of the README, but they keep the exploration from becoming only prose.
- The roadmap records the staged development of the project, including the boundary that matters most here: this is not a quantum advantage demo, not a D-Wave hardware simulator, and not a proof of quantum supremacy. It is a teaching and thinking tool built around one shared path-space canvas.

The **central comparison** currently focuses on:

- Hard DP compresses histories into local values.
- Soft-DP treats complete paths as a classical thermal distribution.
- The feasible-subspace quantum annealing proxy evolves amplitudes over complete feasible paths.

All three can be projected back onto the same layered graph. What differs is the hidden way each one listens to the possible futures.

## Why This Exists

Back in high school, when I was studying chemistry and physics competitions, I only touched the edge of things that stayed with me: physical chemistry and thermodynamics, kinetic versus thermodynamic products, crystals and phase transitions, the Schrodinger equation, special relativity. I did not go very far, but those subjects left behind a particular hunger. I kept wanting to apply them beyond their original territory, toward more general systems: individuals, collectives, choices, histories, the strange ways a human life searches through possibility.

Then, during my undergraduate years, I moved into broad computer science. For a while I stepped away from the scientific view of the world. After that I worked for a year in financial data, which gave me something less romantic but very valuable: a habit of abstraction, and a sense of how general ideas survive contact with engineering practice.

Now, in my master's period, I have somehow returned to quantum questions. Quantum mechanics was one of the few old regions where my intuition had not yet lit up. So this project is a way to combine an older scientific fascination with a newer practical ability: to explore one small edge of how humans traverse the world, using visualization to build intuition and hands-on implementation to learn the texture of the problem.

Before studying the actual principles and limits of quantum annealing carefully, my naive intuition gave it a kind of romance. Compared with ordinary thermal models, it seemed to promise a path toward the global optimum without the undignified panic of reheating again and again, without being trapped forever behind local energy barriers. Compared with hard DP, whose local and deterministic wisdom can feel like "do your assigned work and trust the future," quantum annealing seemed, in my imagination, to listen synchronically to the whispers among different possibilities.

That romance is part of why I was drawn to it.

The hands-on work has also made the limit very clear: this romance does not automatically extend into positive evidence for quantum supremacy. The proxy here is small, controlled, and pedagogical. But I am old enough (not sure) now to appreciate even these fractions of reality. It is already a privilege, an honor to touch a question like this with my own hands.

## About AI Coding

The meaning and language of this README are fully human-written and original. The engineering part of the project was developed mainly with Codex, together with a workflow I have been shaping through personal projects: something close to a state machine, and also very close to what people have recently started calling a harness. Cybernetics does enjoy returning under new names.

I do not want to divide the work with AI by saying, for example, "I designed this data class, the AI wrote that plotting function." Most of the ideas came while I was learning the principles and the surrounding technical ecosystem, but the concrete implementation is too entangled for that kind of accounting to feel honest.

So here is the distinction I care about: the human role is to keep the purpose, and to let that purpose permeate the whole project.

We live in a typed world. We have semantics. Lambda calculus is a beautiful warning against underestimating reduction: with only abstraction and application, functions can even stand in for data. Relations are astonishingly powerful. But a project is not only a pile of reducible transformations. No speed of logical metonymy can turn every entity into relation without remainder. The decision of what something is for cannot be automated away.

What does it mean for purpose to permeate a project? AI can now work surprisingly well at the coarsest level of planning and at the finest level of local execution. The difficult part is the mixing layer between them. Coffee and milk are simple before mixing and simple again after mixing, but in the middle the pattern is at its most complex. Building with AI often feels like living in that middle layer: adding small grains of structure, watching where the system wants to avalanche, then nudging it back toward the purpose.

The image I like is the growth of a single-crystal turbine blade. You do not place every atom by hand. You shape the thermal gradient, the selector, and the boundary conditions so that one orientation survives the competition and grows through a complex form. That is close to how I want to work with AI: not as a replacement for intention, and not as a passive tool, but as a medium whose crystallization still needs a direction.

This project is one small crystal grown under that condition.
