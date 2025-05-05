# Appendix D: Security Considerations

## Overview

Migrating folders between repositories involves handling source code, potentially sensitive information, and authentication credentials. This guide covers security best practices to ensure your migration process is secure and does not expose sensitive data or create vulnerabilities.

## Managing Sensitive Information During Migrations

### Identifying Sensitive Data

Before migration, scan repositories for sensitive information that should not be transferred or should be handled carefully:

```bash
# Search for potential passwords or keys
git grep -i "password\|secret\|key\|token" -- "*.config" "*.json" "*.xml" "*.properties"

# Search for potential API keys (alphanumeric strings of certain length)
git grep -E "[a-zA-Z0-9_]{32,}" -- "*.config" "*.json" "*.xml" "*.properties"

# Search for AWS access keys
git grep -E "AKIA[0-9A-Z]{16}" -- "*"

# Search for private keys
git grep -A 2 -B 2 "BEGIN PRIVATE KEY" -- "*"
```

### Handling Secrets in Repository History

If sensitive data is found in the repository history:

```bash
# Option 1: Use BFG Repo Cleaner to remove sensitive data
java -jar bfg.jar --replace-text secrets.txt source-repo.git

# Where secrets.txt contains patterns like:
# password=*** [FILTERED]
# apiKey=*** [FILTERED]

# Option 2: Use git filter-repo to remove sensitive files
git filter-repo --path-glob "*.pem" --invert-paths

# Option 3: Use git filter-repo with a blob callback to redact sensitive content
git filter-repo --blob-callback '
    if b"PASSWORD" in blob.data:
        data = blob.data.replace(b"PASSWORD=secret123", b"PASSWORD=***REDACTED***")
        blob.data = data
        return True
    return False
'
```

### Preventing Secret Leakage During Migration

```bash
# Create a .gitattributes file to prevent certain files from being migrated
cat > .gitattributes << EOF
*.pem filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
**/secrets/** filter=git-crypt diff=git-crypt
EOF

# Add and commit the .gitattributes file
git add .gitattributes
git commit -m "Add .gitattributes for sensitive files"

# Use git-crypt to encrypt sensitive files
git-crypt init
git-crypt add-gpg-user user@example.com

# Alternatively, exclude sensitive files during extraction
git filter-repo --path path/to/folder/ --path-glob "*.pem" --invert-paths --path-glob "*.pem"
```

## Authentication and Authorization Best Practices

### Secure Credential Management

```bash
# Use credential helpers instead of hardcoding credentials
git config --global credential.helper store  # Stores credentials unencrypted (use with caution)
git config --global credential.helper 'cache --timeout=3600'  # Caches credentials in memory

# For Windows, use the Windows Credential Manager
git config --global credential.helper wincred

# For macOS, use the Keychain
git config --global credential.helper osxkeychain

# For Linux, use libsecret
git config --global credential.helper libsecret
```

### Using SSH Keys Securely

```bash
# Generate a new SSH key for repository access
ssh-keygen -t ed25519 -C "migration@example.com" -f ~/.ssh/migration_key

# Use a passphrase to protect the key
# When prompted, enter a strong passphrase

# Add the key to the SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/migration_key

# Add the public key to your Git hosting service
cat ~/.ssh/migration_key.pub
# Copy the output and add it to GitHub/GitLab/Azure DevOps

# Configure Git to use the specific key for a repository
git config core.sshCommand "ssh -i ~/.ssh/migration_key -F /dev/null"
```

### Temporary Access Tokens

For migrations using HTTPS:

```bash
# GitHub: Create a Personal Access Token with limited scope and expiration
# GitLab: Create a Project Access Token with limited scope and expiration
# Azure DevOps: Create a Personal Access Token with limited scope and expiration

# Use the token in the clone URL
git clone https://username:token@github.com/org/repo.git

# Or store it in the credential helper
echo "https://username:token@github.com" | git credential approve
```

### Role-Based Access Control

Ensure appropriate permissions are set for both source and destination repositories:

1. **Source Repository**:
   - Read access is sufficient for extraction
   - Avoid using admin credentials if not needed

2. **Destination Repository**:
   - Write access is required for importing
   - Consider creating a dedicated service account for migrations
   - Remove unnecessary permissions after migration

