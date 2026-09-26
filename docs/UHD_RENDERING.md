# UHD / 4K Rendering Plan

PrehistoricTux targets **3840×2160 presentation quality**, even though the current development monitors are 1920×1080.

## Why the stock engine needs a small rendering extension

SuperTux 0.7.0 uses a bounded logical viewport. The upstream viewport code caps the logical game area at **1368×800** and scales that logical space to the physical window.

At 3840×2160, a normal logical sprite can therefore be enlarged by roughly 2.7–2.8× on screen. A 64×48 texture may end up occupying around 180×135 physical pixels. If the source art itself is only 64×48, the GPU has no extra detail to reveal.

Simply replacing a 64×48 sprite with a 256×192 PNG is not enough in stock SuperTux: sprite surface dimensions also participate in logical drawing size, so the creature becomes four times larger in the game world.

## PrehistoricTux solution

The repository contains:

    engine-patches/0001-uhd-logical-surface-scale.patch

The patch makes the existing `.surface` `(scale X Y)` field affect the surface's **logical size**, while the renderer still receives the full source texture.

A future 4× raptor frame can therefore look like this:

    (supertux-surface
      (scale 0.25 0.25)
      (diffuse-texture
        (file "raptor-walk-0@4x.png")
        (filter "linear")
      )
    )

A 256×192 texture is then drawn as a 64×48 logical game surface. Collision and level geometry stay unchanged while UHD output can sample the high-resolution texture.

## Art production targets

- gameplay tiles: 32×32 logical → **128×128 master**
- ordinary creatures/props: **4× logical size**
- Palaszarusz and large set pieces: at least **4× logical size**
- full-screen / major background plates: **3840×2160 minimum**
- wide parallax layers: preferably **4096 px or wider**
- transparent gameplay art: PNG with clean alpha
- original masters should retain layers/vector data outside the runtime add-on when possible

The existing images are prototypes. They should not be mechanically enlarged and called UHD. The new pass needs genuinely new detail: cleaner silhouettes, material definition, lighting, scales/skin/feather texture, foliage, rock structure and controlled edge detail.

## Build the UHD-capable engine on Garuda

Upstream Arch dependencies are documented by SuperTux. On a normal Arch/Garuda setup the required package set is:

    sudo pacman -S cmake base-devel libogg libvorbis openal sdl2 sdl2_image sdl2_ttf freetype2 libraqm curl openssl glew harfbuzz fribidi glm zlib fmt physfs

The easiest route on Garuda is now:

    bash scripts/setup-garuda-uhd-build.sh

That explicitly asks for sudo, installs only missing packages with `pacman --needed`, then starts the isolated engine build.

To inspect dependencies without installing anything:

    bash scripts/check-uhd-build-deps.sh

If dependencies are already present, build directly:

    bash scripts/build-uhd-engine.sh

The build is isolated under `.engine/`; it does not overwrite the system SuperTux package.

Run PrehistoricTux with the patched engine:

    bash scripts/run-uhd-engine.sh

For an actual physical 4K monitor:

    PREHISTORICTUX_GEOMETRY=3840x2160 \
    PREHISTORICTUX_VIDEO_MODE=fullscreen \
    bash scripts/run-uhd-engine.sh

On the current 1080p displays, leave the default safe 1920×1080 mode. We can still author and validate 4K-capable assets there.

## Audit current artwork

    python scripts/uhd-audit.py

This reports which prototype PNGs are still below the 4× source target.

For release gating later:

    python scripts/uhd-audit.py --strict

Strict mode should only become part of CI once the prototype art replacement is substantially complete.
