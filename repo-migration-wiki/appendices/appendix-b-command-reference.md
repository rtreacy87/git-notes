# Appendix B: Command Reference

## Overview

This appendix provides a comprehensive reference for all Git and related commands used in folder migrations with preserved history. Each command is explained with syntax, common options, and practical examples.

## Git Filter-Repo Commands

Git filter-repo is the recommended tool for extracting folders with their history.

### Basic Syntax

```bash
git filter-repo [options]
```

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--path` | Keep files matching the specified path | `--path path/to/folder/` |
| `--path-glob` | Keep files matching the specified glob pattern | `--path-glob '*.java'` |
| `--path-regex` | Keep files matching the specified regex pattern | `--path-regex '.*\.java$'` |
| `--invert-paths` | Invert the meaning of paths (exclude instead of include) | `--invert-paths` |
| `--path-rename` | Rename paths matching a pattern | `--path-rename old/path/:new/path/` |
| `--refs` | Only consider the specified refs | `--refs refs/heads/main` |
| `--force` | Allow operation even on a dirty working directory | `--force` |
| `--prune-empty` | Remove empty commits | `--prune-empty always` |
| `--preserve-commit-hashes` | Try to preserve original commit hashes | `--preserve-commit-hashes` |
| `--preserve-commit-encoding` | Preserve original commit encoding | `--preserve-commit-encoding` |
| `--mailmap` | Apply mailmap file to fix author/committer names and emails | `--mailmap ../mailmap.txt` |
| `--replace-text` | Replace strings in files | `--replace-text ../replacements.txt` |
| `--strip-blobs-bigger-than` | Remove blobs bigger than the specified size | `--strip-blobs-bigger-than 10M` |
| `--analyze` | Analyze repository history and print report | `--analyze` |

### Examples

#### Extract a folder with its history

```bash
# Extract a folder and keep its path structure
git filter-repo --path path/to/folder/

# Extract a folder and move it to the root
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./

# Extract multiple folders
git filter-repo --path path/to/folder1/ --path path/to/folder2/

# Extract a folder and rename it
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:new/path/

# Extract a folder with specific file types
git filter-repo --path path/to/folder/ --path-glob '*.java' --path-glob '*.xml'

# Extract a folder and fix author information
git filter-repo --path path/to/folder/ --mailmap ../mailmap.txt

# Extract a folder and remove large files
git filter-repo --path path/to/folder/ --strip-blobs-bigger-than 10M

# Extract a folder and remove empty commits
git filter-repo --path path/to/folder/ --prune-empty always

# Extract a folder from a specific branch
git filter-repo --path path/to/folder/ --refs refs/heads/main
```

## Git Subtree Commands

Git subtree provides an alternative approach for managing repository subsets.

### Subtree Add

Adds a repository as a subtree.

```bash
git subtree add --prefix=<prefix> <repository> <ref> [--squash]
```

#### Options

| Option | Description |
|--------|-------------|
| `--prefix=<prefix>` | The directory to add the subtree to |
| `<repository>` | The repository URL or local path |
| `<ref>` | The branch, tag, or commit to add |
| `--squash` | Merge subtree changes as a single commit |

#### Examples

```bash
# Add a repository as a subtree
git subtree add --prefix=path/to/folder https://github.com/user/repo.git main

# Add a repository as a subtree with squashing
git subtree add --prefix=path/to/folder https://github.com/user/repo.git main --squash

# Add a local repository as a subtree
git subtree add --prefix=path/to/folder ../local-repo main
```

### Subtree Pull

Updates a subtree from its source.

```bash
git subtree pull --prefix=<prefix> <repository> <ref> [--squash]
```

#### Examples

```bash
# Update a subtree
git subtree pull --prefix=path/to/folder https://github.com/user/repo.git main

# Update a subtree with squashing
git subtree pull --prefix=path/to/folder https://github.com/user/repo.git main --squash
```

### Subtree Push

Pushes changes from a subtree back to its source.

```bash
git subtree push --prefix=<prefix> <repository> <ref>
```

#### Examples

```bash
# Push changes from a subtree
git subtree push --prefix=path/to/folder https://github.com/user/repo.git main
```

### Subtree Split

Extracts a subtree into a separate branch.

```bash
git subtree split --prefix=<prefix> [--branch <branch>]
```

#### Options

| Option | Description |
|--------|-------------|
| `--prefix=<prefix>` | The directory containing the subtree |
| `--branch <branch>` | The name of the branch to create |

#### Examples

```bash
# Extract a subtree into a branch
git subtree split --prefix=path/to/folder -b folder-branch

