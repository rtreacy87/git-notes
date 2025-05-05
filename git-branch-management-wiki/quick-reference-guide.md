# Quick Reference Guide: Git Branch Management

This guide provides a quick reference for common Git commands used in branch management, particularly when merging updates from the main branch into a testing branch.

## Complete Workflow for Updating Testing Branch from Main

```bash
# 1. Switch to your testing branch
git checkout testing_branch_v1.0.0

# 2. Fetch the latest changes from the remote repository
git fetch origin

# 3. Merge the main branch into your testing branch
git merge origin/main

# 4. Resolve any conflicts (if necessary)
# Edit conflicted files, then:
git add <resolved-file>
git commit -m "Merge main into testing_branch_v1.0.0"

# 5. Push the updated testing branch to the remote repository
git push origin testing_branch_v1.0.0
```

## Checking Branch Status

```bash
# Check which branch you're currently on (current branch has an asterisk)
git branch

# View detailed status of your working directory
git status

# See the commit history of your current branch
git log --oneline --graph --decorate
```

## Managing Local Changes

```bash
# Save changes to tracked files
git add <file>       # Add specific file
git add .            # Add all files

# Commit changes
git commit -m "Your descriptive commit message"

# Temporarily store changes without committing
git stash save "Work in progress on feature X"

# Retrieve stashed changes later
git stash list       # List all stashes
git stash apply      # Apply most recent stash
git stash apply stash@{n}  # Apply specific stash
git stash pop        # Apply and remove most recent stash
```

## Handling Merge Conflicts

```bash
# View files with conflicts
git status

# Abort a merge with conflicts
git merge --abort

# After manually resolving conflicts
git add <resolved-file>
git commit -m "Resolve merge conflicts"

# Use a visual merge tool
git mergetool
```

## Alternative Approach: Rebase

```bash
# Rebase your testing branch on top of main
git checkout testing_branch_v1.0.0
git fetch origin
git rebase origin/main

# If conflicts occur during rebase
git rebase --continue  # After resolving conflicts
git rebase --abort     # To cancel the rebase operation
```

## Recovery Commands

```bash
# Discard all local changes in your working directory
git reset --hard

# Undo the last commit but keep the changes
git reset --soft HEAD~1

# Undo the last commit and discard the changes
git reset --hard HEAD~1

# Abort an in-progress merge
git merge --abort

# Return to state before merge started
git reset --hard ORIG_HEAD
```

## Remote Repository Operations

```bash
# Update your local repository with remote changes
git fetch origin

# Update specific branch
git fetch origin main

# View all remote branches
git branch -r

# View all local and remote branches
git branch -a
```

## Branch Creation and Deletion

```bash
# Create a new branch from current position
git branch new_branch_name

# Create and switch to a new branch
git checkout -b new_branch_name

# Delete a local branch (after merging)
git branch -d branch_name

# Force delete a local branch (even if not merged)
git branch -D branch_name

# Delete a remote branch
git push origin --delete branch_name
```

---

For more detailed instructions and explanations, refer to the specific wiki pages in this series.
