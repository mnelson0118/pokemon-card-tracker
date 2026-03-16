# Pokédex Card Tracker

A beautiful, interactive web app to track your Pokémon trading card collection. Mark cards as collected, track your spending, and view card details with zoom functionality.

## Features

- 🎴 Track all 45 Pokémon cards with product images from TCGPlayer
- 💰 Track how much you've spent on each card
- 🌙 Dark mode (default) and light mode
- 🔍 Click card images to view in full size and zoom in for details
- 🔎 Search and filter cards by name, number, or generation
- 📊 Real-time statistics (collected count, total spent, progress %)
- 💾 Automatic data saving to browser storage

## How to Use

1. Visit: `https://[YOUR-USERNAME].github.io/pokemon-card-tracker/`
2. Click "Mark collected" to add a card to your collection (you'll be prompted for the price)
3. Click any card image to view it in full size and zoom
4. Use filters to search by name, number, or generation
5. Toggle dark/light mode with the moon icon

## Setup Instructions

### First Time Setup:
1. Go to https://github.com/new
2. Create a new repository named `pokemon-card-tracker`
3. Clone it to your computer: `git clone https://github.com/YOUR-USERNAME/pokemon-card-tracker.git`
4. Copy the `pokemon_collection.html` file into the repository folder as `index.html`
5. Create a `README.md` file (this file)
6. Push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: Pokédex Card Tracker"
   git push -u origin main
   ```
7. Go to your repository settings > Pages
8. Set "Build and deployment" source to "Deploy from a branch"
9. Select "main" branch and "/ (root)" folder
10. Save and your site will be live at `https://YOUR-USERNAME.github.io/pokemon-card-tracker/`

## Data Storage

Your collection data is saved locally in your browser's storage. It persists between sessions on the same device/browser.

**To backup your data:**
- Open browser DevTools (F12)
- Go to Console
- Run: `copy(localStorage.getItem('pokemon_collection_data'))`
- Paste into a text file to save

**To restore your data:**
- Go to Console
- Run: `localStorage.setItem('pokemon_collection_data', '[PASTE YOUR DATA HERE]')`

## Technologies

- HTML5
- CSS3 (with CSS custom properties for theming)
- Vanilla JavaScript
- Browser localStorage for persistence

## License

MIT License - feel free to modify and share!