```bash
# Azure DevOps CLI example to check permissions
az repos permission show --repository-id <repository-id> --subject <user-email> --org <organization-url> --project <project-name>

# Azure DevOps CLI example to grant permissions
az repos permission update --repository-id <repository-id> --subject <user-email> --allow-bit 4 --org <organization-url> --project <project-name>
```

## Audit Trail Maintenance

### Preserving Commit Attribution

```bash
# Use git filter-repo to preserve author information
git filter-repo --path path/to/folder/ --preserve-commit-encoding --preserve-commit-hashes

# If author emails need to be updated, use a mailmap file
cat > mailmap.txt << EOF
New Name <new.email@example.com> <old.email@example.com>
New Name <new.email@example.com> Old Name <old.email@example.com>
EOF

git filter-repo --path path/to/folder/ --mailmap mailmap.txt
```

### Logging Migration Activities

```bash
# Create a log directory
mkdir -p migration-logs

# Log all migration commands with timestamps
exec > >(tee -a migration-logs/migration-$(date +%Y%m%d-%H%M%S).log)
exec 2>&1

echo "Starting migration at $(date)"
# Run migration commands
echo "Completed migration at $(date)"

# Archive logs securely
tar -czf migration-logs-$(date +%Y%m%d).tar.gz migration-logs/
gpg -e -r user@example.com migration-logs-$(date +%Y%m%d).tar.gz
```

### Creating Migration Reports

```bash
# Generate a migration report
cat > migration-report.md << EOF
# Folder Migration Report

## Migration Details
- Source Repository: $SOURCE_REPO
- Destination Repository: $DEST_REPO
- Folder Path: $FOLDER_PATH
- Target Path: $TARGET_PATH
- Migration Date: $(date)
- Migration Performed By: $(git config user.name) <$(git config user.email)>

## Statistics
- Files Migrated: $(find $TARGET_PATH -type f | wc -l)
- Commits Preserved: $(git log --oneline -- $TARGET_PATH | wc -l)
- Authors: $(git log --format='%an' -- $TARGET_PATH | sort | uniq | wc -l)

## Sensitive Data Handling
- Scanned for sensitive data: Yes/No
- Sensitive data found: Yes/No
- Remediation actions taken: [Details]

## Verification Steps
- Build verification: Passed/Failed
- Test verification: Passed/Failed
- Security scan: Passed/Failed

## Approvals
- Technical Approval: [Name, Date]
- Security Approval: [Name, Date]
EOF
```

## Network and Transfer Security

### Secure Transport Protocols

```bash
# Always use HTTPS or SSH for Git operations
# HTTPS example
git clone https://github.com/org/repo.git

# SSH example
git clone git@github.com:org/repo.git

# Verify SSL certificates
git config --global http.sslVerify true

# If behind a corporate proxy with SSL inspection
git config --global http.sslVerify false  # Use with caution and only if necessary
```

### Working with Private Networks

```bash
# Configure proxy settings if needed
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# For SSH connections through a proxy
cat >> ~/.ssh/config << EOF
Host github.com
    ProxyCommand nc -X connect -x proxy.example.com:8080 %h %p
    ServerAliveInterval 60
EOF
```

### Secure File Transfer

For transferring repositories between air-gapped networks:

```bash
# Create a bundle of the repository
git bundle create repo-bundle.bundle --all

# Encrypt the bundle
gpg -e -r recipient@example.com repo-bundle.bundle

# Transfer the encrypted bundle to the target network

# On the target network, decrypt the bundle
gpg -d repo-bundle.bundle.gpg > repo-bundle.bundle

# Create a new repository from the bundle
mkdir new-repo
cd new-repo
git init
git bundle unbundle ../repo-bundle.bundle
```

## Repository Security Configuration

### Branch Protection

After migration, ensure appropriate branch protection rules are in place:

```bash
# Azure DevOps CLI example to add branch policy
az repos policy create --repository-id <repository-id> --branch main --policy-type Microsoft.RequiredReviewers --org <organization-url> --project <project-name> --blocking true --enabled true --parameters '{
    "requiredReviewerIds": ["reviewer-id"],
    "minimumApproverCount": 1
}'

# GitHub API example (using curl)
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/org/repo/branches/main/protection -d '{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {},
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}'
```

