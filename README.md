# CourtVision AI

Predictive analytics and explainable AI project for the EXL Analytics & AI Hackathon 2026, focused on Wimbledon 2026 predictions.

## Mission

Build a credible, explainable, and presentation-ready tennis prediction system that can forecast:

- Men's and women's top 8 quarterfinalists
- Knockout match winners across quarterfinals, semifinals, and finals
- Set-difference signal for knockout-stage scoring

## Team

| Name | Email | Location |
| --- | --- | --- |
| Rohit Kumar | rohit6053patel@gmail.com | USA |
| Abhinay Singh | abhi1863@gmail.com | India |
| Harshit Singh | harshitsingh398@gmail.com | India |

**Everyone is a co-owner of this product.** We work as one team with shared ownership. Task distribution will be finalized after our first successful meeting and team discussion. Areas of focus include data engineering, model development, explainability, and presentation.

## Operating Model

We will run like a small product team:

- **Project management:** [Jira Scrum board](https://rohit6053patel.atlassian.net/jira/software/c/projects/CV26/boards/3)
- **Knowledge base:** Confluence
- **Code/versioning:** GitHub
- **Async communication:** WhatsApp or Slack free workspace
- **Meetings:** Google Meet
- **AI automation:** Jira/Confluence/GitHub MCP where available, with manual fallback templates

## Current Status (as of 10 June 2026)

- ✅ Repository created
- ✅ Team invited to GitHub
- ✅ Team added to Google Cloud project `AGI-Lab` with Editor access
- ✅ Registration deadline passed
- ⏳ Jira board setup: **[CV26 in progress](https://rohit6053patel.atlassian.net/jira/software/c/projects/CV26/boards/3)**
- ⏳ Confluence pages: pending
- 📅 **Phase 1 submission in 18 days** (28 June 2026, 11:59 PM IST) — *CRITICAL PRIORITY*

## Important Dates

| Milestone | Date | Status |
| --- | --- | --- |
| Registration deadline | 8 June 2026 | ✅ Closed |
| Doubt session 1 | 12 June 2026 | 📅 Upcoming |
| Doubt session 2 | 19 June 2026 | 📅 Upcoming |
| **Phase 1 submission** | **28 June 2026, 11:59 PM IST** | **🔴 PRIORITY** |
| Phase 2 submission | 3-4 July 2026 | 📅 Upcoming |
| Phase 3 submission | 7-12 July 2026 | 📅 Upcoming |
| Leaderboard published | 14 July 2026 | 📅 Upcoming |
| Final presentations | 20-24 July 2026 | 📅 Upcoming |

## Repository Structure

```text
data/                 Raw and processed datasets; keep large data out of git when possible
docs/                 Team docs, sprint plans, meeting agendas, Confluence-ready pages
jira/                 Jira import CSVs and board setup notes
notebooks/            Exploration and modeling notebooks
reports/              Evaluation summaries and presentation-ready outputs
scripts/              Automation and utility scripts
src/                  Reusable project code
submissions/          Final prediction files and submission packages
```

## Definition of Done

A task is done only when:

- Code or document changes are committed to a branch
- Results are reproducible or clearly documented
- Evaluation impact is recorded when the task affects modeling
- Jira ticket is updated with status, owner, and evidence
- Pull request is reviewed before merging to `main`

## Full Project Setup

Follow these steps when joining the project on a new machine.

### 1. Accept Team Access

Make sure you can access each shared workspace:

- **GitHub:** Accept the repository invitation for `entangleX/CourtVision`.
- **Jira:** Open the [CV26 Scrum Board](https://rohit6053patel.atlassian.net/jira/software/c/projects/CV26/boards/3) and confirm you can view assigned tickets.
- **Confluence:** Confirm you can access the project knowledge base when pages are shared.
- **Google Cloud:** Accept the Google Cloud invitation for project `AGI-Lab`.

Google Cloud project details:

- Project name: `AGI-Lab`
- Project ID: `agi-lab-499017`
- Project number: `8095576102`
- Access: Harshit Singh and Abhinay Singh have Editor permission

Team members do not need to create separate Google Cloud free trials or add credit cards for this project.

### 2. Install Local Tools

Install these tools before working in VS Code:

- [Git](https://git-scm.com/downloads)
- [VS Code](https://code.visualstudio.com/)
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- VS Code extension: Cloud Code
- VS Code extension: Python

Recommended Python setup:

- Python 3.11+
- `venv` for local virtual environments
- Jupyter extension for notebooks

### 3. Clone the Repository

```bash
git clone https://github.com/entangleX/CourtVision.git
cd CourtVision
```

If you use SSH instead of HTTPS:

```bash
git clone git@github.com:entangleX/CourtVision.git
cd CourtVision
```

### 4. Open in VS Code

```bash
code .
```

Install recommended extensions if VS Code prompts you. Use the integrated terminal for the rest of setup.

### 5. Configure Google Cloud

Log in with the same Google account that was invited to `AGI-Lab`:

```bash
gcloud auth login
gcloud config set project agi-lab-499017
gcloud config list
```

Confirm the active project is `agi-lab-499017`.

With the Cloud Code VS Code extension, sign in from the Cloud Code status bar and select project `agi-lab-499017`.

Do not commit API keys, service account JSON files, `.env` files, or access tokens to GitHub.

### 6. Create a Python Workspace

Create and activate a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

If a requirements file is added later, install it with:

```bash
pip install -r requirements.txt
```

For now, keep experiments in `notebooks/` and reusable code in `src/`.

### 7. Explore the Project

- **Sprint plans & decisions:** See `docs/` folder
- **Modeling exploration:** See `notebooks/` (recommended order: 01 → 02 → 03 → 04)
- **Jira board:** [CV26 Scrum Board](https://rohit6053patel.atlassian.net/jira/software/c/projects/CV26/boards/3)
- **Code standards:** Check branch protection rules before opening PRs

### 8. Start Working

1. Review this README and the sprint plan in `docs/`
2. Join the team Jira board and claim a task from Sprint 0
3. Pull the latest `main`: `git pull origin main`
4. Create a feature branch: `git checkout -b feature/task-description`
5. Commit early and often; push to your branch
6. Open a PR for team review before merging to `main`

## Quick Setup (Initial Onboarding)

If setting up the project for the first time:

1. ✅ Repository already created
2. Import `jira/courtvision_ai_jira_backlog.csv` into Jira (if not done)
3. Copy `docs/confluence/*.md` into Confluence pages
4. Ensure all three team members have access to Jira, Confluence, GitHub, Google Cloud, and team chat
5. Start Sprint 0 immediately and keep all decisions in docs

---

## References & Resources

### Tennis-Specific Prediction Models

- **[hikmatazimzade/tennis-ai](https://github.com/hikmatazimzade/tennis-ai)** – XGBoost/CatBoost models with web UI and complete data science pipeline
- **[KutayKoray/ATP-Tennis-Prediction-Using-ANN](https://github.com/KutayKoray/ATP-Tennis-Prediction-Using-ANN)** – Neural network for Wimbledon prediction that outperformed IBM SlamTracker
- **[tommywood81/tennis-tomorrow-public](https://github.com/tommywood81/tennis-tomorrow-public)** – LSTM sequence-based approach for ATP match prediction
- **[neenza/tnnp](https://github.com/neenza/tnnp)** – Neural network model with ~68% accuracy on tennis match prediction
- **[GitHub Tennis Prediction Topic](https://github.com/topics/tennis-prediction)** – Browse 50+ tennis prediction repositories

### Explainable AI & Interpretability

- **[SHAP (SHapley Additive exPlanations)](https://github.com/shap/shap)** ⭐ Industry standard for model interpretability; integrates with XGBoost, scikit-learn, neural networks
- **[InterpretML (Microsoft)](https://github.com/interpretml/interpret)** – Explainable Boosting Machine (EBM) and interactive visualizations
- **[Awesome Explainable AI](https://github.com/wangyongjie-ntu/Awesome-Explainable-AI)** – Curated XAI libraries, papers, and tutorials

### Data & APIs

- **[Tennis-API.com](https://tennis-api.com/)** – Live scores, rankings, historical match data, ATP/WTA coverage
- **[Kaggle Tennis Datasets](https://www.kaggle.com/search?q=tennis+dataset)** – Historical match data and player statistics
- **[ATP Tour Official Data](https://www.atptour.com/)** – Authoritative source for player rankings and match records

### Hackathon & Competition Examples

- **[Kaggle March Madness Solutions](https://github.com/topics/march-madness)** – Tournament prediction structure similar to Wimbledon knockout format
- **[NFL Big Data Bowl](https://github.com/topics/nfl-big-data-bowl)** – Hackathon format, workflow patterns, and submission guidelines

### Recommended Learning Resources

- **Feature Engineering for Sports:** Head-to-head records, surface-specific stats, player ranking trends, rolling performance indices
- **Common Approaches:** XGBoost/CatBoost for interpretability, LSTM for temporal patterns, ensemble methods for robustness
- **Evaluation Metrics:** Accuracy, log-loss, ROC-AUC, custom metrics for set-difference signals

---

Webhook smoke test: Teams bot delivery check.
