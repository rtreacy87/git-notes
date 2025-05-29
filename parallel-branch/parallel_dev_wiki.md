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
   
   If you see conflicts (Git will tell you), see the "Handling Conflicts" section below.

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

## Azure DevOps Pipeline Configuration

Your build pipeline should be configured to:
1. **Trigger on changes** to both `main` and `testing` branches
2. **Pull code** from the `main` branch  
3. **Pull tests** from the `testing` branch
4. **Combine them** for building and testing
5. **Run automatically** when either branch is updated

### Sample Azure Pipeline YAML
```yaml
trigger:
  branches:
    include:
    - main
    - testing

resources:
  repositories:
  - repository: self
    trigger:
      branches:
        include:
        - main
        - testing

stages:
- stage: BuildAndTest
  jobs:
  - job: BuildAndTest
    pool:
      vmImage: 'ubuntu-latest'  # or windows-latest
    
    steps:
    - checkout: self
      persistCredentials: true
    
    # Fetch both branches
    - script: |
        git fetch origin main:main
        git fetch origin testing:testing
      displayName: 'Fetch all branches'
    
    # Build from main branch code
    - script: |
        git checkout main
        # Add your build commands here
        # Example: dotnet build, npm install, etc.
      displayName: 'Build application from main'
    
    # Run tests from testing branch
    - script: |
        git checkout testing
        # Add your test execution commands here
        # Example: dotnet test, npm test, etc.
      displayName: 'Run tests from testing branch'
```

*Note: Your DevOps admin should configure this pipeline based on your specific technology stack.*

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
- **Team contact**: [Add your team's contact information here]

## FAQ

**Q: How often should I sync the testing branch with main?**
A: Daily, preferably first thing in the morning before you start working.

**Q: Should I test against the code developer's feature branch or wait for main?**
A: Generally wait for features to be merged to main, but you can test feature branches early if coordinating directly with the code developer.

**Q: What if I find bugs in a feature that's not yet merged to main?**
A: Comment on the Pull Request in Azure DevOps or contact the code developer directly to discuss the issues before the feature is merged.

**Q: What if I accidentally delete something important?**
A: Don't panic! Git keeps history. Contact your team lead or use `git log` to find previous versions.

**Q: Can I work on multiple features at once?**  
A: Code developers can work on multiple feature branches, but it's better to complete one before starting another to avoid complications.

**Q: What if the pipeline fails?**
A: Check the pipeline logs in Azure DevOps. Usually it's either a merge conflict or a failing test that needs to be fixed.