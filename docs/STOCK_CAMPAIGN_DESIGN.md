# PrehistoricTux — Stock SuperTux Campaign

## Direction

This branch intentionally uses only the official SuperTux 0.7.0 runtime asset set.
No custom sprites, UHD engine patches or custom tilesets are required.

## Level design rules

1. Every secret must be spatially believable: behind a wall, above a ceiling,
   below a bridge, inside a side cave, or unlocked by a switch.
2. Coins lead the player toward useful movement lines, optional routes and secrets.
   They are not scattered randomly in empty space.
3. Enemy choice follows the room geometry. Jumping enemies belong where vertical
   timing matters; cannons and mines belong in controlled approach lanes.
4. Each level has a dominant biome, matching background layers and matching music.
5. Difficulty is taught, then combined, then tested.
6. Checkpoints come after substantial challenges, not before every hazard.
7. Camera tricks are used only to support visibility or reveal a set-piece.
8. Main path, optional challenge route and secret route must remain visually distinct.

## Campaign structure

1. Frostline Ascent — movement fundamentals, vertical routes, first hidden wall.
2. Frozen Outpost — switches, cannons, mines, door logic, layered enemy pressure.
3. Crystal Descent — cave navigation, falling hazards and constrained combat.
4. Above the Clouds — moving platforms, wind/airborne threats and precision jumps.
5. Rootbound Forest — dense forest, climbing, branching paths and ambushes.
6. Flooded Chambers — water, fish, timing windows and underwater detours.
7. Ancient Ruin — crushers, traps, switches and multi-stage traversal.
8. Castle Finale — castle gauntlet and boss-style ending.

## Music / visual rule

Use music from the same official biome family whenever possible:
antarctic with snow/ice, forest with forest, castle with castle, tropical with water/coast.
Do not use unrelated music merely because it sounds dramatic.