# Extract a subtree and create a new repository
git subtree split --prefix=path/to/folder -b folder-branch
mkdir ../new-repo
cd ../new-repo
git init
git pull ../original-repo folder-branch
```

## Git Submodule Commands

Git submodules allow you to include other Git repositories within your repository.

### Submodule Add

Adds a repository as a submodule.

```bash
git submodule add <repository> [<path>]
```

#### Options

| Option | Description |
|--------|-------------|
| `<repository>` | The repository URL |
| `<path>` | The path where the submodule should be placed |

#### Examples

```bash
# Add a repository as a submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Add a repository as a submodule with a specific branch
git submodule add -b main https://github.com/user/repo.git path/to/submodule
```

### Submodule Update

Updates submodules to their latest commits.

```bash
git submodule update [--init] [--recursive]
```

#### Options

| Option | Description |
|--------|-------------|
| `--init` | Initialize submodules if they haven't been yet |
| `--recursive` | Update nested submodules |

#### Examples

```bash
# Update submodules
git submodule update

# Initialize and update submodules
git submodule update --init

# Initialize and update submodules recursively
git submodule update --init --recursive
```

### Submodule Status

Shows the status of submodules.

```bash
git submodule status
```

#### Examples

```bash
# Show status of all submodules
git submodule status

# Show status of a specific submodule
git submodule status path/to/submodule
```

## Git Core Commands for Migration

These core Git commands are essential for folder migrations.

### Clone

Creates a copy of a repository.

```bash
git clone [options] <repository> [<directory>]
```

#### Options

| Option | Description |
|--------|-------------|
| `--mirror` | Create a mirror clone (includes all refs) |
| `--bare` | Create a bare repository |
| `--depth <depth>` | Create a shallow clone with the specified depth |
| `--branch <branch>` | Check out the specified branch |
| `--single-branch` | Clone only the history of the specified branch |

#### Examples

```bash
# Clone a repository
git clone https://github.com/user/repo.git

# Create a mirror clone (for backups)
git clone --mirror https://github.com/user/repo.git repo-backup.git

# Clone with limited history
git clone --depth 100 https://github.com/user/repo.git

# Clone a specific branch
git clone --branch develop --single-branch https://github.com/user/repo.git
```

### Remote

Manages remote repositories.

```bash
git remote add <name> <url>
git remote remove <name>
git remote -v
```

#### Examples

```bash
# Add a remote
git remote add origin https://github.com/user/repo.git

# Add the extracted repository as a remote
git remote add extracted-folder ../extracted-repo

# List all remotes
git remote -v

# Remove a remote
git remote remove extracted-folder
```

### Fetch

Retrieves objects and refs from a remote repository.

```bash
git fetch [<remote>] [<refspec>...]
```

#### Examples

```bash
# Fetch from all remotes
git fetch --all

# Fetch from a specific remote
git fetch origin

# Fetch a specific branch
git fetch origin main

# Fetch from the extracted repository
git fetch extracted-folder
```

### Checkout

Switches branches or restores working tree files.

```bash
git checkout <branch>
git checkout -b <new-branch>
```

#### Examples

```bash
# Switch to an existing branch
git checkout main

# Create and switch to a new branch
git checkout -b import-folder-branch

# Create a branch for the import
git checkout -b import-$(date +%Y%m%d)
```

### Read-tree

Reads tree information into the index.

```bash
git read-tree [options] <tree-ish>
```

#### Options

| Option | Description |
|--------|-------------|
| `--prefix=<prefix>` | Read the tree into the index under the specified directory |
| `-u` | Update the working directory with the result |

#### Examples

```bash
# Import a folder to a specific location
git read-tree --prefix=path/to/target/location -u extracted-folder/main

