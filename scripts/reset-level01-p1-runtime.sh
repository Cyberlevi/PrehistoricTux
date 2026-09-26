#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SURFACES=(
  addon/images/prehistoric/creatures/raptor/raptor-walk-0.surface
  addon/images/prehistoric/creatures/raptor/raptor-walk-1.surface
  addon/images/prehistoric/creatures/raptor/raptor-walk-2.surface
  addon/images/prehistoric/creatures/raptor/raptor-walk-3.surface
  addon/images/prehistoric/creatures/raptor/raptor-squished.surface
  addon/images/prehistoric/terrain/jungle-fill.surface
  addon/images/prehistoric/terrain/jungle-top.surface
)

GENERATED_RUNTIME=(
  addon/images/prehistoric/creatures/raptor/raptor-walk-0@4x.png
  addon/images/prehistoric/creatures/raptor/raptor-walk-1@4x.png
  addon/images/prehistoric/creatures/raptor/raptor-walk-2@4x.png
  addon/images/prehistoric/creatures/raptor/raptor-walk-3@4x.png
  addon/images/prehistoric/creatures/raptor/raptor-squished@4x.png
  addon/images/prehistoric/terrain/jungle-fill@4x.png
  addon/images/prehistoric/terrain/jungle-top@4x.png
)

echo "Restoring tracked P1 surface bindings to the branch version..."
git restore -- "${SURFACES[@]}"

echo "Removing generated runtime P1 PNGs..."
rm -f -- "${GENERATED_RUNTIME[@]}"

echo
echo "P1 runtime art reset to the repository state."
echo "Incoming source exports under art/incoming/level01 are intentionally preserved."
