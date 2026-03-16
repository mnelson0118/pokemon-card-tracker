# Pokédex Card Tracker

A beautiful, responsive web app for tracking your Pokémon trading card collection. Works perfectly on **iPhone, iPad, computer, and any browser**.

## ✨ Features

### Collection Management
- 📱 Track all 45 Generation 1 Pokémon cards
- ✅ Mark cards as collected with one tap
- 💰 Record the price you paid for each card
- 🎯 View total spent on your collection

### Smart Filtering
- Filter by: All, Collected, or Missing
- Filter by Generation (Gen 1, Gen 2, etc.)
- Search cards by name
- Collapsible filter menu to reduce clutter

### Data Sync Across All Devices
- 🌐 **NEW:** Cloud sync with Firebase
- Sync your collection across iPhone, iPad, Chrome, Safari, Firefox
- Changes appear instantly across all devices
- Works offline - auto-syncs when back online

### Beautiful Design
- 🌙 Dark mode (default) with light mode toggle
- 📷 Click cards to zoom and inspect details
- TCG Player links to buy authentic cards
- Touch-friendly buttons (44px minimum height)
- Optimized for all screen sizes

## 🎯 Responsive Layout

### Desktop (1200px+)
- 6 columns of cards
- Spacious 20px gaps
- Full progress bar visible
- Large text and buttons

### Tablet (768px - 1199px)
- 4-5 columns of cards
- 20px gaps
- Progress bar visible
- Medium-sized text

### Mobile iPhone (430px)
- 3 columns of cards
- 8-10px gaps
- Collapsible filters to save space
- Touch-optimized buttons (44px height minimum)
- Compact header with grid layout

## 🚀 Quick Start

### Use Without Cloud Sync (Just Local Storage)
1. Download `index.html`
2. Open in any browser
3. Start marking cards!
4. Data saves automatically in your browser

### Enable Cloud Sync (Optional)
1. Follow the setup steps in `FIREBASE_SETUP.md`
2. Update the Firebase config in `index.html`
3. Deploy to GitHub Pages
4. Your data syncs across all devices!

## 📋 Collection Stats

Track your progress:
- **Collected:** Number of cards you own
- **Total:** 45 cards in Generation 1
- **Spent:** Total amount paid for collected cards
- **Progress Bar:** Visual representation of collection completion

## 🔒 Data & Privacy

- ✅ **Local First:** Data saves to browser first
- ✅ **Cloud Backup:** Optional Firebase backup
- ✅ **Encrypted:** All data encrypted in transit
- ✅ **Private:** Anonymous auth - no login needed
- ✅ **No Ads:** No tracking, no telemetry

## 🛠 Technologies

- **HTML5** for structure
- **CSS3** with responsive design (mobile-first)
- **Vanilla JavaScript** (no frameworks)
- **Firebase** (optional cloud sync)
- **GitHub Pages** hosting

## 📱 Browser Support

Works on:
- ✅ Safari (iPhone/iPad)
- ✅ Chrome (Desktop/Mobile)
- ✅ Firefox (Desktop/Mobile)
- ✅ Edge (Desktop)
- ✅ Samsung Internet (Android)

## 🎮 How to Use

### Mark a Card Collected
1. Tap/Click the card
2. Click **"Mark collected"** button
3. Enter the price you paid
4. Card is saved!

### View Collection Details
- Tap the **Collected** filter to see only cards you own
- Search by name using the search box
- Click card images to zoom and inspect

### Manage Your Collection
- Use **Filters** button to show/hide filter options
- Toggle **🌙/☀️** button to switch dark/light mode
- Click **⟲** button to reset everything (requires typing "RESET")

### Cloud Sync
- Changes auto-save to the cloud (if Firebase is set up)
- Open on any device to see your collection
- Perfect for comparing collections with friends!

## 📦 Project Files

- `index.html` - Complete app (single file, easy to deploy)
- `README.md` - This file
- `FIREBASE_SETUP.md` - Firebase configuration guide
- `pokemon_cards_data.json` - Card data reference

## 🔧 Customization

Want to add more Pokémon generations?

1. Update the `sampleData` array in `index.html`
2. Add cards with: `id`, `name`, `generation`, `cardLink`, `imageUrl`
3. Update filter buttons for new generations
4. Deploy!

## 📈 Roadmap (Future Ideas)

- [ ] Add more Pokémon generations (Gen 2, 3, etc.)
- [ ] Import/export collection data (CSV)
- [ ] Collection value calculation (market prices)
- [ ] Share collections with friends
- [ ] Photo upload for card verification
- [ ] Wishlist feature

## 🐛 Troubleshooting

### Cards Not Saving?
- Check browser console (F12)
- Clear cache and refresh
- Try a different browser

### Cloud Sync Not Working?
- See `FIREBASE_SETUP.md` for troubleshooting
- App works fine with just localStorage
- Firebase is optional!

### Responsive Layout Issues?
- Close/open DevTools (F12) to refresh
- Try different screen orientation
- Clear browser cache

## 📄 License

Free to use, modify, and deploy for personal use.

## 🙏 Credits

- Pokémon data from TCGPlayer.com
- Card images from TCGPlayer CDN
- Built with ❤️ for Pokémon card collectors

## 💬 Questions?

Check out the Firebase setup guide in `FIREBASE_SETUP.md` or see the comments in `index.html` for code documentation.

---

**Happy collecting! 🎉**

Track your Pokédex cards, sync across all your devices, and manage your collection like a pro!
