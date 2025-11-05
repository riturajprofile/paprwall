# Security Policy

## Supported Versions

We take security seriously and provide security updates for the following versions of PaprWall:

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |
| < 1.0   | :x:                |

**Note**: We recommend always using the latest version available on [PyPI](https://pypi.org/project/paprwall/) or [GitHub Releases](https://github.com/riturajprofile/paprwall/releases).

## Reporting a Vulnerability

We appreciate your efforts to responsibly disclose security vulnerabilities.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- **Primary**: riturajprofile.me@gmail.com
- **Alternative**: riturajprofile@outlook.com

**Subject Line**: `[SECURITY] Brief description of the issue`

### What to Include

Please include the following information in your report:
- Type of vulnerability (e.g., injection, XSS, authentication bypass)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability
- Suggested fix (if you have one)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Initial Response**: Within 7 days with our assessment
- **Updates**: We'll keep you informed about our progress every 7-14 days
- **Fix Timeline**: 
  - Critical vulnerabilities: 7-14 days
  - High severity: 30 days
  - Medium/Low severity: 60-90 days

### If Your Report is Accepted

- We'll work with you to understand and validate the issue
- We'll develop and test a fix
- We'll release a security update
- We'll credit you in the release notes (unless you prefer to remain anonymous)
- Your name will be added to our Security Hall of Fame

### If Your Report is Declined

- We'll explain why we don't consider it a security vulnerability
- We may suggest alternative channels (like a feature request or bug report)
- You're welcome to disagree and provide additional context

## Security Best Practices for Users

# Verify AppImage integrity
sha256sum -c PaprWall-2.1.1-x86_64.AppImage.sha256

### Safe Installation
```bash
# Always install from official sources
pip install paprwall  # From PyPI
# Or download from GitHub releases only
