# External Tools for Repository Migration

## Overview

This guide covers the primary tools available for migrating folders between repositories while preserving commit history. Each tool has specific strengths and use cases, and understanding these differences will help you select the most appropriate approach for your migration scenario.

## Git-based Tools

### Git Filter-Repo

Git filter-repo is the recommended tool for complex history rewriting operations, including folder migrations. It was created as a superior alternative to git filter-branch, offering better performance and safety features.

#### Installation

```bash
# For Debian/Ubuntu
sudo apt-get install git-filter-repo

# For macOS with Homebrew
brew install git-filter-repo

# For Windows with Chocolatey
choco install git-filter-repo

# Alternative: Install via pip (Python package manager)
pip install git-filter-repo
```

For detailed installation instructions, see [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md).

#### Basic Usage for Folder Extraction

```bash
# Clone the repository
git clone https://repository-url.git source-repo
cd source-repo

# Extract a specific folder with its history
git filter-repo --path folder-to-extract/ --path-rename folder-to-extract/:./

# Verify the result
git log
```

#### Key Features

- **Performance**: Significantly faster than git filter-branch, especially for large repositories
- **Safety**: Prevents common mistakes by refusing to modify a repo with unclean status
- **Flexibility**: Provides extensive options for history rewriting
- **Maintainability**: Actively maintained and recommended by Git maintainers

#### When to Use

- When you need to extract a folder with its complete history
- For large repositories where performance matters
- When you need fine-grained control over the migration process

### Git Subtree

Git subtree is a built-in Git command that helps manage repository subsets. While primarily designed for including external repositories within your project, it can also be used for certain migration scenarios.

#### Command Syntax

```bash
# Add a subtree
git subtree add --prefix=<folder-name> <repository-url> <branch> --squash

# Extract a folder to its own repository
git subtree split --prefix=<folder-path> -b <branch-name>
```

#### Advantages and Limitations

**Advantages:**
- Built into Git (no additional installation required)
- Preserves commit history when used correctly
- Works well for simple scenarios

**Limitations:**
- More complex to use for history preservation
- Can create large, unwieldy commits when using --squash
- Less efficient for large repositories

#### When to Use

- For simpler migration scenarios
- When git filter-repo is not available
- When you want to maintain a connection to the original repository

### Git Submodule

Git submodules allow you to include other Git repositories within your repository. While not primarily a migration tool, submodules can be part of a strategy to refactor repositories.

#### Converting a Folder to a Submodule

```bash
# Create a new repository from a folder
cd original-repo
git subtree split --prefix=folder-to-extract -b temp-branch
mkdir ../new-repo
cd ../new-repo
git init
git pull ../original-repo temp-branch

# Push the new repository
git remote add origin https://new-repository-url.git
git push -u origin master

# Replace the folder with a submodule in the original repo
cd ../original-repo
git rm -r folder-to-extract
git commit -m "Remove folder-to-extract, will replace with submodule"
git submodule add https://new-repository-url.git folder-to-extract
git commit -m "Add folder-to-extract as a submodule"
```

#### Advantages and Disadvantages

**Advantages:**
- Maintains a clear connection between repositories
- Allows independent versioning of the extracted code
- Built into Git

**Disadvantages:**
- More complex workflow for developers
- Not a true migration (original code remains linked)
- Requires additional steps to initialize and update

#### When to Use

- When you want the extracted code to remain linked to the original repository
- When the extracted code needs independent versioning
- For code that is shared across multiple repositories

## DevOps-specific Tools

### Azure DevOps Migration Tools

Microsoft provides tools specifically designed for migrating between Azure DevOps repositories.

#### Key Features

- Repository migration utilities
- Work item and history synchronization
- Configuration options for folder-specific migrations

#### CLI Usage Example

```bash
# Install the Azure DevOps CLI extension
az extension add --name azure-devops

# Clone the source repository
git clone https://dev.azure.com/organization/project/_git/source-repo
cd source-repo

# Use git filter-repo to extract the folder
git filter-repo --path folder-to-extract/

# Create a new repository in Azure DevOps
az repos create --name new-repo --project project --organization https://dev.azure.com/organization

# Push to the new repository
git remote add origin https://dev.azure.com/organization/project/_git/new-repo
git push -u origin --all
```

#### When to Use

- When migrating between Azure DevOps repositories
- When you need to preserve work item links and other Azure DevOps-specific metadata
- For enterprise-scale migrations

### Repository Importer Extensions

Various extensions are available in the Azure DevOps Marketplace to assist with repository migrations.

#### Notable Extensions

- **Git Repository Importer**: Facilitates importing Git repositories into Azure DevOps
- **TFS/VSTS Sync Migration Tools**: Helps migrate work items and history

#### Configuration for Targeted Imports

Most extensions provide configuration files or UI options to specify:
- Source and destination repositories
- Folders to include/exclude
- History depth to preserve
- Mapping between source and destination paths

## Third-party Utilities

### GitKraken

GitKraken is a visual Git client that can assist with repository management tasks, including aspects of migration.

#### Key Features for Migration

- Visual repository cloning and management
- Graphical history browsing for verification
- Conflict resolution with visual diff tools

#### When to Use

- When you prefer a GUI for managing complex Git operations
- For visualizing and verifying repository history before and after migration
- When resolving complex merge conflicts during the import phase

### git-split-diffs

A specialized tool for complex repository splitting scenarios.

#### Installation

```bash
npm install -g git-split-diffs
```

#### Basic Usage

```bash
git-split-diffs --source-repo=/path/to/source --target-repo=/path/to/target --path=folder/to/extract
```

#### When to Use

- For complex splitting scenarios not easily handled by git filter-repo
- When you need to preserve history across multiple interrelated folders
- For integration with DevOps pipelines

### RepoSurgeonTools

A collection of specialized tools for repository manipulation, particularly useful for complex history rewriting scenarios.

#### Key Features

- Advanced history rewriting capabilities
- Handling of complex folder structures
- Preservation of commit metadata

#### When to Use

- For the most complex migration scenarios
- When other tools have limitations that prevent successful migration
- When you need fine-grained control over every aspect of the migration

## Tool Selection Guide

| Tool | Best For | Complexity | Performance | History Preservation |
|------|----------|------------|-------------|---------------------|
| Git Filter-Repo | Most migration scenarios | Medium | Excellent | Excellent |
| Git Subtree | Simple extractions | Medium | Good | Good |
| Git Submodule | Linked repositories | High | N/A | N/A (different approach) |
| Azure DevOps Tools | Azure DevOps migrations | Medium | Good | Good |
| GitKraken | Visual verification | Low | N/A | N/A (visualization only) |
| git-split-diffs | Complex splits | High | Good | Very Good |
| RepoSurgeonTools | Advanced scenarios | Very High | Variable | Excellent |

## Next Steps

After selecting the appropriate tool for your migration scenario, proceed to [Preparation Steps](./wiki-03-preparation-steps.md) to prepare your repositories for the migration process.

## See Also

- [Preparation Steps](./wiki-03-preparation-steps.md)
- [Extracting the Folder with its History](./wiki-04-extracting-folder-history.md)
- [Appendix A: Tool Installation Guide](./appendices/appendix-a-tool-installation.md)
- [Appendix B: Command Reference](./appendices/appendix-b-command-reference.md)

## Glossary

- **Git Filter-Repo**: A tool for rewriting Git repository history, more efficient and safer than git filter-branch.
- **Git Subtree**: A Git command for managing repository subsets within a main repository.
- **Git Submodule**: A Git feature that allows you to include other Git repositories within your repository.
- **Repository Importer**: Tools designed to facilitate the migration of repositories between systems.
