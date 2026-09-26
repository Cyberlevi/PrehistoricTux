# UHD source-art workspace

This directory documents the source-art workflow. Runtime assets remain under `addon/images/prehistoric/`.

Production artwork should be kept at 4× logical resolution or higher. Layered/vector masters can be stored outside the runtime add-on when their format is not directly supported by SuperTux; exported PNGs are promoted into the runtime tree with:

    python scripts/promote-uhd-source.py \
      --surface addon/images/prehistoric/creatures/raptor/raptor-walk-0.surface \
      --source /path/to/raptor-walk-0@4x.png \
      --logical 64x48

The command validates dimensions, copies the new source next to the binding and rewrites the `.surface` file to the correct logical scale.

Prototype PNG files are intentionally retained until their production replacement has been verified in-engine.
