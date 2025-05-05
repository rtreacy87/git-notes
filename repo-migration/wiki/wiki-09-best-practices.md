# Best Practices and Case Studies

## Overview

This guide presents best practices for folder migrations with preserved history, along with real-world case studies that illustrate successful approaches and lessons learned. These insights will help you plan and execute your migrations more effectively, avoiding common pitfalls and leveraging proven strategies.

## Git Command Reference for History Preservation

### Essential Git Commands for Migration

| Command | Purpose | Example |
|---------|---------|---------|
| `git filter-repo` | Extract folder with history | `git filter-repo --path path/to/folder/` |
| `git read-tree` | Import folder to specific location | `git read-tree --prefix=target/path -u source/branch` |
| `git merge --allow-unrelated-histories` | Merge repositories with different histories | `git merge --allow-unrelated-histories extracted/main` |
| `git log --follow` | View history of a file or folder across renames | `git log --follow -- path/to/folder` |
| `git remote add` | Add a repository as a remote | `git remote add extracted-folder ../extracted-repo` |
| `git fetch` | Retrieve objects from a remote | `git fetch extracted-folder` |
| `git clone --mirror` | Create a complete backup | `git clone --mirror https://repo-url.git backup` |

### Advanced Git Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `git subtree add` | Add repository as a subtree | `git subtree add --prefix=path/to/folder repo-url main` |
| `git subtree split` | Extract folder as separate history | `git subtree split --prefix=path/to/folder -b folder-branch` |
| `git filter-repo --path-rename` | Move folder to new location | `git filter-repo --path-rename old/path/:new/path/` |
| `git filter-repo --mailmap` | Fix author information | `git filter-repo --mailmap ../mailmap.txt` |
| `git filter-repo --refs` | Process specific refs | `git filter-repo --path folder/ --refs refs/heads/main` |
| `git filter-repo --prune-empty` | Remove empty commits | `git filter-repo --path folder/ --prune-empty always` |

## Tips for Maintaining Clean History During Migrations

### Before Migration

1. **Clean up the source repository**:
   ```bash
   # Remove unnecessary files
   git filter-repo --path-glob '*.log' --invert-paths
   
   # Fix author information if needed
   git filter-repo --mailmap ../mailmap.txt
   ```

2. **Standardize line endings**:
   ```bash
   # Configure Git to handle line endings consistently
   git config --global core.autocrlf input
   
   # Add .gitattributes file
   echo "* text=auto" > .gitattributes
   git add .gitattributes
   git commit -m "Add .gitattributes for consistent line endings"
   ```

3. **Remove large binary files**:
   ```bash
   # Identify large files
   git filter-repo --analyze
   
   # Remove large files
   git filter-repo --strip-blobs-bigger-than 10M
   ```

### During Migration

1. **Preserve commit metadata**:
   ```bash
   # Use git filter-repo with default options to preserve metadata
   git filter-repo --path path/to/folder/
   ```

2. **Maintain atomic commits**:
   ```bash
   # Avoid squashing commits during migration
   git subtree add --prefix=path/to/folder repo-url main  # Without --squash
   ```

3. **Keep meaningful commit messages**:
   ```bash
   # If needed, rewrite commit messages to add context
   git filter-repo --message-callback 'return b"[Migrated] " + message'
   ```

### After Migration

1. **Verify commit history integrity**:
   ```bash
   # Check commit count
   git rev-list --count HEAD
   
   # Examine commit messages and changes
   git log --stat
   ```

2. **Add migration documentation**:
   ```bash
   # Create a migration note
   echo "# Migration History\n\nThis folder was migrated from [source-repo] on [date]." > MIGRATION.md
   git add MIGRATION.md
   git commit -m "Add migration documentation"
   ```

3. **Tag the migration point**:
   ```bash
   # Create a tag to mark the migration
   git tag -a migration-complete -m "Folder migration completed on $(date)"
   git push origin migration-complete
   ```

## Sample Migration Script Templates

### Basic Migration Script

```bash
#!/bin/bash
# basic_migration.sh

# Configuration
SOURCE_REPO=$1
DEST_REPO=$2
FOLDER_PATH=$3
TARGET_PATH=$4
BRANCH_NAME="import-$(echo $FOLDER_PATH | tr '/' '-')-$(date +%Y%m%d)"

# Create working directory
WORK_DIR="migration-$(date +%Y%m%d-%H%M%S)"
mkdir -p $WORK_DIR
cd $WORK_DIR

echo "Starting migration of $FOLDER_PATH to $TARGET_PATH"

# Step 1: Clone source repository
echo "Cloning source repository..."
git clone $SOURCE_REPO source-repo
cd source-repo

# Step 2: Extract folder with history
echo "Extracting folder with history..."
git filter-repo --path "$FOLDER_PATH/" --path-rename "$FOLDER_PATH/:/"

# Step 3: Clone destination repository
echo "Cloning destination repository..."
cd ..
git clone $DEST_REPO dest-repo
cd dest-repo

# Step 4: Create branch for import
echo "Creating branch for import..."
git checkout -b $BRANCH_NAME

# Step 5: Add extracted repo as remote
echo "Adding extracted repo as remote..."
git remote add extracted-folder "../source-repo"
git fetch extracted-folder

# Step 6: Import the folder
echo "Importing folder to target location..."
mkdir -p $TARGET_PATH
git read-tree --prefix="$TARGET_PATH" -u extracted-folder/main
git commit -m "Import $FOLDER_PATH from source repository with history"

# Step 7: Push the changes
echo "Changes ready to be pushed."
echo "To push the changes, run:"
echo "cd $WORK_DIR/dest-repo && git push origin $BRANCH_NAME"

echo "Migration completed successfully!"
```

