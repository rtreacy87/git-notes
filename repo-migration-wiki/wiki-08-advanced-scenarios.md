# Advanced Scenarios and Troubleshooting

## Overview

This guide covers advanced migration scenarios and troubleshooting techniques for complex situations that may arise during folder migrations. These approaches are designed for experienced Git users who need to handle challenging migration requirements or resolve issues that occur during the standard migration process.

## Moving Multiple Folders Simultaneously

When you need to move multiple folders while preserving their individual histories, you have several options.

### Approach 1: Sequential Extraction and Import

This approach processes each folder individually:

```bash
#!/bin/bash
# migrate_multiple_folders.sh

SOURCE_REPO=$1
DEST_REPO=$2
FOLDERS_FILE=$3  # CSV file with source_folder,target_folder

# Clone repositories
git clone $SOURCE_REPO source-repo
git clone $DEST_REPO dest-repo

# Create a branch in the destination repo
cd dest-repo
BRANCH_NAME="import-multiple-folders-$(date +%Y%m%d)"
git checkout -b $BRANCH_NAME
cd ..

# Process each folder
while IFS=, read -r source_folder target_folder
do
    echo "Processing folder: $source_folder -> $target_folder"
    
    # Clone source repo for this folder
    mkdir -p "temp-$source_folder"
    cd "temp-$source_folder"
    git clone ../source-repo .
    
    # Extract the folder with history
    git filter-repo --path "$source_folder/" --path-rename "$source_folder/:/"
    
    # Go to destination repo
    cd ../dest-repo
    
    # Create target directory if needed
    mkdir -p "$target_folder"
    
    # Add the extracted repo as a remote
    git remote add "extracted-$source_folder" "../temp-$source_folder"
    git fetch "extracted-$source_folder"
    
    # Import the folder
    git read-tree --prefix="$target_folder" -u "extracted-$source_folder/main"
    git commit -m "Import $source_folder to $target_folder with history"
    
    # Remove the remote
    git remote remove "extracted-$source_folder"
    
    # Go back to the main directory
    cd ..
    
    echo "Completed migration of $source_folder to $target_folder"
done < "$FOLDERS_FILE"

# Push the branch with all imported folders
cd dest-repo
git push origin $BRANCH_NAME

echo "All migrations completed!"
```

### Approach 2: Parallel Extraction with Final Merge

This approach extracts all folders in parallel and then merges them:

```bash
#!/bin/bash
# parallel_folder_migration.sh

SOURCE_REPO=$1
DEST_REPO=$2
FOLDERS_FILE=$3  # CSV file with source_folder,target_folder

# Clone source repository
git clone $SOURCE_REPO source-repo

# Process each folder in parallel
while IFS=, read -r source_folder target_folder
do
    echo "Extracting folder: $source_folder"
    
    # Create a directory for this folder
    mkdir -p "extracted-$source_folder"
    cd "extracted-$source_folder"
    
    # Clone source repo for this folder
    git clone ../source-repo .
    
    # Extract the folder with history
    git filter-repo --path "$source_folder/" --path-rename "$source_folder/:/"
    
    # Go back to the main directory
    cd ..
    
    echo "Extracted $source_folder"
done < "$FOLDERS_FILE" &

# Wait for all extractions to complete
wait

# Clone destination repository
git clone $DEST_REPO dest-repo
cd dest-repo

# Create a branch for the import
BRANCH_NAME="import-multiple-folders-$(date +%Y%m%d)"
git checkout -b $BRANCH_NAME

# Import each extracted folder
while IFS=, read -r source_folder target_folder
do
    echo "Importing folder: $source_folder -> $target_folder"
    
    # Create target directory if needed
    mkdir -p "$target_folder"
    
    # Add the extracted repo as a remote
    git remote add "extracted-$source_folder" "../extracted-$source_folder"
    git fetch "extracted-$source_folder"
    
    # Import the folder
    git read-tree --prefix="$target_folder" -u "extracted-$source_folder/main"
    git commit -m "Import $source_folder to $target_folder with history"
    
    # Remove the remote
    git remote remove "extracted-$source_folder"
    
    echo "Imported $source_folder to $target_folder"
done < "$FOLDERS_FILE"

# Push the branch with all imported folders
git push origin $BRANCH_NAME

echo "All migrations completed!"
```

## Handling Large Repositories or History

Large repositories with extensive history can present performance challenges during migration.

### Shallow Clone with History Depth