# Import multiple folders
git read-tree --prefix=path/to/location1 -u extracted-folder1/main
git read-tree --prefix=path/to/location2 -u extracted-folder2/main
```

### Merge

Joins two or more development histories together.

```bash
git merge [options] <commit>...
```

#### Options

| Option | Description |
|--------|-------------|
| `--allow-unrelated-histories` | Allow merging unrelated histories |
| `--no-commit` | Perform the merge but don't commit |
| `--squash` | Squash all commits into a single commit |

#### Examples

```bash
# Merge the extracted repository
git merge --allow-unrelated-histories extracted-folder/main

# Merge with squashing
git merge --squash extracted-folder/main

# Merge without committing
git merge --no-commit --allow-unrelated-histories extracted-folder/main
```

### Commit

Records changes to the repository.

```bash
git commit [options]
```

#### Options

| Option | Description |
|--------|-------------|
| `-m <message>` | Use the given message as the commit message |
| `-a` | Automatically stage all modified and deleted files |
| `--amend` | Amend the previous commit |

#### Examples

```bash
# Commit changes
git commit -m "Import folder with history from source repository"

# Commit all changes
git commit -a -m "Update imported folder"

# Amend the previous commit
git commit --amend -m "Import folder with history from source repository"
```

### Push

Updates remote refs along with associated objects.

```bash
git push [options] [<remote>] [<refspec>...]
```

#### Options

| Option | Description |
|--------|-------------|
| `-u, --set-upstream` | Set upstream for git pull/status |
| `--force` | Force push (use with caution) |
| `--tags` | Push all tags |

#### Examples

```bash
# Push a branch
git push origin import-folder-branch

# Push and set upstream
git push -u origin import-folder-branch

# Push all branches
git push --all origin

# Push all tags
git push --tags origin
```

### Log

Shows commit logs.

```bash
git log [options] [<revision range>] [[--] <path>...]
```

#### Options

| Option | Description |
|--------|-------------|
| `--follow` | Continue listing the history beyond renames |
| `--stat` | Show statistics for files modified in each commit |
| `--oneline` | Show each commit on a single line |
| `--graph` | Draw a text-based graphical representation of the commit history |

#### Examples

```bash
# View commit history for a folder
git log -- path/to/folder

# View commit history following renames
git log --follow -- path/to/folder

# View commit history with statistics
git log --stat -- path/to/folder

# View commit history as a graph
git log --graph --oneline -- path/to/folder

# Count commits affecting a folder
git log --oneline -- path/to/folder | wc -l
```

## Azure DevOps CLI Commands

These commands are useful for managing Azure DevOps repositories and branch policies.

### Repository Commands

```bash
# List repositories
az repos list --org <organization-url> --project <project-name> -o table

# Show repository details
az repos show --id <repository-id> --org <organization-url> --project <project-name>

# Create a new repository
az repos create --name <repository-name> --project <project-name> --org <organization-url>
```

### Branch Policy Commands

```bash
# List branch policies
az repos policy list --repository-id <repository-id> --branch <branch-name> --org <organization-url> --project <project-name>

# Show policy details
az repos policy show --id <policy-id> --org <organization-url> --project <project-name>

# Create a branch policy
az repos policy create --repository-id <repository-id> --branch <branch-name> --policy-type <policy-type> --org <organization-url> --project <project-name>

# Update a policy
az repos policy update --id <policy-id> --status <active|disabled> --org <organization-url> --project <project-name>

# Delete a policy
az repos policy delete --id <policy-id> --org <organization-url> --project <project-name>
```

## BFG Repo Cleaner Commands

BFG is useful for removing large files or sensitive data from Git repositories.

```bash
# Remove files larger than 10MB
java -jar bfg.jar --strip-blobs-bigger-than 10M <repository.git>

# Remove specific files
java -jar bfg.jar --delete-files "*.mp4" <repository.git>

# Replace sensitive data
java -jar bfg.jar --replace-text passwords.txt <repository.git>
```

## Command Examples for Common Scenarios

### Complete Folder Migration Workflow

```bash
# 1. Create backups
git clone --mirror https://source-repository-url.git source-repo-backup.git
git clone --mirror https://destination-repository-url.git dest-repo-backup.git

# 2. Clone source repository
git clone https://source-repository-url.git source-repo
cd source-repo

# 3. Extract folder with history
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./

# 4. Clone destination repository
cd ..
git clone https://destination-repository-url.git dest-repo
cd dest-repo

# 5. Create branch for import
git checkout -b import-folder-branch

