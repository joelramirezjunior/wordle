# Wordle Solver Engine (& Game) (ESAP)

This repository contains the foundational code for a Wordle solver project developed for the ESAP (Engineering Summer Academy at Penn) program at the University of Pennsylvania.

The codebase is publicly accessible and free to use. The official solution will not be published until ESAP concludes in August.

---

## Overview

Your task is to implement a Wordle solver that can automatically guess a hidden five-letter word in six attempts or fewer, using feedback from each guess. This project emphasizes logic, string processing, and deduction algorithms under clear constraints.

---

## File Descriptions

### `main.py`

The entry point of the application. Supports two modes:

* **Interactive mode** (`-i`): Lets a human play the game in the terminal.
* **Simulation mode** (default): Uses the solver to automatically play the game.

### `wordle.py`

Implements the core **Wordle game engine**. Responsible for:

* Validating guesses
* Processing feedback (green/yellow/red logic)
* Tracking game state and user progress
  This is the backend used by both interactive and automated modes.

### `wordle_simulator.py`

A minimal wrapper around the `Wordle` engine. Designed for testing and benchmarking solvers.

* Simulates guesses
* Logs game state and results
* Can be extended to run batch experiments

### `wordle_solver.py`

This is where **you** implement your solver. The `WordleSolver` class should use the game's feedback to intelligently guess the next word. You will be graded based on correctness and efficiency.

### `vocabulary.txt`

A list of valid five-letter words (one per line). All guesses and solutions must come from this vocabulary.

### `rules.txt`

A lightweight markup file that defines how terminal color-coding should appear in interactive mode. Used for visual feedback (e.g., green for correct letters, yellow for wrong position, red for incorrect).

---

## How to Run

**To play manually:**

```bash
python3 main.py -i
```

**To run your solver:**

```bash
python3 main.py
```

Make sure you've written a valid `WordleSolver` class in `wordle_solver.py`. Your class will be automatically detected and used in simulation mode.

---

## Guidelines

* Maximum of 6 guesses per game.
* All guesses must be valid dictionary words.
* Solver must make use of previous feedback to refine future guesses.
* You are encouraged to test frequently using the simulator.

---

## Licensing & Release

This repository is provided for educational use. It is open-source and may be reused or modified. The official solution is withheld until the conclusion of the ESAP program in August.