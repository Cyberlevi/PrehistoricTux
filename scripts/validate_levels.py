#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDON = ROOT / "addon"


def strip_strings_and_comments(text: str) -> str:
    out = []
    in_string = False
    escaped = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            out.append(" ")
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(" ")
            i += 1
            continue
        if ch == ";":
            while i < len(text) and text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def matching_paren(text: str, start: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    i = start
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
        elif ch == ";":
            nl = text.find("\n", i)
            if nl < 0:
                return len(text) - 1
            i = nl
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError(f"unclosed expression starting at byte {start}")


def expressions(text: str, name: str):
    token = f"({name}"
    pos = 0
    while True:
        start = text.find(token, pos)
        if start < 0:
            return
        end = matching_paren(text, start)
        yield text[start:end + 1]
        pos = end + 1


def scalar(expr: str, key: str) -> int:
    m = re.search(rf"\({re.escape(key)}\s+(-?\d+)\)", expr)
    if not m:
        raise ValueError(f"missing ({key} N)")
    return int(m.group(1))


def expand_tiles(tilemap: str) -> list[int]:
    start = tilemap.find("(tiles")
    if start < 0:
        raise ValueError("tilemap has no tiles")
    end = matching_paren(tilemap, start)
    raw = tilemap[start + len("(tiles"):end]
    nums = [int(n) for n in re.findall(r"-?\d+", raw)]
    expanded: list[int] = []
    i = 0
    while i < len(nums):
        n = nums[i]
        if n < 0:
            if i + 1 >= len(nums):
                raise ValueError("RLE repeat has no tile value")
            expanded.extend([nums[i + 1]] * abs(n))
            i += 2
        else:
            expanded.append(n)
            i += 1
    return expanded


def tiles_count(tilemap: str) -> int:
    return len(expand_tiles(tilemap))


def addon_path_from_absolute(ref: str) -> pathlib.Path:
    return ADDON / ref.lstrip("/")


def validate_custom_references(path: pathlib.Path, text: str) -> list[str]:
    errors: list[str] = []

    for ref in re.findall(r'\(sprite\s+"([^"]+)"\)', text):
        if ref.startswith("/images/prehistoric/"):
            target = addon_path_from_absolute(ref)
            if not target.is_file():
                errors.append(f"missing custom sprite: {ref}")

    for ref in re.findall(r'import\(\"([^"]+)\"\)', text):
        if ref.startswith("levels/prehistoric_tux/"):
            target = ADDON / ref
            if not target.is_file():
                errors.append(f"missing imported script: {ref}")

    return errors


WORLD_PATH_DATA = {
    10: 6, 11: 10, 12: 23, 13: 30,
    14: 5, 15: 9, 16: 29, 17: 27,
    18: 20, 19: 18, 20: 12, 21: 3,
    22: 17, 23: 24, 24: 31, 25: 0,
    26: 20, 27: 18, 28: 17, 29: 24,
}


def validate_worldmap_path(tilemap: str) -> list[str]:
    errors: list[str] = []
    width = scalar(tilemap, "width")
    height = scalar(tilemap, "height")
    values = expand_tiles(tilemap)
    if len(values) != width * height:
        return errors

    NORTH, SOUTH, EAST, WEST, STOP = 1, 2, 4, 8, 16
    dirs = [
        (NORTH, 0, -1, SOUTH, "north"),
        (SOUTH, 0, 1, NORTH, "south"),
        (EAST, 1, 0, WEST, "east"),
        (WEST, -1, 0, EAST, "west"),
    ]

    for y in range(height):
        for x in range(width):
            tile_id = values[y * width + x]
            data = WORLD_PATH_DATA.get(tile_id, 0)
            if not data:
                continue

            for bit, dx, dy, reciprocal, label in dirs:
                if not (data & bit):
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < width and 0 <= ny < height):
                    if not (data & STOP):
                        errors.append(f"path tile {tile_id} at {x},{y} points {label} off-map without STOP")
                    continue

                neighbor_id = values[ny * width + nx]
                neighbor_data = WORLD_PATH_DATA.get(neighbor_id, 0)
                if not (neighbor_data & reciprocal):
                    if data & STOP:
                        continue
                    errors.append(
                        f"path tile {tile_id} at {x},{y} points {label} to "
                        f"{neighbor_id} at {nx},{ny} without reciprocal connection"
                    )

    return errors


