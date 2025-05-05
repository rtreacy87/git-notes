# Automation Options

## Overview

For organizations that need to perform multiple folder migrations or want to standardize the migration process, automation can significantly improve efficiency and reduce errors. This guide covers various approaches to automating the folder migration process, from simple scripts to complex CI/CD pipelines.

## Creating PowerShell Scripts for Repeatable Migrations

PowerShell provides a powerful scripting environment for automating Git operations on Windows and cross-platform environments.

### Basic Migration Script

Here's a sample PowerShell script that automates the basic folder migration process:

```powershell
# migration.ps1
param (
    [Parameter(Mandatory=$true)]
    [string]$SourceRepoUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$DestRepoUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$FolderPath,
    
    [Parameter(Mandatory=$false)]
    [string]$TargetPath = "./",
    
    [Parameter(Mandatory=$false)]
    [switch]$PreserveHistory = $true
)

# Create working directory
$workDir = "migration-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
New-Item -ItemType Directory -Path $workDir | Out-Null
Set-Location $workDir

Write-Host "Step 1: Cloning source repository..." -ForegroundColor Green
git clone $SourceRepoUrl source-repo
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to clone source repository"
    exit 1
}

Write-Host "Step 2: Extracting folder with history..." -ForegroundColor Green
Set-Location source-repo
if ($PreserveHistory) {
    # Check if git-filter-repo is installed
    $filterRepoInstalled = $null -ne (Get-Command git-filter-repo -ErrorAction SilentlyContinue)
    if (-not $filterRepoInstalled) {
        Write-Error "git-filter-repo is not installed. Please install it first."
        exit 1
    }
    
    # Extract folder with history
    if ($TargetPath -eq "./") {
        git filter-repo --path "$FolderPath/" --path-rename "$FolderPath/:$TargetPath"
    } else {
        git filter-repo --path "$FolderPath/"
    }
} else {
    # Simple copy without history
    New-Item -ItemType Directory -Path "../extracted-folder" -Force | Out-Null
    Copy-Item -Path $FolderPath -Destination "../extracted-folder" -Recurse
    Set-Location "../extracted-folder"
    git init
    git add .
    git commit -m "Initial commit of extracted folder"
}

Write-Host "Step 3: Cloning destination repository..." -ForegroundColor Green
Set-Location ..
git clone $DestRepoUrl dest-repo
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to clone destination repository"
    exit 1
}

Write-Host "Step 4: Importing folder into destination repository..." -ForegroundColor Green
Set-Location dest-repo
git remote add extracted-folder "../source-repo"
git fetch extracted-folder

# Create a branch for the import
$branchName = "import-$($FolderPath.Replace('/', '-'))-$(Get-Date -Format 'yyyyMMdd')"
git checkout -b $branchName

if ($TargetPath -ne "./") {
    # Create target directory if it doesn't exist
    if (-not (Test-Path $TargetPath)) {
        New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    }
    
    # Use read-tree to place the folder in the target location
    git read-tree --prefix="$TargetPath" -u extracted-folder/main
    git commit -m "Import $FolderPath from source repository with history"
} else {
    # Merge the extracted repository
    git merge --allow-unrelated-histories extracted-folder/main
}

Write-Host "Step 5: Push changes to destination repository..." -ForegroundColor Green
Write-Host "Changes are ready to be pushed. Review and then run:" -ForegroundColor Yellow
Write-Host "cd $workDir/dest-repo" -ForegroundColor Yellow
Write-Host "git push origin $branchName" -ForegroundColor Yellow

Write-Host "Migration completed successfully!" -ForegroundColor Green
```

### Usage Example

```powershell
# Run the script with parameters
.\migration.ps1 -SourceRepoUrl "https://github.com/org/source-repo.git" `
                -DestRepoUrl "https://github.com/org/dest-repo.git" `
                -FolderPath "src/components/feature" `
                -TargetPath "components/imported-feature"
```

## Using Azure DevOps Pipelines for Automated Migrations

For organizations using Azure DevOps, pipelines can automate the migration process with better integration and logging.

### Sample Azure DevOps Pipeline YAML

```yaml
# azure-pipelines.yml
trigger: none  # Manual trigger only

parameters:
  - name: sourceRepoUrl
    type: string
    displayName: 'Source Repository URL'
  - name: destRepoUrl
    type: string
    displayName: 'Destination Repository URL'
  - name: folderPath
    type: string
    displayName: 'Folder Path to Migrate'
  - name: targetPath
    type: string
    displayName: 'Target Path in Destination Repo'
    defaultValue: './'

