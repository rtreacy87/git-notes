# Preparing for Branch Updates

## Overview

Before merging changes from the main branch into your testing branch, it's important to prepare your working environment. This wiki covers the essential steps to check your current branch status, save any local changes, and ensure a clean working directory for the merge process.

## Prerequisites

Before proceeding, ensure you have:

1. Git installed on your local machine
2. Access to the repository containing your main and testing branches
3. Basic understanding of Git branching concepts (see [Understanding Branch Management Basics](./01-understanding-branch-management-basics.md))

## Checking Your Current Branch Status

Before making any changes, it's important to understand the current state of your local repository. This helps prevent unexpected issues during the merge process.

### 1. Identifying Your Current Branch

First, check which branch you're currently on:

```bash
git branch
```

This command lists all local branches, with an asterisk (*) next to your current branch:

```
  main
* testing_branch_v1.0.0
  feature/login-page
```

In this example, you're currently on `testing_branch_v1.0.0`.

### 2. Viewing the Status of Your Working Directory

Next, check if you have any uncommitted changes:

```bash
git status
```

This command shows:
- Which branch you're on
- Whether your branch is up to date with the remote
- Which files have been modified, added, or deleted
- Which changes are staged for commit

Example output:

```
On branch testing_branch_v1.0.0
Your branch is up to date with 'origin/testing_branch_v1.0.0'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/components/UserProfile.js

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/utils/validation.js

no changes added to commit (use "git add" and/or "git commit -a")
```

### 3. Reviewing Recent Commits

To understand the recent history of your branch:

```bash
git log --oneline --graph --decorate -n 5
```

This shows the last 5 commits with a visual representation of the branch structure:

```
* a7d3f1c (HEAD -> testing_branch_v1.0.0, origin/testing_branch_v1.0.0) Add user profile validation
* 3e5f2d8 Implement user profile page
* 9c4d2b7 Fix navigation bug
* 2b1e8f6 (origin/main, main) Update dependencies
* 5a7d9c3 Implement authentication system
```

In this example, you can see that your testing branch has three commits that aren't in the main branch.

## Saving Local Changes

If you have uncommitted changes that you want to keep, you need to handle them before updating your branch. There are two main approaches:

### 1. Committing Your Changes

If your changes are complete and ready to be part of your branch's history:

```bash
# Stage all modified files
git add .

# Or stage specific files
git add src/components/UserProfile.js src/utils/validation.js

# Commit the changes with a descriptive message
git commit -m "Add user input validation to profile page"
```

#### When to Use This Approach

- When your changes are complete and logically cohesive
- When you want the changes to be part of your branch's permanent history
- When you want to preserve the exact state of your work

### 2. Stashing Your Changes

If your changes are incomplete or you're not ready to commit them:

```bash
# Stash all changes with a descriptive message
git stash save "Work in progress on user profile validation"
```

This command saves your changes in a "stash" - a temporary storage area - and reverts your working directory to the last commit.

To view your stashed changes later:

```bash
git stash list
```

To apply your stashed changes after the merge:

```bash
# Apply the most recent stash without removing it from the stash list
git stash apply

# Or apply a specific stash
git stash apply stash@{0}

# Apply and remove the most recent stash from the stash list
git stash pop
```

#### When to Use This Approach

- When your changes are incomplete or not ready to commit
- When you want to temporarily set aside your work
- When you're experimenting with changes you might want to discard

## Ensuring Clean Working Directory

A clean working directory helps prevent conflicts during the merge process. After committing or stashing your changes, verify that your working directory is clean:

```bash
git status
```

You should see:

```
On branch testing_branch_v1.0.0
Your branch is up to date with 'origin/testing_branch_v1.0.0'.

nothing to commit, working tree clean
```

### Handling Unwanted Changes

If you have changes that you don't want to keep:

```bash
# Discard changes to all files
git reset --hard

# Discard changes to specific files
git checkout -- src/components/UserProfile.js
```

⚠️ **Warning**: These commands permanently discard your changes. Use them with caution, especially `git reset --hard`, which discards all uncommitted changes.

### Cleaning Untracked Files

If you have untracked files that you don't want to keep:

```bash
# Show what would be deleted (dry run)
git clean -n

# Delete untracked files
git clean -f

# Delete untracked files and directories
git clean -fd
```

⚠️ **Warning**: `git clean` permanently deletes files that aren't tracked by Git. Use the `-n` flag first to see what would be deleted.

## Updating Your Local Repository

Before merging, ensure your local repository is up to date with the remote:

```bash
# Fetch the latest changes from all remote branches
git fetch origin

# Check if there are any new changes to your testing branch
git log HEAD..origin/testing_branch_v1.0.0 --oneline
```

If there are new changes on the remote testing branch, you should pull them before merging from main:

```bash
git pull origin testing_branch_v1.0.0
```

## Verification Steps

Before proceeding to merge the main branch, verify that:

1. You're on the correct testing branch
   ```bash
   git branch
   ```

2. Your working directory is clean
   ```bash
   git status
   ```

3. Your local branch is up to date with the remote
   ```bash
   git pull origin testing_branch_v1.0.0
   ```

4. You've saved any local changes (committed or stashed)

## Troubleshooting Common Issues

### Issue: Unable to Switch Branches Due to Conflicts

**Symptom**: Git prevents you from switching branches because of uncommitted changes that would be overwritten.

**Solution**: Commit or stash your changes before switching branches.

```bash
git stash save "Work in progress"
git checkout testing_branch_v1.0.0
```

### Issue: Accidentally Committed to the Wrong Branch

**Symptom**: You realize you've made commits on the main branch instead of your testing branch.

**Solution**: Use cherry-pick to apply those commits to your testing branch.

```bash
# Note the commit hashes you want to move
git log --oneline -n 5

# Switch to your testing branch
git checkout testing_branch_v1.0.0

# Cherry-pick the commits
git cherry-pick <commit-hash>

# Switch back to main and reset it (if you have permission)
git checkout main
git reset --hard origin/main
```

### Issue: Stashed Changes Are Lost

**Symptom**: You can't find your stashed changes.

**Solution**: Check the stash reflog to see if they're still available.

```bash
git fsck --no-reflog | grep dangling | grep commit
```

## Next Steps

Now that your working environment is prepared, you're ready to merge changes from the main branch into your testing branch. Continue to [Step-by-Step Guide: Merging Main into Testing Branch](./03-merging-main-into-testing-branch.md) for detailed instructions on the merge process.

## See Also

- [Understanding Branch Management Basics](./01-understanding-branch-management-basics.md)
- [Step-by-Step Guide: Merging Main into Testing Branch](./03-merging-main-into-testing-branch.md)
- [Git Documentation on git-stash](https://git-scm.com/docs/git-stash)

## Glossary

- **Working Directory**: The files that you're currently working on.
- **Staging Area**: A file maintained by Git that contains information about what will go into your next commit.
- **Commit**: A snapshot of your repository at a specific point in time.
- **Stash**: A temporary storage area for changes that you're not ready to commit.
- **Clean Working Directory**: A working directory with no uncommitted changes.
- **Cherry-pick**: The act of applying a specific commit from one branch to another.