def validate_level(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    clean = strip_strings_and_comments(text)

    if clean.count("(") != clean.count(")"):
        errors.append("unbalanced parentheses")
    if "(supertux-level" not in clean:
        errors.append("missing supertux-level root")
    if "(version 3)" not in clean:
        errors.append("expected level format version 3")

    if path.suffix == ".stwm":
        for required in ("(worldmap-spawnpoint", "(level", "(tilemap"):
            if required not in clean:
                errors.append(f"missing worldmap object {required[1:]}")
    else:
        for required in ("(camera", "(spawnpoint", "(tilemap"):
            if required not in clean:
                errors.append(f"missing required object {required[1:]}")
        if "(sequencetrigger" not in clean and "(scripttrigger" not in clean:
            errors.append("level has no completion/story trigger")

    for index, tm in enumerate(expressions(text, "tilemap"), start=1):
        try:
            width = scalar(tm, "width")
            height = scalar(tm, "height")
            actual = tiles_count(tm)
            expected = width * height
            if actual != expected:
                errors.append(
                    f"tilemap {index}: expands to {actual} tiles, expected {expected} "
                    f"({width}x{height})"
                )
            if path.suffix == ".stwm" and re.search(r'\(name\s+"pathing"\)', tm):
                errors.extend(validate_worldmap_path(tm))
        except ValueError as exc:
            errors.append(f"tilemap {index}: {exc}")

    errors.extend(validate_custom_references(path, text))
    return errors


def validate_sprite(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    clean = strip_strings_and_comments(text)

    if clean.count("(") != clean.count(")"):
        errors.append("unbalanced parentheses")
    if "(supertux-sprite" not in clean:
        errors.append("missing supertux-sprite root")

    action_names = re.findall(r'\(name\s+"([^"]+)"\)', text)
    if not action_names:
        errors.append("sprite defines no actions")

    for images_expr in expressions(text, "images"):
        refs = re.findall(r'"([^"]+)"', images_expr)
        for ref in refs:
            if ref.startswith("/"):
                if ref.startswith("/images/prehistoric/"):
                    target = addon_path_from_absolute(ref)
                else:
                    continue
            else:
                target = path.parent / ref
            if not target.is_file():
                errors.append(f"missing image frame: {ref}")

    return errors


def validate_tileset(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    clean = strip_strings_and_comments(text)

    if clean.count("(") != clean.count(")"):
        errors.append("unbalanced parentheses")
    if "(supertux-tiles" not in clean:
        errors.append("missing supertux-tiles root")

    ids = [int(value) for value in re.findall(r'\(id\s+(\d+)\)', text)]
    for ids_expr in expressions(text, "ids"):
        ids.extend(int(value) for value in re.findall(r"\b\d+\b", ids_expr) if int(value) > 0)

    if not ids:
        errors.append("tileset defines no tile ids")
    if len(ids) != len(set(ids)):
        errors.append("tileset contains duplicate tile ids")
    if any(tile_id <= 0 for tile_id in ids):
        errors.append("tileset contains non-positive tile id")

    for images_expr in expressions(text, "images"):
        refs = re.findall(r'\"([^"]+)\"', images_expr)
        for ref in refs:
            if ref.startswith("/"):
                if not ref.startswith("/images/prehistoric/"):
                    continue
                target = addon_path_from_absolute(ref)
            else:
                target = path.parent / ref
            if not target.is_file():
                errors.append(f"missing tile image: {ref}")

    return errors


def validate_addon_metadata() -> list[str]:
    errors: list[str] = []
    nfos = sorted(ADDON.glob("*.nfo"))
    if len(nfos) != 1:
        return [f"expected exactly one top-level .nfo file, found {len(nfos)}"]

    path = nfos[0]
    text = path.read_text(encoding="utf-8")
    m = re.search(r'\(id\s+"([^"]+)"\)', text)
    if not m:
        errors.append("add-on metadata has no id")
        return errors

    addon_id = m.group(1)
    if path.stem != addon_id:
        errors.append(f".nfo filename {path.stem!r} does not match id {addon_id!r}")
    if not re.fullmatch(r"[a-z0-9-]+", addon_id):
        errors.append(f"invalid add-on id: {addon_id!r}")

    return errors


def report(path: pathlib.Path, errors: list[str]) -> bool:
    rel = path.relative_to(ROOT)
    if errors:
        print(f"FAIL {rel}")
        for error in errors:
            print(f"  - {error}")
        return False
    print(f"OK   {rel}")
    return True


def main() -> int:
    level_files = sorted((ADDON / "levels").rglob("*.stl"))
    worldmaps = sorted((ADDON / "levels").rglob("*.stwm"))
    sprites = sorted((ADDON / "images" / "prehistoric").rglob("*.sprite"))
    tilesets = sorted((ADDON / "images" / "prehistoric").rglob("*.strf"))

    if not level_files:
        print("ERROR: no .stl levels found", file=sys.stderr)
        return 1
    if not worldmaps:
        print("ERROR: no .stwm worldmaps found", file=sys.stderr)
        return 1
    if not sprites:
        print("ERROR: no custom prehistoric .sprite files found", file=sys.stderr)
        return 1
    if not tilesets:
        print("ERROR: no custom prehistoric .strf tilesets found", file=sys.stderr)
        return 1

    ok = True
    for path in level_files + worldmaps:
        ok = report(path, validate_level(path)) and ok
    for path in sprites:
        ok = report(path, validate_sprite(path)) and ok
    for path in tilesets:
        ok = report(path, validate_tileset(path)) and ok

    metadata_errors = validate_addon_metadata()
    metadata_path = next(iter(sorted(ADDON.glob("*.nfo"))), ADDON / "<missing>.nfo")
    ok = report(metadata_path, metadata_errors) and ok

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
