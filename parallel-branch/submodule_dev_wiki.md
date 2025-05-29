# Parallel Development Guide: Code and Tests Using Git Submodules

## Overview

This guide explains how to work on code and tests in parallel using Git submodules when you have:
- **Code Developer**: Working on the main application code
- **Test Developer**: Writing tests for the application  
- **Shared Goal**: Both need to work simultaneously with complete independence

## Repository Strategy

This approach uses **two separate repositories**:
- **Main Repository** (`YourApp`): Contains the application code + references the test repository
- **Test Repository** (`YourApp-Tests`): Contains all test files (added as a submodule to main repo)
- **Azure Pipeline**: Uses the main repository, which automatically includes the test submodule

### Benefits of Submodules
- **Complete separation**: Tests and code are in different repositories
- **Independent development**: No merge conflicts between code and test work
- **Version control**: You can pin tests to specific versions of the code
- **Clean history**: Each repository has its own commit history
- **Easy collaboration**: Each developer owns their repository completely

## Initial Setup

### Step 1: Repository Creation (DevOps Admin)

**Create two repositories in Azure DevOps:**
1. `YourApp` (main application repository)
2. `YourApp-Tests` (test repository)

### Step 2: Setup for Code Developer

1. **Clone the main repository**:
   ```bash
   git clone https://dev.azure.com/YourOrg/YourProject/_git/YourApp
   cd YourApp
   ```

2. **Add the test repository as a submodule**:
   ```bash
   git submodule add https://dev.azure.com/YourOrg/YourProject/_git/YourApp-Tests tests
   git commit -m "Add tests submodule"
   git push origin main
   ```

3. **Your repository structure will look like**:
   ```
   YourApp/
   ├── src/              # Your application code
   ├── docs/             # Documentation
   ├── tests/            # Submodule pointing to YourApp-Tests repo
   ├── .gitmodules       # Submodule configuration (auto-created)
   └── README.md
   ```

### Step 3: Setup for Test Developer

**Option A: Work directly in the test repository**
```bash
git clone https://dev.azure.com/YourOrg/YourProject/_git/YourApp-Tests
cd YourApp-Tests
```

**Option B: Work through the main repository (recommended)**
```bash
git clone --recurse-submodules https://dev.azure.com/YourOrg/YourProject/_git/YourApp
cd YourApp/tests
```

## Daily Workflow

### For the Code Developer

#### Working on Features
1. **Get the latest changes**:
   ```bash
   git pull origin main
   git submodule update --remote
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your code changes** in the `src/` directory

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add new feature functionality"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request** in Azure DevOps for the main repository

6. **After PR is merged, update submodule reference**:
   ```bash
   git checkout main
   git pull origin main
   # If test developer has new tests, update the submodule pointer
   git submodule update --remote
   git add tests
   git commit -m "Update tests submodule reference"
   git push origin main
   ```

#### When Test Developer Updates Tests
1. **Pull the latest submodule changes**:
   ```bash
   git submodule update --remote
   git add tests
   git commit -m "Update tests to latest version"
   git push origin main
   ```

### For the Test Developer

#### Daily Work (Option A: Direct repository access)
1. **Get latest changes**:
   ```bash
   git pull origin main
   ```

2. **Make your test changes**

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add tests for user authentication"
   git push origin main
   ```

#### Daily Work (Option B: Through main repository)
1. **Navigate to the tests directory**:
   ```bash
   cd YourApp/tests
   ```

2. **Get latest changes**:
   ```bash
   git pull origin main
   ```

3. **Make your test changes**

4. **Commit and push to the test repository**:
   ```bash
   git add .
   git commit -m "Add tests for user authentication"
   git push origin main
   ```

5. **Update the main repository to reference your new tests**:
   ```bash
   cd ..  # Back to main repository root
   git add tests
   git commit -m "Update tests submodule to include new authentication tests"
   git push origin main
   ```

#### Staying in Sync with Code Changes
1. **Regularly check what's new in the main application**:
   ```bash
   # If working from Option A
   git clone --recurse-submodules https://dev.azure.com/YourOrg/YourProject/_git/YourApp temp-checkout
   cd temp-checkout
   # Review recent changes
   git log --oneline -10
   cd ../YourApp-Tests  # Back to your test repo
   ```

   ```bash
   # If working from Option B
   cd YourApp  # Main repository
   git pull origin main
   git log --oneline -10  # See recent changes
   cd tests  # Back to test work
   ```

## Advanced Submodule Operations

### Cloning a Repository with Submodules
**New team members should use**:
```bash
git clone --recurse-submodules https://dev.azure.com/YourOrg/YourProject/_git/YourApp
```

**If you already cloned without submodules**:
```bash
git submodule init
git submodule update
```

### Updating Submodules
```bash
# Update to latest commit in test repository
git submodule update --remote

# Update and merge any local changes
git submodule update --remote --merge

# Update all submodules recursively
git submodule update --recursive --remote
```

### Working on Specific Test Versions
```bash
# Pin tests to a specific commit (useful for releases)
cd tests
git checkout [specific-commit-hash]
cd ..
git add tests
git commit -m "Pin tests to version X.Y.Z"
```

## Communication Guidelines

### When to Communicate
- **Code Developer**: Notify test developer when you:
  - Merge a new feature to main (new functionality available)
  - Change existing APIs or interfaces
  - Remove or rename functions/classes
  - Plan to create a release tag

