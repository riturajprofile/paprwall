#!/bin/bash
# PyPI Upload Script
# This script uploads the built package to PyPI using the stored token

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}PaprWall PyPI Upload Script${NC}"
echo "================================"

# Check if token exists
TOKEN_FILE=".secrets/pypi_token.txt"
if [ ! -f "$TOKEN_FILE" ]; then
    echo -e "${RED}Error: PyPI token not found at $TOKEN_FILE${NC}"
    exit 1
fi

# Read token
PYPI_TOKEN=$(cat "$TOKEN_FILE")

# Check if dist directory exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist/*.whl dist/*.tar.gz 2>/dev/null)" ]; then
    echo -e "${YELLOW}No distribution files found. Building package...${NC}"
    python -m build
fi

# Check the distribution
echo -e "\n${YELLOW}Checking distribution files...${NC}"
twine check dist/*

if [ $? -ne 0 ]; then
    echo -e "${RED}Distribution check failed. Please fix the errors and try again.${NC}"
    exit 1
fi

# Ask for confirmation
echo -e "\n${YELLOW}Ready to upload to PyPI${NC}"
echo "Files to upload:"
ls -lh dist/*.whl dist/*.tar.gz

echo -e "\n${YELLOW}Do you want to proceed? (y/n)${NC}"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${RED}Upload cancelled${NC}"
    exit 0
fi

# Upload to PyPI
echo -e "\n${GREEN}Uploading to PyPI...${NC}"
TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_TOKEN" twine upload dist/*

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Successfully uploaded to PyPI!${NC}"
    echo -e "Your package is now available at: ${GREEN}https://pypi.org/project/paprwall/${NC}"
    echo -e "\nUsers can install with: ${GREEN}pip install paprwall${NC}"
else
    echo -e "\n${RED}❌ Upload failed. Check the error messages above.${NC}"
    exit 1
fi
