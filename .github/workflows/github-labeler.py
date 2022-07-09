#!/usr/bin/env python3

"""

The script applies a label in the form "Target: {branchName}. If necessary, it
removes labels in the same form, but NOT for the target branch. For instance, if
someone edited the target branch from v4.0.x to v5.0.x

"""

import os
import re
import sys

from github import Github

# ==============================================================================

GITHUB_BASE_REF   = os.environ.get('GITHUB_BASE_REF')
GITHUB_TOKEN      = os.environ.get('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
GITHUB_REF        = os.environ.get('GITHUB_REF')

# Sanity check
if (GITHUB_BASE_REF is None or
    GITHUB_TOKEN is None or
    GITHUB_REPOSITORY is None):
    print("Error: this script is designed to run as a Github Action")
    exit(1)

# ==============================================================================

# Given a pullRequest object, the function checks what labels are currently on
# the pull request, removes any matching the form "Target: {branch}" (if
# {branch} is not the current target branch), and adds the correct label.
def ensureLabels(pullRequest):
    prBaseBranch = GITHUB_BASE_REF
    prTargetLabels = list()
    needsLabel = True
    for label in pullRequest.get_labels():
        if label.name.startswith("Target:"):
            prTargetLabels.append(label)
    for targetLabel in prTargetLabels:
        if targetLabel.name != f"Target: {prBaseBranch}":
            pullRequest.remove_from_labels(targetLabel)
    if needsLabel:
        pullRequest.add_to_labels(f"Target: {prBaseBranch}")
    return

# ==============================================================================

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)
# Extract the PR number from GITHUB_REF
print(GITHUB_REF)
match  = re.search("/(\d+)/", GITHUB_REF)
pr_num = int(match.group(1))
pr     = repo.get_pull(pr_num)
ensureLabels(pr)

