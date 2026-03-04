#!/bin/bash

# GitHub PR Monitor Script
# Checks for new pull requests and triggers review

REPO="Kyla-Chat/Kyla-Go"
TOKEN_FILE="/root/.openclaw/workspace/.github_token"
STATE_FILE="/root/.openclaw/workspace/memory/github_pr_state.json"

# Read token
TOKEN=$(cat "$TOKEN_FILE")

# Fetch open PRs
PRS=$(curl -s -H "Authorization: token $TOKEN" "https://api.github.com/repos/$REPO/pulls?state=open")

# Initialize state file if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo '{"reviewed_prs": []}' > "$STATE_FILE"
fi

# Extract PR numbers
PR_NUMBERS=$(echo "$PRS" | jq -r '.[].number')

if [ -z "$PR_NUMBERS" ]; then
    echo "No open pull requests found."
    exit 0
fi

# Check each PR
for PR_NUM in $PR_NUMBERS; do
    # Check if already reviewed
    REVIEWED=$(jq -r ".reviewed_prs | contains([\"$PR_NUM\"])" "$STATE_FILE")
    
    if [ "$REVIEWED" = "false" ]; then
        echo "New PR found: #$PR_NUM"
        echo "TRIGGER_REVIEW:$PR_NUM"
    fi
done
