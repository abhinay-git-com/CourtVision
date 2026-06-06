# GitHub Workflow

## Branches

- `main`: stable, submission-ready work only
- `feature/<ticket-key>-short-description`: new work
- `fix/<ticket-key>-short-description`: fixes
- `docs/<ticket-key>-short-description`: documentation-only work

## Pull Request Rules

- Every meaningful change goes through a pull request.
- PR title should include Jira key when available, for example `CVA-12 Build Elo baseline`.
- At least one teammate should review before merge.
- Keep PRs small enough to review quickly.

## Commit Style

Use clear commits:

```text
CVA-12 add ranking baseline model
CVA-14 document dataset schema
CVA-18 update phase 1 prediction checklist
```

## Release Tags

Create tags for submissions:

```text
phase-1-submission
phase-2-submission
phase-3-submission
final-presentation
```

