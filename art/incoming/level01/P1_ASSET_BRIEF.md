# Level 01 — Priority 1 UHD art brief

This is the first production-art gate for PrehistoricTux.

## Raptor set

Runtime logical size: **64×48**  
Minimum source frame: **256×192**  
Required frames:

1. `raptor-walk-0@4x.png`
2. `raptor-walk-1@4x.png`
3. `raptor-walk-2@4x.png`
4. `raptor-walk-3@4x.png`
5. `raptor-squished@4x.png`

**Canonical facing direction: RIGHT.** The sprite definition uses these source frames for rightward movement and mirrors them for leftward movement.

The production raptor is a lean feathered prehistoric hunter. It should look dangerous and athletic without gore or exaggerated monster anatomy. Keep a stable side-view camera, consistent body volume and a clean transparent background. The walk cycle must keep the feet on a stable floor line so the sprite does not visually bounce.

Do not bake a ground shadow into the PNG. Do not use text, borders, glow outlines or scenery inside the sprite frame.

A horizontal five-frame sprite sheet may be supplied to `scripts/slice-raptor-sheet.py`. Each cell must have a 4:3 aspect ratio and be at least 256×192.

## Jungle terrain

Runtime logical tile: **32×32**  
Minimum source tile: **128×128**

Required:

- `jungle-fill@4x.png`
- `jungle-top@4x.png`

The fill tile should read as dark moist prehistoric soil with roots, stone fragments and restrained organic detail. It must not create a fake walkable edge.

The top tile should have a clearly readable upper platform edge with roots, moss and fern fragments, while still joining the fill tile naturally underneath.

Both tiles must be fully opaque. Horizontal seams should be visually continuous.

## Workflow

Place/export files under the exact paths in `art/level01-production.json`, then run:

    python scripts/level01-p1-qa.py
    python scripts/promote-level01-art.py --priority 1 --dry-run

Only after QA passes:

    python scripts/promote-level01-art.py --priority 1
    python scripts/level01-art-status.py
    python scripts/uhd-audit.py

Finally test in-engine:

    bash scripts/play-level.sh 1
