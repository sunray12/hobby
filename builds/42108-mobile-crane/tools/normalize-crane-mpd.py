"""Adapt the attributed LDraw OMR 42108 model for strict Nova review."""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np


source, library, target, report = map(Path, sys.argv[1:5])
renames = {
    "42108 - ropeLQ-1.ldr": "42108 - hoist cord.dat",
    "42108 - minifigChainStuds-1.ldr": "42108 - load chain.dat",
}
official_replacements = {
    "42108 - 15413.dat": "15413.dat",
    "42108 - 18575.dat": "18575.dat",
    "42108 - 33299b.dat": "33299b.dat",
    "42108 - 40918-f1.dat": "40918-f1.dat",
    "42108 - 35185.dat": "35185.dat",
    "42108 - 13971.dat": "13971.dat",
}
counts = Counter()
line_changes = []
section = None
out = []
imported_part_geometry = False


def part_line(text):
    f = text.split(maxsplit=14)
    return f, np.array([float(x) for x in f[5:14]]).reshape(3, 3)


def fmt(x):
    return f"{x:.9f}".rstrip("0").rstrip(".") if abs(x) >= 0.5e-9 else "0"


def note(kind, line_number, **extra):
    counts[kind] += 1
    line_changes.append(dict(kind=kind, original_line=line_number, section=section, **extra))


for lineno, line in enumerate(source.read_text().splitlines(), 1):
    if line.startswith("0 FILE "):
        section = line.removeprefix("0 FILE ")
        imported_part_geometry = section.lower().endswith(".dat")
        if section in renames:
            line = "0 FILE " + renames[section]
    if section in renames:
        if line.startswith("0 Name: "):
            line = "0 Name: " + renames[section]
        if line == "0 !LDRAW_ORG Unofficial_Model":
            line = "0 !LDRAW_ORG Unofficial_Part"
            note("flex_classification", lineno, replacement=renames[section])
    if line.startswith("1 "):
        fields, rotation = part_line(line)
        ref = fields[-1]
        if section in renames:
            if not np.any(rotation):
                assert section == "42108 - ropeLQ-1.ldr" and ref == "4-4cyli.dat"
                note("zero_geometry_omitted", lineno)
                continue
        elif not imported_part_geometry:
            # LEGO inventory elements 6109283/6109285 identify the black
            # 60-tooth top and light bluish gray bottom respectively.
            if section == "42108 - Substep_Step-134.ldr" and ref in {"18938.dat", "18939.dat"}:
                replacement_color = {"18938.dat": "0", "18939.dat": "71"}[ref]
                assert fields[1] != replacement_color
                note("turntable_color", lineno, reference=ref, previous=fields[1], replacement=replacement_color)
                fields[1] = replacement_color
            if not np.allclose(rotation.T @ rotation, np.eye(3), atol=2e-6, rtol=0):
                u, s, v = np.linalg.svd(rotation)
                assert np.linalg.det(rotation) > 0 and np.max(abs(s - 1)) < 0.001
                rotation = u @ v
                fields[5:14] = [fmt(x) for x in rotation.flat]
                note("rotation_precision", lineno, reference=ref)
            if ref in renames:
                fields[-1] = renames[ref]
            elif ref in official_replacements:
                replacement = official_replacements[ref]
                assert (library / "parts" / replacement).is_file()
                fields[-1] = replacement
                note("current_official_part", lineno, previous=ref, replacement=replacement)
            elif (part_path := library / "parts" / ref).is_file():
                part_data = part_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
                if part_data and part_data[0].startswith("0 ~Moved to "):
                    aliases = [x for x in part_data if x.startswith(("1 ", "2 ", "3 ", "4 ", "5 "))]
                    if len(aliases) == 1 and aliases[0].startswith("1 "):
                        alias, alias_rotation = part_line(aliases[0])
                        if alias[1] == "16" and np.linalg.det(alias_rotation) > 0:
                            old_position = np.array([float(x) for x in fields[2:5]])
                            alias_position = np.array([float(x) for x in alias[2:5]])
                            fields[2:5] = [fmt(x) for x in old_position + rotation @ alias_position]
                            fields[5:14] = [fmt(x) for x in (rotation @ alias_rotation).flat]
                            fields[-1] = alias[-1]
                            note("moved_alias", lineno, previous=ref, replacement=alias[-1])
        line = " ".join(fields)
    out.append(line)
    if section == "42108 - main.ldr" and line.startswith("0 !LICENSE "):
        out.extend([
            "0 // Source assembly: Max Martin Richter [MMR1988], LDraw Official Model Repository.",
            "0 // https://library.ldraw.org/omr/sets/1113",
            "0 // Review adaptation: rotation precision, flex rendering cleanup, official part references,",
            "0 // and turntable colours aligned with LEGO elements 6109283 and 6109285.",
            "0 // Static build pose; source assembly and this adaptation omit stickers.",
        ])

# Drop imported definitions that became unreachable after adopting their official
# counterparts. Keep original attribution and steps on all retained blocks.
blocks = {}
for line in out:
    if line.startswith("0 FILE "):
        section = line.removeprefix("0 FILE ").casefold()
        blocks[section] = []
    blocks[section].append(line)

reachable = set()


def visit(name):
    if name in reachable or name not in blocks:
        return
    reachable.add(name)
    for line in blocks[name]:
        if line.startswith("1 "):
            visit(line.split(maxsplit=14)[14].casefold())
        elif "[donPart=42108 - ldcLQRopeSeg.dat]" in line:
            visit("42108 - ldclqropeseg.dat")


visit(next(iter(blocks)))
counts["unreachable_blocks_omitted"] = len(blocks) - len(reachable)
crlf = "\r\n"
result = crlf.join(line for name, block in blocks.items() if name in reachable for line in block)
target.write_bytes((result.rstrip() + crlf).encode())
report.write_text(json.dumps({"counts": dict(counts), "modifications": line_changes}, indent=2) + "\n")
