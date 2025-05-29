# Parallel Development Guide: Code and Tests in Separate Branches

## Overview

This guide explains how to work on code and tests in parallel using separate Git branches when you have:
- **Code Developer**: Working on the main application code
- **Test Developer**: Writing tests for the application
- **Shared Goal**: Both need to work simultaneously without interfering with each other

## Branch Strategy

- **`main` branch**: Contains the stable, reviewed application code
- **`feature/*` branches**: Where code developers work on new features before merging to main
- **`testing` branch**: Contains all test files and test-related code
- **Azure Pipeline**: Combines main and testing branches to build and test the application

## Initial Setup

### For the Code Developer

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://dev.azure.com/YourOrg/YourProject/_git/YourRepo
   cd YourRepo
   ```

2. **Make sure you're on the main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Your workflow**: Create feature branches for each new feature, then merge to main through Pull Requests.

### For the Test Developer

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://dev.azure.com/YourOrg/YourProject/_git/YourRepo
   cd YourRepo
   ```

2. **Create or switch to the testing branch**:
   ```bash
   git checkout -b testing
   git push -u origin testing
   ```
   
   *Note: If the testing branch already exists, use:*
   ```bash
   git checkout testing
   git pull origin testing
   ```

## Daily Workflow

### For the Code Developer

#### Starting a New Feature
1. **Get the latest main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   *Example: `git checkout -b feature/user-authentication`*

3. **Make your code changes** using your preferred editor

4. **Save and commit your changes regularly**:
   ```bash
   git add .
   git commit -m "Add user login functionality"
   git push origin feature/your-feature-name
   ```

#### Completing a Feature
1. **Make sure your feature branch is up to date**:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature-name
   git merge main
   ```
   
   If there are conflicts, resolve them (see "Handling Conflicts" section).

2. **Push your updated feature branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request in Azure DevOps**:
   - Go to your Azure DevOps project
   - Navigate to Repos > Pull Requests
   - Click "New Pull Request"
   - Select your feature branch as source and `main` as target
   - Add a description of your changes
   - Click "Create"

4. **After Pull Request is approved and merged**:
   ```bash
   git checkout main
   git pull origin main
   git branch -d feature/your-feature-name
   ```

5. **Notify the test developer** about the new feature that was merged to main

### For the Test Developer

#### Daily Sync (Do this every morning)
1. **Switch to your testing branch**:
   ```bash
   git checkout testing
   ```

2. **Get the latest code changes**:
   ```bash
   git pull origin main
   git merge main
   ```
   
   This process ensures your testing branch stays up-to-date with the main codebase:
   - `git pull origin main` fetches the latest commits from the remote main branch
   - `git merge main` integrates those changes into your current testing branch
   
   By doing this daily, you can write tests against the most current application code.

   If you see conflicts (Git will tell you), see the "Handling Conflicts" section below.

   Step 1: Initial state
   
   ![Git Workflow Step 1](https://raw.githubusercontent.com/rtreacy87/git-notes/main/figures/git_workflow_step1.png)

  In the initial state:

   1. `origin/main` (the remote repository) has commits A, B, and C
   2. `local/main` (your local copy of main) only has commit A (it's outdated)
   3. `testing` branch has commit A plus your test-specific commit D

  
   Step 2: After git pull origin main
   
   
  ![Git Workflow Step 2](https://github.com/rtreacy87/git-notes/figures/git_workflow_step2.png)  

   After running `git pull origin main`, only your local main branch is updated with commits B and C from the remote main branch. 

   At this point:
   1. Your local main branch now has commits A, B, and C
   2. Your testing branch still only has commits A and D
   3. No changes have been made to your testing branch yet

   The `git merge main` command that follows is what actually brings those changes (B and C) from your local main branch into your testing branch.

   Step 3: After git merge main
   
  ![Git Workflow Step 3](https://github.com/rtreacy87/git-note/sfigures/git_workflow_step3.png)  

    After `git merge main` is called:

   1. Git takes the changes from your local main branch (commits B and C)
   2. It combines those changes with your existing work in the testing branch (commit D)
   3. It creates a new merge commit (M) that includes all changes from both branches

   This merge commit (M) is special because it has two parent commits:
   - One parent is your latest testing branch commit (D)
   - The other parent is the latest main branch commit (C)

   The result is that your testing branch now contains all your test-specific changes (D) plus all the latest application code changes from main (B and C), allowing you to write tests against the most current code.

    Legend: 
   - A,B,C,D = commits
   - M = merge commit
   - Vertical lines = branch timeline (each column represents a separate branch)
   - Horizontal lines = commits being merged from one branch to another

   The process then updates your local main with the latest changes from remote (B and C), and then merges those changes into your testing branch, creating a merge commit M that combines everything.

   This workflow ensures you're always testing against the latest code while keeping your test-specific changes intact.

3. **Push the updated testing branch**:
   ```bash
   git push origin testing
   ```

#### Adding New Tests
1. **Make sure you're on the testing branch**:
   ```bash
   git checkout testing
   ```

2. **Make your test changes** using your preferred editor

3. **Save and commit your changes**:
   ```bash
   git add .
   git commit -m "Describe what tests you added"
   git push origin testing
   ```

## Handling Conflicts

Sometimes when you merge `main` into `testing`, Git will find conflicts. Here's how to handle them:

1. **Git will tell you there are conflicts** and list the files
2. **Open each conflicted file** in your editor
3. **Look for conflict markers** that look like this:
   ```
   <<<<<<< HEAD
   Your test code
   =======
   Code from main branch
   >>>>>>> main
   ```
4. **Decide what to keep**:
   - Keep your test code
   - Keep the main branch code
   - Keep both (if they don't conflict)
   - Modify to make both work together

5. **Remove the conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)
6. **Save the file**
7. **Mark the conflict as resolved**:
   ```bash
   git add filename.ext
   ```
8. **Complete the merge**:
   ```bash
   git commit -m "Resolved merge conflicts"
   git push origin testing
   ```


### Conflict Resolution Options

| Option                          | Command                                    | Description                                               | When to Use                                                            |
|---------------------------------|--------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------------------|
| **Abort the merge**             | `git merge --abort`                        | Cancels the merge and returns to the state before merging | When you want to start over or need more time to prepare               |
| **Keep your code** (HEAD)       | `git checkout --ours tests/test_user.py`   | Uses only your version (testing branch)                   | When your changes are correct and main branch changes can be discarded |
| **Accept incoming code** (main) | `git checkout --theirs tests/test_user.py` | Uses only the main branch version                         | When main branch changes are correct and your changes can be discarded |
| **Manual resolution**           | Edit file directly                         | Manually edit the file to combine changes                 | When both versions contain important changes that need to be preserved |
| **Use merge tool**              | `git mergetool`                            | Opens a visual tool to help resolve conflicts             | For complex conflicts where visual comparison helps                    |

## Using an External Merge Tool

 ### Azure DevOps Conflicts Tab Extension

For team members working with Azure DevOps, the [Conflicts Tab extension](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.conflicts-tab) provides a convenient way to resolve merge conflicts directly in the web interface:

1. **Install the extension**:
   - Go to the [Conflicts Tab extension page](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.conflicts-tab)
   - Click "Get it free"
   - Select your organization and install

2. **Using the extension during Pull Requests**:
   - When a PR has conflicts, a new "Conflicts" tab will appear
   - Click on the tab to see all conflicted files
   - For each file, you'll see:
     - Your changes (testing branch)
     - The target branch changes (main)
     - A merged result editor

3. **Resolving conflicts**:
   - Select which changes to keep using the checkboxes
   - Or manually edit the merged result
   - Click "Accept Merge" for each file
   - Once all conflicts are resolved, complete the PR

4. **Benefits of using the extension**:
   - No need to switch context to your local environment
   - Visual comparison makes conflicts easier to understand
   - Teammates can collaborate on conflict resolution
   - History of conflict resolutions is preserved in the PR

This tool is especially useful for remote teams or when you want to resolve simple conflicts quickly without having to pull changes locally.


## Communication Guidelines

### When to Communicate
- **Code Developer**: Notify test developer when you:
  - Create a Pull Request for a new feature
  - Merge a feature to main (new functionality available for testing)
  - Change existing functionality in main
  - Remove or rename functions/classes
  - Change file structure

- **Test Developer**: Notify code developer when you:
  - Need new functions or test hooks in the code
  - Find bugs through testing
  - Need specific test data or configurations
  - Tests are failing due to recent main branch changes

### Recommended Communication Frequency
- **Daily standup**: Quick sync on what each person is working on
- **Weekly integration meeting**: Review how well the branches are staying in sync

## Troubleshooting

### "I can't switch branches"
**Problem**: Git says "Please commit your changes or stash them before you switch branches"

**Solution**:
```bash
# Save your work temporarily
git stash

