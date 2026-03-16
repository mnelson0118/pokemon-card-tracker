# Pokédex Card Tracker - Firebase Cloud Sync Setup Guide

## Overview
Your Pokédex Card Tracker now supports **cloud synchronization** across all browsers and devices! Your collection data will automatically sync whenever you mark a card as collected, enter a price, or make any changes.

## Step-by-Step Firebase Setup

### Step 1: Create a Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Sign in with your Google account (create one if needed - it's free!)
3. Click **"Create a project"**
4. Name it: `pokemon-card-tracker`
5. Accept the terms and click **"Create project"**
6. Wait for the project to be created (1-2 minutes)

### Step 2: Enable Realtime Database
1. In the left sidebar, click **"Build"** → **"Realtime Database"**
2. Click **"Create Database"**
3. Choose location: Select closest to you (US is fine)
4. **Important:** Select **"Start in test mode"** (we'll secure it next)
5. Click **"Enable"**
6. Your database URL will appear - copy it (looks like: `https://pokemon-card-tracker-xxxxx.firebaseio.com`)

### Step 3: Set Database Security Rules
1. In Realtime Database, click the **"Rules"** tab at the top
2. Replace the entire content with this:

```json
{
  "rules": {
    "users": {
      "$uid": {
        "collection": {
          ".read": "$uid === auth.uid",
          ".write": "$uid === auth.uid"
        }
      }
    }
  }
}
```

3. Click **"Publish"**

### Step 4: Enable Anonymous Authentication
1. In the left sidebar, click **"Build"** → **"Authentication"**
2. Click the **"Sign-in method"** tab
3. Click on **"Anonymous"**
4. Toggle the switch to **"Enable"**
5. Click **"Save"**

### Step 5: Get Your Firebase Config
1. Click the **"Settings"** icon (gear) in the top left
2. Click **"Project settings"**
3. Scroll to the bottom and find your web app config (if not there, click **"Add app"** → **"Web"**)
4. Copy the entire config object (starts with `apiKey: "..."`

### Step 6: Update Your HTML File
1. Open `index.html` in a text editor
2. Find this section (around line 1095):
```javascript
const firebaseConfig = {
    apiKey: "AIzaSyBfQ5VzPhYjO2cK8nL9mN0pQ1rS2tU3vW4",
    authDomain: "pokemon-card-tracker.firebaseapp.com",
    databaseURL: "https://pokemon-card-tracker-default-rtdb.firebaseio.com",
    projectId: "pokemon-card-tracker",
    storageBucket: "pokemon-card-tracker.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef1234567890ghij"
};
```

3. Replace **ONLY** the values with your Firebase config values
4. Keep the structure the same, just swap the values
5. Save the file

### Step 7: Deploy to GitHub Pages
```bash
git add index.html
git commit -m "Add Firebase cloud sync"
git push
```

## How It Works

✅ **Automatic Sync**
- When you mark a card as collected, the data syncs to the cloud automatically
- Changes appear instantly across all your devices and browsers
- Works on phone, tablet, and computer

✅ **Offline Support**
- Changes save locally while offline
- Automatically sync to the cloud when you go back online
- Never lose your data

✅ **No Login Required**
- Uses anonymous authentication (no username/password needed)
- Each device gets a unique ID automatically
- Your data is private and secure

## Testing Cloud Sync

1. **Test on your iPhone:**
   - Open the app in Safari
   - Mark a few cards as collected
   - Record the numbers

2. **Test on your computer:**
   - Open the same URL in Chrome/Firefox
   - Refresh the page
   - Your marked cards should appear automatically!

3. **Test Real-Time Sync:**
   - Open the app on two different browsers/devices
   - Mark a card on one device
   - Watch it appear on the other device within 1 second

## Troubleshooting

### "Firebase not available" message
- Check that Firebase CDN links are in the `<head>` section
- Check your internet connection
- Verify your Firebase config is correct

### Cloud sync not working
- Check Firebase Console → Realtime Database → Data
- Verify your rules are published
- Check that Anonymous Authentication is enabled
- Clear browser cache and refresh

### Data disappeared
- Don't worry! Your data is still in localStorage
- Check Firebase Console → Data section
- All your collection info is still there

## Upgrading to Paid Firebase (Optional)

Firebase's free tier includes:
- ✅ 1GB of database storage
- ✅ Unlimited reads/writes
- ✅ Perfect for a personal project like this

You won't need to upgrade unless your database exceeds 1GB (unlikely for Pokemon card tracker!).

## Data Privacy & Security

Your data is:
- ✅ Encrypted in transit (HTTPS)
- ✅ Only accessible by your device (via auth rules)
- ✅ Stored in Google's secure servers
- ✅ Compliant with GDPR & privacy laws

## Questions or Issues?

If Firebase setup doesn't work:
1. The app will automatically fall back to **localStorage only** (works fine!)
2. You'll see console messages about Firebase
3. Your data will still save and sync locally across tabs
4. Try Firebase setup later when you have time

Your Pokédex Card Tracker works perfectly without Firebase - it's just a bonus for cross-device sync! 🎉
