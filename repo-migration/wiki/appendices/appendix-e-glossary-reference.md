# Appendix E: Glossary and Reference

## Glossary of Key Terms

### Git Terminology

| Term | Definition |
|------|------------|
| **Blob** | The object type used to store file contents in Git |
| **Branch** | A lightweight movable pointer to a commit |
| **Commit** | A snapshot of the repository at a specific point in time |
| **Commit Hash** | A unique SHA-1 identifier for a commit |
| **Commit History** | The record of all changes made to files in a Git repository |
| **Force Push** | A Git push that overwrites the remote history with the local history |
| **Git** | A distributed version control system |
| **Git Object** | The basic storage unit in Git (blob, tree, commit, or tag) |
| **HEAD** | A reference to the current commit or branch |
| **Merge** | The process of combining changes from different branches |
| **Merge Conflict** | When Git cannot automatically merge changes |
| **Ref** | A name that points to a commit (e.g., branch or tag) |
| **Remote** | A connection to another Git repository |
| **Repository (Repo)** | A collection of files and their history |
| **SHA-1** | The hash function used to identify Git objects |
| **Tree** | The object type used to store directory structures in Git |
| **Working Directory** | The directory where you modify files |

### Migration-Specific Terminology

| Term | Definition |
|------|------------|
| **Atomic Commit** | A commit that represents a single logical change |
| **Branch Policy** | Rules that control how code can be committed to specific branches |
| **Destination Repository** | The repository where the folder will be imported |
| **Extraction** | The process of isolating a folder and its history from a repository |
| **Filter-Branch** | A Git command for rewriting history (now deprecated) |
| **Filter-Repo** | A tool for rewriting Git repository history |
| **History Preservation** | Maintaining the commit history during migration |
| **Import** | The process of adding the extracted folder to the destination repository |
| **Mailmap** | A file that maps incorrect author information to correct information |
| **Migration** | The process of moving code between repositories |
| **Monorepo** | A repository containing multiple projects |
| **Path Rename** | Changing the path of files during history rewriting |
| **Shallow Clone** | A Git clone with limited history depth |
| **Source Repository** | The repository containing the folder to be migrated |
| **Sparse Checkout** | Checking out only specific parts of a repository |
| **Subtree** | A Git feature for including one repository within another |
| **Submodule** | A Git feature that allows you to include other Git repositories within your repository |
| **Unrelated Histories** | Git repositories with no common ancestor commits |

### DevOps Terminology

| Term | Definition |
|------|------------|
| **Azure DevOps** | Microsoft's DevOps platform |
| **CI/CD** | Continuous Integration/Continuous Deployment |
| **DevOps** | Practices that combine software development and IT operations |
| **GitHub** | A web-based hosting service for Git repositories |
| **GitLab** | A web-based DevOps platform with Git repository management |
| **Pipeline** | An automated process for building, testing, and deploying code |
| **Pull Request (PR)** | A method of submitting contributions to a repository |
| **TFS** | Team Foundation Server, Microsoft's legacy source control system |
| **Work Item** | A record of a task, bug, or feature in Azure DevOps |

## Quick Reference Guide

### Essential Git Commands for Migration

```bash
# Clone a repository
git clone https://repository-url.git

# Create a backup
git clone --mirror https://repository-url.git repo-backup.git

# Extract a folder with git filter-repo
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./

# Add a remote
git remote add extracted-folder ../extracted-repo

# Fetch from a remote
git fetch extracted-folder

# Import a folder to a specific location
git read-tree --prefix=path/to/target/location -u extracted-folder/main

# Commit the changes
git commit -m "Import folder with history from source repository"

# Push the changes
git push origin branch-name
```

### Common Migration Patterns

#### Basic Folder Migration

```bash
# 1. Clone source repository
git clone https://source-repository-url.git source-repo
cd source-repo

# 2. Extract folder with history
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./

# 3. Clone destination repository
cd ..
git clone https://destination-repository-url.git dest-repo
cd dest-repo

# 4. Create branch for import
git checkout -b import-folder-branch

# 5. Add extracted repo as remote
git remote add extracted-folder ../source-repo
git fetch extracted-folder

# 6. Import the folder
mkdir -p path/to/target/location
git read-tree --prefix=path/to/target/location -u extracted-folder/main
git commit -m "Import folder with history from source repository"

# 7. Push the changes
git push -u origin import-folder-branch
```

#### Multiple Folder Migration

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

#### Migration with Conflict Resolution

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