# Switch branches
git checkout [branch-name]

# Get your work back (only if you want to apply it to this branch)
git stash pop
```

### "My changes disappeared"
**Problem**: Your recent changes aren't showing up

**Possible causes**:
1. **You're on the wrong branch**: Check with `git branch` (current branch has a `*`)
2. **Changes weren't committed**: Check with `git status`
3. **Changes weren't pushed**: Use `git push origin [branch-name]`

### "I made changes to the wrong branch"
**Problem**: You accidentally made code changes to the testing branch or test changes to main

**Solution**:
```bash
# Save your changes
git stash

# Switch to the correct branch
git checkout [correct-branch]

# Apply your changes to the correct branch
git stash pop

# Commit to the correct branch
git add .
git commit -m "Your message"
git push origin [correct-branch]
```

## Quick Reference Commands

### Essential Commands
```bash
# See which branch you're on
git branch

# Switch to a branch
git checkout [branch-name]

# Get latest changes from server
git pull origin [branch-name]

# Save your changes
git add .
git commit -m "Your message"
git push origin [branch-name]

# See what changes you have
git status
```

### Branch-Specific Workflows

**Code Developer** (feature branch workflow):
```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/feature-name

# Work on feature
git add .
git commit -m "Description"
git push origin feature/feature-name

# When ready, create Pull Request in Azure DevOps
# After merge, clean up
git checkout main
git pull origin main
git branch -d feature/feature-name
```

**Test Developer** (testing branch):
```bash
git checkout testing
git pull origin main
git merge main
# Handle any conflicts
git push origin testing
# Make test changes
git add .
git commit -m "Description"  
git push origin testing
```

## Getting Help

- **Git documentation**: [https://git-scm.com/docs](https://git-scm.com/docs)
- **Azure DevOps help**: [https://docs.microsoft.com/en-us/azure/devops/](https://docs.microsoft.com/en-us/azure/devops/)


