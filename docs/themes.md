# Theme Selection Guide

## Overview

You can now choose what type of wallpapers you want! The app supports **12 predefined themes** plus **custom search queries**.

---

## 🎨 Available Themes

### 1. **nature** (default)
Natural landscapes and outdoor scenes
- Keywords: nature, landscape, scenery

### 2. **city**
Urban landscapes and cityscapes
- Keywords: city, urban, architecture, skyline

### 3. **minimal**
Minimalist and clean designs
- Keywords: minimal, abstract, simple, clean

### 4. **space**
Space and astronomy
- Keywords: space, galaxy, nebula, stars, cosmos

### 5. **ocean**
Ocean and coastal scenes
- Keywords: ocean, sea, beach, waves, water

### 6. **mountains**
Mountain landscapes
- Keywords: mountains, peaks, alpine, summit

### 7. **sunset**
Sunset and sunrise scenes
- Keywords: sunset, sunrise, dusk, dawn, golden hour

### 8. **animals**
Wildlife and animals
- Keywords: animals, wildlife, nature, fauna

### 9. **forest**
Forest and woodland scenes
- Keywords: forest, trees, woods, jungle

### 10. **abstract**
Abstract art and patterns
- Keywords: abstract, pattern, texture, art

### 11. **flowers**
Flowers and botanical scenes
- Keywords: flowers, floral, botanical, garden

### 12. **dark**
Dark and moody wallpapers
- Keywords: dark, night, black, moody

---

## 📋 How to Use

### View All Themes

```bash
riturajprofile-wallpaper --themes
```

### Check Current Theme

```bash
riturajprofile-wallpaper --current-theme
```

### Set a Theme

```bash
# Set to space theme
riturajprofile-wallpaper --set-theme space

# Set to ocean theme
riturajprofile-wallpaper --set-theme ocean

# Set to city theme
riturajprofile-wallpaper --set-theme city
```

### Fetch Wallpapers with New Theme

```bash
# After setting theme, fetch new images
riturajprofile-wallpaper --fetch
```

### Use Custom Search Query

Want something specific? Use a custom query:

```bash
# Search for mountains and lakes
riturajprofile-wallpaper --custom-query "mountains lakes"

# Search for cyberpunk cities
riturajprofile-wallpaper --custom-query "cyberpunk neon city"

# Search for autumn scenes
riturajprofile-wallpaper --custom-query "autumn fall colors"

# Then fetch
riturajprofile-wallpaper --fetch
```

---

## 🖼️ Complete Workflow

```bash
# 1. See available themes
riturajprofile-wallpaper --themes

# 2. Set your preferred theme
riturajprofile-wallpaper --set-theme space

# 3. Fetch wallpapers with that theme
riturajprofile-wallpaper --fetch

# 4. Enjoy! Wallpaper will rotate automatically

# 5. Change theme anytime
riturajprofile-wallpaper --set-theme ocean
riturajprofile-wallpaper --fetch
```

---

## 🎯 Examples

### Get Space Wallpapers

```bash
riturajprofile-wallpaper --set-theme space
riturajprofile-wallpaper --fetch
```

### Get Minimal/Clean Wallpapers

```bash
riturajprofile-wallpaper --set-theme minimal
riturajprofile-wallpaper --fetch
```

### Get Sunset Wallpapers

```bash
riturajprofile-wallpaper --set-theme sunset
riturajprofile-wallpaper --fetch
```

### Get Custom "Tokyo Night" Wallpapers

```bash
riturajprofile-wallpaper --custom-query "tokyo night cityscape"
riturajprofile-wallpaper --fetch
```

---

## ⚙️ Configuration File

Themes are stored in: `~/.config/riturajprofile-wallpaper/preferences.json`

```json
{
  "theme": "space",
  "custom_query": ""
}
```

You can also edit this file directly!

---

## 💡 Tips

1. **Mix and Match**: Each source (Pixabay, Pexels) will use your theme
2. **Custom Queries**: Use custom queries for very specific wallpapers
3. **Theme Persistence**: Your theme choice is saved and used for daily fetches
4. **Change Anytime**: Switch themes as often as you like
5. **Quality**: All images are fetched in high resolution (min 1920px width)

---

## 🔄 Daily Auto-Fetch

When auto-fetch runs daily, it uses your current theme setting. So if you set theme to "ocean", every day you'll get new ocean wallpapers!

---

## 📱 GUI Support

The theme selector will also be available in the GUI:
- Dropdown menu with all themes
- Custom query input field
- "Apply" button to fetch with new theme
- Preview of current theme

---

## 🌟 Theme Combinations

You can create interesting combinations:

```bash
# Morning routine: sunset theme
riturajprofile-wallpaper --set-theme sunset

# Work hours: minimal theme  
riturajprofile-wallpaper --set-theme minimal

# Evening: space theme
riturajprofile-wallpaper --set-theme space
```

---

**Enjoy your personalized wallpapers!** 🎨
