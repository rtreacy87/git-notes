# DevOps Repository Migration Lab

This lab provides hands-on experience with modifying code in a DevOps environment, making commits, and migrating content to a new repository while preserving commit history.

## Lab Overview

In this lab, you will:
1. Set up a simple web application in a Git repository
2. Make modifications to the code and commit your changes
3. Create a new repository
4. Migrate the code to the new repository while preserving commit history

## Prerequisites

- Git installed on your local machine
- Access to a DevOps platform ([GitHub](https://github.com), [Azure DevOps](https://dev.azure.com), [GitLab](https://gitlab.com), etc.)
- Basic familiarity with Git commands
- A text editor or IDE

## Lab Instructions

### Part 1: Setting Up the Initial Repository

1. Create a new repository in your DevOps platform named "weather-app-original"

2. Clone the repository to your local machine:
   ```bash
   git clone <your-repository-url> weather-app-original
   cd weather-app-original
   ```

3. Copy the initial code files from this lab folder to your repository:
   - index.html
   - styles.css
   - script.js

4. Add and commit the files:
   ```bash
   git add .
   git commit -m "Initial commit: Basic weather app"
   git push origin main
   ```

5. Open the application in your browser to verify it works. You should see a simple weather app interface.

### Part 2: Making Code Modifications

1. First Modification: Update the UI
   - Open `styles.css` and change the background color from `#f5f5f5` to `#e6f7ff`
   - Update the header color from `#333` to `#0066cc`
   - Commit your changes:
     ```bash
     git add styles.css
     git commit -m "Update UI colors for better contrast"
     git push origin main
     ```

2. Second Modification: Add Temperature Conversion
   - Open `script.js` and uncomment the temperature conversion function (lines 25-35)
   - Add a call to this function in the `displayWeather` function
   - Commit your changes:
     ```bash
     git add script.js
     git commit -m "Add temperature conversion functionality"
     git push origin main
     ```

3. Verify your changes by opening the application in your browser again.

### Part 3: Creating a New Repository

1. Create a new repository in your DevOps platform named "weather-app-new"

2. Do not initialize the repository with any files (no README, .gitignore, or license)

### Part 4: Migrating the Code with History

1. Navigate to your original repository directory:
   ```bash
   cd weather-app-original
   ```

2. Add the new repository as a remote:
   ```bash
   git remote add new-repo <your-new-repository-url>
   ```

3. Push all branches and tags to the new repository:
   ```bash
   git push new-repo --all
   git push new-repo --tags
   ```

4. Clone the new repository to verify the migration:
   ```bash
   cd ..
   git clone <your-new-repository-url> weather-app-new
   cd weather-app-new
   ```

5. Verify that all files and commit history have been migrated:
   ```bash
   git log
   ```

   You should see all your previous commits, including:
   - Initial commit
   - UI color update
   - Temperature conversion functionality

### Part 5: Advanced Migration (Optional)

If you want to practice more advanced migration techniques:

1. Create a folder structure in the original repository:
   ```bash
   cd ../weather-app-original
   mkdir -p src/app
   git mv index.html src/app/
   git mv styles.css src/app/
   git mv script.js src/app/
   git commit -m "Reorganize files into src/app folder"
   git push origin main
   ```

2. Create a new repository named "weather-app-restructured"

3. Use git filter-repo to extract the src/app folder with history:
   ```bash
   # Install git-filter-repo if not already installed
   # pip install git-filter-repo

   # Clone a fresh copy of the repository
   cd ..
   git clone <your-original-repository-url> weather-app-extract
   cd weather-app-extract
   
   # Extract the src/app folder with history
   git filter-repo --path src/app/ --path-rename src/app/:./
   
   # Add the new repository as a remote
   git remote add restructured <your-restructured-repository-url>
   
   # Push to the new repository
   git push restructured --all
   git push restructured --tags
   ```

4. Verify the migration by cloning the restructured repository and checking the commit history.

## Lab Completion

You have successfully:
1. Set up a simple web application in a Git repository
2. Made modifications to the code and committed your changes
3. Created a new repository
4. Migrated the code to the new repository while preserving commit history

These skills are essential for managing code in a DevOps environment, especially when reorganizing repositories or splitting monolithic codebases into smaller, more manageable components.

## Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo)
- [Moving Folders Between Repositories Wiki](../wiki/README.md)
