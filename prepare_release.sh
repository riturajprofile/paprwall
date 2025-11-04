#!/usr/bin/env bash
#
# Release preparation script
# Checks everything before creating a release
#
set -e

echo "╔═══════════════════════════════════════════╗"
echo "║     Paprwall Release Preparation          ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

ERRORS=0

check() {
    local desc="$1"
    shift
    
    printf "Checking: %-50s" "$desc"
    
    if "$@" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        ((ERRORS++))
        return 1
    fi
}

# Get version
VERSION=$(grep -E "version=\"[0-9.]+\"" setup.py | sed -E 's/.*version="([0-9.]+)".*/\1/')
echo_info "Preparing release for Paprwall v$VERSION"
echo ""

# Check git status
echo "📋 Git Status"
echo "─────────────────────────────────────────────"

if [ -n "$(git status --porcelain)" ]; then
    echo_warning "Working directory has uncommitted changes"
    git status --short
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo_success "Working directory is clean"
fi

# Check if we're on main branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    echo_warning "Not on main branch (current: $BRANCH)"
fi

echo ""

# Check version consistency
echo "🔢 Version Numbers"
echo "─────────────────────────────────────────────"

SETUP_VERSION=$(grep -E "version=\"[0-9.]+\"" setup.py | sed -E 's/.*version="([0-9.]+)".*/\1/')
PYPROJECT_VERSION=$(grep -E "^version = \"[0-9.]+\"" pyproject.toml | sed -E 's/.*version = "([0-9.]+)".*/\1/')

echo "setup.py:       $SETUP_VERSION"
echo "pyproject.toml: $PYPROJECT_VERSION"

if [ "$SETUP_VERSION" = "$PYPROJECT_VERSION" ]; then
    echo_success "Version numbers match"
else
    echo_error "Version mismatch!"
    ((ERRORS++))
fi

echo ""

# Check required files
echo "📁 Required Files"
echo "─────────────────────────────────────────────"

check "setup.py exists" test -f setup.py
check "pyproject.toml exists" test -f pyproject.toml
check "README.md exists" test -f README.md
check "LICENSE exists" test -f LICENSE
check "INSTALL.md exists" test -f INSTALL.md
check "install.sh exists" test -f install.sh
check "uninstall.sh exists" test -f uninstall.sh
check "requirements.txt exists" test -f requirements.txt
check "MANIFEST.in exists" test -f MANIFEST.in

echo ""

# Check scripts are executable
echo "🔐 Script Permissions"
echo "─────────────────────────────────────────────"

check "install.sh is executable" test -x install.sh
check "uninstall.sh is executable" test -x uninstall.sh
check "build.sh is executable" test -x build.sh
check "build_binaries.sh is executable" test -x build_binaries.sh
check "test.sh is executable" test -x test.sh
check "setup_venv.sh is executable" test -x setup_venv.sh

echo ""

# Check Python syntax
echo "🐍 Python Syntax"
echo "─────────────────────────────────────────────"

check "Python files compile" python3 -m py_compile src/paprwall/*.py src/paprwall/**/*.py

echo ""

# Check for TODO/FIXME
echo "📝 Code Quality"
echo "─────────────────────────────────────────────"

TODO_COUNT=$(grep -r "TODO\|FIXME" src/ --include="*.py" | wc -l || echo 0)
if [ "$TODO_COUNT" -gt 0 ]; then
    echo_warning "Found $TODO_COUNT TODO/FIXME comments"
    echo "Review these before release:"
    grep -rn "TODO\|FIXME" src/ --include="*.py" | head -5
    echo ""
else
    echo_success "No TODO/FIXME comments found"
fi

echo ""

# Check dependencies
echo "📦 Dependencies"
echo "─────────────────────────────────────────────"

check "requests available" python3 -c "import requests"
check "PIL available" python3 -c "from PIL import Image"
check "APScheduler available" python3 -c "from apscheduler.schedulers.background import BackgroundScheduler"

echo ""

# Summary
echo "═══════════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Ready to release v$VERSION"
    echo ""
    echo "Next steps:"
    echo ""
    echo "  1. Build packages:"
    echo "     ./build.sh"
    echo ""
    echo "  2. Test installation:"
    echo "     ./test.sh"
    echo ""
    echo "  3. Build binaries (optional):"
    echo "     ./build_binaries.sh"
    echo ""
    echo "  4. Commit and tag:"
    echo "     git add ."
    echo "     git commit -m \"Release v$VERSION\""
    echo "     git tag -a v$VERSION -m \"Release version $VERSION\""
    echo "     git push origin main"
    echo "     git push origin v$VERSION"
    echo ""
    echo "  5. Create GitHub release:"
    echo "     https://github.com/riturajprofile/paprwall/releases/new"
    echo ""
    exit 0
else
    echo -e "${RED}✗ $ERRORS check(s) failed${NC}"
    echo ""
    echo "Please fix the errors above before releasing."
    echo ""
    exit 1
fi
