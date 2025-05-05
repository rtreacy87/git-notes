# Post-Migration Tasks

## Overview

After successfully migrating a folder with its history from one repository to another, several important tasks must be completed to ensure the migration is fully integrated and operational. This guide covers the essential post-migration steps to finalize the process and ensure everything works correctly in the new location.

## Re-enabling Branch Policies

If you disabled branch policies before the migration, you should re-enable them now.

### Azure DevOps CLI (Recommended)

```bash
# Install Azure DevOps CLI extension if not already installed
az extension add --name azure-devops

# List branch policies to verify their current state
az repos policy list --repository-id <repository-id> --branch <branch-name> --org <organization-url> --project <project-name>

# Re-enable a specific policy (note the policy ID from the list command)
az repos policy update --policy-id <policy-id> --status active --org <organization-url> --project <project-name>
```

### Verification Steps

After re-enabling policies, verify they are working correctly:

```bash
# Make a small change to test the policies
cd destination-repo-working
git checkout -b policy-test-branch
echo "# Test file" > test-policy.md
git add test-policy.md
git commit -m "Test branch policies"
git push origin policy-test-branch

# Create a pull request through the web interface and verify policies are applied
```

## Updating Build Pipelines and References

### Identifying Affected Pipelines

First, identify all build pipelines that reference the moved folder:

```bash
# For Azure DevOps, list all pipelines
az pipelines list --org <organization-url> --project <project-name> -o table

# For each pipeline, check if it references the moved folder
az pipelines show --id <pipeline-id> --org <organization-url> --project <project-name>
```

### Updating Pipeline YAML Files

For YAML-based pipelines, update the file paths:

```bash
# Clone the repository containing pipeline definitions
git clone https://dev.azure.com/organization/project/_git/pipeline-repo
cd pipeline-repo

# Find all YAML files referencing the old path
grep -r "old/path/to/folder" --include="*.yml" .

# Update the files with the new path
sed -i 's|old/path/to/folder|new/path/to/folder|g' path/to/pipeline.yml

# Commit and push the changes
git add .
git commit -m "Update folder paths in pipeline definitions"
git push
```

### Updating Classic Pipelines

For classic (GUI-defined) pipelines:

1. Navigate to the pipeline in Azure DevOps
2. Select "Edit"
3. Update all references to the old folder path
4. Save the pipeline

### Verifying Pipeline Updates

After updating the pipelines:

```bash
# Manually trigger each updated pipeline to verify it works correctly
az pipelines run --id <pipeline-id> --org <organization-url> --project <project-name>

# Check the build logs for any remaining path issues
```

## Updating Documentation and References

### Identifying Documentation to Update

```bash
# Find documentation files that reference the old path
cd destination-repo-working
grep -r "old/path/to/folder" --include="*.md" --include="*.html" --include="*.txt" .
```

### Updating Documentation Files

```bash
# Update references in documentation files
sed -i 's|old/path/to/folder|new/path/to/folder|g' path/to/documentation.md

# Commit and push the changes
git add .
git commit -m "Update folder references in documentation"
git push
```

### Updating Wiki Pages

For Azure DevOps or GitHub wikis:

```bash
# Clone the wiki repository
git clone https://dev.azure.com/organization/project/_git/project.wiki
cd project.wiki

# Find wiki pages referencing the old path
grep -r "old/path/to/folder" --include="*.md" .

# Update the references
sed -i 's|old/path/to/folder|new/path/to/folder|g' path/to/wiki-page.md

# Commit and push the changes
git add .
git commit -m "Update folder references in wiki pages"
git push
```

### Updating External References

Identify and update references in external systems:

1. Issue tracking systems (Jira, Azure Boards, etc.)
2. Shared documentation (Confluence, SharePoint, etc.)
3. Team communication channels (Teams, Slack, etc.)

## Cleaning Up Temporary Files and Repositories

After verifying everything works correctly, clean up the temporary files and repositories created during the migration:

```bash
# Remove temporary working directories
rm -rf source-repo-working
rm -rf extracted-folder-repo
rm -rf destination-repo-working

# Keep backups for a defined period (e.g., 30 days) before removing them
# After the retention period:
rm -rf source-repo-backup
rm -rf destination-repo-backup
```

### Archiving Migration Logs

