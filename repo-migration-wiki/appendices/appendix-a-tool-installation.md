# Appendix A: Tool Installation Guide

## Overview

This guide provides detailed installation instructions for all tools mentioned in the folder migration wiki. It covers different operating systems and environments to ensure you can set up the necessary tools regardless of your platform.

## Git Client Installation

### Windows

1. **Download the installer**:
   - Visit [Git for Windows](https://git-scm.com/download/win)
   - Download the latest version

2. **Run the installer**:
   - Accept the license agreement
   - Choose installation options (defaults are usually fine)
   - Select your preferred editor
   - Choose how to use Git from the command line
   - Select HTTPS transport backend (OpenSSL recommended)
   - Configure line ending conversions (recommended: Checkout Windows-style, commit Unix-style)
   - Configure terminal emulator (recommended: MinTTY)
   - Configure extra options (defaults are usually fine)
   - Complete the installation

3. **Verify installation**:
   ```bash
   git --version
   ```

### macOS

1. **Using Homebrew (recommended)**:
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Git
   brew install git
   ```

2. **Using the installer**:
   - Visit [Git for macOS](https://git-scm.com/download/mac)
   - Download and run the installer

3. **Verify installation**:
   ```bash
   git --version
   ```

### Linux (Debian/Ubuntu)

```bash
# Update package lists
sudo apt update

# Install Git
sudo apt install git

# Verify installation
git --version
```

### Linux (Red Hat/Fedora)

```bash
# Install Git
sudo dnf install git

# Verify installation
git --version
```

## Git Filter-Repo Installation

Git filter-repo is a powerful tool for rewriting Git history and is the recommended tool for folder migrations.

### Windows

1. **Using pip (Python package manager)**:
   ```bash
   # Install Python if not already installed
   # Download from https://www.python.org/downloads/windows/

   # Install git-filter-repo
   pip install git-filter-repo
   ```

2. **Using Chocolatey**:
   ```bash
   # Install Chocolatey if not already installed
   # See https://chocolatey.org/install

   # Install git-filter-repo
   choco install git-filter-repo
   ```

3. **Manual installation**:
   ```bash
   # Clone the repository
   git clone https://github.com/newren/git-filter-repo.git
   
   # Add to PATH
   # Copy git-filter-repo/git-filter-repo to a directory in your PATH
   # For example, copy to C:\Program Files\Git\usr\bin\
   ```

### macOS

1. **Using Homebrew (recommended)**:
   ```bash
   brew install git-filter-repo
   ```

2. **Using pip**:
   ```bash
   pip3 install git-filter-repo
   ```

3. **Manual installation**:
   ```bash
   # Clone the repository
   git clone https://github.com/newren/git-filter-repo.git
   
   # Add to PATH
   cp git-filter-repo/git-filter-repo /usr/local/bin/
   chmod +x /usr/local/bin/git-filter-repo
   ```

### Linux (Debian/Ubuntu)

```bash
# Using apt (if available in your distribution)
sudo apt update
sudo apt install git-filter-repo

# If not available via apt, use pip
sudo apt install python3-pip
pip3 install git-filter-repo

# Or manual installation
git clone https://github.com/newren/git-filter-repo.git
sudo cp git-filter-repo/git-filter-repo /usr/local/bin/
sudo chmod +x /usr/local/bin/git-filter-repo
```

### Linux (Red Hat/Fedora)

```bash
# Using dnf (if available)
sudo dnf install git-filter-repo

# If not available via dnf, use pip
sudo dnf install python3-pip
pip3 install git-filter-repo

# Or manual installation
git clone https://github.com/newren/git-filter-repo.git
sudo cp git-filter-repo/git-filter-repo /usr/local/bin/
sudo chmod +x /usr/local/bin/git-filter-repo
```

### Verification

After installation, verify that git-filter-repo is working correctly:

```bash
git filter-repo --version
```

## Azure DevOps CLI Installation

The Azure DevOps CLI is useful for managing Azure DevOps resources, including repositories and branch policies.

### Windows, macOS, and Linux

1. **Install Azure CLI**:
   - Windows: Download from [Microsoft's website](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
   - macOS: `brew install azure-cli`
   - Linux (Debian/Ubuntu): 
     ```bash
     curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
     ```
   - Linux (Red Hat/Fedora):
     ```bash
     sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
     sudo dnf install -y https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm
     sudo dnf install azure-cli
     ```

2. **Add the Azure DevOps extension**:
   ```bash
   az extension add --name azure-devops
   ```

3. **Verify installation**:
   ```bash
   az devops -h
   ```

4. **Configure defaults** (optional):
   ```bash
   az devops configure --defaults organization=https://dev.azure.com/your-organization project=your-project
   ```

## Git TFS Installation

Git-TFS is a tool for working with TFS repositories using Git.

### Windows

1. **Using Chocolatey**:
   ```bash
   choco install gittfs
   ```

2. **Manual installation**:
   - Download the latest release from [git-tfs releases](https://github.com/git-tfs/git-tfs/releases)
   - Extract to a directory
   - Add the directory to your PATH

3. **Verify installation**:
   ```bash
   git tfs --version
   ```

### macOS and Linux

Git-TFS requires .NET Framework or Mono:

```bash
# Install Mono (macOS)
brew install mono

# Install Mono (Debian/Ubuntu)
sudo apt install mono-complete

# Install Mono (Red Hat/Fedora)
sudo dnf install mono-complete

# Download and extract git-tfs
wget https://github.com/git-tfs/git-tfs/releases/download/v0.31.0/GitTfs-0.31.0.zip
unzip GitTfs-0.31.0.zip -d git-tfs

# Add to PATH
sudo cp git-tfs/git-tfs /usr/local/bin/
sudo chmod +x /usr/local/bin/git-tfs

# Verify installation
git tfs --version
```

## BFG Repo Cleaner Installation

BFG Repo Cleaner is useful for removing large files or sensitive data from Git repositories.

### All Platforms (requires Java)

1. **Install Java** if not already installed:
   - Windows: Download from [Oracle](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) or use `choco install openjdk`
   - macOS: `brew install openjdk`
   - Linux (Debian/Ubuntu): `sudo apt install default-jre`
   - Linux (Red Hat/Fedora): `sudo dnf install java-latest-openjdk`

2. **Download BFG**:
   ```bash
   # Download the JAR file
   wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar -O bfg.jar
   ```

3. **Create a wrapper script** (optional but recommended):
   - Windows (bfg.bat):
     ```batch
     @echo off
     java -jar path\to\bfg.jar %*
     ```
   - macOS/Linux (bfg):
     ```bash
     #!/bin/bash
     java -jar /path/to/bfg.jar "$@"
     ```

4. **Make the script executable** (macOS/Linux):
   ```bash
   chmod +x bfg
   ```

5. **Add to PATH**:
   - Move the script to a directory in your PATH
   - Or add the directory containing the script to your PATH

6. **Verify installation**:
   ```bash
   # If using the wrapper script
   bfg --version
   
   # Or directly with Java
   java -jar bfg.jar --version
   ```

## GitKraken Installation

GitKraken is a graphical Git client that can help visualize repository history.

### All Platforms

1. **Download the installer**:
   - Visit [GitKraken's website](https://www.gitkraken.com/download)
   - Download the appropriate version for your operating system

2. **Run the installer**:
   - Follow the installation wizard
   - Sign in with your GitKraken account (create one if needed)

3. **Verify installation**:
   - Launch GitKraken
   - It should open and allow you to clone or open repositories

## Git Subtrac Installation

Git Subtrac is a tool for extracting subtrees from Git repositories.

### All Platforms (requires Node.js)

1. **Install Node.js** if not already installed:
   - Windows: Download from [Node.js website](https://nodejs.org/) or use `choco install nodejs`
   - macOS: `brew install node`
   - Linux (Debian/Ubuntu): `sudo apt install nodejs npm`
   - Linux (Red Hat/Fedora): `sudo dnf install nodejs`

2. **Install git-subtrac**:
   ```bash
   npm install -g git-subtrac
   ```

3. **Verify installation**:
   ```bash
   git-subtrac --version
   ```

## Git Split-Diffs Installation

Git Split-Diffs is a tool for complex repository splitting scenarios.

### All Platforms (requires Node.js)

1. **Install Node.js** if not already installed (see above)

2. **Install git-split-diffs**:
   ```bash
   npm install -g git-split-diffs
   ```

3. **Verify installation**:
   ```bash
   git-split-diffs --help
   ```

## Troubleshooting Installation Issues

### Common Git Installation Issues

1. **Git not found in PATH**:
   - Windows: Ensure the Git installation directory is in your PATH
   - macOS/Linux: Run `which git` to check if Git is in your PATH

2. **Permission denied**:
   - macOS/Linux: Use `sudo` for installation commands
   - Windows: Run the command prompt or PowerShell as administrator

3. **SSL certificate problems**:
   ```bash
   # Disable SSL verification (use with caution)
   git config --global http.sslVerify false
   ```

### Common Git Filter-Repo Installation Issues

1. **Module not found**:
   - Ensure Python is installed and in your PATH
   - Try installing with `pip` instead of package managers

2. **Command not found**:
   - Check if the installation directory is in your PATH
   - Try using the full path to the executable

3. **Dependency issues**:
   ```bash
   # Install dependencies
   pip install pygit2
   ```

### Common Azure DevOps CLI Issues

1. **Extension not found**:
   - Ensure Azure CLI is installed first
   - Try updating Azure CLI: `az upgrade`

2. **Authentication issues**:
   ```bash
   # Log in to Azure
   az login
   
   # Set default organization
   az devops configure --defaults organization=https://dev.azure.com/your-organization
   ```

## Environment-specific Considerations

### Corporate Environments with Proxies

If you're behind a corporate proxy:

```bash
# Configure Git to use proxy
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# Configure npm to use proxy (for Node.js-based tools)
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080

# Configure pip to use proxy (for Python-based tools)
pip install --proxy http://proxy.example.com:8080 git-filter-repo
```

### Air-gapped Environments

For environments without internet access:

1. **Download packages on a connected system**:
   ```bash
   # For Git Filter-Repo
   pip download git-filter-repo -d ./packages
   
   # For npm packages
   npm pack git-split-diffs
   ```

2. **Transfer the packages to the air-gapped system**

3. **Install from local files**:
   ```bash
   # For Git Filter-Repo
   pip install --no-index --find-links ./packages git-filter-repo
   
   # For npm packages
   npm install -g ./git-split-diffs-1.0.0.tgz
   ```

## Next Steps

After installing the necessary tools, proceed to the following resources:

- [Introduction and Prerequisites](../wiki-01-introduction-prerequisites.md)
- [External Tools for Repository Migration](../wiki-02-external-tools.md)
- [Appendix B: Command Reference](./appendix-b-command-reference.md)

## See Also

- [Preparation Steps](../wiki-03-preparation-steps.md)
- [Extracting the Folder with its History](../wiki-04-extracting-folder-history.md)
- [Appendix E: Glossary and Reference](./appendix-e-glossary-reference.md)