## Common Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `fatal: not a git repository` | Command run outside a Git repository | Navigate to the repository directory |
| `fatal: ambiguous argument 'HEAD'` | Repository is empty | Create an initial commit |
| `fatal: refusing to merge unrelated histories` | Git preventing merge of unrelated repositories | Use `--allow-unrelated-histories` flag |
| `fatal: path 'path/to/folder' does not exist in 'HEAD'` | Specified folder doesn't exist | Check the path or branch |
| `fatal: destination path 'repo' already exists` | Directory already exists | Remove or rename the existing directory |
| `fatal: cannot create directory: Permission denied` | Insufficient permissions | Check and fix directory permissions |
| `error: failed to push some refs` | Remote contains work you don't have locally | Pull changes first or use force push if appropriate |
| `fatal: cannot do a partial commit during a merge` | Attempting to commit during an unresolved merge | Resolve all conflicts first |
| `fatal: cannot update paths and switch to branch at the same time` | Conflicting Git commands | Separate the operations |

## Further Reading and Community Resources

### Official Documentation

- [Git Documentation](https://git-scm.com/doc)
- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [GitHub Documentation](https://docs.github.com/en)
- [GitLab Documentation](https://docs.gitlab.com/)

### Books

- "Pro Git" by Scott Chacon and Ben Straub
- "Git Internals" by Scott Chacon
- "Version Control with Git" by Jon Loeliger and Matthew McCullough
- "Git for Teams" by Emma Jane Hogbin Westby

### Online Tutorials and Courses

- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [GitHub Learning Lab](https://lab.github.com/)
- [Git-SCM Interactive Tutorial](https://git-scm.com/book/en/v2)
- [Pluralsight Git Courses](https://www.pluralsight.com/paths/git)

### Community Forums and Resources

- [Stack Overflow - Git](https://stackoverflow.com/questions/tagged/git)
- [Stack Overflow - Git Filter-Repo](https://stackoverflow.com/questions/tagged/git-filter-repo)
- [GitHub Community Forum](https://github.community/)
- [Azure DevOps Community](https://developercommunity.visualstudio.com/AzureDevOps)
- [Reddit - r/git](https://www.reddit.com/r/git/)

### Tools and Utilities

- [Git Filter-Repo](https://github.com/newren/git-filter-repo)
- [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitKraken](https://www.gitkraken.com/)
- [SourceTree](https://www.sourcetreeapp.com/)
- [Azure DevOps Migration Tools](https://github.com/nkdAgility/azure-devops-migration-tools)

## Cheat Sheet for Common Migration Tasks

### Preparation

```bash
# Create backups
git clone --mirror https://source-repository-url.git source-repo-backup.git
git clone --mirror https://destination-repository-url.git dest-repo-backup.git

# Set up working environment
mkdir migration-project
cd migration-project

# Clone repositories
git clone https://source-repository-url.git source-repo
git clone https://destination-repository-url.git dest-repo
```

### Extraction

```bash
# Basic extraction
git filter-repo --path path/to/folder/

# Extract and move to root
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./

# Extract multiple folders
git filter-repo --path path/to/folder1/ --path path/to/folder2/

# Extract with specific file types
git filter-repo --path path/to/folder/ --path-glob '*.java' --path-glob '*.xml'
```

### Import

```bash
# Import to root
git merge --allow-unrelated-histories extracted-folder/main

# Import to specific location
mkdir -p path/to/target/location
git read-tree --prefix=path/to/target/location -u extracted-folder/main
git commit -m "Import folder with history"

# Import with subtree
git subtree add --prefix=path/to/target/location ../extracted-repo main
```

### Verification

```bash
# Check file count
find path/to/target/location -type f | wc -l

# Check commit count
git log --oneline -- path/to/target/location | wc -l

# Compare file structure
diff -r source-repo/path/to/folder dest-repo/path/to/target/location

# Verify build
cd dest-repo
./build.sh
```

## Next Steps

After reviewing this glossary and reference guide, you may want to explore:

- [Introduction and Prerequisites](../wiki-01-introduction-prerequisites.md) for an overview of the migration process
- [Best Practices and Case Studies](../wiki-09-best-practices.md) for real-world examples
- [Migration Templates and Checklists](../wiki-10-templates-checklists.md) for ready-to-use templates

## See Also

- [External Tools for Repository Migration](../wiki-02-external-tools.md)
- [Appendix A: Tool Installation Guide](./appendix-a-tool-installation.md)
- [Appendix B: Command Reference](./appendix-b-command-reference.md)