pool:
  vmImage: 'ubuntu-latest'

steps:
- checkout: none

- script: |
    # Install git-filter-repo
    pip install git-filter-repo
  displayName: 'Install git-filter-repo'

- script: |
    # Configure Git
    git config --global user.name "Azure DevOps Migration"
    git config --global user.email "migration@example.com"
    
    # Clone source repository
    git clone $(sourceRepoUrl) source-repo
    cd source-repo
    
    # Extract folder with history
    if [ "$(targetPath)" = "./" ]; then
      git filter-repo --path "$(folderPath)/" --path-rename "$(folderPath)/:$(targetPath)"
    else
      git filter-repo --path "$(folderPath)/"
    fi
    
    cd ..
    
    # Clone destination repository
    git clone $(destRepoUrl) dest-repo
    cd dest-repo
    
    # Create branch for import
    BRANCH_NAME="import-$(echo $(folderPath) | tr '/' '-')-$(date +%Y%m%d)"
    git checkout -b $BRANCH_NAME
    
    # Add source as remote and fetch
    git remote add extracted-folder "../source-repo"
    git fetch extracted-folder
    
    if [ "$(targetPath)" != "./" ]; then
      # Create target directory if needed
      mkdir -p "$(targetPath)"
      
      # Use read-tree to place the folder in the target location
      git read-tree --prefix="$(targetPath)" -u extracted-folder/main
      git commit -m "Import $(folderPath) from source repository with history"
    else
      # Merge the extracted repository
      git merge --allow-unrelated-histories extracted-folder/main
    fi
    
    # Push changes
    git push origin $BRANCH_NAME
    
    echo "##vso[task.setvariable variable=branchName;isOutput=true]$BRANCH_NAME"
  displayName: 'Migrate Folder with History'
  name: migration

- script: |
    echo "Migration completed successfully!"
    echo "Changes pushed to branch: $(migration.branchName)"
    echo "Create a pull request to merge these changes into the main branch."
  displayName: 'Migration Summary'
```

### Pipeline Execution

1. Navigate to your Azure DevOps project
2. Go to Pipelines and create a new pipeline
3. Select "Azure Repos Git" as the source
4. Select your repository
5. Choose "Existing Azure Pipelines YAML file"
6. Select the path to your YAML file
7. Run the pipeline with the required parameters

## Sample Automation Scripts for Common Scenarios

### Scenario 1: Migrating Multiple Folders

```bash
#!/bin/bash
# migrate_multiple_folders.sh

SOURCE_REPO=$1
DEST_REPO=$2
FOLDERS_FILE=$3  # File containing list of folders to migrate

# Clone repositories
git clone $SOURCE_REPO source-repo
git clone $DEST_REPO dest-repo

# Read folders from file
while IFS=, read -r folder target
do
    echo "Migrating folder: $folder to $target"
    
    # Create a temporary directory for this folder
    mkdir -p "temp-$folder"
    cd "temp-$folder"
    
    # Clone source again for this specific folder
    git clone ../source-repo .
    
    # Extract folder with history
    git filter-repo --path "$folder/" --path-rename "$folder/:/"
    
    # Go to destination repo
    cd ../dest-repo
    
    # Create a branch for this import
    BRANCH_NAME="import-$(echo $folder | tr '/' '-')-$(date +%Y%m%d)"
    git checkout -b $BRANCH_NAME
    
    # Add the extracted repo as a remote
    git remote add "extracted-$folder" "../temp-$folder"
    git fetch "extracted-$folder"
    
    # Create target directory if needed
    mkdir -p "$target"
    
    # Import the folder
    git read-tree --prefix="$target" -u "extracted-$folder/main"
    git commit -m "Import $folder to $target with history"
    
    # Push the branch
    git push origin $BRANCH_NAME
    
    # Return to the main directory
    cd ..
    
    echo "Completed migration of $folder to $target"
done < "$FOLDERS_FILE"

echo "All migrations completed!"
```

Usage:
```bash
# Create a CSV file with source and target paths
echo "src/components/feature1,components/feature1" > folders.csv
echo "src/utils/common,utils/imported" >> folders.csv

# Run the script
./migrate_multiple_folders.sh https://github.com/org/source-repo.git https://github.com/org/dest-repo.git folders.csv
```

### Scenario 2: Scheduled Migration with Notifications

```powershell
# scheduled_migration.ps1

