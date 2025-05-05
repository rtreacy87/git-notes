# Advanced Scenarios and Troubleshooting

## Overview

This wiki covers advanced branch management scenarios and troubleshooting techniques for complex situations that may arise when merging branches. These approaches are designed for developers who need to handle challenging merge scenarios or recover from problematic merges.

## Prerequisites

Before proceeding, ensure you have:

1. Git installed on your local machine
2. Access to the repository containing your branches
3. Basic understanding of Git branching and merging concepts
4. Familiarity with the standard merge process (see [Merging Main into Testing Branch](./03-merging-main-into-testing-branch.md))

## Handling Complex Merge Conflicts

Standard merge conflicts can usually be resolved by editing the conflicted files directly. However, complex conflicts may require more sophisticated tools and approaches.

### Using Visual Merge Tools

Visual merge tools provide a graphical interface for resolving conflicts, making it easier to understand and combine changes from different branches.

#### 1. Configuring a Merge Tool

First, configure Git to use your preferred merge tool:

```bash
# For meld (Linux/macOS)
git config --global merge.tool meld

# For kdiff3 (cross-platform)
git config --global merge.tool kdiff3

# For p4merge (cross-platform)
git config --global merge.tool p4merge

# For Visual Studio Code
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd "code --wait $MERGED"
```

#### 2. Installing Merge Tools

