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
- Current production audit on the Garuda target machine: **7/52 active bindings are UHD-ready**.
- Existing PNGs remain gameplay prototypes.
- Target master scale: **4×** for gameplay art.
- Full-screen background target: **3840×2160 minimum**.

## Current milestone

A concrete **24-asset Level 01 production queue** is tracked in `art/level01-production.json`. The first P1 batch has now passed target-machine QA and promotion: **7/24 ready (29.2%)**.

Priority 1:
- 5 raptor runtime frames
- jungle fill/top terrain

Priority 2:
- snake
- pterosaur
- caveman

Priority 3:
- checkpoint
- broken nest
- distant sauropod
- distant volcano

Promotion is batchable through `scripts/promote-level01-art.py`, while `scripts/level01-art-status.py` reports vertical-slice completion independently of the global 52-binding audit.

Remaining engine gate: visually confirm the dedicated scale test. The right raptor must render at exactly half the logical size of the left raptor.


## Deterministic P1 candidate generator

The repository can now generate the first seven Level 01 UHD candidate assets locally instead of waiting on manually prepared binary artwork.

Garuda setup:

    bash scripts/setup-garuda-art-tools.sh

Generate + QA only:

    python scripts/generate-level01-p1-candidate.py

Generate + QA + activate the P1 runtime bindings:

    python scripts/generate-level01-p1-candidate.py --promote

The generator authors the raptor and jungle artwork directly at the 4× runtime-source sizes. It is not a mechanical enlargement of the old prototype PNGs. The generated set still remains a replaceable production candidate: any later artist/image-generation export can go through the same P1 QA and promotion pipeline.


## P1 one-command visual gate

After the patched UHD engine and Pillow are installed:

    bash scripts/test-level01-p1.sh

This command generates the seven Priority-1 assets, runs QA, promotes them into the local runtime bindings, renders an actual-asset contact sheet at `art/incoming/level01/P1_PREVIEW.png`, revalidates the content, and launches Level 01 through the patched UHD engine.

To revert only the local P1 runtime promotion while preserving incoming source exports:

    bash scripts/reset-level01-p1-runtime.sh

Important: promoted 4× sources must be tested with `scripts/play-uhd-level.sh`, not the stock SuperTux binary, because stock 0.7.0 ignores the logical `.surface` scale field.


## Target-machine P1 verification

The first Level 01 production batch has now been exercised on the Garuda workstation:

- Pillow/tooling setup succeeded
- all 7 Priority-1 assets were generated
- P1 art QA passed
- raptor floor-line drift measured **0.0%**
- dry-run promotion accepted **7/7**
- runtime promotion completed **7/7**
- Level 01 status reached **7/24 (29.2%)**
- global UHD audit reached **7/52**
- structural validation passed after promotion
- Level 01 launched through the patched UHD engine without an immediate runtime/parser failure

Remaining manual gate: visual approval of the actual in-game raptor/jungle appearance. The generated P1 set is still a replaceable production candidate, not locked final art.
