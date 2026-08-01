# Contributing

## Workflow

1. Create a focused branch from the default branch.
2. Make the smallest change that addresses the issue.
3. Update the relevant wiki page or README when behavior or setup changes.
4. Run backend and frontend checks relevant to the change.
5. Review the diff for secrets, generated files, and unrelated edits.
6. Open a pull request with a clear summary and validation results.

## Conventions

- Keep backend code compatible with the pinned dependencies in `backend/requirements.txt`.
- Keep API behavior documented in [API Reference](API-Reference.md).
- Never commit `.env`, `.env.local`, passwords, tokens, or production credentials.
