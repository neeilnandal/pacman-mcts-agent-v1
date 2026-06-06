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

## Code Quality Notes

The current implementation is a strong academic prototype, but it should be cleaned before being treated as a polished GitHub project.

Recommended improvements:

| Area               | Current issue                    | Suggested fix                                  |
| ------------------ | -------------------------------- | ---------------------------------------------- |
| Team creation      | Uses `eval()`                    | Replace with explicit class mapping            |
| Score tracking     | Uses global variables            | Move into a tracker class                      |
| MCTS selection     | Uses average reward only         | Add UCT exploration term                       |
| Naming             | Some inconsistent variable names | Rename for readability                         |
| Plotting           | Mixed into agent logic           | Move plotting to separate evaluation script    |
| Defensive behavior | Simple heuristic                 | Add patrol zones and better invader prediction |
| Evaluation         | Only score plot                  | Add win rate, average score, food returned     |

## Suggested Safer Team Creation

Replace:

```python
return [eval(first)(firstIndex), eval(second)(secondIndex)]
```

with:

```python
AGENT_REGISTRY = {
    "PacmanAgent": PacmanAgent,
    "GhostAgent": GhostAgent,
}

def createTeam(firstIndex, secondIndex, isRed, first="PacmanAgent", second="GhostAgent"):
    return [
        AGENT_REGISTRY[first](firstIndex),
        AGENT_REGISTRY[second](secondIndex),
    ]
```

This avoids unnecessary dynamic evaluation.

## OODA Summary

### Observe

The game requires agents to attack and defend at the same time. Pacman must collect food, avoid ghosts, and return home safely.

### Orient

A single fixed policy is too weak. The agent needs different behaviors depending on risk, carried food, and enemy position.

### Decide

Use feature-based food seeking for safe attack, MCTS-inspired planning for return-home behavior, and rule-based defense for the Ghost agent.

### Act

Implement a hybrid team with offensive and defensive agents, score tracking, and repeated-game visualization.

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

A student, AI researcher, game-AI learner, or contest participant building a Capture the Flag Pac-Man team.

### Pain Point

Simple reflex agents collect food but often die because they do not manage risk or retreat timing.

### Smallest Useful Version

A hybrid attacker-defender team that collects food, detects ghost threats, and returns home when risk increases.

### Current Version

The project implements food-seeking, MCTS-inspired retreat planning, defensive invader chasing, and score visualization.

### What Still Needs Work

The next step is cleaner engineering: remove globals, add UCT, separate evaluation logic, and report win-rate metrics.

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

## Meta Description

```text
Hybrid Pac-Man Capture the Flag AI agent using MCTS-inspired offensive planning, rule-based defensive ghost behavior, ghost-threat detection, and score visualization.
```

## Peer Review Verdict

This is a good academic Game AI project with clear portfolio value.

It should be presented as a hybrid heuristic-search agent, not as a full industrial-grade MCTS implementation. The MCTS component is useful but simplified. The strongest part is the situational agent design: food seeking when safe, return-home planning when risk increases, and defensive invader chasing.

The main weakness is engineering polish. Globals, `eval()`, embedded plotting, and simplified MCTS selection should be cleaned in a v2.

## Final Verdict

Keep and publish after light cleanup.

This project is especially relevant for a profile targeting AI, reinforcement learning, game AI, and multi-agent systems. It shows applied decision-making under uncertainty, not just model training.

## Portfolio One-Liner

Built a hybrid **Pac-Man Capture the Flag AI agent** combining MCTS-inspired offensive planning, rule-based defensive ghost behavior, food-seeking heuristics, threat detection, and match-score visualization.

## GitHub Repository Description

```text
Hybrid Pac-Man Capture the Flag agent using MCTS-inspired offensive planning and rule-based defensive behavior.
```