param (
    [string]$ConfigFile = "migration-config.json"
)

# Load configuration
$config = Get-Content -Path $ConfigFile | ConvertFrom-Json

# Set up logging
$logFile = "migration-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
Start-Transcript -Path $logFile

try {
    Write-Host "Starting scheduled migration at $(Get-Date)" -ForegroundColor Green
    
    # Run the migration for each configured folder
    foreach ($migration in $config.migrations) {
        Write-Host "Migrating $($migration.folderPath) to $($migration.targetPath)" -ForegroundColor Cyan
        
        # Call the main migration script
        & .\migration.ps1 -SourceRepoUrl $config.sourceRepoUrl `
                          -DestRepoUrl $config.destRepoUrl `
                          -FolderPath $migration.folderPath `
                          -TargetPath $migration.targetPath
        
        if ($LASTEXITCODE -ne 0) {
            throw "Migration failed for $($migration.folderPath)"
        }
    }
    
    # Send success notification
    if ($config.notifications.enabled) {
        $body = "Migration completed successfully at $(Get-Date)`n`nDetails:`n"
        foreach ($migration in $config.migrations) {
            $body += "- $($migration.folderPath) to $($migration.targetPath)`n"
        }
        
        Send-MailMessage -From $config.notifications.from `
                         -To $config.notifications.to `
                         -Subject "Folder Migration Completed" `
                         -Body $body `
                         -SmtpServer $config.notifications.smtpServer
    }
    
    Write-Host "Migration completed successfully!" -ForegroundColor Green
}
catch {
    Write-Error "Migration failed: $_"
    
    # Send failure notification
    if ($config.notifications.enabled) {
        $body = "Migration failed at $(Get-Date)`n`nError: $_`n`nSee log file for details: $logFile"
        
        Send-MailMessage -From $config.notifications.from `
                         -To $config.notifications.to `
                         -Subject "Folder Migration Failed" `
                         -Body $body `
                         -SmtpServer $config.notifications.smtpServer
    }
    
    exit 1
}
finally {
    Stop-Transcript
}
```

Configuration file (migration-config.json):
```json
{
  "sourceRepoUrl": "https://github.com/org/source-repo.git",
  "destRepoUrl": "https://github.com/org/dest-repo.git",
  "migrations": [
    {
      "folderPath": "src/components/feature1",
      "targetPath": "components/feature1"
    },
    {
      "folderPath": "src/utils/common",
      "targetPath": "utils/imported"
    }
  ],
  "notifications": {
    "enabled": true,
    "from": "migrations@example.com",
    "to": ["team@example.com"],
    "smtpServer": "smtp.example.com"
  }
}
```

## CI/CD Integration for Migration Validation

To ensure migrations are validated properly, you can integrate validation steps into your CI/CD pipeline:

```yaml
# validation-pipeline.yml
trigger:
  branches:
    include:
    - 'import-*'  # Only run on import branches

pool:
  vmImage: 'ubuntu-latest'

steps:
- checkout: self

- script: |
    # Identify imported folder(s)
    BRANCH_NAME=$(git branch --show-current)
    IMPORTED_FOLDER=$(echo $BRANCH_NAME | sed 's/import-//' | sed 's/-[0-9]\{8\}$//' | tr '-' '/')
    
    echo "Validating imported folder: $IMPORTED_FOLDER"
    
    # Run tests if they exist
    if [ -d "$IMPORTED_FOLDER/tests" ]; then
      cd $IMPORTED_FOLDER/tests
      echo "Running tests in $IMPORTED_FOLDER/tests"
      # Run appropriate test command based on the project
      if [ -f "package.json" ]; then
        npm test
      elif [ -f "pom.xml" ]; then
        mvn test
      elif [ -f "build.gradle" ]; then
        ./gradlew test
      else
        echo "No recognized test framework found"
      fi
    fi
    
    # Validate file integrity
    echo "Validating file integrity..."
    find $IMPORTED_FOLDER -type f -name "*.java" -o -name "*.js" -o -name "*.cs" | xargs -I{} sh -c 'echo "Checking {}"; cat {} | grep -v "^$" > /dev/null || echo "Empty file: {}"'
    
    # Check for broken references
    echo "Checking for broken references..."
    grep -r "import " $IMPORTED_FOLDER --include="*.java" | grep -v "java\." | cut -d" " -f2 | sort | uniq > imports.txt
    while read import; do
      class=$(echo $import | tr '.' '/' | sed 's/;$//')
      if [ ! -f "$class.java" ] && [ ! -f "$class.class" ]; then
        echo "Potential broken reference: $import"
      fi
    done < imports.txt
    
    echo "Validation completed"
  displayName: 'Validate Imported Folder'