```bash
# Create an archive of migration logs
mkdir -p migration-archives
tar -czf migration-archives/migration-logs-$(date +%Y%m%d).tar.gz migration-logs/

# Store the archive in a secure location
```

## Testing the Moved Code in the New Location

### Running Automated Tests

```bash
# Navigate to the destination repository
cd destination-repo

# Run tests for the moved code
cd path/to/moved/folder

# For Java projects
mvn test

# For JavaScript projects
npm test

# For .NET projects
dotnet test
```

### Manual Testing Checklist

Create a checklist for manual testing:

1. Verify all files are present in the new location
2. Check that the code compiles/builds successfully
3. Run the application and test basic functionality
4. Test specific features that might be affected by the move
5. Verify integrations with other components

### Integration Testing

```bash
# Run integration tests that involve the moved code
cd destination-repo
./run-integration-tests.sh

# Check for any failures related to the moved code
```

## Communication Plan for Stakeholders

### Announcement Template

```markdown
# Folder Migration Completed

## Summary
The folder `[old/path/to/folder]` has been successfully migrated to `[new/path/to/folder]` in the `[destination-repo]` repository. The complete commit history has been preserved.

## What Changed
- Folder location: `[old/path/to/folder]` → `[new/path/to/folder]`
- Repository: `[source-repo]` → `[destination-repo]`

## Action Required
1. Update your local clones:
   ```bash
   git clone https://repository-url.git
   # or
   git pull
   ```
2. Update any local references to the old path
3. Review updated documentation at [link]

## Timeline
- Migration completed: [date]
- Transition period ends: [date] (after this date, the old location will no longer be maintained)

## Questions or Issues?
Contact [name] at [email] or [chat channel]
```

### Communication Channels

Send the announcement through appropriate channels:

1. Team email distribution list
2. Team chat channels (Teams, Slack, etc.)
3. Project announcements in Azure DevOps or GitHub
4. Team meetings or standups

## Validation Procedures Using Monitoring Tools

### Setting Up Monitoring

```bash
# Configure monitoring for the new location
cd destination-repo

# For example, set up code coverage monitoring
./configure-coverage-monitoring.sh path/to/moved/folder

# Set up performance monitoring
./configure-performance-monitoring.sh path/to/moved/folder
```

### Monitoring Checklist

Monitor the following metrics after the migration:

1. Build success rate
2. Test pass rate
3. Code coverage
4. Performance metrics
5. Error rates in production
6. User-reported issues related to the moved code

### Creating a Dashboard

```bash
# For Azure DevOps, create a dashboard with relevant widgets
az boards dashboard create --name "Migration Monitoring" --org <organization-url> --project <project-name>

# Add widgets to track the metrics
```

## Post-Migration Review

Schedule a post-migration review meeting with the team to:

1. Discuss any issues encountered during or after the migration
2. Identify lessons learned for future migrations
3. Document the process improvements
4. Celebrate the successful migration

## Post-Migration Checklist

- [ ] Re-enabled all branch policies
- [ ] Updated all build pipelines and verified they work
- [ ] Updated all documentation and references
- [ ] Cleaned up temporary files and repositories
- [ ] Archived migration logs
- [ ] Tested the moved code in the new location
- [ ] Communicated the changes to all stakeholders
- [ ] Set up monitoring for the new location
- [ ] Conducted a post-migration review
- [ ] Updated the migration documentation with lessons learned

## Next Steps

After completing all post-migration tasks, you may want to explore [Advanced Scenarios and Troubleshooting](./wiki-08-advanced-scenarios.md) for handling more complex migration scenarios or troubleshooting any issues that arise.

## See Also

- [Importing into the Destination Repository](./wiki-05-importing-destination.md)
- [Automation Options](./wiki-06-automation-options.md)
- [Advanced Scenarios and Troubleshooting](./wiki-08-advanced-scenarios.md)
- [Appendix D: Security Considerations](./appendices/appendix-d-security-considerations.md)

## Glossary

- **Branch Policy**: Rules that control how code can be committed to specific branches in a repository
- **Build Pipeline**: An automated process that builds, tests, and deploys code
- **Integration Testing**: Testing how components work together
- **Monitoring**: The process of observing and tracking the performance and health of applications
- **Stakeholder**: Anyone who is affected by or has an interest in the migration
