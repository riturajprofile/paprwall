#!/bin/bash
# Quick setup script for Paprwall API keys

set -e

echo "🎨 Paprwall API Keys Setup"
echo "=========================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Copy example if it exists
if [ -f .env.example ]; then
    cp .env.example .env
    echo "✅ Created .env from .env.example"
else
    # Create new .env
    cat > .env << 'EOF'
# Paprwall API Keys Configuration
# Get free keys from the provider websites

# Pixabay API Key
# Get from: https://pixabay.com/api/docs/
PIXABAY_API_KEY=YOUR_PIXABAY_API_KEY_HERE

# Unsplash Access Key
# Get from: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY=YOUR_UNSPLASH_ACCESS_KEY_HERE

# Pexels API Key
# Get from: https://www.pexels.com/api/
PEXELS_API_KEY=YOUR_PEXELS_API_KEY_HERE
EOF
    echo "✅ Created .env file"
fi

echo ""
echo "📝 Setup Instructions:"
echo ""
echo "1. Get FREE API keys from:"
echo "   • Pixabay: https://pixabay.com/api/docs/"
echo "   • Unsplash: https://unsplash.com/developers"
echo "   • Pexels: https://www.pexels.com/api/"
echo ""
echo "2. Edit .env file and add your keys:"
echo "   nano .env"
echo ""
echo "3. Test your setup:"
echo "   paprwall --test pixabay"
echo "   paprwall --test pexels"
echo ""
echo "4. Fetch wallpapers:"
echo "   paprwall --fetch"
echo ""
echo "🔒 Security: The .env file is in .gitignore and won't be committed to git."
echo ""
