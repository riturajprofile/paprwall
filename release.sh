#!/usr/bin/env bash
#
# Quick release script for version 1.1.0
# Automates the release process
#
set -euo pipefail

VERSION="1.1.0"

echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall v${VERSION} Release            ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Must be run from project root"
    exit 1
fi

# Run pre-release checks
echo_info "Running pre-release checks..."
if ./prepare_release.sh; then
    echo_success "Pre-release checks passed"
else
    echo_warning "Some checks failed. Continue anyway? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo_info "Creating release for v${VERSION}"
echo ""

# Show what will be done
cat << EOF
This script will:
  1. Add all changes to git
  2. Commit with release message
  3. Create git tag v${VERSION}
  4. Show instructions for pushing

Your current git status:
EOF

git status --short
echo ""

# Confirm
echo_warning "Proceed with release? (y/N)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Release cancelled"
    exit 0
fi

echo ""

# Add all files
echo_info "Adding files to git..."
git add .
echo_success "Files added"

# Commit
echo_info "Creating commit..."
git commit -m "Release v${VERSION} - Distribution ready

- Added complete distribution system
- Fixed tkinter module not found error
- Enhanced installation experience
- Multi-distro support
- Comprehensive documentation
- Build and test scripts"

echo_success "Commit created"

# Create tag
echo_info "Creating tag v${VERSION}..."
git tag -a "v${VERSION}" -m "Release version ${VERSION}

New in this version:
- Complete distribution system with install.sh
- Fixed tkinter issues with proper venv setup
- Multi-distro support (Ubuntu, Fedora, Arch, etc.)
- Build scripts for packages and binaries
- Enhanced documentation

See CHANGELOG.md for full details."

echo_success "Tag created"

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║     Release Prepared! 🎉                  ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo_success "Git commit and tag created locally"
echo ""
echo "📝 Next steps:"
echo ""
echo "  1. Review the commit:"
echo "     git show HEAD"
echo ""
echo "  2. Push to GitHub:"
echo "     git push origin main"
echo "     git push origin v${VERSION}"
echo ""
echo "  3. Create GitHub Release:"
echo "     https://github.com/riturajprofile/paprwall/releases/new"
echo "     - Tag: v${VERSION}"
echo "     - Title: Paprwall v${VERSION} - Distribution Ready"
echo "     - Copy description from CHANGELOG.md"
echo ""
echo "  4. Optional - Build and attach binaries:"
echo "     ./build.sh"
echo "     ./build_binaries.sh"
echo "     # Then upload from dist/ folder"
echo ""
echo "  5. Test the one-line installer:"
echo "     curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash"
echo ""
echo "Installation link for users:"
echo "  ${BLUE}curl -fsSL https://raw.githubusercontent.com/riturajprofile/paprwall/main/install.sh | bash${NC}"
echo ""