- script: |
    # Generate validation report
    echo "# Migration Validation Report" > validation-report.md
    echo "## Imported Folder" >> validation-report.md
    BRANCH_NAME=$(git branch --show-current)
    IMPORTED_FOLDER=$(echo $BRANCH_NAME | sed 's/import-//' | sed 's/-[0-9]\{8\}$//' | tr '-' '/')
    echo "Folder: $IMPORTED_FOLDER" >> validation-report.md
    
    echo "## File Statistics" >> validation-report.md
    echo "Total files: $(find $IMPORTED_FOLDER -type f | wc -l)" >> validation-report.md
    echo "Java files: $(find $IMPORTED_FOLDER -name "*.java" | wc -l)" >> validation-report.md
    echo "JavaScript files: $(find $IMPORTED_FOLDER -name "*.js" | wc -l)" >> validation-report.md
    echo "XML files: $(find $IMPORTED_FOLDER -name "*.xml" | wc -l)" >> validation-report.md
    
    echo "## Commit History" >> validation-report.md
    echo "Total commits: $(git log --oneline -- $IMPORTED_FOLDER | wc -l)" >> validation-report.md
    echo "Authors: $(git log --format='%an' -- $IMPORTED_FOLDER | sort | uniq | wc -l)" >> validation-report.md
    
    echo "## Validation Results" >> validation-report.md
    echo "See build logs for detailed validation results." >> validation-report.md
    
    # Publish the report as an artifact
    mkdir -p $(Build.ArtifactStagingDirectory)/reports
    cp validation-report.md $(Build.ArtifactStagingDirectory)/reports/
  displayName: 'Generate Validation Report'

- task: PublishBuildArtifacts@1
  inputs:
    pathtoPublish: '$(Build.ArtifactStagingDirectory)/reports'
    artifactName: 'ValidationReports'
  displayName: 'Publish Validation Report'
```

## Error Handling and Reporting in Automated Migrations

Robust error handling is crucial for automated migrations. Here's a sample bash script with comprehensive error handling:

```bash
#!/bin/bash
# robust_migration.sh

set -e  # Exit immediately if a command fails

# Configuration
SOURCE_REPO=$1
DEST_REPO=$2
FOLDER_PATH=$3
TARGET_PATH=$4
LOG_FILE="migration-$(date +%Y%m%d-%H%M%S).log"
ERROR_FILE="migration-errors-$(date +%Y%m%d-%H%M%S).log"

# Function to log messages
log() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

# Function to log errors
log_error() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERROR: $1" | tee -a "$LOG_FILE" "$ERROR_FILE"
}

# Function to clean up on exit
cleanup() {
    log "Cleaning up temporary files and directories..."
    if [ -d "source-repo" ]; then
        rm -rf source-repo
    fi
    if [ -d "extracted-repo" ]; then
        rm -rf extracted-repo
    fi
    if [ -d "dest-repo" ]; then
        rm -rf dest-repo
    fi
    log "Cleanup completed"
}

# Set up trap for cleanup on exit
trap cleanup EXIT

