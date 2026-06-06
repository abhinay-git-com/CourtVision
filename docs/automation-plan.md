# Free Automation Plan

## Goal

Use AI and automation to reduce project-management overhead while keeping the stack free.

## Free Stack

| Need | Tool |
| --- | --- |
| Jira automation | Jira Free automation rules and CSV import |
| Confluence documentation | Confluence Free |
| GitHub versioning | GitHub Free |
| AI assistant | Codex or ChatGPT for drafting, summarizing, and code help |
| Local scripts | Python or shell scripts committed to repo |
| Meetings | Google Meet |

## MCP Automation Targets

When credentials are available, configure MCP servers or API scripts for:

- Creating Jira tickets from markdown backlog
- Updating Jira ticket status from GitHub PR labels
- Creating Confluence pages from `docs/confluence/*.md`
- Summarizing daily standups into a Confluence meeting note
- Generating sprint review notes from merged pull requests

## Manual Fallback

Until API credentials are connected:

- Import `jira/courtvision_ai_jira_backlog.csv` into Jira.
- Copy markdown pages from `docs/confluence/` into Confluence.
- Use GitHub issue templates and pull request templates for discipline.
- Keep weekly review notes in `docs/confluence/decision-log.md`.

## Suggested Jira Automation Rules

1. When PR link is added to a Jira ticket, move ticket to **In Review**.
2. When ticket is moved to **Done**, require a comment with evidence.
3. Every weekday morning IST, send reminder for tickets in **Blocked**.
4. Every Friday evening IST, summarize incomplete sprint tickets.

