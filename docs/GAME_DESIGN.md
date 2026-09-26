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
