# Level 01 incoming UHD exports

Drop genuine production PNG exports into the folders below using the exact filenames listed in `art/level01-production.json`.

Priority 1 is the first visible quality jump:
- raptor frames
- jungle fill/top terrain

Then validate without changing runtime bindings:

    python scripts/promote-level01-art.py --priority 1 --dry-run

When every listed file is correct:

    python scripts/promote-level01-art.py --priority 1

After promotion:

    python scripts/uhd-audit.py
    python scripts/level01-art-status.py
    bash scripts/play-level.sh 1

Do not place mechanically enlarged prototype images here. Incoming files are expected to contain genuinely new 4× detail.
