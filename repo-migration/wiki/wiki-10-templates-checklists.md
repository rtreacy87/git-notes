# Migration Templates and Checklists

## Overview

This guide provides ready-to-use templates and comprehensive checklists for planning, executing, and verifying folder migrations with preserved history. These resources will help ensure your migrations are thorough, consistent, and successful.

## Pre-migration Assessment Checklist

Use this checklist to assess the migration requirements and readiness:

### Repository Assessment

- [ ] **Source Repository**
  - [ ] Identified the exact repository URL
  - [ ] Confirmed access permissions
  - [ ] Verified repository size and history depth
  - [ ] Checked for any branch policies or restrictions
  - [ ] Identified any large binary files or submodules

- [ ] **Destination Repository**
  - [ ] Identified the exact repository URL
  - [ ] Confirmed access permissions
  - [ ] Verified available space
  - [ ] Checked for any branch policies or restrictions
  - [ ] Determined if the repository is empty or contains existing code

### Folder Assessment

- [ ] **Source Folder**
  - [ ] Identified the exact path of the folder to migrate
  - [ ] Verified the folder exists in the source repository
  - [ ] Determined the size of the folder (files and history)
  - [ ] Identified any dependencies on other parts of the repository
  - [ ] Checked for any symbolic links or submodules within the folder

- [ ] **Target Location**
  - [ ] Determined the exact path in the destination repository
  - [ ] Checked for any naming conflicts with existing folders
  - [ ] Verified the path structure is appropriate for the project
  - [ ] Considered impact on existing code organization

### Technical Assessment

- [ ] **Tools and Environment**
  - [ ] Verified Git client version (2.24.0+ recommended)
  - [ ] Installed git-filter-repo
  - [ ] Checked available disk space for working directories
  - [ ] Verified network bandwidth for repository operations
  - [ ] Identified any proxy or firewall restrictions

- [ ] **Integration Points**
  - [ ] Identified all build pipelines referencing the folder
  - [ ] Listed all documentation referencing the folder
  - [ ] Determined impact on dependent projects
  - [ ] Checked for hardcoded paths in code or configuration

### Organizational Assessment

- [ ] **Stakeholders**
  - [ ] Identified all teams affected by the migration
  - [ ] Determined communication requirements
  - [ ] Scheduled the migration during a low-impact time
  - [ ] Obtained necessary approvals

- [ ] **Training and Support**
  - [ ] Assessed team familiarity with Git operations
  - [ ] Prepared guidance for developers after migration
  - [ ] Established support channels for post-migration issues

## Tool Selection Decision Tree

Use this decision tree to select the most appropriate migration tool:

```
Start
├── Is git-filter-repo available?
│   ├── Yes
│   │   ├── Is the folder structure complex?
│   │   │   ├── Yes → Use git-filter-repo with path-rename options
│   │   │   └── No → Use git-filter-repo with basic options
│   │   │
│   │   └── Is the repository very large (>1GB)?
│   │       ├── Yes → Use git-filter-repo with performance optimizations
│   │       └── No → Use git-filter-repo with default settings
│   │
│   └── No
│       ├── Can you install git-filter-repo?
│       │   ├── Yes → Install git-filter-repo and use it
│       │   └── No → Continue
│       │
│       ├── Is git subtree available?
│       │   ├── Yes → Use git subtree split
│       │   └── No → Continue
│       │
│       └── Is git filter-branch available?
│           ├── Yes → Use git filter-branch (with caution)
│           └── No → Consider manual copy without history
│
├── Is this a migration between different DevOps systems?
│   ├── Yes
│   │   ├── Azure DevOps involved?
│   │   │   ├── Yes → Consider Azure DevOps Migration Tools
│   │   │   └── No → Continue
│   │   │
│   │   └── TFS to Git migration?
│   │       ├── Yes → Consider git-tfs
│   │       └── No → Use git-filter-repo if available
│   │
│   └── No → Continue
│
├── Do you need to maintain a link to the original repository?
│   ├── Yes
│   │   ├── Need independent versioning?
│   │   │   ├── Yes → Use git submodule
│   │   │   └── No → Use git subtree
│   │   │
│   │   └── Continue
│   │
│   └── No → Use git-filter-repo if available
│
└── End
```

## Step-by-step Migration Procedure Templates

### Basic Folder Migration Procedure

