#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import sys


def replace_exact(path: pathlib.Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text and old not in text:
        print(f"OK      {label}: already applied")
        return
    if old not in text:
        raise RuntimeError(f"{label}: expected SuperTux 0.7.0 source block not found in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED {label}")


def replace_exact_count(
    path: pathlib.Path, old: str, new: str, label: str, expected_count: int
) -> None:
    text = path.read_text(encoding="utf-8")
    old_count = text.count(old)
    new_count = text.count(new)

    if old_count == 0 and new_count == expected_count:
        print(f"OK      {label}: already applied")
        return

    if old_count + new_count != expected_count:
        raise RuntimeError(
            f"{label}: expected {expected_count} total source block(s), "
            f"found old={old_count}, patched={new_count} in {path}"
        )

    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"PATCHED {label}: {old_count} block(s)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the PrehistoricTux logical-surface UHD changes to a clean SuperTux 0.7.0 tree."
    )
    parser.add_argument("source", type=pathlib.Path)
    args = parser.parse_args()
    root = args.source.resolve()

    surface_hpp = root / "src/video/surface.hpp"
    surface_cpp = root / "src/video/surface.cpp"
    canvas_cpp = root / "src/video/canvas.cpp"
    batch_cpp = root / "src/video/surface_batch.cpp"
    world_cpp = root / "src/worldmap/world_select.cpp"

    for path in (surface_hpp, surface_cpp, canvas_cpp, batch_cpp, world_cpp):
        if not path.is_file():
            raise RuntimeError(f"missing expected SuperTux source file: {path}")

    replace_exact(
        surface_hpp,
        """  Surface(const TexturePtr& diffuse_texture, const TexturePtr& displacement_texture, Flip flip, const std::string& filename = "");
  Surface(const TexturePtr& diffuse_texture, const TexturePtr& displacement_texture, const Rect& region, Flip flip, const std::string& filename = "");
""",
        """  Surface(const TexturePtr& diffuse_texture, const TexturePtr& displacement_texture, Flip flip,
          const std::string& filename = "", const Vector& logical_scale = Vector(1.0f, 1.0f));
  Surface(const TexturePtr& diffuse_texture, const TexturePtr& displacement_texture, const Rect& region, Flip flip,
          const std::string& filename = "", const Vector& logical_scale = Vector(1.0f, 1.0f));
""",
        "surface constructor declarations",
    )

    replace_exact(
        surface_hpp,
        """  const Rect m_region;
  const Flip m_flip;
  const std::string m_source_filename;
""",
        """  const Rect m_region;
  const Flip m_flip;
  const Vector m_logical_scale;
  const std::string m_source_filename;
""",
        "logical scale member",
    )

    replace_exact(
        surface_cpp,
        """  auto surface = new Surface(diffuse_texture, displacement_texture, flip, filename);
  return SurfacePtr(surface);
""",
        """  Vector logical_scale(1.0f, 1.0f);
  std::vector<float> scale_v;
  if (mapping.get("scale", scale_v))
  {
    if (scale_v.size() != 2 || scale_v[0] <= 0.0f || scale_v[1] <= 0.0f)
    {
      throw std::runtime_error("Surface scale must contain two positive values.");
    }
    logical_scale = Vector(scale_v[0], scale_v[1]);
  }

  auto surface = new Surface(diffuse_texture, displacement_texture, flip,
                             filename, logical_scale);
  return SurfacePtr(surface);
""",
        "surface scale parser",
    )

    replace_exact(
        surface_cpp,
        """Surface::Surface(const TexturePtr& diffuse_texture,
                 const TexturePtr& displacement_texture,
                 Flip flip, const std::string& filename) :
  m_diffuse_texture(diffuse_texture),
  m_displacement_texture(displacement_texture),
  m_region(0, 0, m_diffuse_texture->get_image_width(), m_diffuse_texture->get_image_height()),
  m_flip(flip),
  m_source_filename(filename)
""",
        """Surface::Surface(const TexturePtr& diffuse_texture,
                 const TexturePtr& displacement_texture,
                 Flip flip, const std::string& filename,
                 const Vector& logical_scale) :
  m_diffuse_texture(diffuse_texture),
  m_displacement_texture(displacement_texture),
  m_region(0, 0, m_diffuse_texture->get_image_width(), m_diffuse_texture->get_image_height()),
  m_flip(flip),
  m_logical_scale(logical_scale),
  m_source_filename(filename)
""",
        "full-surface constructor",
    )

    replace_exact(
        surface_cpp,
        """Surface::Surface(const TexturePtr& diffuse_texture,
                 const TexturePtr& displacement_texture,
                 const Rect& region,
                 Flip flip, const std::string& filename) :
  m_diffuse_texture(diffuse_texture),
  m_displacement_texture(displacement_texture),
  m_region(region),
  m_flip(flip),
  m_source_filename(filename)
""",
        """Surface::Surface(const TexturePtr& diffuse_texture,
                 const TexturePtr& displacement_texture,
                 const Rect& region,
                 Flip flip, const std::string& filename,
                 const Vector& logical_scale) :
  m_diffuse_texture(diffuse_texture),
  m_displacement_texture(displacement_texture),
  m_region(region),
  m_flip(flip),
  m_logical_scale(logical_scale),
  m_source_filename(filename)
""",
        "region constructor",
    )

    replace_exact(
        surface_cpp,
        """  SurfacePtr surface(new Surface(m_diffuse_texture,
                                 m_displacement_texture,
                                 m_region,
                                 m_flip ^ flip));
""",
        """  SurfacePtr surface(new Surface(m_diffuse_texture,
                                 m_displacement_texture,
                                 m_region,
                                 m_flip ^ flip,
                                 m_source_filename, m_logical_scale));
""",
        "clone scale preservation",
    )

    replace_exact(
        surface_cpp,
        """  SurfacePtr surface(new Surface(m_diffuse_texture,
                                 m_displacement_texture,
                                 rect,
                                 m_flip));
""",
        """  SurfacePtr surface(new Surface(m_diffuse_texture,
                                 m_displacement_texture,
                                 rect,
                                 m_flip,
                                 m_source_filename, m_logical_scale));
""",
        "region scale preservation",
    )

    replace_exact(
        surface_cpp,
        """int
Surface::get_width() const
{
  return m_region.get_width();
}

int
Surface::get_height() const
{
  return m_region.get_height();
}
""",
        """int
Surface::get_width() const
{
  return static_cast<int>(static_cast<float>(m_region.get_width()) * m_logical_scale.x);
}

int
Surface::get_height() const
{
  return static_cast<int>(static_cast<float>(m_region.get_height()) * m_logical_scale.y);
}
""",
        "logical surface dimensions",
    )

    replace_exact(
        canvas_cpp,
        """  draw_surface_part(surface, Rectf(0.0f, 0.0f, static_cast<float>(surface->get_width()), static_cast<float>(surface->get_height())),
                    dstrect, layer, style);
""",
        """  draw_surface_part(surface, Rectf(surface->get_region()),
                    dstrect, layer, style);
""",
        "scaled draw source region",
    )

    replace_exact_count(
        batch_cpp,
        """  m_srcrects.emplace_back(Rectf(0, 0,
                                static_cast<float>(m_surface->get_width()),
                                static_cast<float>(m_surface->get_height())));
""",
        """  m_srcrects.emplace_back(Rectf(m_surface->get_region()));
""",
        "surface batch source regions",
        2,
    )

    replace_exact(
        world_cpp,
        """    Rectf rect = world.icon->get_region();
    rect = Rectf(0, 0, rect.get_width() * size / 2.f, rect.get_height() * size / 2.f);
""",
        """    Rectf rect(0, 0, static_cast<float>(world.icon->get_width()),
                     static_cast<float>(world.icon->get_height()));
    rect = Rectf(0, 0, rect.get_width() * size / 2.f, rect.get_height() * size / 2.f);
""",
        "world-select logical icon size",
    )

    print("PrehistoricTux UHD engine changes applied successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