### Repository Settings

Ensure secure settings in the destination repository:

```bash
# GitHub API example to disable merge commits
curl -X PATCH -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/org/repo -d '{
  "allow_merge_commit": false,
  "allow_squash_merge": true,
  "allow_rebase_merge": true
}'

# Azure DevOps CLI example to set repository policies
az repos policy create --repository-id <repository-id> --branch main --policy-type Git.CommitMessage --org <organization-url> --project <project-name> --blocking true --enabled true --parameters '{
    "pattern": "^(feat|fix|docs|style|refactor|test|chore)\\(.+\\): .+",
    "rejectionMessage": "Commit message must follow conventional commits format"
}'
```

## Security Scanning and Verification

### Pre-migration Security Scanning

```bash
# Scan for secrets before migration
git clone https://source-repository-url.git source-repo
cd source-repo

# Using trufflehog (install first: pip install trufflehog)
trufflehog --regex --entropy=True .

# Using gitleaks (install first: go get github.com/zricethezav/gitleaks)
gitleaks detect --source . --verbose

# Using git-secrets (install first: brew install git-secrets)
git secrets --register-aws
git secrets --scan
```

### Post-migration Verification

```bash
# Verify no secrets were migrated
cd destination-repo
trufflehog --regex --entropy=True path/to/target/location

# Verify file integrity
cd source-repo
find path/to/folder -type f -exec md5sum {} \; | sort > ../source-checksums.txt
cd ../destination-repo
find path/to/target/location -type f -exec md5sum {} \; | sort > ../dest-checksums.txt
cd ..
diff -u source-checksums.txt dest-checksums.txt

# Verify commit signatures if used
cd destination-repo
git log --show-signature -- path/to/target/location
```

### Continuous Security Monitoring

Set up ongoing security monitoring for the migrated code:

```bash
# Create a pre-commit hook for secret detection
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
git secrets --pre_commit_hook -- "$@"
EOF
chmod +x .git/hooks/pre-commit

# Set up automated scanning in CI/CD
# Example GitHub Actions workflow
cat > .github/workflows/security-scan.yml << EOF
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - name: Scan for secrets
      uses: zricethezav/gitleaks-action@master
EOF
```

## Incident Response Plan

### Preparing for Security Incidents

Create a plan for responding to security incidents during or after migration:

```markdown
# Migration Security Incident Response Plan

## Incident Types
1. Sensitive data exposure
2. Unauthorized access
3. Data loss or corruption

## Response Team
- Security Lead: [Name, Contact]
- Repository Admin: [Name, Contact]
- Development Lead: [Name, Contact]
- Legal/Compliance: [Name, Contact]

## Response Procedures

### For Sensitive Data Exposure
1. Identify the exposed data
2. Remove the data from the repository
   ```bash
   git filter-repo --path-glob "**/exposed-file.txt" --invert-paths
   git push --force
   ```
3. Rotate any exposed credentials
4. Notify affected parties
5. Document the incident

### For Unauthorized Access
1. Revoke access immediately
   ```bash
   # GitHub example
   curl -X DELETE -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/org/repo/collaborators/username
   
   # Azure DevOps example
   az repos permission reset --repository-id <repository-id> --subject <user-email> --org <organization-url> --project <project-name>
   ```
2. Audit recent activity
3. Change all credentials
4. Notify security team
5. Document the incident

### For Data Loss or Corruption
1. Stop all ongoing migrations
2. Restore from backups
   ```bash
   cd backup-repo.git
   git push --force --all https://destination-repository-url.git
   ```
3. Verify restoration
4. Investigate root cause
5. Document the incident
```

## Next Steps

After addressing security considerations for your migration, refer to the following resources:

- [Post-Migration Tasks](../wiki-07-post-migration-tasks.md)
- [Best Practices and Case Studies](../wiki-09-best-practices.md)
- [Appendix E: Glossary and Reference](./appendix-e-glossary-reference.md)

## See Also

- [Introduction and Prerequisites](../wiki-01-introduction-prerequisites.md)
- [Preparation Steps](../wiki-03-preparation-steps.md)
- [Appendix A: Tool Installation Guide](./appendix-a-tool-installation.md)