**Meld**:
- Linux: `sudo apt-get install meld` (Ubuntu/Debian) or `sudo dnf install meld` (Fedora)
- macOS: `brew install meld`
- Windows: Download from [Meld's website](https://meldmerge.org/)

**KDiff3**:
- Linux: `sudo apt-get install kdiff3` (Ubuntu/Debian) or `sudo dnf install kdiff3` (Fedora)
- macOS: `brew install kdiff3`
- Windows: Download from [KDiff3's website](https://kdiff3.sourceforge.net/)

**P4Merge**:
- All platforms: Download from [Perforce's website](https://www.perforce.com/products/helix-core-apps/merge-diff-tool-p4merge)

#### 3. Launching the Merge Tool

When you encounter conflicts during a merge, launch the merge tool:

```bash
git mergetool
```

This command will open your configured merge tool for each conflicted file, one at a time.

#### 4. Using the Merge Tool Interface

Most merge tools display:
- The base version (common ancestor)
- Your version (current branch)
- Their version (branch being merged)
- The output/result version

Navigate the interface to:
1. Review the differences between versions
2. Select which changes to keep
3. Manually edit the result if needed
4. Save the resolved file and move to the next conflict

#### 5. Completing the Merge

After resolving all conflicts with the merge tool:

```bash
# Check if all conflicts are resolved
git status

# Complete the merge
git commit -m "Merge main into testing_branch_v1.0.0 with complex conflict resolution"
```

### Handling Binary File Conflicts

Binary files (images, PDFs, etc.) cannot be merged like text files. When binary files conflict:

```bash
# Choose your version
git checkout --ours path/to/binary/file.pdf

# Or choose the main branch version
git checkout --theirs path/to/binary/file.pdf

# Mark the conflict as resolved
git add path/to/binary/file.pdf
```

### Handling Multiple Conflicts in Related Files

When multiple related files have conflicts, consider:

1. **Resolving them together**: Understand how the changes are related before resolving each conflict.

2. **Using a consistent approach**: Apply the same resolution strategy to similar conflicts.

3. **Testing incrementally**: After resolving a group of related conflicts, build and test to ensure functionality.

## Using Alternative Approaches: Rebase vs. Merge

While merging is the standard approach for integrating changes, rebasing offers an alternative with different trade-offs.

### Understanding Rebase

Rebasing rewrites the commit history by moving your branch's commits to start from a different point:

```
Before rebase:
      A---B---C testing_branch_v1.0.0
     /
D---E---F---G main

After rebase:
              A'--B'--C' testing_branch_v1.0.0
             /
D---E---F---G main
```

The original commits (A, B, C) are replaced with new commits (A', B', C') that have the same changes but different parent commits.

### When to Use Rebase Instead of Merge

Consider rebasing when:
- You want a cleaner, linear history without merge commits
- Your testing branch hasn't been shared with others yet
- You want to integrate the latest changes from main before submitting a pull request

Avoid rebasing when:
- Your branch is shared with others (it rewrites history)
- You want to preserve the exact history of when changes were integrated
- You're not comfortable resolving potentially complex conflicts

### Performing a Rebase

```bash
# Switch to your testing branch
git checkout testing_branch_v1.0.0

# Fetch the latest changes
git fetch origin

# Rebase onto the main branch
git rebase origin/main
```

### Handling Conflicts During Rebase

Rebasing applies your commits one by one on top of the target branch, potentially causing multiple rounds of conflicts:

1. When a conflict occurs, Git pauses the rebase:
   ```
   CONFLICT (content): Merge conflict in src/components/UserProfile.js
   error: could not apply a2b3c4d... Add validation to user profile
   hint: Resolve all conflicts manually, mark them as resolved with
   hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
   hint: You can instead skip this commit: run "git rebase --skip".
   hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
   ```

2. Resolve the conflict as you would during a merge:
   ```bash
   # Edit the file to resolve the conflict
   # Then mark it as resolved
   git add src/components/UserProfile.js
   ```

3. Continue the rebase:
   ```bash
   git rebase --continue
   ```

4. Repeat for each conflict until the rebase is complete.

### Pushing After a Rebase

Since rebasing rewrites history, you'll need to force push:

```bash
git push --force-with-lease origin testing_branch_v1.0.0
```

⚠️ **Warning**: `--force-with-lease` is safer than `--force` as it prevents overwriting others' changes, but still use with caution on shared branches.

## Recovering from Failed Merges

Sometimes merges go wrong, and you need to recover to a clean state.

### Aborting an In-Progress Merge

If you haven't committed the merge yet:

```bash
git merge --abort
```

This command restores your working directory to the state before the merge started.

### Reverting a Completed Merge

If you've already committed the merge and pushed it:

```bash
# Find the merge commit
git log --merges -n 1

# Revert the merge commit
git revert -m 1 <merge-commit-hash>

# Push the revert
git push origin testing_branch_v1.0.0
```

The `-m 1` option specifies that you want to revert to the first parent (your branch before the merge).

### Resetting to Before the Merge

If you've committed the merge but haven't pushed it:

```bash
# Find the commit before the merge
git reflog

# Reset to that commit
git reset --hard HEAD@{1}  # Adjust the number as needed
```

⚠️ **Warning**: `git reset --hard` discards all changes since the specified commit. Make sure you have a backup or are certain you want to discard these changes.

### Recovering Lost Work

If you accidentally lost work during a merge or rebase:

```bash
# View the reflog to find lost commits
git reflog

# Create a new branch at the lost commit
git branch recovered-work <commit-hash>

# Or cherry-pick the lost commit
git cherry-pick <commit-hash>
```

## Advanced Merge Strategies

Git offers several merge strategies for different scenarios:

### Octopus Merge (Multiple Branches)

To merge multiple branches at once:

```bash
git merge branch1 branch2 branch3
```

This creates a single merge commit with multiple parents. Use this for integrating several feature branches that don't conflict.

### Ours Strategy (Discard Their Changes)

To keep your version in all conflicts:

```bash
git merge -s ours origin/main
```

This creates a merge commit but discards all changes from the main branch. Use with extreme caution, as it effectively ignores the main branch changes.

### Theirs Strategy (Take Their Changes)

While there's no built-in "theirs" strategy, you can achieve it with:

```bash
git merge origin/main
git checkout --theirs .
git add .
git commit
```

This takes all changes from the main branch in conflicts.

### Patience Strategy (Better Conflict Resolution)

For complex merges with many changes:

```bash
git merge --strategy-option=patience origin/main
```

This uses a more careful algorithm that often produces better results for complex changes.

## Troubleshooting Common Advanced Issues

### Issue: "fatal: refusing to merge unrelated histories"

**Symptom**: Git refuses to merge branches that don't share a common history.

**Solution**: If you're certain you want to merge unrelated branches:

```bash
git merge --allow-unrelated-histories origin/main
```

### Issue: Merge Conflicts in Every File

**Symptom**: Almost every file has conflicts, making resolution impractical.

**Solution**: Consider alternative approaches:

```bash
# Abort the current merge
git merge --abort

# Option 1: Take all your changes for specific files
git merge origin/main
git checkout --ours -- src/specific-folder/
git add src/specific-folder/
git commit

# Option 2: Start fresh with main and apply your changes as a patch
git checkout main
git checkout -b new_testing_branch
git diff testing_branch_v1.0.0..main > changes.patch
git apply changes.patch
```

### Issue: Merge Introduces Bugs

**Symptom**: After merging, the application has new bugs or fails tests.

**Solution**: Use `git bisect` to find the problematic commit:

```bash
# Start the bisect process
git bisect start

# Mark the current state as bad
git bisect bad

# Mark a known good state (before the merge)
git bisect good <commit-before-merge>

# Git will checkout commits for you to test
# For each commit, test and mark as good or bad
git bisect good  # or git bisect bad

# When the problematic commit is found, end the bisect
git bisect reset
```

Once you identify the problematic commit, you can fix it specifically or revert it.

## Next Steps

After mastering these advanced techniques, consider:

1. Establishing branch management best practices for your team
2. Setting up automated testing for merged branches
3. Documenting your team's preferred approaches for handling complex merges

Continue to [Best Practices for Branch Management](./05-best-practices-for-branch-management.md) for guidance on establishing effective branch management protocols.

## See Also

- [Merging Main into Testing Branch](./03-merging-main-into-testing-branch.md)
- [Best Practices for Branch Management](./05-best-practices-for-branch-management.md)
- [Git Documentation on Advanced Merging](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging)

## Glossary

- **Rebase**: A Git operation that moves or combines a sequence of commits to a new base commit.
- **Force Push**: Overwrites the remote branch with your local branch, potentially discarding commits.
- **Merge Strategy**: An algorithm Git uses to perform a merge.
- **Octopus Merge**: A merge involving more than two branches.
- **Cherry-pick**: Applying a specific commit from one branch to another.
- **Bisect**: A binary search process to find which commit introduced a bug.
- **Reflog**: A log of all references (branches, tags) and how they've changed over time.
