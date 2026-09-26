# SuperTux upstream review — 2026-09-26

## What we can reuse

SuperTux is GPL-licensed engine code. Its README states that most of the `data` directory is CC-BY-SA. The current repository uses C++, CMake and a version-3 text level format. The engine already provides the mechanics we need for the first vertical slice: platforming, badguys, moving/path objects, particles, scripted triggers, checkpoints/spawn points, cutscene scripting, editor tooling and add-on packaging.

## Recommended architecture

Do **not** rewrite the engine for the first milestone. Build PrehistoricTux as an add-on/content layer first. This lets us validate level pacing and art direction rapidly. Add custom C++ badguys only when stock object behaviour cannot represent the dinosaur mechanic.

## Compatibility

Current upstream has 0.7.0 releases in 2026, while 0.6.3 remains an older stable milestone. We will develop against current level format v3 and keep the content isolated so a compatibility pass can be done before release.

## Licensing consequence

If we redistribute a modified SuperTux engine, the corresponding GPL obligations apply. Reused/derived data assets must retain their applicable attribution/share-alike terms. Original prehistoric assets need explicit metadata from day one.

## Immediate implementation order

1. Playable geometry using stock objects.
2. Worldmap and story triggers.
3. Original jungle/volcano tileset.
4. Original dinosaur sprites and animation sheets.
5. Custom behaviour code for snake, flying hunter and Palaszarusz.
6. Performance/UHD polish and packaging.
