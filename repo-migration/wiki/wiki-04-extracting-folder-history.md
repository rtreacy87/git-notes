# Extracting the Folder with its History

## Overview

This guide covers the process of extracting a folder from a source repository while preserving its complete commit history. We'll focus primarily on using git filter-repo, the recommended tool for this task, with alternatives mentioned where appropriate.

## Using Git Filter-Repo

Git filter-repo is the most efficient and reliable tool for extracting folders with their history. It replaces the older git filter-branch command and provides better performance and safety features.

### Basic Extraction Process

Follow these steps to extract a folder with its complete history:

1. **Prepare your working environment**:

   ```bash
   # Clone the source repository (if not already done)
   git clone https://source-repository-url.git source-repo-working
   cd source-repo-working
   
   # Create a new branch for the extraction
   git checkout -b extraction-branch
   ```

2. **Run git filter-repo to extract the folder**:

   ```bash
   # Extract a folder and maintain its path structure
   git filter-repo --path path/to/folder/
   
   # OR extract a folder and move it to the root
   git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./
   ```

3. **Verify the extraction**:

   ```bash
   # Check the repository structure
   ls -la
   
   # Verify the commit history was preserved
   git log
   ```

### Command Explanation

- `--path path/to/folder/`: Specifies the folder path to keep (everything else will be removed)
- `--path-rename path/to/folder/:./`: Moves the specified folder to the root of the repository
- The trailing slash in the path is important to ensure the entire folder is selected

### Advanced Extraction Options

For more complex scenarios, git filter-repo offers additional options:

#### Extracting Multiple Folders

```bash
# Keep multiple folders
git filter-repo --path path/to/folder1/ --path path/to/folder2/

# Keep multiple folders and rename them
git filter-repo --path path/to/folder1/ --path-rename path/to/folder1/:./folder1-new/ \
                --path path/to/folder2/ --path-rename path/to/folder2/:./folder2-new/
```

#### Filtering by File Type

```bash
# Keep only specific file types within a folder
git filter-repo --path path/to/folder/ --path-glob '*.java' --path-glob '*.xml'
```

#### Preserving Specific Branches

By default, git filter-repo operates on all branches. To limit to specific branches:

```bash
# First, create a new repository with only the branches you want
git clone --single-branch --branch main https://source-repository-url.git source-repo-filtered
cd source-repo-filtered

# Then run filter-repo
git filter-repo --path path/to/folder/
```

## Verifying the Extracted History

After extraction, it's crucial to verify that the history has been preserved correctly:

```bash
# Check the number of commits
git rev-list --count HEAD

# Compare with the number of commits in the original repository for this folder
cd ../source-repo-working
git rev-list --count HEAD -- path/to/folder/

# Return to the extracted repository
cd ../source-repo-filtered

# Examine the commit history
git log --name-status

# Check for any merge commits that might have been affected
git log --merges
```

### What to Look For

1. **Commit count**: The number of commits should be similar to the number of commits that modified the folder in the original repository
2. **Author information**: Author names and emails should be preserved
3. **Commit messages**: Original commit messages should be intact
4. **File paths**: File paths should be correct according to your extraction options
5. **Merge commits**: Complex merge history might be affected by the extraction

## Handling Edge Cases

### Submodules

If the folder you're extracting contains submodules:

```bash
# First, check if there are submodules in the folder
git submodule status -- path/to/folder/

# Extract the folder with submodules
git filter-repo --path path/to/folder/ --preserve-submodules
```

### Large Files (LFS)

If your repository uses Git LFS:

```bash
# Check for LFS objects in the folder
git lfs ls-files -- path/to/folder/

# Extract with LFS support
git filter-repo --path path/to/folder/ --preserve-blobs
```

### Symbolic Links

If your folder contains symbolic links:

```bash
# Find symbolic links in the folder
find path/to/folder/ -type l

# Extract with symbolic links (no special options needed, just be aware)
git filter-repo --path path/to/folder/
```

## Troubleshooting Common Extraction Issues

### Issue: Missing Commits

**Symptom**: Some commits that should be in the history are missing.

**Solution**:
```bash
# Try again with the --refs option to ensure all refs are processed
git filter-repo --path path/to/folder/ --refs refs/heads/* --refs refs/tags/*
```

### Issue: Corrupted Repository

**Symptom**: Git operations fail with errors about corrupted objects.

**Solution**:
```bash
# Start fresh with a new clone
git clone https://source-repository-url.git source-repo-new
cd source-repo-new

# Try the extraction with the --force option
git filter-repo --path path/to/folder/ --force
```

### Issue: Unexpected Empty Commits

**Symptom**: The history contains empty commits that don't modify any files.

**Solution**:
```bash
# Extract again with the --prune-empty always option
git filter-repo --path path/to/folder/ --prune-empty always
```

### Issue: Path Not Found

**Symptom**: Git filter-repo reports that the specified path doesn't exist.

**Solution**:
```bash
# Check if the path exists in the current branch
ls -la path/to/folder/

# Try with a branch where the folder exists
git checkout branch-with-folder
git filter-repo --path path/to/folder/
```

## Comparing Output from Different Extraction Tools

While git filter-repo is recommended, you might want to compare results with other tools:

### Git Subtree Split

```bash
# Extract using git subtree split
git subtree split --prefix=path/to/folder -b folder-branch

# Create a new repository from the branch
mkdir ../folder-repo
cd ../folder-repo
git init
git pull ../source-repo-working folder-branch
```

### Git Filter-Branch (Legacy Approach)

```bash
# Extract using git filter-branch (not recommended for performance reasons)
git filter-branch --prune-empty --subdirectory-filter path/to/folder HEAD
```

### Comparison Metrics

To compare the results from different tools:

```bash
# Count commits in each extracted repository
cd filter-repo-result
git rev-list --count HEAD
cd ../subtree-result
git rev-list --count HEAD
cd ../filter-branch-result
git rev-list --count HEAD

# Compare file structure
find . -type f | sort > ../filter-repo-files.txt
cd ../subtree-result
find . -type f | sort > ../subtree-files.txt
cd ..
diff filter-repo-files.txt subtree-files.txt
```

## Next Steps

After successfully extracting the folder with its history, proceed to [Importing into the Destination Repository](./wiki-05-importing-destination.md) to complete the migration process.

## See Also

- [External Tools for Repository Migration](./wiki-02-external-tools.md)
- [Preparation Steps](./wiki-03-preparation-steps.md)
- [Importing into the Destination Repository](./wiki-05-importing-destination.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)

## Glossary

- **Git Filter-Repo**: A tool for rewriting Git repository history, more efficient and safer than git filter-branch.
- **Git Subtree Split**: A Git command that extracts a subdirectory into a separate branch with its history.
- **Git Filter-Branch**: A legacy Git command for rewriting history, now deprecated in favor of git filter-repo.
- **Submodule**: A Git feature that allows you to include other Git repositories within your repository.
- **Git LFS (Large File Storage)**: An extension to Git that replaces large files with text pointers inside Git.
