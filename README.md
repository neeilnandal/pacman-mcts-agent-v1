# Pac-Man Capture the Flag Agent with MCTS and Rule-Based Defense

A Python AI agent for the **Pac-Man Capture the Flag** environment, combining **Monte Carlo Tree Search-inspired planning** for offensive Pacman behavior with a **rule-based defensive Ghost agent**.

The project implements a two-agent team:

* `PacmanAgent`: offensive food-seeking and return-home behavior
* `GhostAgent`: defensive patrol and invader-chasing behavior

The agent is designed for a competitive Capture the Flag setting where each team tries to collect food from the opponent’s side while defending its own territory.

## Repository Summary

| Field           | Details                                                       |
| --------------- | ------------------------------------------------------------- |
| Project type    | Game AI agent                                                 |
| Environment     | Pac-Man Capture the Flag                                      |
| Main techniques | MCTS-inspired search, rule-based agents, heuristic evaluation |
| Language        | Python                                                        |
| Core file       | `myTeam.py` or equivalent contest agent file                  |
| Visualization   | Red/blue score tracking across games                          |
| Main objective  | Build a competitive attacker-defender team                    |

## Problem

Pac-Man Capture the Flag is a multi-agent decision problem.

Each team must balance two goals:

* Attack the opponent’s side and collect food
* Defend its own territory from invading Pacmen

A strong agent cannot only chase food. It must also know when to retreat, avoid ghosts, return carried food safely, and defend against opponents.

The real problem is:

```text
How can an agent balance food collection, survival, return-home timing, and defensive coverage in a partially observable adversarial game?
```

## Solution

This project uses a hybrid decision strategy.

The offensive agent uses simple feature-based food seeking when conditions are safe. When risk increases, or when enough food has been collected, it switches to an MCTS-inspired planner that evaluates actions based on distance to the home border.

The defensive agent uses hand-crafted features to chase enemy Pacmen, avoid stopping, and stay on defense.

## Team Structure

The team is created using:

```python
def createTeam(firstIndex, secondIndex, isRed, first='PacmanAgent', second='GhostAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]
```

Default team:

```text
Agent 1: PacmanAgent
Agent 2: GhostAgent
```

## Agent Design

### PacmanAgent

The `PacmanAgent` is responsible for offensive play.

It switches between three behaviors:

| Situation                      | Behavior                            |
| ------------------------------ | ----------------------------------- |
| Safe and carrying limited food | Move toward nearest food            |
| Enemy ghost nearby             | Use MCTS-inspired return strategy   |
| Carrying more than 5 food      | Return toward home border           |
| Opponent ghosts are scared     | Continue aggressive food collection |

The offensive feature evaluation rewards food collection and penalizes distance to food.

```python
weights = {
    'minDistToFood': -1,
    'getFood': 100
}
```

### GhostAgent

The `GhostAgent` is responsible for defense.

It evaluates legal actions using defensive features:

| Feature             | Purpose                                |
| ------------------- | -------------------------------------- |
| `defensive`         | Reward staying as a ghost on home side |
| `total_oppo_pacman` | Penalize enemy invaders                |
| `opposite_distance` | Move closer to invading opponents      |
| `stop`              | Penalize stopping                      |
| `back`              | Track reversing behavior               |

Defensive weights:

```python
{
    'total_oppo_pacman': -1000,
    'defensive': 100,
    'opposite_distance': -10,
    'stop': -100
}
```

## MCTS-Inspired Planning

The project includes an `MCTSAgent` class that performs search over future game states.

Core components:

| Component            | Role                                    |
| -------------------- | --------------------------------------- |
| Node expansion       | Expands unexplored legal actions        |
| Reward calculation   | Rewards movement toward the home border |
| Backpropagation      | Updates parent nodes with reward        |
| Best-child selection | Chooses child with best average reward  |
| Time budget          | Stops search after about 0.82 seconds   |

The MCTS search is mainly used when the Pacman needs to return home safely.

## Reward Function

The MCTS reward encourages the agent to move toward the center line, which represents the route back to home territory.

```python
feature['min_distance'] = minimum_distance
weight = {'min_distance': -1}
```

A smaller distance to the center line gives a better reward.

This makes sense when the agent is carrying food or facing ghost pressure.

## Score Tracking

The project includes score tracking across multiple games.

It stores red and blue scores in arrays:

```python
red_score_array = [0] * 10
blue_score_array = [0] * 10
```

The score plot shows performance across games using Matplotlib.

This is useful for comparing the agent’s behavior over repeated matches.

## App / Code Workflow

```text
Create team
        |
Register initial game state
        |
Compute map dimensions and center line
        |
For each turn:
        |
Check whether agent is Pacman or Ghost
        |
If Pacman:
    Check food, carried food, ghost threats, scared timers
    Choose food-seeking action or MCTS return action
        |
If Ghost:
    Evaluate defensive features
    Choose best defensive action
        |
Track scores across games
        |
Plot red vs blue team scores
```

