#!/usr/bin/env bash
set -euo pipefail

echo "==> Detecting package manager..."
detect_pm() {
  if command -v apt-get >/dev/null 2>&1; then echo apt; return; fi
  if command -v dnf >/dev/null 2>&1; then echo dnf; return; fi
  if command -v yum >/dev/null 2>&1; then echo yum; return; fi
  if command -v pacman >/dev/null 2>&1; then echo pacman; return; fi
  if command -v zypper >/dev/null 2>&1; then echo zypper; return; fi
  echo none
}
PM="$(detect_pm)"
echo "   -> $PM"

install_pkgs() {
  local pkgs="$*"
  case "$PM" in
    apt)
      sudo apt-get update -y
      sudo apt-get install -y $pkgs
      ;;
    dnf|yum)
      sudo "$PM" install -y $pkgs
      ;;
    pacman)
      sudo pacman -Sy --noconfirm $pkgs
      ;;
    zypper)
      sudo zypper install -y $pkgs
      ;;
    *)
      echo "WARN: Unknown package manager. Please install: $pkgs" >&2
      ;;
  esac
}

echo "==> Ensuring Python, venv, and Tkinter are available..."
case "$PM" in
  apt)    install_pkgs python3 python3-venv python3-tk ;;
  dnf|yum)install_pkgs python3 python3-venv python3-tkinter ;;
  pacman) install_pkgs python tk ;;        # venv is in python, tkinter provided by tk
  zypper) install_pkgs python3 python3-venv python3-tk ;;
  none)   echo "Please install python3 + venv + tkinter manually, then re-run."; exit 1 ;;
esac

echo "==> Creating virtual environment (.venv)..."
python3 -m venv .venv

echo "==> Activating venv and installing paprwall..."
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
# Editable install so changes in the repo reflect immediately
pip install -e .

echo "==> Done."
echo
echo "Try these commands now (in this shell with venv active):"
echo "  wallpaper-gui                 # Launch Tkinter GUI"
echo "  wallpaper-manager --help      # Simple CLI (URL/local/history)"
echo "  paprwall --help               # Advanced rotating CLI (online sources)"
echo
echo "To activate the venv in future terminals:"
echo "  source .venv/bin/activate"
