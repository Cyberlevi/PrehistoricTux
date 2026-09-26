# Release checklist

PrehistoricTux follows the official SuperTux add-on package layout.

## Before packaging

1. Run the static validator:
   ```bash
   python scripts/validate_campaign.py
   ```
2. Play the prologue and all eight campaign levels.
3. Verify that the worldmap progression reaches every level.
4. Check each dinosaur sprite for correct facing, hitbox and death animation.
5. Check secret areas, moving platforms, switches and end sequences.
6. Make sure the add-on metadata version is incremented for every published update.

## Build archive

```bash
bash scripts/package-addon.sh
```

The generated archive is:

`PrehistoricTux-The-Lost-Egg.zip`

The archive root contains:
- `cyberlevi-prehistorictux.nfo`
- `levels/`
- `images/`

This matches the official SuperTux add-on packaging convention.

## Official add-on repository submission

The SuperTux add-ons repository expects:
- the packaged archive under its `repository/` directory,
- optional screenshots under `screenshots/<addon-id>/`,
- a matching entry in the current add-on index,
- the archive checksum and immutable commit URL.

The project add-on id is:

`cyberlevi-prehistorictux`

## Attribution

Selected level geometry and gameplay foundations are adapted from official SuperTux 0.7.0 content under CC-BY-SA 4.0. Original attribution is preserved in adapted level files. Project-specific campaign sequencing, story integration and dinosaur artwork are part of PrehistoricTux.