## Key Features

* Hybrid offensive and defensive team design
* MCTS-inspired search for return-home decisions
* Rule-based food seeking
* Enemy ghost threat detection
* Home-border distance calculation
* Defensive invader chasing
* Score tracking across games
* Matplotlib score visualization
* Designed for Pac-Man Capture the Flag contest environments

## Installation

This project is intended to run inside a Pac-Man Capture the Flag codebase that provides:

```text
captureAgents.py
game.py
util.py
capture.py
```

Clone or place this agent file inside the contest environment.

Example structure:

```text
pacman-capture-the-flag/
│
├── capture.py
├── captureAgents.py
├── game.py
├── util.py
├── myTeam.py
├── README.md
└── requirements.txt
```

The Pac-Man framework files are required separately.

## Running the Agent

Example command inside the Capture the Flag framework:

```bash
python capture.py -r myTeam -b baselineTeam
```

To run multiple games:

```bash
python capture.py -r myTeam -b baselineTeam -n 10
```

To run without graphics:

```bash
python capture.py -r myTeam -b baselineTeam -n 10 -q
```

Command-line options may vary depending on the specific Pac-Man framework version.

## First-Principles Design

The core decision is not:

```text
Which move gives the highest immediate score?
```

The better question is:

```text
Which move improves the agent’s chance of collecting food and surviving long enough to return it?
```

That is why the offensive agent changes behavior when ghost risk increases or carried food becomes valuable.

## Founder-Style Product Diagnosis

### User

A student, AI researcher and/or game-AI learner building a Capture the Flag Pac-Man team.

### Pain Point

Simple reflex agents collect food but often die because they do not manage risk or retreat timing.

### Smallest Useful Version

A hybrid attacker-defender team that collects food, detects ghost threats, and returns home when risk increases.

## Security and Code Safety Notes

This project is low-risk because it runs locally inside a game framework and does not use private data or external APIs.

| Area            | Status                                        |
| --------------- | --------------------------------------------- |
| API keys        | None                                          |
| Secrets         | None                                          |
| User data       | None                                          |
| File uploads    | None                                          |
| Network calls   | None                                          |
| Main code risk  | Use of `eval()` in team creation              |
| Recommended fix | Replace `eval()` with explicit class registry |

## Scientific and AI Skills Demonstrated

This project demonstrates:

* Multi-agent game AI
* Heuristic evaluation functions
* Monte Carlo Tree Search-inspired planning
* Reward design
* Defensive agent design
* Risk-aware action selection
* Game-state feature extraction
* Score tracking and visualization
* Agent behavior switching

The strongest AI skill shown is not just MCTS. It is the combination of search, heuristics, and situational behavior switching.

## Limitations

* MCTS does not currently use full UCT exploration
* Rollouts are shallow and reward is simple
* Ghost behavior is rule-based rather than predictive
* Score tracking uses global state
* Plotting is embedded in gameplay logic
* No formal win-rate table
* No ablation study comparing food-only vs MCTS behavior
* No saved CSV evaluation logs

## Future Improvements

* Add UCT formula to MCTS child selection
* Add simulation rollouts beyond immediate reward
* Add opponent modeling
* Add dynamic escape-route planning
* Add patrol zones for GhostAgent
* Add capsule-aware offensive behavior
* Add CSV logging for match scores
* Add win-rate and average-score metrics
* Separate plotting into `evaluate.py`
* Add command-line evaluation runner
* Add ablation study for MCTS vs reflex behavior

## Suggested Repository Structure

```text
pacman-capture-the-flag-mcts-agent/
│
├── myTeam.py
├── README.md
├── requirements.txt
├── .gitignore
├── reports/
│   └── results_summary.md
└── plots/
    └── score_comparison.png
```

If you refactor further:

```text
pacman-capture-the-flag-mcts-agent/
│
├── agents/
│   ├── offensive_agent.py
│   ├── defensive_agent.py
│   └── mcts.py
├── evaluation/
│   ├── run_matches.py
│   └── plot_scores.py
├── myTeam.py
├── README.md
└── requirements.txt
```

## SEO Keywords

Relevant keywords:

* Pac-Man Capture the Flag AI
* Monte Carlo Tree Search
* MCTS game agent
* multi-agent game AI
* Pacman AI agent
* heuristic game AI
* adversarial search
* defensive agent
* offensive Pacman agent
* Python game AI project

## Repository Topics

```text
pacman
capture-the-flag
game-ai
mcts
monte-carlo-tree-search
multi-agent-systems
heuristic-search
python
adversarial-search
ai-agent
```
