# Moving Folders with Complete Commit History Between DevOps Repositories

## Wiki 1: Introduction and Prerequisites
- Purpose and benefits of preserving commit history when moving folders
- When to use this approach vs. other migration strategies
- Prerequisites and required tools:
  - Git client installation
  - Appropriate permissions on both repositories
  - Git filter-repo tool installation (preferred over git filter-branch)
  - Backup of both repositories before starting
- Important considerations and potential risks

## Wiki 2: External Tools for Repository Migration

### Git-based Tools
- **Git Filter-repo**: Advanced history rewriting tool (replacement for git-filter-branch)
  - Installation and setup
  - Basic usage patterns for folder extraction
  - Performance advantages over filter-branch
  
- **Git Subtree**: Native Git command for managing repository subsets
  - When to use subtree vs. other approaches
  - Command syntax for extraction and merging
  - Limitations when preserving history

- **Git Submodule**: For maintaining separate repositories with references
  - Converting a folder to a submodule
  - Advantages and disadvantages for history preservation

### DevOps-specific Tools
- **Azure DevOps Migration Tools**
  - Repository migration utilities
  - Work item and history synchronization
  - Configuration options for folder-specific migrations

- **Repository Importer Extensions**
  - Available marketplace extensions
  - Configuration for targeted imports
  - Validation and verification features

### Third-party Utilities
- **GitKraken**: Visual Git client with repository management features
  - Repository cloning and management
  - Visual history browsing and verification
  - Conflict resolution features

- **git-split-diffs**: For complex repository splitting scenarios
  - Installation and configuration
  - Usage for selective history preservation
  - Integration with DevOps pipelines

- **RepoSurgeonTools**: Specialized toolset for repository manipulation
  - Advanced history rewriting scenarios
  - Handling complex folder structures
  - Preserving commit metadata

## Wiki 3: Preparation Steps
- Creating backups of both repositories
- Setting up local clones of both repositories
- Configuring Git credentials and access to both repositories
- Identifying the folder to be moved and its path
- Planning the target location in the destination repository
- Temporarily disabling branch policies if necessary
- Tool selection guide: choosing the right approach based on scenario

## Wiki 4: Extracting the Folder with its History
- Using git filter-repo to extract the folder with its history
- Step-by-step commands with explanations
- Verifying the extracted history in the new repository
- Handling edge cases (submodules, LFS files, etc.)
- Troubleshooting common extraction issues
- Comparing output from different extraction tools

## Wiki 5: Importing into the Destination Repository
- Preparing the destination repository for the import
- Merging the extracted folder into the destination
- Resolving potential conflicts
- Preserving commit metadata (authors, dates, messages)
- Verifying the imported history in the destination repository
- Tool-specific import procedures and best practices

## Wiki 6: Automation Options
- Creating PowerShell scripts for repeatable migrations
- Using Azure DevOps pipelines for automated migrations
- Sample automation scripts for common scenarios
- CI/CD integration for migration validation
- Error handling and reporting in automated migrations
- Scheduling considerations for minimal disruption

## Wiki 7: Post-Migration Tasks
- Re-enabling branch policies
- Updating build pipelines and references
- Updating documentation and references
- Cleaning up temporary files and repositories
- Testing the moved code in the new location
- Communication plan for stakeholders
- Validation procedures using monitoring tools

## Wiki 8: Advanced Scenarios and Troubleshooting
- Moving multiple folders simultaneously
- Handling large repositories or history
- Migrating between significantly different DevOps versions
- Addressing common errors and their solutions
- Performance considerations for large migrations
- Using specialized tools for complex migrations

## Wiki 9: Best Practices and Case Studies
- Git command reference for history preservation
- Tips for maintaining clean history during migrations
- Sample migration script templates
- Real-world case studies and lessons learned
- Tool comparison matrix with strengths/weaknesses
- Additional resources and references

## Wiki 10: Migration Templates and Checklists
- Pre-migration assessment checklist
- Tool selection decision tree
- Step-by-step migration procedure templates
- Post-migration verification checklist
- Rollback procedures and contingency planning
- Stakeholder communication templates

---

## Appendices

### Appendix A: Tool Installation Guide
- Detailed installation instructions for all mentioned tools
- Environment-specific considerations (Windows, Linux, macOS)
- Troubleshooting installation issues

### Appendix B: Command Reference
- Complete command syntax for all migration scenarios
- Examples with explanations
- Parameter reference with best practices

### Appendix C: Performance Optimization
- Techniques for handling large repositories
- Hardware recommendations for complex migrations
- Caching and network considerations

### Appendix D: Security Considerations
- Managing sensitive information during migrations
- Authentication and authorization best practices
- Audit trail maintenance

### Appendix E: Glossary and Reference
- Definition of key terms
- Quick reference guide
- Further reading and community resources