```markdown
# Basic Folder Migration Procedure

## Prerequisites
- Git client installed (version 2.24.0+)
- git-filter-repo installed
- Access to both source and destination repositories
- Backups of both repositories

## Procedure

### 1. Prepare the Environment
```bash
# Create a working directory
mkdir migration-project
cd migration-project
```

### 2. Clone the Source Repository
```bash
# Clone the source repository
git clone https://source-repository-url.git source-repo
cd source-repo
```

### 3. Extract the Folder with History
```bash
# Extract the folder with its history
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./
```

### 4. Verify the Extraction
```bash
# Check the repository structure
ls -la

# Verify the commit history
git log
```

### 5. Clone the Destination Repository
```bash
# Go back to the working directory
cd ..

# Clone the destination repository
git clone https://destination-repository-url.git dest-repo
cd dest-repo
```

### 6. Create a Branch for the Import
```bash
# Create a new branch
git checkout -b import-folder-branch
```

### 7. Import the Extracted Folder
```bash
# Add the extracted repository as a remote
git remote add extracted-folder ../source-repo
git fetch extracted-folder

# Import the folder to the desired location
mkdir -p path/to/target/location
git read-tree --prefix=path/to/target/location -u extracted-folder/main
git commit -m "Import folder with history from source repository"
```

### 8. Verify the Import
```bash
# Check the repository structure
ls -la path/to/target/location

# Verify the commit history
git log -- path/to/target/location
```

### 9. Push the Changes
```bash
# Push the branch to the remote repository
git push -u origin import-folder-branch
```

### 10. Create a Pull Request
- Create a pull request through the web interface
- Add appropriate reviewers
- Include details about the migration in the description
```

### Advanced Migration Procedure with Conflict Resolution

```markdown
# Advanced Migration Procedure with Conflict Resolution

## Prerequisites
- Git client installed (version 2.24.0+)
- git-filter-repo installed
- Access to both source and destination repositories
- Backups of both repositories

## Procedure

### 1. Prepare the Environment
```bash
# Create a working directory
mkdir migration-project
cd migration-project

# Create a log directory
mkdir logs
```

### 2. Create Backups
```bash
# Create mirror clones of both repositories
git clone --mirror https://source-repository-url.git source-repo-backup.git
git clone --mirror https://destination-repository-url.git dest-repo-backup.git
```

### 3. Clone the Source Repository
```bash
# Clone the source repository
git clone https://source-repository-url.git source-repo
cd source-repo
```

### 4. Clean Up the Source Repository (Optional)
```bash
# Remove large binary files if needed
git filter-repo --strip-blobs-bigger-than 10M

# Normalize author information if needed
git filter-repo --mailmap ../mailmap.txt
```

### 5. Extract the Folder with History
```bash
# Extract the folder with its history
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./
```

### 6. Verify the Extraction
```bash
# Check the repository structure
ls -la

# Verify the commit history
git log > ../logs/extracted-history.log
```

### 7. Clone the Destination Repository
```bash
# Go back to the working directory
cd ..

# Clone the destination repository
git clone https://destination-repository-url.git dest-repo
cd dest-repo
```

### 8. Create a Branch for the Import
```bash
# Create a new branch
git checkout -b import-folder-branch
```

### 9. Prepare the Target Location
```bash
# Create the target directory if it doesn't exist
mkdir -p path/to/target/location

