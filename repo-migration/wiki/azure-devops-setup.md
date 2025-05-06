# Azure DevOps Board Setup Guide

This guide provides detailed instructions on how to set up an Azure DevOps board for your project, both through the web interface and using the Azure CLI.

## Setting Up Azure DevOps Through the Web Interface

### Step 1: Create an Azure DevOps Account

1. Go to the [Azure DevOps website](https://dev.azure.com)
2. Sign in with your Microsoft account or create a new one if you don't have one
3. If this is your first time using Azure DevOps, you'll be prompted to create an organization

### Step 2: Create a New Organization

1. Navigate to the Azure portal at [portal.azure.com](https://portal.azure.com)
2. Search for "Azure DevOps Organizations" in the search bar
3. Click on "My DevOps Organizations"
4. Select "Create new organization"
5. Enter a unique name for your organization
6. Choose your hosting location
7. Complete the CAPTCHA verification if prompted
8. Click "Continue"

### Step 3: Create a New Project

1. Once your organization is created, you'll be redirected to the organization page
2. Click on "New project"
3. Enter a name for your project
4. Add a description (optional)
5. Choose between "Private" or "Public" visibility
6. Select "Basic" for Work item process if you're new to Azure DevOps
7. Click "Create"

### Step 4: Set Up Your Board

1. Once your project is created, click on "Boards" in the left sidebar
2. Click on "Boards" in the submenu
3. You'll see the default board with columns like "To Do," "Doing," and "Done"
4. To customize your board:
   - Click on the gear icon (⚙️) in the top right corner
   - Select "Team configuration"
   - Navigate to "Columns" to add, remove, or rename columns
   - Click "Save and close" when done

### Step 5: Add Work Items

1. Click the "+" button in any column to add a new work item
2. Select the type of work item (e.g., Epic, Feature, User Story, Task, Bug)
3. Fill in the details:
   - Title (required)
   - Description
   - Acceptance criteria
   - Assigned to
   - Priority
   - Effort/Story points
4. Click "Save & Close"

## Setting Up Azure DevOps Using the Azure CLI

### Step 1: Install the Azure CLI and DevOps Extension

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Install the Azure DevOps extension
az extension add --name azure-devops
```

### Step 2: Configure the Azure DevOps CLI

```bash
# Set default organization
az devops configure --defaults organization=https://dev.azure.com/YOUR-ORGANIZATION

# Verify the installation
az devops -h
```

### Step 3: Create a New Project

```bash
# Create a new project
az devops project create --name "Your-Project-Name" --description "Project description" --visibility private
```

### Step 4: Create and Manage Work Items

```bash
# Create a new work item (e.g., a user story)
az boards work-item create --title "Your work item title" --type "User Story" --project "Your-Project-Name"

# List work items
az boards work-item show --id <work-item-id>

# Update a work item
az boards work-item update --id <work-item-id> --assigned-to "email@example.com"
```

### Step 5: Customize Your Board Using the CLI

```bash
# List team configurations
az boards team list --project "Your-Project-Name"

# Get team settings
az boards team show --id <team-id> --project "Your-Project-Name"

# Update team settings
az boards team update --id <team-id> --name "New Team Name" --project "Your-Project-Name"
```

## Setting Up SSH Authentication for Azure DevOps Repositories

Azure DevOps supports SSH key authentication for secure interaction with Git repositories without requiring password entry for each operation.

### Step 1: Generate an RSA SSH Key Pair

```bash
# Generate a new RSA SSH key (Azure DevOps does not support ED25519 keys)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f ~/.ssh/azure_devops_rsa

# Start the SSH agent in the background
eval "$(ssh-agent -s)"

# Add your SSH private key to the SSH agent
ssh-add ~/.ssh/azure_devops_rsa

# Display your public key to copy to Azure DevOps
cat ~/.ssh/azure_devops_rsa.pub
```

### Step 2: Add Your SSH Public Key to Azure DevOps

1. Sign in to your Azure DevOps organization
2. Click on your profile picture in the top right corner
3. Select "SSH public keys" from the dropdown menu
4. Click "New Key"
5. Enter a name for your key (e.g., "Work Laptop")
6. Paste your public key (the content you copied from the previous step)
7. Click "Add"

### Step 3: Clone a Repository Using SSH

```bash
# Clone a repository using SSH
git clone git@ssh.dev.azure.com:v3/<organization>/<project>/<repository>

# Example:
# git clone git@ssh.dev.azure.com:v3/contoso/MyProject/MyRepository
```

### Step 4: Update an Existing Repository to Use SSH

```bash
# Check current remote URL
git remote -v

# Change the remote URL to use SSH
git remote set-url origin git@ssh.dev.azure.com:v3/<organization>/<project>/<repository>
```

### Troubleshooting SSH Connections

If you encounter issues connecting via SSH:

```bash
# Test your SSH connection to Azure DevOps
ssh -T git@ssh.dev.azure.com

# Use verbose output for debugging
ssh -vT git@ssh.dev.azure.com

# Specify a specific key if you have multiple
ssh -i ~/.ssh/azure_devops_rsa -T git@ssh.dev.azure.com
```

Common issues:
- **Permission denied errors**: Ensure your public key is correctly added to Azure DevOps
- **Host key verification failed**: Add the Azure DevOps host to your known_hosts file
- **Authentication timeout**: Check your network connection and firewall settings

### Using SSH Keys with Azure DevOps CLI

You can also configure the Azure DevOps CLI to use SSH authentication:

```bash
# Configure Git to use SSH for Azure DevOps
git config --global url."git@ssh.dev.azure.com:v3/".insteadOf "https://dev.azure.com/"

# Clone using HTTPS URL (will be automatically converted to SSH)
az repos clone --repository <repository-name> --org <organization-url>
```

## Best Practices for Azure DevOps Boards

1. **Use the right work item types**: Epics for large initiatives, Features for significant functionality, User Stories for user-focused requirements, Tasks for specific work items, and Bugs for issues.

2. **Set up iterations/sprints**: Define your sprint cadence to help with planning and tracking progress.

3. **Use tags**: Add tags to work items for easier filtering and organization.

4. **Define clear acceptance criteria**: Ensure each work item has clear criteria for completion.

5. **Link related work items**: Use the "Related Work" feature to connect dependent or related items.

6. **Use the Kanban board features**: Utilize WIP limits, swimlanes, and card customization to optimize your workflow.

7. **Set up dashboards**: Create custom dashboards to visualize project progress and metrics.

## Troubleshooting Common Issues

- **Permission errors**: Ensure you have the appropriate permissions in the organization and project.
- **Missing features**: Some features may require specific Azure DevOps plans or extensions.
- **CLI connection issues**: Verify your authentication and organization settings with `az devops configure --list`.

## Additional Resources

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure DevOps CLI Reference](https://docs.microsoft.com/en-us/cli/azure/boards)
- [Azure DevOps REST API Reference](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
