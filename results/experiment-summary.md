# Experiment Summary

## Objective

Evaluate the performance of the hybrid Pac-Man Capture the Flag agent against the baseline Capture Agent.

## Experimental Setup

Environment

- Pac-Man Capture the Flag

Red Team

- Custom MCTS-inspired agent

Blue Team

- Baseline Capture Team

Games

- 10 independent matches

Layout

- defaultCapture

## Metrics

The following metrics were recorded:

- Food collected
- Food successfully returned
- Enemy invaders intercepted
- Agent captures
- Agent deaths
- Final team score
- Match winner

## Results

The agent consistently outperformed the baseline team across repeated games.

Average score difference favoured the custom team.

The offensive agent successfully balanced food collection with return-home decisions, while the defensive agent prevented multiple enemy incursions.

## Key Observation

The strongest behaviour occurred when the offensive agent abandoned food collection and returned home before nearby ghosts could intercept it.

This reduced unnecessary losses while preserving accumulated score.

## Conclusion

The hybrid strategy demonstrated more stable behaviour than a purely greedy food-collection policy.
