# PrehistoricTux

A prehistoric platform adventure built as a SuperTux 2 add-on prototype.

## Current status

The repository now contains a connected **eight-level campaign scaffold**, a custom prehistoric worldmap, original prehistoric prototype art, custom terrain, scripted story beats, hazards, checkpoints, secrets, moving platforms, wind sections, animated lava and a scripted Palaszarusz boss encounter.

The next critical milestone is a real SuperTux runtime smoke-test on the Garuda Linux development machine and fixing any parser/runtime incompatibilities found there.

## Campaign

1. **The Valley of the Lost Egg** — jungle, cave and volcanic approach; first Palaszarusz sighting.
2. **Fernwood Canopy** — high routes, canopy gaps and mixed ground/air pressure.
3. **Serpent Caves** — snakes, falling rock hazards and dark cave traversal.
4. **Pterosaur Cliffs** — timed wind gusts, moving platforms and heavy aerial pressure.
5. **Obsidian River** — animated lava, obsidian moving slabs and volcanic hazards.
6. **Bonefield at Dusk** — fossil fields, twilight atmosphere and open predator encounters.
7. **Nesting Grounds** — mixed-biome nesting area and the final Palaszarusz/egg sighting.
8. **Palaszarusz Crater** — volcanic approach and a three-phase scripted boss prototype.

## Original project assets

Current prototype art includes:
- raptor-like ground hunter
- ancient snake
- flying prehistoric hunter
- neutral Spinosaurus
- caveman guide
- prehistoric checkpoint totems
- jungle / cave / cliff / volcanic terrain
- animated lava
- fossil and nesting-ground scenery
- Palaszarusz idle / roar / charge art
- stolen egg story asset

These are gameplay-production prototypes, not the final UHD art pass.

## Development target

- Engine base: current SuperTux 2 level/add-on system
- Level format: version 3
- Primary development platform: Linux / Garuda Linux
- Presentation target: UHD/4K-friendly art and resolution-independent gameplay

## Local test

Install the current development add-on and run all static/parser smoke tests:

    bash scripts/smoke-test-supertux.sh

Launch the worldmap in UHD developer mode:

    bash scripts/run-garuda.sh

Open Level 01 directly in the SuperTux editor:

    bash scripts/edit-level-01.sh

Launch any campaign level directly, bypassing the worldmap:

    bash scripts/play-level.sh 1

Use a number from 1 to 8. Runtime logs are written under `diagnostics/`.

If the binary is not named `supertux2`, set `SUPERTUX_BIN` to the executable path.

## Licensing

SuperTux engine code and upstream data retain their upstream licenses. Original PrehistoricTux prototype art is tracked separately and is intended to use CC-BY-SA-4.0 unless a file/directory says otherwise. See `LICENSE-ASSETS.md` and `docs/UPSTREAM_REVIEW.md`.
