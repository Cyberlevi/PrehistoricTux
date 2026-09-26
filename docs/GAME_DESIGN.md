# Game Design

## Story
A giant creature steals a warm egg from a broken nest. Tux follows the trail through eight regions. At first the dinosaurs appear to be the threat, but the route gradually reveals that many are defending nesting territory. The final crater reframes Palaszarusz as the guardian at the center of the conflict.

## Design rules
- Secrets must be behind believable geometry or alternate routes.
- Coins indicate movement arcs and optional routes, not random empty space.
- Enemy placement must match the room and platform geometry.
- Music and background remain consistent with each biome.
- Each level teaches a mechanic, combines it, then tests it.
- Checkpoints follow meaningful challenge sections.
- Dinosaur sprites reuse stable stock enemy AI rather than custom engine code.
- Original SuperTux secret, switch, moving-platform, water and boss logic is retained where it strengthens the level.

## Dinosaur roles
- Raptor: fast ground hunter using Snowball/Smartball-compatible AI.
- Pterosaur: aerial hunter using flying-enemy-compatible AI.
- Trike: heavy ground pressure using larger stock badguy-compatible AI.

## Level ecology

- 01 The Valley of the Lost Egg — first raptor encounters; tracks establish the predator trail.
- 02 The Dinosaur Trail — raptor hunting territory; faster ground pressure, few heavy creatures.
- 03 Ancient Caves — larger ground guardians and cave wildlife; fewer fast predators.
- 04 Pterosaur Cliffs — aerial pterosaur territory with vertical platforming.
- 05 Flooded Ruins — aquatic enemies remain primary; pterosaurs patrol only the open upper ruins.
- 06 The Bonefield — trike-dominated heavy territory among fossil remains.
- 07 Nesting Grounds — mixed defense: raptors near nests, pterosaurs overhead, heavy guardians deeper inside.
- 08 Palaszarusz Crater — all major prehistoric threats return before the final confrontation.

## Production enemy cast

The campaign uses a level-specific prehistoric cast rather than repeating a single enemy skin.

- Raptor / Alpha Raptor: early trail, nesting grounds and finale
- Trike / Ankylosaur: caves, bonefield and guarded routes
- Pterosaur / Hunter Pterosaur: cliffs, flooded upper ruins and finale
- Plesiosaur: Flooded Ruins
- Nestling: Nesting Grounds
- Palaszarusz: oversized final-crater encounter

Visual scale intentionally varies from small nestlings to a substantially larger Palaszarusz while keeping hitboxes readable for SuperTux-style platforming.