- **Test Developer**: Notify code developer when you:
  - Push major test updates that should be referenced in main
  - Find bugs through testing
  - Need new test hooks or configurations in the code
  - Complete test coverage for a feature

### Recommended Communication Frequency
- **Daily standup**: Quick sync on progress
- **Feature completion**: When code developer merges features
- **Test completion**: When test developer finishes testing a feature
- **Weekly sync**: Review submodule update frequency

## Azure DevOps Pipeline Configuration

### Pipeline Strategy
Your build pipeline should operate on the **main repository** and will automatically include the test submodule.

### Sample Azure Pipeline YAML
```yaml
trigger:
  branches:
    include:
    - main
    - feature/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

stages:
- stage: BuildAndTest
  jobs:
  - job: BuildAndTest
    steps:
    # Checkout with submodules
    - checkout: self
      submodules: true
      persistCredentials: true
    
    # Alternative: Manual submodule update
    - script: |
        git submodule update --init --recursive
        git submodule update --remote
      displayName: 'Update submodules to latest'
    
    # Build the main application
    - script: |
        cd src
        # Add your build commands here
        # Example: dotnet build, npm install && npm run build, etc.
      displayName: 'Build application'
    
    # Run tests from submodule
    - script: |
        cd tests
        # Add your test execution commands here
        # Example: dotnet test, npm test, pytest, etc.
      displayName: 'Run tests'
    
    # Optional: Generate test reports
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'  # or VSTest, NUnit, etc.
        testResultsFiles: '**/test-results.xml'
        searchFolder: 'tests'
      displayName: 'Publish test results'
```

### Pipeline Triggers
You can also set up the pipeline to trigger when the **test repository** changes:

```yaml
resources:
  repositories:
  - repository: tests
    type: git
    name: YourProject/YourApp-Tests
    trigger:
      branches:
        include:
        - main

trigger:
  branches:
    include:
    - main
    - feature/*
  paths:
    include:
    - src/*
    - tests/*
```

## Troubleshooting

### "Submodule folder is empty"
**Problem**: After cloning, the tests folder exists but is empty

**Solution**:
```bash
git submodule init
git submodule update
```

### "I can't push my test changes"
**Problem**: When working in the submodule, pushes fail

**Solution**: Make sure you're pushing to the correct repository
```bash
cd tests
git remote -v  # Should show YourApp-Tests repository
git push origin main
```

### "My submodule is in detached HEAD state"
**Problem**: The submodule is not on a branch

**Solution**:
```bash
cd tests
git checkout main
git pull origin main
cd ..
git add tests
git commit -m "Update submodule to track main branch"
```

### "I accidentally committed in the wrong repository"
**Problem**: Made commits in main repo that should be in test repo (or vice versa)

**Solution**: 
```bash
# Create a patch of your changes
git format-patch -1 HEAD

# Reset the wrong commit
git reset --hard HEAD~1

# Apply patch in correct repository
cd [correct-repository]
git apply [patch-file]
```

## Quick Reference Commands

### Essential Submodule Commands
```bash
# Clone with submodules
git clone --recurse-submodules [repository-url]

# Update submodules to latest
git submodule update --remote

# Initialize submodules after clone
git submodule init && git submodule update

# Work in submodule
cd tests
git checkout main
# Make changes
git add . && git commit -m "message" && git push origin main

# Update main repo to reference new submodule version
cd ..
git add tests
git commit -m "Update tests submodule"
git push origin main
```

### Code Developer Workflow
```bash
# Daily start
git pull origin main
git submodule update --remote

# Feature work
git checkout -b feature/name
# Make changes in src/
git add . && git commit -m "feature changes"
git push origin feature/name
# Create PR in Azure DevOps

# After PR merge
git checkout main && git pull origin main
```

### Test Developer Workflow (Option B)
```bash
# Daily start
cd YourApp/tests
git pull origin main

# Test work
# Make changes
git add . && git commit -m "test changes"
git push origin main

# Update main repo reference
cd ..
git add tests
git commit -m "Update tests submodule"
git push origin main
```

## FAQ

**Q: Which approach should I use - Option A or Option B for test development?**
A: Option B is recommended as it keeps everything in sync automatically and makes it easier to see code changes.

**Q: How often should we update the submodule reference in main?**
A: After every significant test update, or at least daily during active development.

**Q: Can I work on multiple features simultaneously?**
A: Yes! Code developer can have multiple feature branches, and test developer can create branches in the test repository to match.

**Q: What happens if I forget to update submodules?**
A: Your tests might be outdated. Always run `git submodule update --remote` when you start work.

**Q: Can the test developer see code changes easily?**
A: Yes, especially with Option B. They can run `git log` in the main repository to see recent code changes.

**Q: What if we want to release a specific version?**
A: Create tags in both repositories and pin the submodule to the specific test tag for that release.

**Q: Is this more complex than the separate branch approach?**
A: Initially yes, but it provides much cleaner separation and eliminates merge conflicts entirely.

## Getting Help

- **Git Submodules documentation**: [https://git-scm.com/book/en/v2/Git-Tools-Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- **Azure DevOps help**: [https://docs.microsoft.com/en-us/azure/devops/](https://docs.microsoft.com/en-us/azure/devops/)
- **Team contact**: [Add your team's contact information here]