For very large repositories, you can use a shallow clone with a specific depth:

```bash
# Clone with limited history depth
git clone --depth 100 https://source-repository-url.git source-repo-shallow
cd source-repo-shallow

# Extract the folder with limited history
git filter-repo --path path/to/folder/
```

### Incremental Processing

For extremely large repositories, process the history in chunks:

```bash
#!/bin/bash
# incremental_migration.sh

SOURCE_REPO=$1
FOLDER_PATH=$2
CHUNK_SIZE=500  # Number of commits per chunk

# Clone source repository
git clone $SOURCE_REPO source-repo
cd source-repo

# Get total number of commits affecting the folder
TOTAL_COMMITS=$(git log --oneline -- $FOLDER_PATH | wc -l)
echo "Total commits affecting $FOLDER_PATH: $TOTAL_COMMITS"

# Calculate number of chunks
CHUNKS=$(( ($TOTAL_COMMITS + $CHUNK_SIZE - 1) / $CHUNK_SIZE ))
echo "Processing in $CHUNKS chunks of $CHUNK_SIZE commits each"

# Create a new repository for the result
mkdir -p ../result-repo
cd ../result-repo
git init

# Process each chunk
for (( i=0; i<$CHUNKS; i++ ))
do
    SKIP=$(( i * $CHUNK_SIZE ))
    TAKE=$CHUNK_SIZE
    
    echo "Processing chunk $((i+1))/$CHUNKS (commits $SKIP to $((SKIP+TAKE)))"
    
    # Create a temporary directory for this chunk
    mkdir -p ../chunk-$i
    cd ../chunk-$i
    
    # Clone source repo for this chunk
    git clone ../source-repo .
    
    # Get the commit range for this chunk
    START_COMMIT=$(git log --skip=$SKIP --max-count=1 --format=%H -- $FOLDER_PATH)
    END_COMMIT=$(git log --skip=$(($SKIP+$TAKE-1)) --max-count=1 --format=%H -- $FOLDER_PATH)
    
    # If we're at the end, use HEAD as the end commit
    if [ -z "$END_COMMIT" ]; then
        END_COMMIT="HEAD"
    fi
    
    echo "Commit range: $START_COMMIT to $END_COMMIT"
    
    # Extract the folder for this commit range
    git filter-repo --path $FOLDER_PATH/ --refs $START_COMMIT..$END_COMMIT
    
    # Go to the result repo
    cd ../result-repo
    
    # Add the chunk repo as a remote
    git remote add chunk-$i ../chunk-$i
    git fetch chunk-$i
    
    # Merge the chunk
    git merge --allow-unrelated-histories chunk-$i/main
    
    # Remove the remote
    git remote remove chunk-$i
    
    # Go back to the main directory
    cd ..
    
    # Clean up the chunk directory
    rm -rf chunk-$i
    
    echo "Completed chunk $((i+1))/$CHUNKS"
done

echo "Migration completed!"
```

### Using Sparse Checkout

For large repositories where you only need a specific folder:

```bash
# Initialize a new repository
mkdir extracted-folder
cd extracted-folder
git init

# Add the source repository as a remote
git remote add origin https://source-repository-url.git

# Configure sparse checkout
git config core.sparseCheckout true
echo "path/to/folder/" > .git/info/sparse-checkout

# Fetch the repository
git fetch origin

# Checkout the main branch
git checkout origin/main

# Now extract the folder with git filter-repo
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./
```

## Migrating Between Significantly Different DevOps Versions

When migrating between different versions of DevOps systems (e.g., from TFS to Azure DevOps), additional considerations are needed.

### Using Azure DevOps Migration Tools

For migrations between TFS and Azure DevOps:

```bash
# Install the migration tools
git clone https://github.com/nkdAgility/azure-devops-migration-tools.git
cd azure-devops-migration-tools

# Build the tools
dotnet build

# Create a configuration file for the migration
cat > migration-config.json << EOF
{
  "Version": "11.9",
  "TelemetryEnableTrace": true,
  "Source": {
    "Collection": {
      "Uri": "https://tfs.example.com/tfs/DefaultCollection"
    },
    "Project": "SourceProject"
  },
  "Target": {
    "Collection": {
      "Uri": "https://dev.azure.com/organization"
    },
    "Project": "TargetProject"
  },
  "Processors": [
    {
      "Enabled": true,
      "Processor": "GitRepositoryProcessor",
      "SourceName": "source-repo",
      "TargetName": "target-repo"
    }
  ]
}
EOF

# Run the migration
dotnet run -- execute --config migration-config.json

# After migration, extract the specific folder with git filter-repo
cd target-repo
git filter-repo --path path/to/folder/
```

