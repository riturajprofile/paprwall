# API Keys Security Guide

## 🔒 Keeping Your API Keys Secure

**IMPORTANT**: This is an open-source project. Never commit API keys to the repository!

## How API Keys Are Handled

### 1. Default Keys (Placeholders Only)
The file `src/riturajprofile_wallpaper/config/default_keys.py` contains **placeholder values only**:
```python
DEFAULT_API_KEYS = {
    "pixabay": {
        "api_key": "YOUR_PIXABAY_API_KEY_HERE"
    }
}
```

These placeholders will NOT work. Users must provide their own keys.

### 2. User Configuration (Secure & Private)
When users install Paprwall, they add their own keys to:
```
~/.config/riturajprofile-wallpaper/api_keys.json
```

This file:
- ✅ Is in the user's home directory (private)
- ✅ Is NOT in the git repository
- ✅ Is listed in `.gitignore`
- ✅ Never gets committed or shared

### 3. Git Ignore Protection
The `.gitignore` file blocks these patterns:
```
**/api_keys.json
**/*_keys.json
*api_key*
*.env
.env
*.secret
```

This prevents accidental commits of API keys.

## For Contributors

### If You're Contributing Code:

1. **Never** add real API keys to code files
2. **Always** use placeholder values like `"YOUR_API_KEY_HERE"`
3. **Test** with your own keys in `~/.config/riturajprofile-wallpaper/api_keys.json`
4. **Check** `.gitignore` before committing

### Getting Your Own API Keys (Free):

1. **Pixabay**: https://pixabay.com/api/docs/
   - Sign up for free account
   - Navigate to API section
   - Copy your API key

2. **Unsplash**: https://unsplash.com/developers
   - Create a free developer account
   - Register a new application
   - Copy your Access Key

3. **Pexels**: https://www.pexels.com/api/
   - Create free account
   - Generate API key
   - Copy your key

### Setting Up Your Local Keys:

```bash
# 1. Install the package
pip install -e .

# 2. Create config directory (if not exists)
mkdir -p ~/.config/riturajprofile-wallpaper/

# 3. Copy example file
cp api_keys.json.example ~/.config/riturajprofile-wallpaper/api_keys.json

# 4. Edit with your real keys
nano ~/.config/riturajprofile-wallpaper/api_keys.json
```

Example `~/.config/riturajprofile-wallpaper/api_keys.json`:
```json
{
  "pixabay": {
    "api_key": "12345678-abcdef1234567890abcdef12",
    "attribution_required": true
  },
  "unsplash": {
    "access_key": "abcdefghijklmnopqrstuvwxyz1234567890",
    "attribution_required": true
  },
  "pexels": {
    "api_key": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0",
    "attribution_required": true
  }
}
```

## For Maintainers

### Before Committing:

```bash
# Check for any API keys in staged files
git diff --cached | grep -i "api.*key"

# Check for sensitive files
git status | grep -E "api_keys|\.env|secret"

# Review .gitignore
cat .gitignore | grep -i key
```

### If API Keys Are Accidentally Committed:

1. **Remove from history**:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Revoke the compromised keys immediately**

3. **Generate new keys**

4. **Force push** (if already pushed to remote):
   ```bash
   git push origin --force --all
   ```

## For Users

### First-Time Setup:

After installing Paprwall:

```bash
# The app will prompt you for API keys on first run
paprwall --fetch

# Or manually create the config file:
paprwall-gui  # GUI will help you set up keys
```

### Adding Keys via GUI:

1. Launch: `paprwall-gui`
2. Go to: **Settings → API Keys**
3. Click: **Add Key** for each service
4. Paste your keys
5. Click: **Save**

### Adding Keys Manually:

1. Get your API keys (free) from provider websites
2. Edit `~/.config/riturajprofile-wallpaper/api_keys.json`
3. Save the file
4. Restart Paprwall if running

## Rate Limits

Free API keys have these typical limits:

- **Pixabay**: 5,000 requests/month
- **Unsplash**: 50 requests/hour (Demo), 5,000/hour (Production)
- **Pexels**: 200 requests/hour

For higher limits, consider API key upgrades from the providers.

## Security Best Practices

### ✅ DO:
- Use the config file in your home directory
- Keep keys private
- Use `.gitignore` patterns
- Revoke compromised keys immediately
- Use separate keys for development/production

### ❌ DON'T:
- Commit keys to git
- Share keys publicly
- Hardcode keys in source files
- Use production keys for testing
- Reuse keys across projects

## Environment Variables & .env File (Alternative Methods)

### Method 1: .env File (Recommended for Development)

Create a `.env` file in your project directory:

```bash
# Copy example template
cp .env.example .env

# Edit with your real keys
nano .env
```

Example `.env` file:
```bash
# Paprwall API Keys Configuration
PIXABAY_API_KEY=your_pixabay_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
PEXELS_API_KEY=your_pexels_key_here
```

**Locations checked (in order):**
1. Current working directory: `./env`
2. Home directory: `~/.env`
3. Config directory: `~/.config/riturajprofile-wallpaper/.env`

### Method 2: System Environment Variables

You can also export environment variables:

```bash
export PIXABAY_API_KEY="your-key-here"
export PEXELS_API_KEY="your-key-here"
export UNSPLASH_ACCESS_KEY="your-key-here"

paprwall --fetch
```

Or add to your shell profile (`~/.bashrc` or `~/.zshrc`):
```bash
# Paprwall API Keys
export PIXABAY_API_KEY="your_pixabay_key_here"
export UNSPLASH_ACCESS_KEY="your_unsplash_key_here"
export PEXELS_API_KEY="your_pexels_key_here"
```

### Priority Order:

The app loads API keys in this priority:

1. **Environment variables** (`.env` file or system `export`)
2. **User config file** (`~/.config/riturajprofile-wallpaper/api_keys.json`)
3. **Default placeholders** (won't work - users must provide keys)

**Note:** `.env` files are automatically ignored by git (in `.gitignore`).

## Troubleshooting

### "Invalid API Key" Error:
1. Check key is correct in config file
2. Verify no extra spaces or quotes
3. Ensure JSON format is valid
4. Check key hasn't expired

### Keys Not Loading:
```bash
# Check config file exists
ls -la ~/.config/riturajprofile-wallpaper/api_keys.json

# Verify JSON syntax
cat ~/.config/riturajprofile-wallpaper/api_keys.json | python3 -m json.tool

# Check permissions
chmod 600 ~/.config/riturajprofile-wallpaper/api_keys.json
```

## Questions?

- **GitHub Issues**: https://github.com/riturajprofile/paprwall/issues
- **Email**: riturajprofile.me@gmail.com

---

**Remember**: API keys are like passwords. Keep them secret, keep them safe! 🔐
