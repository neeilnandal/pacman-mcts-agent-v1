# Performance Analysis

## Offensive Behaviour

The offensive agent generally prioritised nearby food while monitoring ghost proximity.

When carrying sufficient food or encountering immediate danger, it switched to return-home planning.

This behaviour reduced avoidable captures.

## Defensive Behaviour

The defensive agent remained on the home side whenever possible.

Visible enemy Pac-Man agents were prioritised over random movement.

Stopping behaviour was strongly discouraged through feature weighting.

## Strengths

- Good offensive-defensive balance
- Reliable food return
- Stable behaviour under pressure
- Low unnecessary deaths

## Weaknesses

- Limited opponent prediction
- No long-horizon planning
- Simplified MCTS implementation
- No learned evaluation function