### Manual Migration with Git

For a more manual approach:

```bash
# Clone the source repository
git clone https://tfs.example.com/tfs/DefaultCollection/SourceProject/_git/source-repo
cd source-repo

# Extract the folder with history
git filter-repo --path path/to/folder/

# Create a new repository in the target system (e.g., Azure DevOps)
# Then push to the new repository
git remote add target https://dev.azure.com/organization/TargetProject/_git/target-repo
git push -u target --all
git push -u target --tags
```

## Addressing Common Errors and Their Solutions

### Error: "fatal: not a git repository"

**Cause**: The command is being run outside a Git repository.

**Solution**:
```bash
# Ensure you're in the correct directory
cd path/to/git/repository

# Or initialize a new repository if needed
git init
```

### Error: "fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree"

**Cause**: The repository is empty or the specified reference doesn't exist.

**Solution**:
```bash
# Check if the repository has any commits
git log

# If empty, create an initial commit
touch README.md
git add README.md
git commit -m "Initial commit"
```

### Error: "fatal: refusing to merge unrelated histories"

**Cause**: Git is preventing the merge of repositories with no common history.

**Solution**:
```bash
# Use the --allow-unrelated-histories flag
git merge --allow-unrelated-histories extracted-folder/main
```

### Error: "fatal: path 'path/to/folder' does not exist in 'HEAD'"

**Cause**: The specified folder doesn't exist in the current branch.

**Solution**:
```bash
# Check if the folder exists
ls -la

# Check if the folder exists in any branch
git branch -a
git checkout branch-with-folder

# Or specify the correct path
git filter-repo --path correct/path/to/folder/
```

### Error: "fatal: destination path 'repo' already exists and is not an empty directory"

**Cause**: Git clone can't create a directory that already exists.

**Solution**:
```bash
# Remove or rename the existing directory
rm -rf repo
# Or
mv repo repo-old

# Then clone again
git clone https://repository-url.git repo
```

### Error: "fatal: cannot create directory at 'path/to/file': Permission denied"

**Cause**: Insufficient permissions to create directories.

**Solution**:
```bash
# Check and fix permissions
ls -la
chmod -R u+w .

# Or run the command with elevated privileges
sudo git clone https://repository-url.git
```

## Performance Considerations for Large Migrations

### Hardware Recommendations

For large migrations, consider these hardware specifications:

- **CPU**: 4+ cores for parallel processing
- **RAM**: 16GB+ to handle large repositories
- **Disk**: SSD with at least 10GB free space per GB of repository size
- **Network**: High-bandwidth connection for large repositories

### Optimizing Git Performance

```bash
# Increase Git's memory buffer
git config --global pack.windowMemory "100m"
git config --global pack.packSizeLimit "100m"
git config --global pack.threads "4"

# Use parallel operations where possible
git -c core.compression=0 clone --depth 1 https://repository-url.git

# Disable automatic garbage collection during the migration
git config --global gc.auto 0
```

### Using Specialized Tools for Complex Migrations

For the most complex migrations, consider specialized tools:

```bash
# Install git-filter-repo with additional dependencies
pip install git-filter-repo
pip install pygit2

# For extremely large repositories, use BFG Repo Cleaner
java -jar bfg.jar --strip-blobs-bigger-than 10M some-big-repo.git

# For complex history rewriting, use git-subtrac
npm install -g git-subtrac
git subtrac init
git subtrac extract path/to/folder/
```

## Next Steps

After addressing advanced scenarios and troubleshooting issues, proceed to [Best Practices and Case Studies](./wiki-09-best-practices.md) to learn from real-world migration experiences and best practices.

## See Also

- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Importing into the Destination Repository](./wiki-05-importing-destination.md)
- [Automation Options](./wiki-06-automation-options.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)
- [Appendix C: Performance Optimization](./appendices/appendix-c-performance-optimization.md)

## Glossary

- **Shallow Clone**: A Git clone with limited history depth
- **Sparse Checkout**: A Git feature that allows checking out only specific parts of a repository
- **BFG Repo Cleaner**: A tool for cleaning large or problematic Git repositories
- **Git Garbage Collection**: The process Git uses to optimize repository storage
- **Unrelated Histories**: Git repositories with no common ancestor commits
