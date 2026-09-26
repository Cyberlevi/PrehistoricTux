# PrehistoricTux Status

Updated: 2026-09-26

## Runtime / engine

- Patched SuperTux engine builds successfully from pinned v0.7.0 source.
- Patched binary reports `supertux2 v0.7.0`.
- Static validation passes for all campaign levels, the worldmap, dev scale test, sprites, surfaces, tilesets, Squirrel scripts and add-on metadata.
- Patched-engine parser/resave smoke test passes **10/10** files:
  - 8 campaign levels
  - 1 UHD surface-scale dev level
  - 1 worldmap
- The earlier SuperTux 0.7.0 headless resave crash was avoided by skipping gameplay Player construction during resave initialization.
- Visual logical-scale test launches after validation. Manual visual confirmation is still required before closing the UHD-engine verification issue.

## UHD art

- Runtime art is routed through `.surface` bindings.
- Current production audit: **0/52 active bindings are genuinely UHD-ready**.
- Existing PNGs remain gameplay prototypes.
- Target master scale: **4×** for gameplay art.
- Full-screen background target: **3840×2160 minimum**.

## Current milestone

1. Confirm the visual scale test: the right raptor must render at exactly half the logical size of the left raptor.
2. Begin the Level 01 production art pass.
3. Promote genuine 4× assets through `scripts/promote-uhd-source.py`.
4. Re-run `python scripts/uhd-audit.py` after every promoted asset.
5. Keep PR #1 draft until visual/runtime playtesting is complete.
