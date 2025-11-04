#!/bin/bash
# Script to build RPM package (requires rpmbuild)
# Install on Fedora/RHEL: sudo dnf install rpm-build
# Install on Ubuntu: sudo apt install rpm

set -e

echo "=========================================="
echo "  Building PaprWall RPM Package"
echo "=========================================="
echo ""

# Check if rpmbuild is installed
if ! command -v rpmbuild &> /dev/null; then
    echo "ERROR: rpmbuild not found"
    echo ""
    echo "Install it with:"
    echo "  Fedora/RHEL: sudo dnf install rpm-build"
    echo "  Ubuntu/Debian: sudo apt install rpm"
    echo ""
    exit 1
fi

# Build the RPM
cd "$(dirname "$0")"
rpmbuild --define "_topdir $(pwd)/packaging/rpm" -ba packaging/rpm/SPECS/paprwall.spec

# Move RPM to root directory
if [ -f packaging/rpm/RPMS/x86_64/paprwall-1.0.2-1.*.rpm ]; then
    mv packaging/rpm/RPMS/x86_64/paprwall-1.0.2-1.*.rpm ./
    echo ""
    echo "✓ RPM package created successfully!"
    ls -lh paprwall-1.0.2-1.*.rpm
else
    echo ""
    echo "ERROR: RPM build failed"
    exit 1
fi
