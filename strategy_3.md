# Strategy 3: Hybrid Expert-Rules and Bayesian Ranking Model

## Best Owner

Abhinay

## Core Idea

Build a conservative, explainable model that combines rankings, grass form, Wimbledon history, and uncertainty penalties into a Bayesian-style player score. This strategy is designed to be robust when data is incomplete, noisy, or hard to model with complex ML.

This should act as our sanity-check model and presentation-friendly fallback.

## Decision This Model Supports

Which players are reliable, explainable quarterfinalist picks when we want to avoid overfitting and keep the reasoning transparent?

## Data Inputs

- Entry ranks.
- Seeds.
- Historical Wimbledon outcomes.
- Grass-court win rates.
- Recent form.
- Head-to-head records when available.
- Official draw sections.
- Injury and withdrawal news.

## Feature Set

Core score:

- Ranking strength.
- Seeding strength.
- Grass-court performance.
- Recent-form performance.
- Wimbledon history.
- Grand Slam consistency.

Uncertainty adjustments:

- Low grass sample-size penalty.
- Recent injury penalty.
- Poor recent form penalty.
- Difficult draw-section penalty.
- Volatile player penalty.

## How to Use Our Historical and Draw Data

Use this strategy as the clearest manual-audit layer over our existing data:

- `data/processed/phase1_player_features.csv`: primary input for ranking, grass, Wimbledon, and recent-form scores.
- `data/processed/phase1_rolling_form_trends.csv`: input for momentum and volatility checks.
- `data/processed/wimbledon_2026_mens_entries.csv`: men's candidate pool.
- `data/processed/wimbledon_2026_womens_entries.csv`: women's candidate pool.
- `data/processed/match_history_combined.csv`: source for historical Wimbledon and grass-court validation.

Step-by-step workflow:

1. Refresh local processed files:

```bash
python scripts/process_and_upload.py --local-only
python scripts/phase1_model.py
```

2. Build the scoring sheet.

Create one row per 2026 entrant using `phase1_player_features.csv`. Include rank, seed if available, grass performance, recent form, Wimbledon history, and Grand Slam consistency.

3. Smooth small-sample rates.

Use Bayesian smoothing for grass win rate and Wimbledon win rate so players with tiny samples do not get unrealistic scores.

4. Add official draw sections.

When the draw is saved locally, create:

```text
data/processed/wimbledon_2026_draw_sections.csv
```

Minimum required columns:

```text
tour, draw_position, section, seed, player, first_round_opponent
```

Join this file to the scoring sheet by `tour` and `player`.

5. Apply section-level risk adjustment.

For each section, subtract a draw difficulty penalty if the player's path includes a top seed, elite grass player, or dangerous recent-form opponent before the quarterfinal.

6. Produce final section rankings.

Sort by adjusted score inside each of the eight sections. Select the top player as the pick and the second player as backup.

## Modeling Method

Create a weighted score for every player:

```text
base_score =
  0.30 * ranking_score
  + 0.20 * seed_score
  + 0.20 * grass_score
  + 0.15 * recent_form_score
  + 0.10 * wimbledon_history_score
  + 0.05 * grand_slam_score
```

Then apply risk adjustment:

```text
final_score = base_score - injury_penalty - draw_difficulty_penalty - volatility_penalty
```

Use a Bayesian smoothing idea for small samples:

```text
smoothed_grass_win_rate =
  (grass_wins + prior_strength * tour_average_grass_win_rate)
  / (grass_matches + prior_strength)
```

This prevents a player with a 3-0 grass record from being treated as more reliable than a player with a 45-15 grass record.

## Draw Selection

1. Score every player.
2. Split the official draw into eight sections.
3. Rank players inside each section.
4. Select the top adjusted-score player per section.
5. Record the second choice as backup in case of withdrawal or late risk news.

## Validation

Primary metric:

- Mean Top 8 hits on historical Wimbledon years.

Secondary metrics:

- Accuracy by draw section.
- Agreement with seed baseline.
- Upset capture rate.
- Stability of picks when weights are changed by plus or minus 10%.

Guardrails:

- No hidden subjective picks without documented reason.
- Every manual adjustment needs a source or explicit rationale.
- Keep weights simple enough to explain in one slide.

## Strengths

- Very explainable.
- Robust with small data.
- Easy to update quickly before submission.
- Good for final human review.
- Useful if complex models produce suspicious picks.

## Weaknesses

- Less adaptive than machine learning.
- Weight choices are partly subjective.
- May underpredict surprising breakout players.

## Deliverables

- `reports/strategy_3_weight_table.md`
- `reports/strategy_3_section_rankings.csv`
- `reports/strategy_3_risk_adjustments.md`
- `submissions/strategy_3_phase1_top8.csv`

## Final Output Format

For each section:

```text
Tour, Section, Pick, Backup Pick, Adjusted Score, Risk Notes
```

## Recommendation

Use this as the explainability and sanity-check track. It should help us defend the final answer even when the more complex models disagree.
