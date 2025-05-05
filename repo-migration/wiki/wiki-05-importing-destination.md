# Importing into the Destination Repository

## Overview

After successfully extracting a folder with its history from the source repository, the next step is to import it into the destination repository. This guide covers the process of preparing the destination repository, merging the extracted folder, and resolving any conflicts that may arise.

## Preparing the Destination Repository

Before importing the extracted folder, you need to prepare the destination repository to receive the changes.

### Create a Branch for the Import

```bash
# Navigate to the destination repository
cd destination-repo-working

# Ensure you have the latest changes
git fetch origin
git checkout main  # or your default branch
git pull

# Create a new branch for the import
git checkout -b import-folder-branch
```

### Prepare the Target Location

If you plan to place the extracted folder in a specific location within the destination repository, prepare that location:

```bash
# Create the target directory if it doesn't exist
mkdir -p path/to/target/location

# If needed, create a placeholder file to establish the directory in Git
touch path/to/target/location/.gitkeep
git add path/to/target/location/.gitkeep
git commit -m "Prepare target location for folder import"
```

## Merging the Extracted Folder

There are several approaches to merging the extracted folder into the destination repository. We'll cover the most common methods.

### Method 1: Using Git Remote (Recommended)

This method adds the extracted repository as a remote and merges it:

```bash
# Navigate to the destination repository
cd destination-repo-working

# Add the extracted repository as a remote
git remote add extracted-folder /path/to/extracted-folder-repo

# Fetch the extracted repository
git fetch extracted-folder

# Merge the extracted repository into the current branch
# If you want the folder at the root:
git merge --allow-unrelated-histories extracted-folder/main

# If you want the folder in a specific location:
git read-tree --prefix=path/to/target/location -u extracted-folder/main

# Commit the changes
git commit -m "Import folder with history from source repository"
```

### Method 2: Using Git Subtree Add

If you prefer using git subtree:

```bash
# Navigate to the destination repository
cd destination-repo-working

# Add the extracted repository as a subtree
git subtree add --prefix=path/to/target/location /path/to/extracted-folder-repo main --squash

# Note: The --squash option will compress the history into a single commit
# Omit --squash to preserve the full history
```

### Method 3: Manual Copy with Git Filter-Repo

For more complex scenarios:

```bash
# Navigate to the destination repository
cd destination-repo-working

# Create a temporary branch
git checkout -b temp-import-branch

# Copy the extracted repository content
cp -r /path/to/extracted-folder-repo/* .

# Add all files
git add .

# Commit the changes
git commit -m "Import folder with history from source repository"

# Use git filter-repo to rewrite the history if needed
git filter-repo --path-rename ./:path/to/target/location/
```

## Resolving Potential Conflicts

Conflicts may arise during the import process, especially if files with the same names exist in both repositories.

### Identifying Conflicts

```bash
# After attempting a merge, Git will show conflicts
git status

# For a more detailed view of conflicts
git diff --name-only --diff-filter=U
```

### Resolving Conflicts

```bash
# Resolve conflicts manually by editing the conflicted files
# After editing, mark them as resolved
git add path/to/resolved/file

# Continue the merge process
git merge --continue

# Or if using read-tree, commit the changes
git commit -m "Resolve conflicts in imported folder"
```

### Using Merge Tools

For complex conflicts, you may want to use a merge tool:

```bash
# Configure your preferred merge tool
git config merge.tool meld  # or kdiff3, vimdiff, etc.

# Launch the merge tool for all conflicts
git mergetool

# After resolving all conflicts
git commit -m "Resolve conflicts in imported folder"
```

## Preserving Commit Metadata

When importing a folder, it's important to preserve the original commit metadata, including authors, dates, and messages.

### Verifying Metadata Preservation

```bash
# Check the commit history to ensure metadata is preserved
git log --pretty=full

# Compare with the original repository's history
cd /path/to/extracted-folder-repo
git log --pretty=full
```

### Fixing Author Information

If author information is not correctly preserved:

```bash
# Use git filter-repo to fix author information
git filter-repo --mailmap ../mailmap.txt

# Where mailmap.txt contains mappings like:
# Correct Name <correct@email.com> <old@email.com>
```

## Verifying the Imported History

After completing the import, verify that the history has been correctly preserved:

```bash
# Navigate to the destination repository
cd destination-repo-working

# Check the commit history for the imported folder
git log -- path/to/target/location

# Compare with the history in the extracted repository
cd /path/to/extracted-folder-repo
git log

# Return to the destination repository
cd ../destination-repo-working

# Check for any merge commits or anomalies
git log --merges -- path/to/target/location
```

### What to Verify

1. **Commit count**: The number of commits should match the extracted repository
2. **Author information**: Author names and emails should be preserved
3. **Commit messages**: Original commit messages should be intact
4. **File paths**: Files should be in the correct location
5. **File content**: Content should match the original files
6. **Functionality**: The imported code should function correctly

## Tool-specific Import Procedures

### Azure DevOps Import

For Azure DevOps repositories:

```bash
# Install the Azure DevOps CLI extension if not already installed
az extension add --name azure-devops

# Push the extracted repository to a new Azure DevOps repository
cd /path/to/extracted-folder-repo
git remote add origin https://dev.azure.com/organization/project/_git/new-repo
git push -u origin --all

# Then follow Method 1 above, using the new Azure DevOps repository as the remote
```

### GitHub Import

For GitHub repositories:

```bash
# Create a new GitHub repository through the web interface

# Push the extracted repository to GitHub
cd /path/to/extracted-folder-repo
git remote add origin https://github.com/username/new-repo.git
git push -u origin --all

# Then follow Method 1 above, using the GitHub repository as the remote
```

## Best Practices

1. **Work in branches**: Always perform imports in a separate branch
2. **Test before merging**: Verify the imported code works correctly before merging to main branches
3. **Preserve history**: Use methods that maintain the commit history whenever possible
4. **Document the process**: Keep notes on the steps taken for future reference
5. **Communicate changes**: Inform team members about the imported folder and any path changes

## Next Steps

After successfully importing the folder into the destination repository, proceed to [Post-Migration Tasks](./wiki-07-post-migration-tasks.md) to complete the migration process.

Before that, you may want to explore [Automation Options](./wiki-06-automation-options.md) if you need to perform similar migrations in the future.

## See Also

- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Automation Options](./wiki-06-automation-options.md)
- [Post-Migration Tasks](./wiki-07-post-migration-tasks.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)

## Glossary

- **Unrelated Histories**: Git repositories with no common ancestor commits
- **Merge Conflict**: When Git cannot automatically merge changes because they affect the same parts of files
- **Remote**: A connection to another Git repository
- **Subtree**: A Git feature for including one repository within another
- **Mailmap**: A file that maps incorrect author information to correct information
