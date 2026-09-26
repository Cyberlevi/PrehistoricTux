#!/usr/bin/env bash
set -euo pipefail

if ! command -v pacman >/dev/null 2>&1; then
  echo "This helper is intended for Garuda/Arch Linux." >&2
  exit 1
fi

sudo pacman -S --needed python-pillow

echo
echo "Art tool ready."
echo "Generate and QA the Level 01 P1 candidate with:"
echo "  python scripts/generate-level01-p1-candidate.py"
echo
echo "Generate, QA and activate it with:"
echo "  python scripts/generate-level01-p1-candidate.py --promote"