### Advanced Migration Script with Error Handling

```bash
#!/bin/bash
# advanced_migration.sh

set -e  # Exit immediately if a command fails

# Configuration
SOURCE_REPO=$1
DEST_REPO=$2
FOLDER_PATH=$3
TARGET_PATH=$4
LOG_FILE="migration-$(date +%Y%m%d-%H%M%S).log"
BRANCH_NAME="import-$(echo $FOLDER_PATH | tr '/' '-')-$(date +%Y%m%d)"

# Function to log messages
log() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

# Function to log errors
log_error() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERROR: $1" | tee -a "$LOG_FILE"
}

# Function to clean up on exit
cleanup() {
    log "Cleaning up temporary files and directories..."
    if [ -d "$WORK_DIR" ]; then
        rm -rf "$WORK_DIR"
    fi
    log "Cleanup completed"
}

# Create working directory
WORK_DIR="migration-$(date +%Y%m%d-%H%M%S)"
mkdir -p $WORK_DIR
cd $WORK_DIR

log "Starting migration of $FOLDER_PATH to $TARGET_PATH"

# Step 1: Create backups
log "Creating backups..."
mkdir -p backups
git clone --mirror $SOURCE_REPO backups/source-repo-backup.git
git clone --mirror $DEST_REPO backups/dest-repo-backup.git

# Step 2: Clone source repository
log "Cloning source repository..."
git clone $SOURCE_REPO source-repo
cd source-repo

# Step 3: Verify folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    log_error "Folder does not exist in source repository: $FOLDER_PATH"
    exit 1
fi

# Step 4: Extract folder with history
log "Extracting folder with history..."
git filter-repo --path "$FOLDER_PATH/" --path-rename "$FOLDER_PATH/:/"

# Step 5: Verify extraction
COMMIT_COUNT=$(git rev-list --count HEAD)
log "Extracted folder with $COMMIT_COUNT commits"

# Step 6: Clone destination repository
log "Cloning destination repository..."
cd ..
git clone $DEST_REPO dest-repo
cd dest-repo

# Step 7: Create branch for import
log "Creating branch for import..."
git checkout -b $BRANCH_NAME

# Step 8: Add extracted repo as remote
log "Adding extracted repo as remote..."
git remote add extracted-folder "../source-repo"
git fetch extracted-folder

# Step 9: Import the folder
log "Importing folder to target location..."
mkdir -p $TARGET_PATH
git read-tree --prefix="$TARGET_PATH" -u extracted-folder/main
git commit -m "Import $FOLDER_PATH from source repository with history"

# Step 10: Verify import
IMPORTED_FILES=$(find "$TARGET_PATH" -type f | wc -l)
log "Imported $IMPORTED_FILES files to $TARGET_PATH"

# Step 11: Add migration documentation
log "Adding migration documentation..."
cat > "$TARGET_PATH/MIGRATION.md" << EOF
# Migration History

This folder was migrated from $SOURCE_REPO on $(date).

Original path: $FOLDER_PATH
Migration date: $(date)
Commit count: $COMMIT_COUNT
EOF

git add "$TARGET_PATH/MIGRATION.md"
git commit -m "Add migration documentation"

# Step 12: Push the changes
log "Changes ready to be pushed."
log "To push the changes, run:"
log "cd $WORK_DIR/dest-repo && git push origin $BRANCH_NAME"

log "Migration completed successfully!"
```

## Real-world Case Studies and Lessons Learned

### Case Study 1: Microservice Extraction

**Scenario**: A team needed to extract a microservice from a monolithic application while preserving its development history.

**Approach**:
1. Identified the folder containing the microservice code
2. Used git filter-repo to extract the folder with history
3. Created a new repository for the microservice
4. Updated build pipelines and dependencies

**Challenges**:
- The microservice had dependencies on shared libraries in the monolith
- Some files needed to be in multiple repositories

**Solution**:
```bash
# Extract the microservice folder
git filter-repo --path services/microservice-a/

# Extract shared libraries needed by the microservice
git filter-repo --path shared/utils/ --path services/microservice-a/ \
                --path-rename shared/utils/:shared/utils/

# Create a new repository for the microservice
git remote add origin https://dev.azure.com/org/project/_git/microservice-a
git push -u origin main
```

**Lessons Learned**:
1. Identify all dependencies before migration
2. Consider creating shared libraries as separate repositories
3. Update CI/CD pipelines before announcing the migration
4. Provide a transition period for developers to adapt

### Case Study 2: Repository Consolidation

**Scenario**: An organization needed to consolidate multiple small repositories into a monorepo structure while preserving history.

