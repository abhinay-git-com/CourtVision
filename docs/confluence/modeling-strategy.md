# Modeling Strategy

## Prediction Problems

1. Top 8 quarterfinalist likelihood for men's and women's draws.
2. Match winner probability for potential matchups.
3. Knockout-stage winner and set-difference prediction.

## Candidate Features

- Current ranking and ranking trend
- Elo or surface-adjusted Elo
- Grass-court performance
- Recent form
- Grand Slam performance
- Head-to-head record
- Serve and return statistics where available
- Injury or withdrawal signals from public sources
- Draw difficulty once the draw is known

## Baselines

- Ranking-only baseline
- Elo baseline
- Logistic regression match model
- Gradient-boosted model if data quality supports it

## Evaluation

- Backtest on previous Wimbledon tournaments
- Compare against ranking-only baseline
- Track calibration, accuracy, log loss, and top 8 hit rate
- Document where the model is uncertain

## Explainability

Every final prediction should include:

- Probability or confidence tier
- Top supporting factors
- Key risks
- Human-readable rationale

