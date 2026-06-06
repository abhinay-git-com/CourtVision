# CourtVision AI

Predictive analytics and explainable AI project for the EXL Analytics & AI Hackathon 2026, focused on Wimbledon 2026 predictions.

## Mission

Build a credible, explainable, and presentation-ready tennis prediction system that can forecast:

- Men's and women's top 8 quarterfinalists
- Knockout match winners across quarterfinals, semifinals, and finals
- Set-difference signal for knockout-stage scoring

## Team

| Name | Role | Email | Location |
| --- | --- | --- | --- |
| Rohit Kumar | Team Lead, Product Owner, Final Presenter | rohit6053patel@gmail.com | USA |
| Abhinay Singh | Data Engineering, Feature Pipeline | abhi1863@gmail.com | India |
| Harshit Singh | Modeling, Evaluation, Experiment Tracking | harshitsingh398@gmail.com | India |

## Operating Model

We will run like a small product team:

- **Project management:** Jira Scrum board
- **Knowledge base:** Confluence
- **Code/versioning:** GitHub
- **Async communication:** WhatsApp or Slack free workspace
- **Meetings:** Google Meet
- **AI automation:** Jira/Confluence/GitHub MCP where available, with manual fallback templates

## Important Dates

| Milestone | Date |
| --- | --- |
| Registration deadline | 8 June 2026 |
| Doubt session 1 | 12 June 2026 |
| Doubt session 2 | 19 June 2026 |
| Phase 1 submission | 28 June 2026, 11:59 PM IST |
| Phase 2 submission | 3-4 July 2026 |
| Phase 3 submission | 7-12 July 2026 |
| Leaderboard published | 14 July 2026 |
| Final presentations | 20-24 July 2026 |

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

## Quick Start

1. Create the GitHub repository.
2. Import `jira/courtvision_ai_jira_backlog.csv` into a Jira Scrum project.
3. Copy `docs/confluence/*.md` into Confluence pages.
4. Invite the three team members to Jira, Confluence, GitHub, and the team chat.
5. Start Sprint 0 immediately and keep all decisions in docs.

