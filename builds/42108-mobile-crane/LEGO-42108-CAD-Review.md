# LEGO Technic 42108 Mobile Crane: CAD review

`LEGO-42108-Mobile-Crane.mpd` is a static LDraw adaptation of Max Martin Richter’s [42108-1 model in the LDraw Official Model Repository](https://library.ldraw.org/omr/sets/1113), not a new reconstruction. The MPD keeps the credited assembly and instruction-step hierarchy, the visible hoist cord and load chain, and the separate demonstration load. It omits stickers, as does the repository model.

## Open the MPD

Use a current [LDraw parts library](https://library.ldraw.org/updates) with LeoCAD, LDCad, or LDraw Nova. The root `42108 - main.ldr` includes `42108 - Mobile Crane.ldr` and `42108 - Cargo.ldr`; loading only the crane section omits the loose load. The library and application are not bundled. For native flex-path editing, use the [original LDCad-authored MPD](https://library.ldraw.org/omr/sets/1113); the review copy classifies the two flex assets as physical parts and preserves their rendered paths, but LDCad regeneration was not tested.

## What changed

- **Flex assets:** The cord and chain each count as one physical placement. The review copy drops 639 all-zero cylinder references that had no visible geometry, leaving the nonzero cord segments and the chain’s rendered links.
- **Placement precision:** 89 near-rotation matrices were projected onto proper rotations without changing the local translations. Where supported, moved library aliases were resolved with their transforms composed; six older embedded part definitions were replaced by their official counterparts across 25 references.
- **Turntable colors:** The toothed half is black (`18938.dat`, LEGO `6109283`) and the plain half is light bluish gray (`18939.dat`, LEGO `6109285`), as shown in [LEGO’s step 134 and element list](https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6310950.pdf).
- **Attribution:** The [OMR source](https://library.ldraw.org/omr/sets/1113) credits Max Martin Richter `[MMR1988]`. Retained sections retain their original credits and [CC BY 2.0 license](https://creativecommons.org/licenses/by/2.0/).

## Inventory comparison

The independent count compares the model with the [Rebrickable 42108-1 inventory](https://rebrickable.com/api/v3/lego/sets/42108-1/parts/), excluding spares. The MPD contains 1,291 physical placements versus 1,292 inventory items. Counting three catalog mold families together permits inventory reconciliation, not a claim of exact mold geometry: `4459` with `2780` (3), `15461` with `46189` (2), and `26287` with `42195` (15). The full comparison also checks color, and the only remaining differences are:

| Part | Inventory | CAD | Difference |
|---|---:|---:|---:|
| `65625` sticker sheet | 1 | 0 | −1 |
| `18654` black Technic 1L round connector | 35 | 36 | +1 |
| `87082` black double-pin connector hub | 6 | 5 | −1 |

The two black-part differences cancel in the total, but the location and cause were not established. Eight black `15413` tires and eight yellow `56145` rims reconcile, as do the extra-long actuator (`40918` / BrickLink `40918c01`), cord (`37597c300`), and load chain (`60169`); catalog references are available in the [Rebrickable inventory](https://rebrickable.com/api/v3/lego/sets/42108-1/parts/) and [BrickLink inventory](https://www.bricklink.com/catalogItemInv.asp?S=42108-1&viewCodes=Y).

## Nova review results

The standard review passed source and geometry validation, BOM generation, rendering, and the Nova-to-LeoCAD BOM comparison. Both tools counted 1,291 placements and reported zero differences against each other. The five final views (perspective, top, front, left and right) were inspected; they show the crane and loose load in the expected overall configuration. This pass does not establish a match to the retail bill of materials or to the moving physical model.

The stricter `--contacts all` review ran the contact scan but did not pass. Nova reported one `technic.invalid_seating` error plus connectivity and overlap warnings. It stopped before its gated rendering and BOM comparison, which were run separately without the full contact scan.

- **Axle seating:** Nova flagged 5L axle `32073.dat` at MPD line 1811 (substep 182, occurrence 551) against 7L beam `32524.dat` at line 1635 (substep 159, occurrence 506). The checker reported that the beam hole runs past the modeled shaft end. This is an unresolved CAD diagnostic, not a verified physical assembly error; the affected parts were not moved just to clear the check.
- **Connectivity:** Nova reported 3,119 detected contact candidates and 466 groups under its permissive connectivity rule. The demonstration load is intentionally separate; the remaining groups are not individually verified. A failed connection inference does not prove that a part is misplaced.
- **Clearances:** Nova reported 2,736 bounding-volume overlap candidates, including 28 deep-overlap warnings. These are screeners, not confirmed collisions; the review did not certify Technic clearances across the assembly.

## Mechanism follow-up

The static geometry shows the eight-wheel carrier, the folded/stowed outriggers, the turntable, the retracted horizontal boom with the long elevation actuator, the hook block and the routed hoist. The manual shows the four-axle steering, independently deployable outriggers, turntable slew, elevation, rack-driven extension, and hoist, with separate lock levers for extension and hoist ([LEGO instructions and function illustrations](https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6310950.pdf)).

To turn this into a motion model, define pivot axes and mechanical limits, then sweep steering (front and rear opposed, outer axles turning more than inner axles), each outrigger separately, and the boom and hoist through multiple poses. Check rack and gear engagement, cord payout and routing, hook travel, and the latch states. A static MPD and a contact scan do not prove these motions or load capacity.

## Reproduce the review

```sh
export LDRAW_DIR=/path/to/ldraw
export LDRAWDIR="$LDRAW_DIR"
xvfb-run -a ./ldraw-agent review LEGO-42108-Mobile-Crane.mpd \
  --views home top front left right --outdir 42108-render-review
xvfb-run -a ./ldraw-agent review LEGO-42108-Mobile-Crane.mpd \
  --contacts all --limit 3000 --views home top front left right \
  --outdir 42108-review
```

Run with [LDraw Nova](https://github.com/anteloc/ldraw-nova) revision `d1e93d73f6ffe6955caa90953a98a0c90fbd5c5c` and LeoCAD 25.09. `xvfb-run` supplies a virtual display for headless Linux; it is not required when a usable display is available.

MPD SHA-256: `db3534b399ee5609355b6428195a09e7330adfabe6e1dee42df79af624152572`.
