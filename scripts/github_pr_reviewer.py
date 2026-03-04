#!/usr/bin/env python3
"""
GitHub PR Reviewer - Automatically reviews PRs and provides improvement suggestions
"""

import os
import json
import requests
import sys

REPO = "Kyla-Chat/Kyla-Go"
TOKEN_FILE = "/root/.openclaw/workspace/.github_token"
STATE_FILE = "/root/.openclaw/workspace/memory/github_pr_state.json"

def read_token():
    """Read GitHub token from file"""
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def get_pr_details(pr_number, token):
    """Fetch PR details from GitHub API"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_pr_files(pr_number, token):
    """Get list of files changed in the PR"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_code_changes(files):
    """Analyze code changes and generate review suggestions"""
    suggestions = []
    
    for file in files:
        filename = file['filename']
        additions = file['additions']
        deletions = file['deletions']
        patch = file.get('patch', '')
        
        # Basic analysis
        review_points = []
        
        # Check file size
        if additions > 300:
            review_points.append(f"Large changeset ({additions} additions). Consider breaking into smaller PRs for easier review.")
        
        # Go-specific checks
        if filename.endswith('.go'):
            if 'TODO' in patch or 'FIXME' in patch:
                review_points.append("Contains TODO/FIXME comments. Please address or create issues for them.")
            
            if 'panic(' in patch:
                review_points.append("Uses panic(). Consider using proper error handling with error returns.")
            
            if 'fmt.Print' in patch:
                review_points.append("Contains fmt.Print statements. Consider using proper logging instead.")
        
        if review_points:
            suggestions.append({
                'file': filename,
                'points': review_points
            })
    
    return suggestions

def post_pr_comment(pr_number, comment, token):
    """Post a review comment on the PR"""
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201

def mark_as_reviewed(pr_number):
    """Mark PR as reviewed in state file"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {"reviewed_prs": []}
    
    if str(pr_number) not in state["reviewed_prs"]:
        state["reviewed_prs"].append(str(pr_number))
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def review_pr(pr_number):
    """Main review function"""
    token = read_token()
    
    # Get PR details
    pr = get_pr_details(pr_number, token)
    print(f"Reviewing PR #{pr_number}: {pr.get('title', 'N/A')}")
    
    # Get changed files
    files = get_pr_files(pr_number, token)
    
    # Analyze changes
    suggestions = analyze_code_changes(files)
    
    # Generate review comment
    if suggestions:
        comment_body = f"## 🤖 Automated Code Review\n\n"
        comment_body += f"Hi! LemonAi here 😼 I've reviewed this PR and have some suggestions:\n\n"
        
        for suggestion in suggestions:
            comment_body += f"### `{suggestion['file']}`\n"
            for point in suggestion['points']:
                comment_body += f"- {point}\n"
            comment_body += "\n"
        
        comment_body += "\n---\n*This is an automated review. Human review is still recommended!*"
        
        # Post comment
        if post_pr_comment(pr_number, comment_body, token):
            print(f"✓ Comment posted on PR #{pr_number}")
        else:
            print(f"✗ Failed to post comment on PR #{pr_number}")
    else:
        # Post a simple acknowledgment
        comment_body = f"## 🤖 Automated Code Review\n\n"
        comment_body += f"Hi! LemonAi here 😼 I've reviewed this PR.\n\n"
        comment_body += f"No major issues detected in the automated scan. The changes look clean!\n\n"
        comment_body += f"**Summary:**\n"
        comment_body += f"- Files changed: {len(files)}\n"
        comment_body += f"- Total additions: {sum(f['additions'] for f in files)}\n"
        comment_body += f"- Total deletions: {sum(f['deletions'] for f in files)}\n\n"
        comment_body += f"---\n*This is an automated review. Human review is still recommended!*"
        
        if post_pr_comment(pr_number, comment_body, token):
            print(f"✓ Acknowledgment posted on PR #{pr_number}")
    
    # Mark as reviewed
    mark_as_reviewed(pr_number)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: github_pr_reviewer.py <pr_number>")
        sys.exit(1)
    
    pr_number = sys.argv[1]
    review_pr(pr_number)
