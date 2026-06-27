# Strategy 1 Draw Simulation Status

Generated: 2026-06-27T12:34:50-04:00

## Status

Complete. The official singles draw was parsed and the draw-aware Elo simulation ran successfully.

## Inputs

- Draw source: `consolidated_workbook`
- `data/tennis_data_consolidated (2).xlsx`
- `data/processed/phase1_player_features.csv`

## Fallback Inputs

- `data/2026_MS_draw.pdf`
- `data/2026_LS_draw (1).pdf`

## Outputs

- `data/processed/wimbledon_2026_draw_sections.csv`
- `reports/strategy_1_draw_simulation_probabilities.csv`
- `reports/strategy_1_draw_simulation_warnings.csv`
- `submissions/strategy_1_phase1_top8.csv`

## Simulation

- Simulations per tour: 20000
- Conservative generic fallback ratings: 6 players

## Section Picks

| Category | Section | Player | QF probability | Backup |
| --- | ---: | --- | ---: | --- |
| Men's Singles | 1 | SINNER, Jannik (ITA) | 0.6831 | JODAR, Rafael (ESP) (0.1037) |
| Men's Singles | 2 | MEDVEDEV, Daniil | 0.2544 | PAUL, Tommy (USA) (0.1994) |
| Men's Singles | 3 | AUGER-ALIASSIME, Felix (CAN) | 0.2541 | TIEN, Learner (USA) (0.1583) |
| Men's Singles | 4 | DJOKOVIC, Novak (SRB) | 0.4219 | RUBLEV, Andrey (0.1494) |
| Men's Singles | 5 | DE MINAUR, Alex (AUS) | 0.2477 | COBOLLI, Flavio (ITA) (0.1328) |
| Men's Singles | 6 | SHELTON, Ben (USA) | 0.2629 | FILS, Arthur (FRA) (0.1611) |
| Men's Singles | 7 | FRITZ, Taylor (USA) | 0.2754 | TIAFOE, Frances (USA) (0.2129) |
| Men's Singles | 8 | ZVEREV, Alexander (GER) | 0.3762 | LEHECKA, Jiri (CZE) (0.1489) |
| Women's Singles | 1 | SABALENKA, Aryna | 0.5720 | OSAKA, Naomi (JPN) (0.1610) |
| Women's Singles | 2 | ANDREEVA, Mirra | 0.2304 | MUCHOVA, Karolina (CZE) (0.2304) |
| Women's Singles | 3 | PEGULA, Jessica (USA) | 0.4125 | JOVIC, Iva (USA) (0.1551) |
| Women's Singles | 4 | GAUFF, Coco (USA) | 0.3244 | BENCIC, Belinda (SUI) (0.2197) |
| Women's Singles | 5 | SVITOLINA, Elina (UKR) | 0.3064 | KOSTYUK, Marta (UKR) (0.2433) |
| Women's Singles | 6 | SWIATEK, Iga (POL) | 0.3922 | EALA, Alexandra (PHI) (0.1407) |
| Women's Singles | 7 | NOSKOVA, Linda (CZE) | 0.2784 | KEYS, Madison (USA) (0.2478) |
| Women's Singles | 8 | RYBAKINA, Elena (KAZ) | 0.3771 | SHNAIDER, Diana (0.1244) |
