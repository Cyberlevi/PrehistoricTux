# Garuda Linux test workflow

The repository now has a one-command local test path for the development PC.

## Play in UHD

From the repository root:

    bash scripts/run-garuda.sh

The launcher installs the current add-on tree into the user's SuperTux add-on directory, runs the static validator, then starts the prehistoric worldmap at 3840×2160 in fullscreen OpenGL developer mode with FPS display enabled.

## Open Level 01 in the editor

    bash scripts/edit-level-01.sh

## Parser-only smoke test

    bash scripts/smoke-test-supertux.sh

This uses SuperTux's own --resave option to force the engine to parse the level and worldmap. It is the quickest local check before a full playtest.

## Override executable

If the locally built binary is not named supertux2:

    SUPERTUX_BIN=/path/to/supertux2 bash scripts/run-garuda.sh

## What to inspect on the first manual run

- custom raptor, snake and flying hunter sprites actually resolve from the add-on
- checkpoint bells activate and respawn correctly
- both secret triggers increment the secret counter
- no jump is blind or impossible
- Palaszarusz becomes visible during the final camera pan
- 3840×2160 framing does not expose empty geometry or badly placed objects
- no collision box feels much larger or smaller than its creature silhouette

## Direct level testing

To bypass the worldmap and test a specific stage directly:

    bash scripts/play-level.sh 1

Use any number from 1 to 8. Each run writes a dedicated log under `diagnostics/level-N.log`. This is the fastest way to isolate runtime issues to a specific level.
