# PrehistoricTux: The Lost Egg

A full-length eight-level SuperTux 0.7.0 add-on campaign.

## Prologue
The worldmap starts with an automatic story cutscene: **The Lost Egg**.

## Campaign
1. The Valley of the Lost Egg
2. The Dinosaur Trail
3. Ancient Caves
4. Pterosaur Cliffs
5. Flooded Ruins
6. The Bonefield
7. Nesting Grounds
8. Palaszarusz Crater

The level geometry and gameplay systems are adapted from selected official SuperTux 0.7.0 levels under CC-BY-SA 4.0. The campaign order, story integration and dinosaur artwork are project-specific adaptations.

## Test
```bash
bash scripts/play-level.sh 1
```

## Worldmap
```bash
bash scripts/play-worldmap.sh
```

## Package
```bash
python scripts/validate_campaign.py
bash scripts/package-addon.sh
```

See `docs/RELEASE.md` for the official add-on submission checklist.
