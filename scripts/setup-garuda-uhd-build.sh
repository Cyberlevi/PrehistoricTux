#!/usr/bin/env bash
set -euo pipefail

if ! command -v pacman >/dev/null 2>&1; then
  echo "This helper is intended for Garuda/Arch Linux (pacman not found)." >&2
  exit 1
fi

PACKAGES=(
  cmake
  ninja
  base-devel
  libogg
  libvorbis
  openal
  sdl2
  sdl2_image
  sdl2_ttf
  freetype2
  libraqm
  curl
  openssl
  glew
  harfbuzz
  fribidi
  glm
  zlib
  fmt
  physfs
  git
)

echo "Installing/confirming SuperTux UHD build dependencies on Garuda/Arch..."
sudo pacman -S --needed "${PACKAGES[@]}"

echo
echo "Dependencies ready."
echo "Starting the isolated patched SuperTux 0.7.0 UHD build..."
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/build-uhd-engine.sh"
