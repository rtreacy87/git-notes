# Introduction and Prerequisites

## Overview

Moving folders between repositories while preserving their commit history is a powerful technique that maintains the valuable context of how code evolved over time. This approach is particularly useful when reorganizing large repositories, splitting monolithic codebases, or consolidating related components.

This wiki explains how to successfully migrate folders between DevOps repositories while keeping their complete commit history intact, ensuring that all contributions, changes, and development context remain accessible in the new location.

## Purpose and Benefits

Preserving commit history during folder migration offers several important advantages:

- **Maintains development context**: Developers can understand why and how code evolved
- **Preserves attribution**: Original author information remains intact for all changes
- **Facilitates troubleshooting**: Historical bugs and their fixes remain traceable
- **Supports compliance**: Audit trails remain intact for regulatory requirements
- **Enables accurate blame/praise**: Tools like `git blame` continue to work correctly
- **Preserves commit timestamps**: The chronological development timeline remains accurate

## When to Use This Approach

This migration approach is ideal for:

| Scenario | Suitability | Reason |
|----------|-------------|--------|
| Moving a component to its own repository | ✅ Excellent | Preserves the complete development history of the component |
| Consolidating related repositories | ✅ Excellent | Maintains history while bringing code together |
| Reorganizing repository structure | ✅ Good | Keeps history while improving organization |
| Temporary code sharing | ❌ Poor | Simpler approaches like copying would be more appropriate |
| Moving individual files | ⚠️ Possible but complex | The effort may outweigh the benefits |

## Prerequisites

### Required Tools

1. **Git Client**
   - Modern Git client (version 2.24.0 or newer recommended)
   - Configured with appropriate credentials for both repositories

2. **Git Filter-Repo**
   - A powerful tool for rewriting Git history (preferred over git filter-branch)
   - See [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md) for installation instructions

3. **Access and Permissions**
   - Write access to both source and destination repositories
   - Permission to force-push to protected branches (if applicable)
   - Ability to temporarily disable branch policies (if needed)
   - For Azure DevOps setup, refer to our [Azure DevOps Setup Guide](./azure-devops-setup.md)

4. **Backup Solution**
   - Method to create full backups of both repositories before starting
   - Storage space for backups

### Environment Setup

Before beginning, ensure you have:

```bash
# Verify Git version (should be 2.24.0+)
git --version

# Verify git-filter-repo is installed
git filter-repo --version

# Create working directory for the migration
mkdir repo-migration-project
cd repo-migration-project
```

## Important Considerations and Risks

### Potential Risks

1. **History Rewriting**
   - This process rewrites Git history, which can cause issues for other repository users
   - All team members need to be informed and prepared for the changes

2. **Force Pushing**
   - The migration typically requires force pushing, which can overwrite remote changes
   - Coordinate with team to ensure no work is lost

3. **Build and Integration Impact**
   - CI/CD pipelines may need updates after migration
   - References to moved files will need updating

4. **Large Repository Challenges**
   - Repositories with extensive history may require significant processing time
   - Additional performance considerations apply (see [Appendix C: Performance Optimization](./appendices/appendix-c-performance-optimization.md))

### Risk Mitigation

1. **Always create backups before starting**
   ```bash
   # Clone with all branches and tags
   git clone --mirror source-repo-url source-repo-backup
   git clone --mirror destination-repo-url destination-repo-backup
   ```

2. **Perform the migration in a controlled environment**
   - Use feature branches for testing the migration
   - Validate results before updating main branches

3. **Communicate with all stakeholders**
   - Inform team members about the planned migration
   - Schedule the migration during low-activity periods
   - Provide clear instructions for handling the changes

4. **Have a rollback plan**
   - Document steps to restore from backups if needed
   - Test the restoration process before proceeding

## Next Steps

Once you've confirmed you have all prerequisites in place and have considered the potential risks, proceed to [External Tools for Repository Migration](./wiki-02-external-tools.md) to learn about the various tools available for this process.

## See Also

- [Preparation Steps](./wiki-03-preparation-steps.md)
- [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md)
- [Appendix D: Security Considerations](./appendices/appendix-d-security-considerations.md)
- [Azure DevOps Setup Guide](./azure-devops-setup.md)

## Glossary

- **Commit History**: The record of all changes made to files in a Git repository, including author information, timestamps, and commit messages.
- **Git Filter-Repo**: A tool for rewriting Git repository history, more efficient and safer than git filter-branch.
- **Force Push**: A Git push that overwrites the remote history with the local history, potentially discarding commits on the remote.
- **Branch Policies**: Rules that control how code can be committed to specific branches in a repository.
