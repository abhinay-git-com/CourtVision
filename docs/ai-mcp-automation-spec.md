# AI and MCP Automation Spec

## Principle

Automate repetitive project management, but keep the source of truth clear:

- Jira is source of truth for work status.
- GitHub is source of truth for code.
- Confluence is source of truth for decisions and documentation.

## Automation Level 1: Ready Now, No Credentials

Use local prompts:

- `scripts/standup_prompt.md`
- `scripts/sprint_review_prompt.md`

Workflow:

1. Paste team updates into the prompt.
2. Ask AI to summarize.
3. Post result to Confluence.
4. Update Jira tickets manually.

## Automation Level 2: API Scripts

After creating Jira and Confluence API tokens, add scripts that:

- Create Jira issues from CSV
- Update ticket status
- Create Confluence pages from markdown
- Comment on Jira tickets with GitHub PR links

Required secrets:

```text
ATLASSIAN_SITE_URL=
ATLASSIAN_EMAIL=
ATLASSIAN_API_TOKEN=
JIRA_PROJECT_KEY=CVA
GITHUB_TOKEN=
```

Store these in `.env` locally or GitHub Actions secrets. Never commit them.

## Automation Level 3: MCP

If MCP servers are available for Jira, Confluence, and GitHub:

### Jira MCP

Target actions:

- Create tickets from `jira/courtvision_ai_jira_backlog.csv`
- Move tickets based on PR status
- Summarize blocked work
- Generate sprint report

### Confluence MCP

Target actions:

- Publish pages from `docs/confluence/`
- Append decision log entries
- Create meeting notes from standup summaries

### GitHub MCP

Target actions:

- Create issues from Jira tickets when useful
- Summarize merged PRs
- Link PRs back to Jira tickets

## Suggested AI Commands

```text
Summarize today's standup and identify Jira tickets that need updates.
```

```text
Create a Confluence meeting note from these raw updates.
```

```text
Review this model experiment result and suggest whether it should replace the current baseline.
```

```text
Turn this sprint goal into Jira tickets with acceptance criteria.
```

## Guardrails

- AI can draft updates, but a human confirms final predictions.
- AI-generated model explanations must match actual metrics and features.
- No credentials, private data, or hackathon-sensitive files should be pasted into public AI tools.
- Use clean evidence links for every automated status update.

