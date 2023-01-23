# git commands

Override git commands to add magic.
Create branches and commit messages based in the issue key.

## Installation

1. Clone the repository `git clone git@github.com:SebastianGoral-freenet/git_commands.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add init script to .bash_profile: `echo "source PATH_TO_REPOSITORY/init.sh" >> ~/.bash_profile"`
4. Open a new shell

## Commands overview

The following commands are currently available:

### create_branch

**Usage:** git create-branch $issue

Creates a new branch with the issue key and summary.

**Examples:**
* `git create-branch 123` creates a branch for GRAON-123
* `git create-branch ERP-123` creates a branch for ERP-123

### commit

**Usage:** git commit $any-normal-git-commit-options

Commit the staged changes with a commit message template based in the issue key and summary of the current branch.
Requires an issue key in the branch name (e.g. `feature/GRAON-123-this-is-an-issue`).
