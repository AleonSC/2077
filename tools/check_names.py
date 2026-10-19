#!/usr/bin/env python3
"""
Check that pose names line up across the AMM .lua file and WolvenKit files.

A typo in one place is the most common reason a custom pose silently fails
to play, so run this before packing the mod.

Usage:
    python tools/check_names.py path/to/my_pose_pack.lua [exported.json ...]

The optional JSON files are .workspot or .anims files that WolvenKit
converted to JSON (right-click the file > Convert to JSON). Every name in the
.lua must appear in each JSON file you pass.
"""

import json
import re
import sys

VALID_NAME = re.compile(r"^[a-z0-9_]+$")


def lua_anims(path):
    """Return {rig: [names]} from the anims table of an AMM pose .lua."""
    text = open(path, encoding="utf-8").read()
    # Drop comments so example names in them don't count.
    text = re.sub(r"--[^\n]*", "", text)
    start = text.find("anims")
    if start == -1:
        sys.exit(f"{path}: no anims table found")
    rigs = {}
    for rig, body in re.findall(r'\["([^"]+)"\]\s*=\s*\{([^}]*)\}', text[start:]):
        rigs[rig] = re.findall(r'"([^"]*)"', body)
    return rigs


def json_strings(node, out):
    """Collect every string value in a JSON document."""
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for value in node.values():
            json_strings(value, out)
    elif isinstance(node, list):
        for value in node:
            json_strings(value, out)
    return out


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    errors = 0
    rigs = lua_anims(argv[1])
    if not rigs:
        sys.exit(f"{argv[1]}: anims table is empty")

    for rig, names in rigs.items():
        seen = set()
        for name in names:
            if not VALID_NAME.match(name):
                print(f"[{rig}] {name!r}: use lowercase, digits, underscores only")
                errors += 1
            if name in seen:
                print(f"[{rig}] {name!r}: listed twice")
                errors += 1
            seen.add(name)

    for path in argv[2:]:
        with open(path, encoding="utf-8") as f:
            strings = json_strings(json.load(f), set())
        for rig, names in rigs.items():
            for name in names:
                if name not in strings:
                    print(f"[{rig}] {name!r}: missing from {path}")
                    errors += 1

    total = sum(len(n) for n in rigs.values())
    if errors:
        sys.exit(f"{errors} problem(s) found in {total} pose name(s).")
    print(f"All {total} pose name(s) look good.")


if __name__ == "__main__":
    main(sys.argv)