# Main migration process
main() {
    log "Starting migration of $FOLDER_PATH to $TARGET_PATH"
    
    # Validate inputs
    if [ -z "$SOURCE_REPO" ] || [ -z "$DEST_REPO" ] || [ -z "$FOLDER_PATH" ]; then
        log_error "Missing required parameters"
        exit 1
    fi
    
    # Set default target path if not provided
    if [ -z "$TARGET_PATH" ]; then
        TARGET_PATH="./"
        log "No target path specified, using root directory"
    fi
    
    # Check for git-filter-repo
    if ! command -v git-filter-repo &> /dev/null; then
        log_error "git-filter-repo is not installed"
        log "Please install git-filter-repo: pip install git-filter-repo"
        exit 1
    fi
    
    # Step 1: Clone source repository
    log "Cloning source repository..."
    if ! git clone "$SOURCE_REPO" source-repo; then
        log_error "Failed to clone source repository: $SOURCE_REPO"
        exit 1
    fi
    
    # Step 2: Verify folder exists
    cd source-repo
    if [ ! -d "$FOLDER_PATH" ]; then
        log_error "Folder does not exist in source repository: $FOLDER_PATH"
        exit 1
    fi
    
    # Step 3: Extract folder with history
    log "Extracting folder with history..."
    if [ "$TARGET_PATH" = "./" ]; then
        if ! git filter-repo --path "$FOLDER_PATH/" --path-rename "$FOLDER_PATH/:./" --force; then
            log_error "Failed to extract folder with git filter-repo"
            exit 1
        fi
    else
        if ! git filter-repo --path "$FOLDER_PATH/" --force; then
            log_error "Failed to extract folder with git filter-repo"
            exit 1
        fi
    fi
    
    # Copy extracted repo to a separate directory
    cd ..
    cp -r source-repo extracted-repo
    
    # Step 4: Clone destination repository
    log "Cloning destination repository..."
    if ! git clone "$DEST_REPO" dest-repo; then
        log_error "Failed to clone destination repository: $DEST_REPO"
        exit 1
    fi
    
    # Step 5: Import folder into destination
    cd dest-repo
    BRANCH_NAME="import-$(echo $FOLDER_PATH | tr '/' '-')-$(date +%Y%m%d)"
    log "Creating branch: $BRANCH_NAME"
    if ! git checkout -b "$BRANCH_NAME"; then
        log_error "Failed to create branch in destination repository"
        exit 1
    fi
    
    log "Adding extracted folder as remote..."
    if ! git remote add extracted-folder "../extracted-repo"; then
        log_error "Failed to add extracted folder as remote"
        exit 1
    fi
    
    log "Fetching from extracted folder..."
    if ! git fetch extracted-folder; then
        log_error "Failed to fetch from extracted folder"
        exit 1
    fi
    
    if [ "$TARGET_PATH" != "./" ]; then
        log "Creating target directory: $TARGET_PATH"
        mkdir -p "$TARGET_PATH"
        
        log "Importing folder to target location..."
        if ! git read-tree --prefix="$TARGET_PATH" -u extracted-folder/main; then
            log_error "Failed to read-tree from extracted folder"
            exit 1
        fi
        
        log "Committing changes..."
        if ! git commit -m "Import $FOLDER_PATH from source repository with history"; then
            log_error "Failed to commit changes"
            exit 1
        fi
    else
        log "Merging extracted folder..."
        if ! git merge --allow-unrelated-histories extracted-folder/main; then
            log_error "Failed to merge extracted folder. There might be conflicts."
            log "Please resolve conflicts manually and commit the changes."
            exit 1
        fi
    fi
    
    # Step 6: Verify the import
    log "Verifying import..."
    if [ "$TARGET_PATH" = "./" ]; then
        VERIFY_PATH="."
    else
        VERIFY_PATH="$TARGET_PATH"
    fi
    
    FILE_COUNT=$(find "$VERIFY_PATH" -type f | wc -l)
    log "Files in imported folder: $FILE_COUNT"
    
    COMMIT_COUNT=$(git log --oneline -- "$VERIFY_PATH" | wc -l)
    log "Commits for imported folder: $COMMIT_COUNT"
    
    # Step 7: Push changes (optional)
    log "Changes are ready to be pushed."
    log "To push the changes, run: cd dest-repo && git push origin $BRANCH_NAME"
    
    log "Migration completed successfully!"
    return 0
}

# Run the main function and capture any errors
if ! main; then
    log_error "Migration failed. See error log for details: $ERROR_FILE"
    exit 1
fi
```

## Scheduling Considerations for Minimal Disruption

When scheduling automated migrations, consider these best practices:

1. **Off-peak Hours**: Schedule migrations during off-peak hours to minimize impact on developers
2. **Notification Windows**: Send notifications before and after migrations
3. **Gradual Approach**: For large repositories, consider migrating folders in batches
4. **Rollback Windows**: Allow time for validation and potential rollbacks
5. **Coordination with Releases**: Avoid scheduling migrations near release dates

### Sample Scheduling Script

```bash
#!/bin/bash
# scheduled_migration_runner.sh

# Configuration
CONFIG_FILE="migration_schedule.json"
LOCK_FILE="/tmp/migration.lock"
LOG_DIR="migration_logs"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Check if another migration is running
if [ -f "$LOCK_FILE" ]; then
    echo "Another migration is already running. Exiting."
    exit 1
fi

# Create lock file
touch "$LOCK_FILE"

# Function to remove lock file on exit
cleanup() {
    rm -f "$LOCK_FILE"
}

trap cleanup EXIT

