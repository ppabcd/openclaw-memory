#!/bin/bash
# Quick script to check for open PRs in Kyla-Go

TOKEN=$(cat /root/.openclaw/workspace/.github_token)
curl -s -H "Authorization: token $TOKEN" https://api.github.com/repos/Kyla-Chat/Kyla-Go/pulls?state=open | jq -r '.[] | "PR #\(.number): \(.title) by @\(.user.login)"'
