# PrehistoricTux UHD Art Direction

This document defines the production look for the 4K art pass. The current pixel-style assets are functional prototypes only.

## Visual target

PrehistoricTux should read as a modern, premium 2D platform game rather than a reskinned SuperTux level set.

The target is:

- highly readable silhouettes at gameplay distance
- rich prehistoric materials and vegetation
- stylized realism rather than photorealism
- family-friendly creatures with believable anatomy
- dramatic lighting without hiding platforms or hazards
- crisp 4K presentation with no visible pixel enlargement
- consistent shape language across creatures, props, terrain and UI

The game can be colorful, but it should not look toy-like. Dangerous creatures should feel dangerous without gore.

## Rendering hierarchy

### Foreground gameplay layer

Highest contrast and sharpest edge definition.

- playable ground
- moving platforms
- enemies
- checkpoints
- interactive hazards
- story characters

These elements must remain readable against every background.

### Midground

Moderate contrast and slightly reduced saturation.

- large ferns
- trunks
- fossil arches
- nest structures
- rock spires
- cave formations

### Background and parallax

Lowest local contrast and softer detail.

- distant volcano
- giant sauropod silhouettes
- canopy layers
- atmospheric cliffs
- smoke, mist and heat haze

Background art must never create false platform edges.

## Lighting language

The campaign should have one coherent light direction per scene.

1. Valley / Fernwood: warm upper-left sunlight with cool green bounce.
2. Serpent Caves: dim cool ambient light, warm mineral accents.
3. Pterosaur Cliffs: hard sunset side light, bright sky rim light.
4. Obsidian River: lava as a strong lower orange/red light source.
5. Bonefield: dusk purple/amber split lighting.
6. Nesting Grounds: low warm sunset with long shadows.
7. Crater: lava underlight plus dark volcanic sky.

Creature frames should be authored for the dominant level lighting but retain enough neutral form shading to work across multiple levels.

## Creature direction

### Raptor-like hunter

Logical frame: **64×48**  
UHD source frame: **256×192 minimum**

- lean, fast silhouette
- feather accents around forearms, tail base and neck
- long balancing tail
- readable eye and jaw at 4K
- four-frame walk prototype should become an 8-frame production run/walk cycle
- separate anticipation, leap, hit and defeat frames later

Avoid oversized cartoon teeth and avoid making it look like a generic lizard.

### Ancient snake

Logical frame: **64×32**  
UHD source frame: **256×128 minimum**

- broad prehistoric head
- heavy neck tapering into a flexible body
- belly scutes readable in motion
- subtle scale highlights
- low silhouette so the player immediately reads it as a ground hazard

Production animation target: 8 slither frames plus strike anticipation and strike frames.

### Pterosaur

Logical frame: **80×48**  
UHD source frame: **320×192 minimum**

- large wing silhouette
- membrane translucency near bright sky
- strong beak shape
- visible shoulder/body mass so it does not resemble a flat bat

Production animation target: 8-frame flight cycle, 3-frame dive anticipation, dive and recovery.

### Spinosaurus

Logical frame: **96×64**  
UHD source frame: **384×256 minimum**

This is neutral wildlife first, not a generic enemy.

- long crocodilian snout
- distinct sail silhouette
- semi-aquatic color language
- slower breathing/idle motion
- curious head movement rather than aggressive attack posing

### Caveman guide

Logical frame: **48×64**  
UHD source frame: **192×256 minimum**

- friendly but capable silhouette
- prehistoric clothing made from believable hide/fiber materials
- face readable without becoming a caricature
- visual motif repeated in signs/checkpoints to connect the world culturally

Production target: idle, point, warning gesture, surprised reaction and short walk cycle.

### Palaszarusz

Logical frame: **192×112**  
UHD source frame: **768×448 minimum**

Palaszarusz must visually dominate every other creature.

- massive chest and neck
- recognizable dorsal silhouette
- scarred volcanic-rock color family
- glowing/warm reflected lava accents, not literal neon skin
- roaring jaw silhouette readable instantly
- heavy footfalls and body inertia in charge animation

Production target:
- 6–8 idle/breathing frames
- 6-frame roar
- 8–10-frame charge
- turn/impact/stagger states
- later bespoke multi-phase boss animation

## Terrain

Logical gameplay tile: **32×32**  
UHD source tile: **128×128**

Do not paint each tile as an isolated square. Adjacent tiles must form larger natural structures.

### Jungle

- dark moist soil
- root networks
- moss and fern overlap
- small stones and leaf litter
- top-edge grass/fern breakup

### Cave

- layered sediment and dark stone
- subtle fossil inclusions
- wet highlights in lower zones
- strong readable top edge for platforms

### Cliffs

- weathered stratified rock
- warmer exposed faces
- cracks aligned across neighboring tiles
- minimal vegetation at high altitude

### Volcano

- black basalt
- warm cracks near lava
- ash deposits
- red/orange bounce light only where physically plausible

### Lava

At least 8 production animation frames later.

- large slow flow shapes
- bright yellow-white hottest cores
- orange/red crust boundaries
- dark cooling fragments
- avoid noisy full-frame sparkle

## Animation rules

- maintain the same silhouette volume between frames
- feet should contact the same logical floor line
- hitboxes remain defined in logical coordinates, never inferred from 4K texture dimensions
- do not shift the visual center between animation frames unless motion requires it
- every production loop should be checked at 60 Hz gameplay and at 25% zoom

## UHD source rules

Runtime source textures should normally be **4× logical dimensions**.

The active `.surface` wrapper maps the high-resolution source back to logical gameplay size using:

    (scale 0.25 0.25)

Do not mechanically upscale the prototype PNG and mark it complete. A production source must contain genuinely new detail.

## Acceptance criteria for a production asset

An asset is ready only when:

1. source dimensions meet the manifest target;
2. the active `.surface` binding reports the correct logical size;
3. silhouette remains readable at 25% preview;
4. no alpha fringe or matte halo is visible;
5. animation anchor does not jitter;
6. material detail survives 4K display but does not shimmer during movement;
7. the asset works against both bright and dark level backgrounds;
8. `python scripts/uhd-audit.py` reports it as `UHD`.

## Production order

1. raptor production set
2. jungle terrain set
3. snake
4. pterosaur
5. caveman
6. checkpoint / platform / hazard props
7. Spinosaurus
8. Palaszarusz
9. cave / cliff / volcano terrain
10. large backgrounds and parallax layers

This order gives Level 01 a genuine production-quality visual slice before the same language is rolled through the complete campaign.
