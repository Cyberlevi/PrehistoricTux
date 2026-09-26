#!/usr/bin/env bash
set -euo pipefail

declare -A COMMAND_PACKAGES=(
  [cmake]=cmake
  [git]=git
  [ninja]=ninja
  [pkg-config]=pkgconf
)

missing=0
for cmd in "${!COMMAND_PACKAGES[@]}"; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf 'OK      %-12s %s\n' "$cmd" "$(command -v "$cmd")"
  else
    printf 'MISSING %-12s package: %s\n' "$cmd" "${COMMAND_PACKAGES[$cmd]}"
    missing=1
  fi
done

echo
echo "Checking key development libraries with pkg-config when available..."
if command -v pkg-config >/dev/null 2>&1; then
  for pc in sdl3 SDL3_image SDL3_ttf freetype2 libcurl glew harfbuzz fribidi glm libavif vorbisfile physfs fmt; do
    if pkg-config --exists "$pc" 2>/dev/null; then
      printf 'OK      pkg-config %-16s %s\n' "$pc" "$(pkg-config --modversion "$pc" 2>/dev/null || true)"
    else
      printf 'CHECK   pkg-config %-16s not detected\n' "$pc"
    fi
  done
fi

echo
if [[ "$missing" -ne 0 ]]; then
  echo "Essential build commands are missing."
  echo "Run:"
  echo "  bash scripts/setup-garuda-uhd-build.sh"
  exit 1
fi

echo "Essential build commands are present."
