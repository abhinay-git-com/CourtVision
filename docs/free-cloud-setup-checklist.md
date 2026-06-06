# Free Cloud Setup Checklist

This setup keeps the team on free plans for a 3-person hackathon team.

## 1. Atlassian

Use Atlassian Free for Jira and Confluence. Atlassian currently positions the free cloud plan around small teams of up to 10 users, which is enough for this team.

### Jira

1. Go to Atlassian and create a free Jira Software site.
2. Create project:
   - Template: Scrum
   - Project name: CourtVision AI
   - Project key: CVA
3. Invite:
   - Rohit Kumar: rohit6053patel@gmail.com
   - Abhinay Singh: abhi1863@gmail.com
   - Harshit Singh: harshitsingh398@gmail.com
4. Import `jira/courtvision_ai_jira_backlog.csv`.
5. Create the board columns listed in `jira/board-setup.md`.
6. Start Sprint 0.

### Confluence

1. Create a free Confluence space named `CourtVision AI`.
2. Copy pages from `docs/confluence/`:
   - `home.md`
   - `modeling-strategy.md`
   - `dataset-research.md`
   - `decision-log.md`
   - `submission-checklist.md`
3. Add Jira board and GitHub links to the home page.

## 2. GitHub

1. Create a new repository:
   - Name: `courtvision-ai`
   - Visibility: private until submission, public only if allowed by hackathon rules
2. Add collaborators:
   - rohit6053patel@gmail.com
   - abhi1863@gmail.com
   - harshitsingh398@gmail.com
3. Push this local repo.
4. Create labels:
   - `data`
   - `model`
   - `evaluation`
   - `documentation`
   - `submission`
   - `blocked`
   - `urgent`
5. Use pull requests for all changes.

## 3. Communication

Use WhatsApp for speed or Slack Free if you want more organization.

Recommended channels if using Slack:

- `#announcements`
- `#daily-standup`
- `#data`
- `#modeling`
- `#submission`
- `#random`

## 4. Meetings

Use Google Meet because it is free and easy across USA/India.

Create recurring calendar events:

- Sprint Planning: Saturday 9:30 PM IST / 12:00 PM ET
- Midweek Sync: Wednesday 9:30 PM IST / 12:00 PM ET
- Sprint Review + Retro: Friday 9:30 PM IST / 12:00 PM ET

## 5. Cloud Folder

Use Google Drive Free for non-code files if needed:

```text
CourtVision AI/
  01 Admin/
  02 Data Notes/
  03 Submissions/
  04 Presentation/
  05 Meeting Recordings/
```

Do not store private credentials in Drive or GitHub.

