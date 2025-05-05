# Instructor Guide: DevOps Repository Migration Lab

This guide provides additional information for instructors facilitating the DevOps Repository Migration Lab.

## Lab Overview

This lab teaches participants how to:
1. Set up a simple web application in a Git repository
2. Make modifications to the code and commit changes
3. Create a new repository
4. Migrate code between repositories while preserving commit history

## Preparation

Before the lab session:

1. Ensure participants have:
   - Git installed on their machines
   - Access to a DevOps platform (GitHub, Azure DevOps, GitLab, etc.)
   - Basic familiarity with Git commands
   - A text editor or IDE

2. Distribute the lab files:
   - index.html
   - styles.css
   - script.js
   - README.md (lab instructions)

3. Optional: Set up a sample repository that participants can fork instead of creating from scratch

## Common Issues and Solutions

### Git Configuration Issues

**Issue**: Participants may not have Git configured with their username and email.

**Solution**: Instruct them to run:
```bash
git config --global user.name "Their Name"
git config --global user.email "their.email@example.com"
```

### Authentication Issues

**Issue**: Participants may have trouble authenticating with their DevOps platform.

**Solutions**:
- For HTTPS: Recommend using credential helpers or personal access tokens
- For SSH: Guide them through setting up SSH keys

### Git Command Errors

**Issue**: Participants may make errors in Git commands.

**Solution**: Prepare a "cheat sheet" of common Git commands and their usage:
```
git clone <url>              # Clone a repository
git add <file>               # Stage changes
git commit -m "message"      # Commit changes
git push <remote> <branch>   # Push changes
git remote add <name> <url>  # Add a remote
```

## Lab Walkthrough

### Part 1: Setting Up the Initial Repository

Emphasize the importance of:
- Creating a clean, well-structured initial commit
- Verifying that the application works before proceeding

### Part 2: Making Code Modifications

Key teaching points:
- Making focused, atomic commits with clear commit messages
- Testing changes before committing
- The importance of descriptive commit messages

### Part 3 & 4: Repository Migration

This is the core learning objective. Ensure participants understand:
- The difference between copying files and migrating with history
- How Git remotes work
- How to verify that history has been preserved

### Part 5: Advanced Migration

This optional section is for more advanced participants. Be prepared to:
- Help with installing git-filter-repo
- Explain the concept of history rewriting
- Discuss use cases for more complex migrations

## Assessment

To assess participant understanding:

1. Check that they have successfully:
   - Created the initial repository with the weather app
   - Made the required modifications with appropriate commit messages
   - Migrated the code to a new repository with history preserved

2. Ask follow-up questions:
   - What are the advantages of preserving commit history during migration?
   - In what scenarios would you use the simple migration vs. the advanced migration?
   - How would you migrate only a specific folder from a larger repository?

## Extended Learning

For participants who complete the lab quickly, suggest these additional exercises:

1. Create a branch in the new repository, make changes, and create a pull request
2. Set up a simple CI/CD pipeline for the application
3. Experiment with more complex migration scenarios:
   - Migrate only specific commits
   - Merge multiple repositories into one
   - Split one repository into multiple repositories

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo)
- [GitHub Learning Lab](https://lab.github.com/)
- [Azure DevOps Labs](https://www.azuredevopslabs.com/)

## Lab Timing

Estimated time for completion:
- Basic lab (Parts 1-4): 45-60 minutes
- Complete lab including advanced section: 75-90 minutes

Adjust timing based on participant experience level.
