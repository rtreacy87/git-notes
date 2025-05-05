# DevOps Repository Migration Lab: Quick Reference

## Git Commands Quick Reference

### Repository Setup and Cloning
```bash
# Create a new repository on GitHub/Azure DevOps/GitLab via web interface

# Clone a repository
git clone <repository-url> <local-folder-name>

# Navigate to repository folder
cd <local-folder-name>
```

### Making Changes
```bash
# Check status of your working directory
git status

# Add files to staging area
git add <file-name>    # Add specific file
git add .              # Add all files

# Commit changes
git commit -m "Your commit message"

# Push changes to remote repository
git push origin main   # or git push origin master
```

### Repository Migration
```bash
# Add a new remote
git remote add <remote-name> <repository-url>

# View configured remotes
git remote -v

# Push all branches to the new remote
git push <remote-name> --all

# Push all tags to the new remote
git push <remote-name> --tags
```

### Advanced Migration with git-filter-repo
```bash
# Install git-filter-repo
pip install git-filter-repo

# Extract a folder with history
git filter-repo --path <folder-path>/ --path-rename <folder-path>/:./

# Extract multiple folders
git filter-repo --path <folder1>/ --path <folder2>/
```

### Viewing History
```bash
# View commit history
git log

# View commit history with graph
git log --graph --oneline --all

# View history for a specific file
git log -- <file-path>
```

## Weather App Code Modifications

### CSS Modifications (styles.css)
```css
/* Change background color */
body {
    background-color: #e6f7ff;  /* Changed from #f5f5f5 */
}

/* Change header color */
h1 {
    color: #0066cc;  /* Changed from #333 */
}
```

### JavaScript Modifications (script.js)
```javascript
// Uncomment the temperature conversion function (lines 25-35)

// Add function call in displayWeather function
function displayWeather(city, data) {
    // ... existing code ...
    
    // Add this line:
    convertTemperature(data.temp);
}
```

## DevOps Platform Quick Links

### GitHub
- [Create a new repository](https://github.com/new)
- [GitHub documentation](https://docs.github.com/en)

### Azure DevOps
- [Create a new repository](https://dev.azure.com/)
- [Azure DevOps documentation](https://docs.microsoft.com/en-us/azure/devops/?view=azure-devops)

### GitLab
- [Create a new repository](https://gitlab.com/projects/new)
- [GitLab documentation](https://docs.gitlab.com/)

## Troubleshooting

### Authentication Issues
- For HTTPS: Use a personal access token instead of password
- For SSH: Ensure your SSH key is added to your account

### Push Rejected
```bash
# If push is rejected due to non-fast-forward
git pull --rebase origin main
git push origin main
```

### Merge Conflicts
```bash
# Resolve conflicts manually in your editor
# After resolving
git add <conflicted-files>
git rebase --continue  # If during rebase
git merge --continue   # If during merge
```

### Reset to Previous State
```bash
# Soft reset (keep changes staged)
git reset --soft HEAD~1

# Hard reset (discard changes)
git reset --hard HEAD~1
```
