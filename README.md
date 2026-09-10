# Genetic Algorithms

A Genetic Algorithm (GA) is a search technique inspired by natural selection. It evolves a population of candidate solutions over multiple generations using three core operations:

- **Selection** — keep the fittest individuals as parents
- **Crossover** — combine two parents to produce children
- **Mutation** — randomly alter a child to maintain diversity

Each generation the population is replaced by the children of the fittest parents, gradually converging toward an optimal solution.

---

## Files

### [`maximise_a_func.py`](./maximise_a_func.py) — Integer domain (binary encoding)

Finds the integer `x` in range `[0, 31]` that maximises `f(x) = x²`.

- Individuals are represented as **5-bit binary chromosomes** (e.g. `[1,0,1,1,0]` → `x = 22`)
- **Selection:** top 4 fittest individuals kept (elitism)
- **Crossover:** single-point bit-splice between two parent chromosomes
- **Mutation:** random bit-flip at a 10% rate
- Population size: 10, Generations: 20
- Expected best: `x = 31`, `f(31) = 961`

### [`maximise_a_func2.py`](./maximise_a_func2.py) — Real-valued domain

Finds the real-valued `x` in range `[-10.0, 10.0]` that maximises `f(x) = x² + 10sin(x)`.

- Individuals are represented as **floating-point values**
- **Selection:** top 6 fittest individuals kept (elitism)
- **Crossover:** BLX-α (Blend Crossover, α=0.5) — children are sampled from a range slightly wider than the interval between the two parents, encouraging exploration
- **Mutation:** Gaussian noise (`N(0,1)`) added at a 1% rate
- Population size: 10, Generations: 20
- Expected best: around `x ≈ -9.0` where `f(x) ≈ 90.56`

---

Date: 10-09-2026

Obadiah Azimeh Nasara