# If there are files that might conflict, move them temporarily
if [ -d "path/to/target/location" ]; then
    mkdir -p path/to/target/location.bak
    mv path/to/target/location/* path/to/target/location.bak/
    git add path/to/target/location.bak
    git commit -m "Temporarily move files to prepare for import"
fi
```

### 10. Import the Extracted Folder
```bash
# Add the extracted repository as a remote
git remote add extracted-folder ../source-repo
git fetch extracted-folder

# Try to import the folder
git read-tree --prefix=path/to/target/location -u extracted-folder/main
```

### 11. Handle Conflicts (If Any)
```bash
# If there are conflicts, the read-tree command will fail
# In that case, try a different approach

# Remove the remote
git remote remove extracted-folder

# Add the extracted repo as a remote again with a different name
git remote add extracted-source ../source-repo
git fetch extracted-source

# Try merging instead
git merge --allow-unrelated-histories extracted-source/main

# If there are merge conflicts, resolve them manually
git status
# Edit conflicted files as needed
git add .
git commit -m "Resolve conflicts in imported folder"
```

### 12. Restore Any Moved Files (If Applicable)
```bash
# If you moved files in step 9, restore them now
if [ -d "path/to/target/location.bak" ]; then
    # Copy files back, handling conflicts manually
    cp -n path/to/target/location.bak/* path/to/target/location/
    
    # Remove the backup
    rm -rf path/to/target/location.bak
    git add path/to/target/location
    git commit -m "Restore original files after import"
fi
```

### 13. Add Migration Documentation
```bash
# Create a migration note
echo "# Migration History\n\nThis folder was migrated from [source-repo] on $(date)." > path/to/target/location/MIGRATION.md
git add path/to/target/location/MIGRATION.md
git commit -m "Add migration documentation"
```

### 14. Verify the Import
```bash
# Check the repository structure
ls -la path/to/target/location

# Verify the commit history
git log -- path/to/target/location > ../logs/imported-history.log

# Compare the histories
cd ..
diff -u logs/extracted-history.log logs/imported-history.log
```

### 15. Push the Changes
```bash
# Go back to the destination repository
cd dest-repo

# Push the branch to the remote repository
git push -u origin import-folder-branch
```

### 16. Create a Pull Request
- Create a pull request through the web interface
- Add appropriate reviewers
- Include details about the migration in the description
- Attach the history logs for reference
```

## Post-migration Verification Checklist

Use this checklist to verify the migration was successful:

### Code Verification

- [ ] **File Completeness**
  - [ ] All files from the source folder are present in the destination
  - [ ] File content matches the original
  - [ ] File permissions are preserved (if relevant)
  - [ ] No unexpected files were included

- [ ] **History Verification**
  - [ ] Commit count matches expected number
  - [ ] Author information is preserved
  - [ ] Commit messages are intact
  - [ ] Commit dates are preserved
  - [ ] Merge commits are handled correctly

- [ ] **Structure Verification**
  - [ ] Folder is in the correct location in the destination repository
  - [ ] Path structure matches the planned structure
  - [ ] No naming conflicts with existing files/folders

### Functionality Verification

- [ ] **Build Verification**
  - [ ] Code builds successfully in the new location
  - [ ] All tests pass
  - [ ] CI/CD pipelines run successfully
  - [ ] No new warnings or errors are introduced

- [ ] **Integration Verification**
  - [ ] Code works correctly with other components
  - [ ] Dependencies are resolved correctly
  - [ ] No broken references to the old location
  - [ ] External systems can access the code as needed

### Documentation Verification

- [ ] **Internal Documentation**
  - [ ] Repository README is updated
  - [ ] Migration documentation is added
  - [ ] Code comments referencing paths are updated
  - [ ] Wiki pages are updated

- [ ] **External Documentation**
  - [ ] External documentation references are updated
  - [ ] Team documentation is updated
  - [ ] Knowledge base articles are updated
  - [ ] Training materials are updated

### Process Verification

- [ ] **Branch Policies**
  - [ ] All branch policies are re-enabled
  - [ ] Protection settings are restored
  - [ ] Code review requirements are in place
  - [ ] Build validation is working

- [ ] **Access Control**
  - [ ] Appropriate permissions are set on the new location
  - [ ] Security policies are applied
  - [ ] Audit logging is enabled
  - [ ] Sensitive information is properly protected

## Rollback Procedures and Contingency Planning

### Rollback Plan Template

```markdown
# Rollback Plan for Folder Migration

## Triggers for Rollback
- Critical functionality is broken
- Build pipelines consistently fail
- Data loss is discovered
- Security vulnerability is introduced
- Business decision to revert

## Pre-Rollback Assessment
1. Determine the scope of the rollback
   - Full rollback to pre-migration state
   - Partial rollback of specific components
   - Fix-forward approach for minor issues

2. Assess impact of rollback
   - Identify affected systems and users
   - Determine downtime requirements
   - Evaluate data synchronization needs

3. Prepare communication plan
   - Draft notifications for affected teams
   - Prepare status updates for stakeholders
   - Set up communication channels for the rollback process

## Rollback Procedure

### Option 1: Restore from Backup (Full Rollback)
```bash
# Navigate to the backup directory
cd path/to/backups

# Restore the source repository
cd source-repo-backup.git
git push --force https://source-repository-url.git --all
git push --force https://source-repository-url.git --tags

# Restore the destination repository
cd ../dest-repo-backup.git
git push --force https://destination-repository-url.git --all
git push --force https://destination-repository-url.git --tags
```

### Option 2: Revert the Import (Partial Rollback)
```bash
# Clone the destination repository
git clone https://destination-repository-url.git dest-repo
cd dest-repo

# Create a rollback branch
git checkout -b rollback-import

# Remove the imported folder
git rm -rf path/to/target/location
git commit -m "Rollback: Remove imported folder"

# If there was a previous version, restore it from before the import
git checkout main~1 -- path/to/target/location
git commit -m "Rollback: Restore previous version of folder"

# Push the rollback branch
git push origin rollback-import

# Create a pull request to merge the rollback
```

### Option 3: Fix Forward
```bash
# Clone the destination repository
git clone https://destination-repository-url.git dest-repo
cd dest-repo

# Create a fix branch
git checkout -b fix-import-issues

# Make necessary fixes
# ...

# Commit and push the fixes
git commit -m "Fix issues with imported folder"
git push origin fix-import-issues

# Create a pull request for the fixes
```

## Post-Rollback Verification
1. Verify repository state
   - Check that files are in the expected state
   - Verify history is intact

2. Verify functionality
   - Run build pipelines
   - Execute test suites
   - Perform manual testing of critical features

3. Verify integrations
   - Check dependent systems
   - Verify external references

## Communication
1. Notify all stakeholders of rollback completion
2. Provide status update on systems
3. Document the rollback process and reasons
4. Schedule follow-up meeting to discuss next steps
```

## Stakeholder Communication Templates

### Pre-Migration Announcement

```markdown
# Upcoming Folder Migration: [Folder Name]

## What's Changing
We will be migrating the folder `[path/to/folder]` from `[source-repo]` to `[destination-repo]` on **[planned date]**.

## Why We're Making This Change
[Explain the business or technical reasons for the migration]

## Impact on Your Work
- During the migration window (**[start time]** to **[end time]**), please avoid making changes to the folder or its contents
- After migration, you will need to update your local repositories
- References to the old location will need to be updated

## What You Need to Do
### Before the Migration
- Complete and commit any work in progress on this folder by **[deadline]**
- Notify the migration team of any concerns or special requirements

### After the Migration
- Pull the latest changes from both repositories
- Update any local references to the folder
- Test your workflows with the new location

## Migration Timeline
- **[date]**: Pre-migration testing
- **[date]**: Migration execution
- **[date]**: Post-migration verification
- **[date]**: Transition period ends (old location will be removed)

## Questions or Concerns?
Please contact [contact person] at [email/chat] if you have any questions or concerns about this migration.

## Additional Resources
- [Link to detailed migration plan]
- [Link to FAQ document]
- [Link to training materials]
```

### Migration Completion Announcement

```markdown
# Folder Migration Completed: [Folder Name]

## Migration Status
The migration of `[path/to/folder]` from `[source-repo]` to `[destination-repo]` has been successfully completed.

## New Location
The folder is now available at:
- Repository: `[destination-repo-url]`
- Path: `[path/to/target/location]`

## What Has Changed
- The folder and all its contents have been moved to the new location
- The complete commit history has been preserved
- Build pipelines have been updated to reference the new location
- Documentation has been updated

## What You Need to Do Now
1. Pull the latest changes from both repositories:
   ```bash
   # For the source repository
   cd path/to/source-repo
   git pull

   # For the destination repository
   cd path/to/destination-repo
   git pull
   ```

2. Update any local references to the folder
3. Test your workflows with the new location
4. Report any issues to [contact person]

## Transition Period
The original folder will remain in the source repository until **[end date]** to allow for a smooth transition. After this date, it will be removed.

## Known Issues
[List any known issues or limitations]

## Questions or Issues?
Please contact [contact person] at [email/chat] if you encounter any issues or have questions about the migration.

## Additional Resources
- [Link to updated documentation]
- [Link to FAQ document]
- [Link to support resources]
```

## Next Steps

After using these templates and checklists for your migration, refer to the appendices for detailed reference information:

- [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)
- [Appendix C: Performance Optimization](./appendices/appendix-c-performance-optimization.md)
- [Appendix D: Security Considerations](./appendices/appendix-d-security-considerations.md)
- [Appendix E: Glossary and Reference](./appendices/appendix-e-glossary-reference.md)

## See Also

- [Introduction and Prerequisites](./wiki-01-introduction-prerequisites.md)
- [Best Practices and Case Studies](./wiki-09-best-practices.md)
- [Post-Migration Tasks](./wiki-07-post-migration-tasks.md)

## Glossary

- **Rollback**: The process of reverting to a previous state after a failed migration
- **Contingency Plan**: A plan designed to take a course of action if an expected outcome fails to materialize
- **Stakeholder**: Anyone who is affected by or has an interest in the migration
- **Verification**: The process of confirming that the migration was successful and meets requirements
- **Transition Period**: A period during which both the old and new locations are maintained to allow for adaptation
