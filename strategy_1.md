# Strategy 1: Draw-Simulation Elo Ensemble

## Best Owner

Rohit

## Core Idea

Build the most tournament-realistic model by estimating player-vs-player win probabilities, placing those probabilities into the official Wimbledon draw, and simulating the tournament many times. The final Phase 1 prediction is the player with the highest quarterfinal probability from each of the eight draw sections.

This should be our primary submission candidate because Wimbledon quarterfinalists are not just the best eight players overall. They are the eight players most likely to survive their individual bracket paths.

## Decision This Model Supports

Which eight men's players and which eight women's players should we submit as predicted quarterfinalists after the official draw is known?

## Data Inputs

- Historical ATP and WTA match logs.
- Wimbledon-specific historical match results.
- 2026 Wimbledon entry lists.
- Official 2026 Wimbledon men's and women's singles draws.
- Seed, rank, draw section, and opponent path.
- Optional manual risk flags for injury, withdrawal, or poor fitness.

## Feature Set

- Overall Elo rating.
- Grass-court Elo rating.
- Recent-form Elo rating from the last 10 to 20 matches.
- Ranking difference.
- Grass win rate over the last 12 to 24 months.
- Wimbledon career performance.
- Recent grass warmup results.
- Best-of-five adjustment for men's matches.
- Draw-path difficulty.

## How to Use Our Historical and Draw Data

Start from the local processed files we already generate:

- `data/processed/match_history_combined.csv`: canonical ATP/WTA historical match log.
- `data/processed/phase1_player_features.csv`: current player-level ranking, grass, Wimbledon, and recent-form features.
- `data/processed/phase1_rolling_form_trends.csv`: rolling player form trends.
- `data/processed/wimbledon_2026_mens_entries.csv`: men's entry list parsed from `MS_Entries.pdf`.
- `data/processed/wimbledon_2026_womens_entries.csv`: women's entry list parsed from `LS_Entries.pdf`.

Step-by-step workflow:

1. Rebuild local processed data from raw inputs:

```bash
python scripts/process_and_upload.py --local-only
python scripts/phase1_model.py
```

2. Build Elo ratings from `match_history_combined.csv`.

Use one Elo rating for all surfaces and one grass-only Elo rating. For every historical match, update the winner upward and the loser downward. For grass matches, also update the grass Elo.

3. Join 2026 entrants to player features.

Use the player names in `wimbledon_2026_mens_entries.csv` and `wimbledon_2026_womens_entries.csv`, then join to `phase1_player_features.csv` and `phase1_rolling_form_trends.csv`.

4. Add the official draw.

Once the official draw is saved locally, create:

```text
data/processed/wimbledon_2026_draw_sections.csv
```

Minimum required columns:

```text
tour, draw_position, section, seed, player, first_round_opponent
```

Sections should be numbered `1` to `8`, where each section contains 16 players and produces one quarterfinalist.

5. Simulate the bracket.

For each simulated match, calculate win probability from the two players' blended Elo strength. Advance one player until the bracket reaches quarterfinalists, semifinals, finalists, and champion. Repeat at least 10,000 times.

6. Produce the Phase 1 picks.

For each tour and each section, select the player with the highest simulated quarterfinal probability. Keep the second-highest player as the backup pick.

## Modeling Method

1. Build player strength ratings.
2. Convert strength differences into match win probabilities.
3. Insert all players into the official 128-player draw.
4. Simulate the tournament 10,000 to 50,000 times.
5. Calculate each player's probability of reaching the quarterfinals.
6. Select one player from each of the eight draw sections.

Recommended ensemble formula:

```text
match_strength =
  0.40 * grass_elo
  + 0.25 * overall_elo
  + 0.15 * recent_form
  + 0.10 * wimbledon_history
  + 0.10 * ranking_signal
```

Then convert the strength difference into match win probability:

```text
P(player_a_beats_player_b) = 1 / (1 + 10 ^ ((rating_b - rating_a) / 400))
```

## Validation

Backtest on prior Wimbledon tournaments.

Primary metric:

- Mean number of actual quarterfinalists captured in the predicted Top 8.

Secondary metrics:

- Brier score for round-reaching probability.
- Log loss for match-level win probability if match data is available.
- Section-level accuracy: did we pick the correct quarterfinalist from each bracket section?

Guardrails:

- Do not use post-tournament results from the same year.
- Use only information available before that year's draw/submission deadline.
- Compare against ranking-only baseline and seed-only baseline.

## Strengths

- Most aligned with the actual tournament structure.
- Naturally handles tough draws and easy draws.
- Easy to explain to judges and leadership.
- Produces probabilities, not just rankings.
- Supports Phase 3 knockout predictions later.

## Weaknesses

- Requires the complete official draw.
- Sensitive to Elo calibration.
- Injury/news adjustments may still need human review.

## Deliverables

- `data/processed/wimbledon_2026_draw_sections.csv`
- `reports/strategy_1_draw_simulation_probabilities.csv`
- `reports/strategy_1_section_winners.md`
- `submissions/strategy_1_phase1_top8.csv`

## Final Output Format

For each tour and section:

```text
Tour, Section, Selected Player, QF Probability, Main Competitors, Key Evidence
```

## Recommendation

Use this as the main model if the official draw is available and parsed correctly. It is the strongest full-fledged approach for a tournament prediction problem.
