#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


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
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == ";":
            nl = text.find("\n", i)
            if nl < 0:
                return len(text) - 1
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
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


def tiles_count(tilemap: str) -> int:
    start = tilemap.find("(tiles")
    if start < 0:
        raise ValueError("tilemap has no tiles")
    end = matching_paren(tilemap, start)
    raw = tilemap[start + len("(tiles"):end]
    nums = [int(n) for n in re.findall(r"-?\d+", raw)]
    expanded = 0
    i = 0
    while i < len(nums):
        n = nums[i]
        if n < 0:
            if i + 1 >= len(nums):
                raise ValueError("RLE repeat has no tile value")
            expanded += abs(n)
            i += 2
        else:
            expanded += 1
            i += 1
    return expanded


def validate_level(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []
    clean = strip_strings_and_comments(text)

    if clean.count("(") != clean.count(")"):
        errors.append("unbalanced parentheses")
    if "(supertux-level" not in clean:
        errors.append("missing supertux-level root")
    if "(version 3)" not in clean:
        errors.append("expected level format version 3")
    for required in ("(camera", "(spawnpoint", "(sequencetrigger"):
        if required not in clean:
            errors.append(f"missing required object {required[1:]}")

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
        except ValueError as exc:
            errors.append(f"tilemap {index}: {exc}")

    return errors


def main() -> int:
    levels = sorted((ROOT / "addon").rglob("*.stl"))
    if not levels:
        print("ERROR: no .stl levels found", file=sys.stderr)
        return 1

    failed = False
    for level in levels:
        errors = validate_level(level)
        rel = level.relative_to(ROOT)
        if errors:
            failed = True
            print(f"FAIL {rel}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {rel}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