# 6. Add extracted repo as remote
git remote add extracted-folder ../source-repo
git fetch extracted-folder

# 7. Import the folder
mkdir -p path/to/target/location
git read-tree --prefix=path/to/target/location -u extracted-folder/main
git commit -m "Import folder with history from source repository"

# 8. Push the changes
git push -u origin import-folder-branch
```

### Migrating Multiple Folders

```bash
# For each folder
for folder in folder1 folder2 folder3; do
    # Clone source repo for this folder
    mkdir -p "temp-$folder"
    cd "temp-$folder"
    git clone ../source-repo .
    
    # Extract the folder with history
    git filter-repo --path "$folder/" --path-rename "$folder/:/"
    
    # Go to destination repo
    cd ../dest-repo
    
    # Create target directory
    mkdir -p "target/$folder"
    
    # Add the extracted repo as a remote
    git remote add "extracted-$folder" "../temp-$folder"
    git fetch "extracted-$folder"
    
    # Import the folder
    git read-tree --prefix="target/$folder" -u "extracted-$folder/main"
    git commit -m "Import $folder with history"
    
    # Remove the remote
    git remote remove "extracted-$folder"
    
    # Go back to the main directory
    cd ..
done
```

### Handling Conflicts During Import

```bash
# Try to import the folder
git read-tree --prefix=path/to/target/location -u extracted-folder/main

# If that fails, try merging
git merge --allow-unrelated-histories extracted-folder/main

# If there are conflicts, resolve them
git status
# Edit conflicted files as needed
git add .
git commit -m "Resolve conflicts in imported folder"
```

### Creating a Migration Report

```bash
# Count files in the source folder
find path/to/folder -type f | wc -l > migration-report.txt
echo "Files in source folder: $(cat migration-report.txt)" > migration-report.txt

# Count commits affecting the folder
git log --oneline -- path/to/folder | wc -l >> migration-report.txt
echo "Commits affecting folder: $(tail -n 1 migration-report.txt)" >> migration-report.txt

# List authors who contributed to the folder
git log --format='%an' -- path/to/folder | sort | uniq >> migration-report.txt
echo "Contributors:" >> migration-report.txt
cat migration-report.txt | grep -v "Files" | grep -v "Commits" >> migration-report.txt

# After migration, count files in the destination
cd ../dest-repo
find path/to/target/location -type f | wc -l >> ../migration-report.txt
echo "Files in destination folder: $(tail -n 1 ../migration-report.txt)" >> ../migration-report.txt

# Count commits in the destination
git log --oneline -- path/to/target/location | wc -l >> ../migration-report.txt
echo "Commits in destination folder: $(tail -n 1 ../migration-report.txt)" >> ../migration-report.txt
```

## Parameter Reference with Best Practices

### Git Filter-Repo Parameters

| Parameter | Best Practice |
|-----------|---------------|
| `--path` | Always include the trailing slash for directories |
| `--path-rename` | Use `old/path/:new/path/` format, including trailing slashes |
| `--refs` | Specify all relevant refs (e.g., `refs/heads/*, refs/tags/*`) |
| `--force` | Use only when necessary, prefer clean working directory |
| `--prune-empty` | Use `--prune-empty always` to remove all empty commits |
| `--mailmap` | Create a comprehensive mailmap file for author normalization |

### Git Read-Tree Parameters

| Parameter | Best Practice |
|-----------|---------------|
| `--prefix` | Ensure the target directory exists before using |
| `-u` | Always include to update the working directory |

### Git Merge Parameters

| Parameter | Best Practice |
|-----------|---------------|
| `--allow-unrelated-histories` | Required for merging repositories with different histories |
| `--squash` | Avoid for migrations where history preservation is important |
| `--no-commit` | Useful for reviewing changes before committing |

## Next Steps

After familiarizing yourself with these commands, refer to the following resources:

- [Extracting the Folder with its History](../wiki-04-extracting-folder-history.md)
- [Importing into the Destination Repository](../wiki-05-importing-destination.md)
- [Appendix C: Performance Optimization](./appendix-c-performance-optimization.md)

## See Also

- [External Tools for Repository Migration](../wiki-02-external-tools.md)
- [Automation Options](../wiki-06-automation-options.md)
- [Appendix A: Tool Installation Guide](./appendix-a-tool-installation.md)