**Approach**:
1. Created a new empty repository for the monorepo
2. Extracted each source repository with its history
3. Imported each repository into a subdirectory of the monorepo
4. Updated build configurations for the new structure

**Challenges**:
- Some repositories had overlapping file paths
- Different repositories had different branching strategies
- Build systems needed significant reconfiguration

**Solution**:
```bash
# For each repository
for repo in repo1 repo2 repo3; do
    # Clone the repository
    git clone https://github.com/org/$repo.git
    cd $repo
    
    # Extract with history, moving to a subdirectory
    git filter-repo --path-rename :$repo/
    
    # Go to the monorepo
    cd ../monorepo
    
    # Add the repository as a remote
    git remote add $repo ../$repo
    git fetch $repo
    
    # Merge the repository
    git merge --allow-unrelated-histories $repo/main
    
    # Remove the remote
    git remote remove $repo
    
    # Go back to the parent directory
    cd ..
done
```

**Lessons Learned**:
1. Plan the monorepo structure carefully before migration
2. Standardize branching strategies across teams
3. Create a comprehensive migration plan with team input
4. Invest time in updating build configurations
5. Provide training for teams unfamiliar with monorepo workflows

### Case Study 3: Legacy Code Migration

**Scenario**: A team needed to migrate legacy code from an old TFS repository to Azure DevOps while preserving history.

**Approach**:
1. Used git-tfs to clone the TFS repository with history
2. Extracted the relevant folders with git filter-repo
3. Pushed the extracted code to Azure DevOps
4. Set up new build pipelines in Azure DevOps

**Challenges**:
- The TFS repository had a complex branching structure
- Some binary files had excessive history
- Author information needed normalization

**Solution**:
```bash
# Clone the TFS repository with git-tfs
git tfs clone http://tfs:8080/tfs/Collection $/Project/Path

# Normalize author information
cat > mailmap.txt << EOF
New Name <new.email@example.com> <old.email@example.com>
New Name <new.email@example.com> Old Name <old.email@example.com>
EOF

# Extract the relevant folders with normalized authors
git filter-repo --path folder1/ --path folder2/ --mailmap mailmap.txt

# Remove large binary files
git filter-repo --strip-blobs-bigger-than 10M

# Push to Azure DevOps
git remote add origin https://dev.azure.com/org/project/_git/new-repo
git push -u origin --all
```

**Lessons Learned**:
1. Clean up and normalize the repository before migration
2. Consider history depth requirements carefully
3. Test the migration process with a subset of the repository
4. Provide clear documentation for the new repository structure
5. Allow time for developers to adapt to the new system

## Tool Comparison Matrix

| Tool | Best For | Complexity | Performance | History Preservation | Limitations |
|------|----------|------------|-------------|---------------------|-------------|
| Git Filter-Repo | General-purpose history rewriting | Medium | Excellent | Excellent | Requires separate installation |
| Git Subtree | Simple folder extraction | Medium | Good | Good | Complex for multiple folders |
| Git Submodule | Linked repositories | High | N/A | N/A | Not a true migration solution |
| Git Filter-Branch | Legacy systems | High | Poor | Good | Slow, deprecated |
| BFG Repo Cleaner | Removing large files | Low | Excellent | Good | Limited to specific operations |
| Azure DevOps Migration Tools | Azure DevOps migrations | Medium | Good | Good | Azure DevOps specific |
| git-tfs | TFS to Git migrations | High | Moderate | Good | TFS specific |
| GitKraken | Visual management | Low | N/A | N/A | Limited automation |

## Additional Resources and References

### Official Documentation

- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- [Git Subtree Documentation](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging#_subtree_merge)
- [Git Submodule Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Azure DevOps Migration Guide](https://docs.microsoft.com/en-us/azure/devops/migrate/migration-overview)

### Books and Articles

- "Pro Git" by Scott Chacon and Ben Straub
- "Git Internals" by Scott Chacon
- "Monorepo vs. Multi-Repo: Pros and Cons"
- "Effective Git History Management"

### Community Resources

- Stack Overflow: [git-filter-repo](https://stackoverflow.com/questions/tagged/git-filter-repo)
- GitHub: [git-filter-repo Issues](https://github.com/newren/git-filter-repo/issues)
- Azure DevOps Community: [Migration Forum](https://developercommunity.visualstudio.com/VisualStudio)

## Next Steps

After reviewing these best practices and case studies, proceed to [Migration Templates and Checklists](./wiki-10-templates-checklists.md) for ready-to-use templates and comprehensive checklists to guide your migration process.

## See Also

- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Importing into the Destination Repository](./wiki-05-importing-destination.md)
- [Advanced Scenarios and Troubleshooting](./wiki-08-advanced-scenarios.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)

## Glossary

- **Monorepo**: A software development strategy where code for many projects is stored in the same repository
- **Multi-repo**: A strategy where different projects are stored in separate repositories
- **Mailmap**: A file that maps incorrect author information to correct information
- **TFS**: Team Foundation Server, Microsoft's legacy source control and project management system
- **Atomic Commit**: A commit that represents a single logical change to the codebase
