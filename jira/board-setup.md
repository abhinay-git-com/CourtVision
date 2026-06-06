# Jira Board Setup

## Recommended Setup

- Product: Jira Software Cloud Free
- Project type: Scrum
- Project name: CourtVision AI
- Project key: CVA
- Board columns:
  - Backlog
  - Selected for Development
  - In Progress
  - Blocked
  - In Review
  - Done

## Components

- Project Setup
- Data
- Modeling
- Evaluation
- Submission
- Documentation
- Presentation
- Automation

## Labels

- phase-1
- phase-2
- phase-3
- data
- model
- eval
- docs
- automation
- urgent

## Import Instructions

1. Create a Jira Software Scrum project named `CourtVision AI`.
2. Go to Jira import from CSV.
3. Upload `jira/courtvision_ai_jira_backlog.csv`.
4. Map:
   - Summary to Summary
   - Issue Type to Issue Type
   - Description to Description
   - Assignee to Assignee
   - Priority to Priority
   - Story Points to Story point estimate
   - Labels to Labels
   - Components to Components
5. Create Sprint 0 and move setup tickets into it.

