"""Read MPD placements independently and reconcile the physical inventory."""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

model, library, crosswalk, colors, output = map(Path, sys.argv[1:6])
part_aliases = {
    "hoist cord": "37597c300",
    "ropelq-1": "37597c300",
    "load chain": "60169",
    "minifigchainstuds-1": "60169",
    "52901": "2723",
    # Inventory-equivalent mold families, not a claim of identical geometry.
    # Rebrickable's part relations list these as M (mold variants).
    "4459": "2780",
    "15461": "46189",
    "26287": "42195",
}
units = Counter()
seen_refs = defaultdict(Counter)
seen_parts = defaultdict(Counter)
sections = {}
for line in model.read_text().splitlines():
    if line.startswith("0 FILE "):
        key = line[7:].casefold()
        sections[key] = []
    if line.startswith("1 "):
        fields = line.split(maxsplit=14)
        sections[key].append((int(fields[1]), fields[14].casefold().replace("\\", "/")))

expected = Counter()
names = {}
ids = defaultdict(set)
for row in csv.DictReader(crosswalk.open()):
    if row["is_spare"] != "False":
        continue
    key = row["part_num"], int(row["color_id"])
    names[key] = row["name"]
    expected[key] += int(row["quantity"])
    for entry in row["ldraw_ids"].split("|"):
        ids[entry.split(":")[0].casefold()].add(row["part_num"])
    ids[row["part_num"].casefold()].add(row["part_num"])

ldraw_colors = defaultdict(set)
color_names = {}
for row in json.loads(colors.read_text())["results"]:
    color_names[row["id"]] = row["name"]
    for external in row["external_ids"].get("LDraw", {}).get("ext_ids", []):
        if external is not None:
            ldraw_colors[int(external)].add(row["id"])

all_expected_colors = {color for _, color in expected}


def walk(section, inherited, stack=()):
    assert section not in stack
    for local_color, ref in sections[section]:
        color = inherited if local_color == 16 else local_color
        ref_code = ref.removesuffix(".dat").removesuffix(".ldr").removeprefix("42108 - ")
        if ref in sections and ref.endswith(".ldr") and ref_code not in part_aliases:
            walk(ref, color, (*stack, section))
        else:
            units[ref_code, color] += 1


def lookup(code):
    if code in part_aliases:
        return {part_aliases[code]}
    if ids.get(code):
        return ids[code]
    # When the canonical file is a mold suffix and the inventory mapping uses
    # the moved file's old number, require a reverse library alias.
    prefix = re.match(r"\d+", code)
    folder = library / "parts"
    candidates = set()
    if prefix:
        for part_file in folder.glob(f"{prefix[0]}*.dat"):
            line = part_file.open(encoding="utf-8-sig", errors="replace").readline()
            if line.strip().casefold() == f"0 ~moved to {code}":
                candidates |= ids[part_file.stem]
    return candidates


walk(next(iter(sections)), 16)
actual = Counter()
for (code, color), quantity in sorted(units.items()):
    parts = lookup(code)
    colors_here = ldraw_colors[color] & all_expected_colors or {color}
    candidates = {(p, c) for p in parts for c in colors_here}
    matched = candidates & expected.keys()
    if len(matched) == 1:
        key, = matched
    elif len(candidates) == 1:
        key, = candidates
    else:
        key = f"unmapped:{code}", color
    actual[key] += quantity
    seen_refs[key][code] += quantity
    seen_parts[key][color] += quantity

with output.open("w") as stream:
    writer = csv.writer(stream)
    writer.writerow(["Rebrickable part", "part name", "Rebrickable color ID", "color",
                     "expected", "CAD", "CAD minus expected", "LDraw refs and quantities", "LDraw color codes",
                     "normalization notes"])
    for p, c in sorted(expected.keys() | actual.keys()):
        key = p, c
        writer.writerow([p, names.get(key, ""), c, color_names.get(c, ""), expected[key], actual[key],
                         actual[key] - expected[key], "; ".join(f"{ref}:{n}" for ref, n in seen_refs[key].items()),
                         "; ".join(str(v) for v in sorted(seen_parts[key])),
                         "; ".join(f"{ref} counted with {p} (mold variant)"
                                   for ref in seen_refs[key] if ref in {"4459", "15461", "26287"})])
print("expected", sum(expected.values()), len(expected), "actual", sum(actual.values()), len(actual))
for key in sorted(expected.keys() | actual.keys()):
    if expected[key] != actual[key]:
        print(key, names.get(key), expected[key], actual[key], dict(seen_refs[key]))
