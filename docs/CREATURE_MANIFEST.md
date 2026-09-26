# Creature implementation manifest

This file maps game-design creatures to the temporary engine behaviours used by the vertical slice. It prevents placeholder choices from silently becoming final designs.

| Game creature | Bootstrap behaviour | Final implementation |
| --- | --- | --- |
| Small prehistoric hunter | `snowball` | Original sprite + tuned walking badguy subclass |
| Ancient snake | `smartball` during geometry tests | Ground-hugging ambush enemy with strike telegraph |
| Heavy territorial dinosaur | `snowman` | Slow charge / knockback behaviour |
| Flying prehistoric hunter | `flyingsnowball` plus scripted dives | Original flying sprite + patrol/dive state machine |
| Spinosaurus | neutral scripted wildlife cameo | Larger ecological encounter; not automatically hostile |
| Palaszarusz | scripted reveal object | Multi-phase bespoke boss |

## Rules

- Placeholder graphics are never presented as final artwork.
- Every attack that can cause a death must have a readable visual or audio tell.
- Wildlife is not universally hostile; later levels include neutral and helpful creatures.
- Custom C++ code starts only after the level geometry and encounter timing survive playtesting.
