# PrehistoricTux — Game Design

## Tone
Family-friendly prehistoric adventure with demanding platforming. Wonder first, danger second: huge creatures, dense vegetation, caves, lava and ancient ruins.

## Core loop
Explore → platform → evade/defeat creatures → discover secrets → reach checkpoint → survive set-piece → progress story.

## Campaign arc
1. The Valley of the Lost Egg
2. Fernwood Canopy
3. Serpent Caves
4. The Pterosaur Cliffs
5. Obsidian River
6. Bonefield at Dusk
7. Nesting Grounds
8. Palaszarusz Crater

## Signature creatures
- Ancient snake: ambushes from foliage and tunnels.
- Small raptor-like hunter: fast ground pressure.
- Armored herbivore: environmental moving hazard rather than villain.
- Flying prehistoric hunter: patrol/dive pattern.
- Palaszarusz: recurring threat and final boss.

## Difficulty
No cheap blind deaths. Hard sections telegraph danger. Checkpoints sit before major difficulty spikes. Secrets demand observation and movement mastery.

## UHD direction
Gameplay remains resolution-independent. New source artwork should be authored oversized or vector-first where practical, then exported into engine-compatible assets without making collision dependent on render resolution.

## Implementation status

- Level 01 — The Valley of the Lost Egg: playable vertical-slice structure, custom prehistoric terrain/art, scripted ambushes and Palaszarusz reveal.
- Level 02 — Fernwood Canopy: full-length geometry scaffold connected to the worldmap, with canopy routes, two checkpoints, two secrets and mixed ground/air pressure.
- Level 03 — Serpent Caves: full-length cave scaffold connected to the worldmap, with falling custom rock hazards, two checkpoints, two secrets and a volcanic transition.
- Level 04 — Pterosaur Cliffs: vertical wind-and-platforming scaffold with timed gusts, moving cliff platforms, two checkpoints and two secrets.
- Level 05 — Obsidian River: animated lava hazards, moving obsidian slabs, falling rock pressure, two checkpoints and two secrets.
- Level 06 — Bonefield at Dusk: twilight fossil-field scaffold with mixed predator pressure, checkpoints and secrets.
- Level 07 — Nesting Grounds: mixed-biome nesting route with neutral wildlife and a scripted Palaszarusz/egg sighting.
- Level 08 — Palaszarusz Crater: full final approach plus a three-phase scripted charge boss prototype and egg recovery ending.
