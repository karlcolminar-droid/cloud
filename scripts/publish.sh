#!/usr/bin/env bash
# Helper to push this project to GitHub and create a repo using gh (GitHub CLI).
# Requires: git and gh CLI configured with authentication.

set -e
if ! command -v git >/dev/null 2>&1; then
  echo "git not found. Install git and run this script again." >&2
  exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) not found. You can still push to a remote manually." >&2
  echo "To create a repo via gh: gh repo create <name> --public --source=. --remote=origin --push"
  exit 1
fi

REPO_NAME=${1:-cloud-render}

git init || true
git add .
if git commit -m "Prepare app for deployment"; then
  echo "Committed changes"
else
  echo "Nothing to commit or commit failed (check git status)" >&2
fi

echo "Creating GitHub repo: $REPO_NAME"
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push

echo "Repository created and pushed. URL: https://github.com/$(gh repo view --json owner --jq .owner)/$REPO_NAME"