# Load configuration
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Get current day of week (0-6, 0 is Sunday)
DAY_OF_WEEK=$(date +%w)

# Get current hour (0-23)
HOUR=$(date +%H)

# Parse configuration and find migrations scheduled for now
SCHEDULED_MIGRATIONS=$(jq -r ".migrations[] | select(.schedule.days[] | tonumber == $DAY_OF_WEEK) | select(.schedule.hour | tonumber == $HOUR)" "$CONFIG_FILE")

if [ -z "$SCHEDULED_MIGRATIONS" ]; then
    echo "No migrations scheduled for now."
    exit 0
fi

# Run each scheduled migration
echo "$SCHEDULED_MIGRATIONS" | jq -c '.' | while read -r migration; do
    SOURCE_REPO=$(echo "$migration" | jq -r '.sourceRepo')
    DEST_REPO=$(echo "$migration" | jq -r '.destRepo')
    FOLDER_PATH=$(echo "$migration" | jq -r '.folderPath')
    TARGET_PATH=$(echo "$migration" | jq -r '.targetPath')
    DESCRIPTION=$(echo "$migration" | jq -r '.description')
    
    echo "Running scheduled migration: $DESCRIPTION"
    echo "Migrating $FOLDER_PATH to $TARGET_PATH"
    
    LOG_FILE="$LOG_DIR/migration-$(date +%Y%m%d-%H%M%S).log"
    
    # Run the migration script
    ./robust_migration.sh "$SOURCE_REPO" "$DEST_REPO" "$FOLDER_PATH" "$TARGET_PATH" > "$LOG_FILE" 2>&1
    
    # Check result
    if [ $? -eq 0 ]; then
        echo "Migration completed successfully. Log: $LOG_FILE"
        
        # Send success notification if configured
        NOTIFY=$(echo "$migration" | jq -r '.notify')
        if [ "$NOTIFY" = "true" ]; then
            NOTIFY_EMAIL=$(echo "$migration" | jq -r '.notifyEmail')
            echo "Migration completed successfully: $DESCRIPTION" | mail -s "Migration Success" "$NOTIFY_EMAIL"
        fi
    else
        echo "Migration failed. Log: $LOG_FILE"
        
        # Send failure notification if configured
        NOTIFY=$(echo "$migration" | jq -r '.notify')
        if [ "$NOTIFY" = "true" ]; then
            NOTIFY_EMAIL=$(echo "$migration" | jq -r '.notifyEmail')
            echo "Migration failed: $DESCRIPTION. See log for details: $LOG_FILE" | mail -s "Migration Failed" "$NOTIFY_EMAIL"
        fi
    fi
done

echo "All scheduled migrations completed."
```

Configuration file (migration_schedule.json):
```json
{
  "migrations": [
    {
      "description": "Migrate UI components",
      "sourceRepo": "https://github.com/org/source-repo.git",
      "destRepo": "https://github.com/org/dest-repo.git",
      "folderPath": "src/components/ui",
      "targetPath": "ui/components",
      "schedule": {
        "days": [6],  // Saturday
        "hour": 2     // 2 AM
      },
      "notify": true,
      "notifyEmail": "team@example.com"
    },
    {
      "description": "Migrate utilities",
      "sourceRepo": "https://github.com/org/source-repo.git",
      "destRepo": "https://github.com/org/dest-repo.git",
      "folderPath": "src/utils",
      "targetPath": "common/utils",
      "schedule": {
        "days": [6],  // Saturday
        "hour": 3     // 3 AM
      },
      "notify": true,
      "notifyEmail": "team@example.com"
    }
  ]
}
```

## Next Steps

After setting up automation for your folder migrations, proceed to [Post-Migration Tasks](./wiki-07-post-migration-tasks.md) to learn about the steps needed to complete the migration process.

## See Also

- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Importing into the Destination Repository](./wiki-05-importing-destination.md)
- [Post-Migration Tasks](./wiki-07-post-migration-tasks.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)
- [Appendix C: Performance Optimization](./appendices/appendix-c-performance-optimization.md)

## Glossary

- **CI/CD**: Continuous Integration/Continuous Deployment, automated processes for building, testing, and deploying code
- **PowerShell**: A task automation and configuration management framework from Microsoft
- **Azure DevOps Pipeline**: A cloud service that provides CI/CD capabilities
- **Cron**: A time-based job scheduler in Unix-like operating systems
- **Task Scheduler**: A component of Windows that provides the ability to schedule the launch of programs or scripts
