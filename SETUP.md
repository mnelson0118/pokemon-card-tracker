# GitHub Pages Setup Guide

Follow these steps to get your Pokédex Card Tracker live on the internet!

## Step 1: Create a GitHub Account (if you don't have one)
- Go to https://github.com
- Sign up for a free account

## Step 2: Create a New Repository
1. Click the "+" icon in the top right corner
2. Select "New repository"
3. Name it: `pokemon-card-tracker`
4. Keep it public (required for free GitHub Pages)
5. **Don't** add README, .gitignore, or license (we have these)
6. Click "Create repository"

## Step 3: Upload Files
You have two options:

### Option A: Using Git (Recommended)
1. Open Terminal/Command Prompt on your computer
2. Install Git from https://git-scm.com if you don't have it
3. Navigate to where you want to store the project:
   ```bash
   cd your-folder
   ```
4. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/pokemon-card-tracker.git
   cd pokemon-card-tracker
   ```
5. Copy these files into the folder:
   - `index.html` (the main file)
   - `README.md`
   - `.gitignore`
6. Push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: Pokédex Card Tracker"
   git push -u origin main
   ```

### Option B: Using GitHub Web Interface
1. Go to your new repository
2. Click "Add file" > "Upload files"
3. Drag and drop these files:
   - `index.html`
   - `README.md`
   - `.gitignore`
4. Click "Commit changes"

## Step 4: Enable GitHub Pages
1. Go to your repository
2. Click "Settings" (top right)
3. Click "Pages" in the left sidebar
4. Under "Build and deployment":
   - Source: Select "Deploy from a branch"
   - Branch: Select "main"
   - Folder: Select "/ (root)"
5. Click "Save"

## Step 5: Access Your Site
Your site will be live at:
```
https://YOUR-USERNAME.github.io/pokemon-card-tracker/
```

(It may take 1-2 minutes to deploy after you enable Pages)

## Updating Your Site
Whenever you make changes:
```bash
git add .
git commit -m "Your message here"
git push
```

Changes will appear on your live site within a few minutes!

## Need Help?
- GitHub Pages Docs: https://docs.github.com/en/pages
- Git Guide: https://git-scm.com/book/en/v2
