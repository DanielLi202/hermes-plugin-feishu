# Contributing

Issues and pull requests are welcome. This is a single-maintainer plugin; small, focused changes are easiest to review.

## Local setup

Use the source tree directly:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
```

No third-party test runner is required for the current suite.

## Your first contribution

New here? Start with the [good first issues](https://github.com/DanielLi202/hermes-tag/contribute) — small, self-contained tasks with the exact files to touch and the verify command above. Comment on one and the maintainer will help you get going; no prior open-source experience needed.

## Branches and PRs

- Create a topic branch for each change.
- Keep behavior changes, docs, and packaging cleanup in separate PRs when possible.
- Include the test command output in the PR description.
- Do not include secrets, live Feishu tokens, or private chat content in issues, tests, or logs.

No CLA is required.
