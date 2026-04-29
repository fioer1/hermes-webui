# Hermes WebUI - Repository Guide

Instructions for AI coding assistants and developers working on the `hermes-webui` codebase.

## Repository Sync Workflow

Before changing remotes, rebasing `master`, or force-pushing, read
[`SYNC_WORKFLOW.md`](SYNC_WORKFLOW.md).

This repo is part of a two-repo setup:

1. `Hermes Agent`
2. `Hermes WebUI`

The sync guide records:

- which remote must be `origin` and which must be `upstream`
- the current known history status of both repos
- the safe update flow for the clean `Hermes WebUI` branch
- the still-pending cleanup status of `Hermes Agent`
- the minimum checks another machine's AI assistant must run before touching history

## Repo Identity

- Official upstream: `https://github.com/nesquena/hermes-webui.git`
- Personal/shared fork: `https://github.com/fioer1/hermes-webui.git`
- Primary branch in this repo: `master`

## Verification

For Git / sync work, prefer the targeted regression suite documented in
[`SYNC_WORKFLOW.md`](SYNC_WORKFLOW.md).
