# PrehistoricTux add-on source

This directory is the first playable-content target for SuperTux.

## Development target

The current upstream SuperTux repository has moved on to 0.7.x development. PrehistoricTux therefore targets the current level format (version 3) and uses only stock objects/assets during the bootstrap phase. Original prehistoric art replaces placeholders progressively.

## Local smoke-test workflow

1. Install/build a compatible SuperTux.
2. Open the built-in level editor.
3. Open `addon/levels/prehistoric_tux/01_lost_egg_valley.stl`.
4. Play-test from the editor.
5. Package the add-on with SuperTux's built-in **Package Add-on** flow once the worldmap is added.

The first level intentionally uses stock engine assets as placeholders so gameplay geometry can be tested before final dinosaur artwork lands.
