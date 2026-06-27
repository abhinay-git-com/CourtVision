# Strategy 2: Feature-Rich Gradient Boosting Model

## Best Owner

Harshit

## Core Idea

Build a supervised machine learning model that predicts whether each player reaches the Wimbledon quarterfinals using player-level and draw-level features. This approach focuses on discovering nonlinear relationships across ranking, surface form, recent momentum, historical performance, and draw difficulty.

This should be our strongest machine-learning track and a useful challenger to the Elo simulation.

## Decision This Model Supports

Which players have the highest probability of becoming Wimbledon quarterfinalists after accounting for form, surface fit, history, and draw context?

## Data Inputs

- Historical ATP and WTA match logs.
- Player rankings and entry ranks.
- Historical Wimbledon outcomes.
- Grass-court match results.
- Recent match results before Wimbledon.
- Official 2026 draw sections.
- Seed and opponent-path features.

## Prediction Target

For each player in each historical Wimbledon draw:

```text
target = 1 if player reached the quarterfinals
target = 0 otherwise
```

## Feature Set

Player strength:

- Entry rank.
- Seed.
- Overall win rate.
- Grass-court win rate.
- Wimbledon career win rate.
- Grand Slam win rate.

Recent form:

- Last 5 match win rate.
- Last 10 match win rate.
- Last 20 match win rate.
- Recent grass win rate.
- Recent opponent quality.

Draw context:

- Draw section.
- Average rank of possible opponents before QF.
- Strongest possible seeded opponent before QF.
- Number of dangerous unseeded players in section.
- Whether a top 4 seed is in the same section.

Risk features:

- Injury or retirement flag.
- Recent long-match fatigue.
- First-round upset risk.
- Low grass sample-size flag.

## How to Use Our Historical and Draw Data

Start from the local processed files already available in the repo:

- `data/processed/match_history_combined.csv`: match-level history for ATP and WTA.
- `data/processed/phase1_player_features.csv`: player-level engineered features for 2026.
- `data/processed/phase1_rolling_form_trends.csv`: rolling player form features.
- `data/processed/phase1_draw_classification_matrix.csv`: current player-level classification matrix.
- `data/processed/wimbledon_2026_mens_entries.csv`: men's Wimbledon 2026 entrants.
- `data/processed/wimbledon_2026_womens_entries.csv`: women's Wimbledon 2026 entrants.

Step-by-step workflow:

1. Rebuild data artifacts:

```bash
python scripts/process_and_upload.py --local-only
python scripts/phase1_model.py
```

2. Create historical training rows.

From `match_history_combined.csv`, create one row per player per Wimbledon year. The target is whether the player reached the quarterfinal. Use only matches and form data available before that Wimbledon started.

3. Add pre-tournament features.

For every player-year, calculate ranking, grass win rate, recent form, Wimbledon history, Grand Slam consistency, and surface-specific momentum. For 2026, reuse `phase1_player_features.csv` and `phase1_rolling_form_trends.csv`.

4. Add draw features after the official draw is available.

Create or join this file:

```text
data/processed/wimbledon_2026_draw_sections.csv
```

Minimum required columns:

```text
tour, draw_position, section, seed, player, first_round_opponent
```

Then engineer draw-context features:

- average rank in section
- best-ranked possible opponent before QF
- number of seeded players in section
- number of strong grass players in section
- whether the player has a top 4 seed in their path

5. Train with year-based validation.

Do not randomly split player rows. Train on earlier Wimbledon years and validate on later years. Example:

```text
Train: 2014-2021
Validate: 2022

Train: 2014-2022
Validate: 2023

Train: 2014-2023
Validate: 2024
```

6. Predict 2026.

Score every 2026 draw player, rank players inside each section, and select the highest-probability player from each section.

## Modeling Method

Recommended model:

```text
CatBoost or LightGBM classifier
```

Fallback if dependencies are difficult:

```text
sklearn HistGradientBoostingClassifier or RandomForestClassifier
```

Training setup:

1. Create one row per player per Wimbledon year.
2. Use only pre-tournament features.
3. Train on earlier years.
4. Validate on later years using walk-forward validation.
5. Predict 2026 quarterfinal probability for every draw player.
6. Select one highest-probability player per draw section.

## Validation

Primary metric:

- Mean Top 8 hits across historical Wimbledon years.

Secondary metrics:

- Section-level winner accuracy.
- Brier score.
- Precision among top 8 predicted players.
- Calibration curve: predicted probability vs observed QF rate.

Guardrails:

- Avoid random train-test split because that leaks future information.
- Use year-based validation.
- Keep ATP and WTA models separate unless sample size becomes too small.
- Compare against ranking-only, seed-only, and Elo-only baselines.

## Strengths

- Captures nonlinear patterns that simple Elo can miss.
- Can learn interaction effects, such as "strong grass form matters more for lower-ranked players."
- Gives feature importance for presentation.
- Good challenger model for the final ensemble.

## Weaknesses

- Historical Wimbledon sample size is limited.
- Can overfit if too many features are added.
- Needs careful leakage control.
- Less intuitive than Elo unless explained well.

## Deliverables

- `data/processed/strategy_2_player_training_matrix.csv`
- `reports/strategy_2_backtest_results.csv`
- `reports/strategy_2_feature_importance.md`
- `reports/strategy_2_2026_qf_probabilities.csv`
- `submissions/strategy_2_phase1_top8.csv`

## Final Output Format

For each player:

```text
Tour, Section, Player, QF Probability, Rank, Seed, Top Features
```

## Recommendation

Use this as the main ML challenger. If it agrees with Strategy 1, those picks become high-confidence. If it disagrees, investigate whether the difference comes from draw path, surface form, or model overfitting.
