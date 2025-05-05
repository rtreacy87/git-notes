# Preparation Steps

## Overview

Proper preparation is critical for a successful folder migration with preserved history. This guide outlines the essential steps to take before beginning the actual migration process, ensuring you have everything in place for a smooth transition.

## Creating Backups

Before making any changes, create comprehensive backups of both repositories to ensure you can recover if anything goes wrong.

```bash
# Create a mirror clone of the source repository (includes all branches and tags)
git clone --mirror https://source-repository-url.git source-repo-backup
cd source-repo-backup
# Verify the backup
git show-ref | wc -l  # Should show the number of refs (branches/tags)

# Create a mirror clone of the destination repository
cd ..
git clone --mirror https://destination-repository-url.git destination-repo-backup
cd destination-repo-backup
# Verify the backup
git show-ref | wc -l
```

### Backup Verification

Always verify your backups before proceeding:

```bash
# Test that you can push the backup (don't actually push)
cd source-repo-backup
git push --dry-run

# Test that you can restore from the backup (in a temporary location)
cd /tmp
git clone source-repo-backup test-restore
cd test-restore
git log  # Verify history is present
```

## Setting Up Local Clones

Create working clones of both repositories for the migration process:

```bash
# Clone the source repository
git clone https://source-repository-url.git source-repo-working
cd source-repo-working

# Ensure you have all branches
git fetch --all

# Clone the destination repository
cd ..
git clone https://destination-repository-url.git destination-repo-working
cd destination-repo-working

# Ensure you have all branches
git fetch --all
```

## Configuring Git Credentials

Ensure your Git credentials are properly configured for both repositories:

```bash
# Configure user information if needed
git config user.name "Your Name"
git config user.email "your.email@example.com"

# For HTTPS repositories, configure credential storage to avoid repeated password prompts
git config credential.helper store  # Stores credentials indefinitely
# OR
git config credential.helper 'cache --timeout=3600'  # Stores credentials for 1 hour

# For SSH repositories, verify your SSH key is working
ssh -T git@github.com  # For GitHub
ssh -T git@ssh.dev.azure.com  # For Azure DevOps
```

### Credential Verification

Test your credentials by performing a simple operation:

```bash
# Test credentials for source repository
cd source-repo-working
git pull

# Test credentials for destination repository
cd ../destination-repo-working
git pull
```

## Identifying the Folder to Be Moved

Clearly identify the folder you want to move and understand its structure:

```bash
# Navigate to the source repository
cd source-repo-working

# List the folder contents
ls -la path/to/folder

# Check the folder's history
git log --follow -- path/to/folder

# Identify any dependencies or references to this folder from other parts of the codebase
grep -r "path/to/folder" --include="*.{extension}" .
```

### Important Considerations

1. **Folder Path**: Note the exact path of the folder relative to the repository root
2. **Dependencies**: Identify any code that depends on the folder you're moving
3. **Size and Complexity**: Assess the folder's size and history complexity
   ```bash
   # Count files in the folder
   find path/to/folder -type f | wc -l
   
   # Check the size of the folder
   du -sh path/to/folder
   
   # Count commits affecting the folder
   git log --oneline -- path/to/folder | wc -l
   ```

## Planning the Target Location

Determine where the folder will be placed in the destination repository:

```bash
# Navigate to the destination repository
cd destination-repo-working

# Check if the target path already exists
ls -la intended/target/path

# If it exists, check its contents and history
git log -- intended/target/path
```

### Considerations for Target Location

1. **Naming Conflicts**: Ensure there are no naming conflicts with existing folders
2. **Path Structure**: Decide whether to maintain the original path structure or use a new one
3. **Integration**: Consider how the moved folder will integrate with existing code

## Temporarily Disabling Branch Policies

If necessary, temporarily disable branch policies that might prevent the migration:

### Azure DevOps CLI (Recommended)

```bash
# Install Azure DevOps CLI extension if not already installed
az extension add --name azure-devops

# List branch policies
az repos policy list --repository-id <repository-id> --branch <branch-name> --org <organization-url> --project <project-name>

# Disable a specific policy (note the policy ID from the list command)
az repos policy update --policy-id <policy-id> --status disabled --org <organization-url> --project <project-name>
```

### Important Notes on Branch Policies

1. **Document Current Settings**: Before disabling any policies, document their current settings so you can restore them later
2. **Minimum Changes**: Only disable policies that would directly interfere with the migration
3. **Security Implications**: Be aware of the security implications of disabling policies
4. **Coordination**: Coordinate with your team to ensure no one pushes to the affected branches during the migration

## Tool Selection Guide

Based on your specific scenario, select the appropriate migration approach:

| Scenario | Recommended Tool | Alternative Tool |
|----------|------------------|------------------|
| Simple folder extraction with history | Git Filter-Repo | Git Subtree Split |
| Large repository with extensive history | Git Filter-Repo | Custom script with Git Plumbing |
| Folder with complex dependencies | Git Filter-Repo with path-rename | RepoSurgeonTools |
| Moving folder to existing repository | Git Filter-Repo + manual merge | Azure DevOps Migration Tools |
| Need to maintain link to original repo | Git Submodule | Git Subtree |

For detailed information on each tool, refer to [External Tools for Repository Migration](./wiki-02-external-tools.md).

## Pre-Migration Checklist

Before proceeding with the migration, verify that you have:

- [ ] Created and verified backups of both repositories
- [ ] Set up working clones of both repositories
- [ ] Configured and tested Git credentials
- [ ] Identified the exact folder to be moved and its dependencies
- [ ] Planned the target location in the destination repository
- [ ] Temporarily disabled any interfering branch policies
- [ ] Selected the appropriate migration tool
- [ ] Informed stakeholders about the planned migration
- [ ] Scheduled the migration during a low-activity period
- [ ] Prepared a rollback plan

## Next Steps

Once you have completed all preparation steps, proceed to [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md) to begin the actual migration process.

## See Also

- [External Tools for Repository Migration](./wiki-02-external-tools.md)
- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md)
- [Appendix D: Security Considerations](./appendices/appendix-d-security-considerations.md)

## Glossary

- **Mirror Clone**: A complete copy of a Git repository, including all references (branches, tags, etc.)
- **Branch Policy**: Rules that control how code can be committed to specific branches in a repository
- **Working Clone**: A standard Git clone used for development or, in this case, migration work
- **Credential Helper**: A Git feature that stores authentication credentials to avoid repeated prompts
