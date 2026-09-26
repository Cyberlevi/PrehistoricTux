#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE_ROOT="$ROOT/.engine"
SRC="$ENGINE_ROOT/supertux-0.7.0-uhd"
BUILD="$ENGINE_ROOT/build-0.7.0-uhd"
PATCHER="$ROOT/scripts/apply-uhd-engine-patch.py"
PATCH_SHA="$(sha256sum "$PATCHER" | awk '{print $1}')"
PATCH_MARKER="$BUILD/.prehistorictux-uhd-patch.sha256"
LOGDIR="$ROOT/diagnostics"
LOG="$LOGDIR/uhd-engine-build.log"

mkdir -p "$LOGDIR"
exec > >(tee "$LOG") 2>&1

for tool in git cmake; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required build tool: $tool" >&2
    if command -v pacman >/dev/null 2>&1; then
      echo >&2
      echo "Garuda/Arch detected. Install the full build dependency set with:" >&2
      echo "  bash scripts/setup-garuda-uhd-build.sh" >&2
    fi
    exit 1
  fi
done

mkdir -p "$ENGINE_ROOT"

if [[ ! -d "$SRC/.git" ]]; then
  git clone --branch v0.7.0 --depth 1 https://github.com/SuperTux/supertux.git "$SRC"
fi

git -C "$SRC" fetch --tags --depth 1 origin v0.7.0
git -C "$SRC" reset --hard v0.7.0
git -C "$SRC" clean -fd
git -C "$SRC" submodule update --init --recursive

python "$PATCHER" "$SRC"

GENERATOR=()
if command -v ninja >/dev/null 2>&1; then
  GENERATOR=(-G Ninja)
fi

cmake -S "$SRC" -B "$BUILD" \
  "${GENERATOR[@]}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_OPENGL=ON \
  -DENABLE_DISCORD=OFF \
  -DBUILD_DOCUMENTATION=OFF

cmake --build "$BUILD" --parallel "$(nproc)"
printf '%s\n' "$PATCH_SHA" > "$PATCH_MARKER"

echo
echo "Patched UHD SuperTux build complete."
echo "Binary: $BUILD/supertux2"
echo "Build log: $LOG"
echo "Patch fingerprint: $PATCH_SHA"
echo
echo "Run PrehistoricTux with:"
echo "  SUPERTUX_BIN=$BUILD/supertux2 bash scripts/run-garuda.sh"
