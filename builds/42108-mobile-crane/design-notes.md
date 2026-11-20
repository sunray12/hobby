# 42108 structure, palette, and mechanisms

Use the [official LEGO instructions](https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6310950.pdf) for the build sequence and the function illustrations near the end. The delivered CAD represents one fixed pose. The functions below describe the retail set or checks to add to a separate motion study; the MPD itself does not encode driven joints.

## Structure and palette

The silhouette is a long four-axle carrier with a low road cab at the front, a turntable and crane operator cab toward the rear, and a boom that stows over the road cab. A yellow outer boom carries the darker telescoping inner section. The gray actuator mounts below the boom, and the hook block reins into the front of the carrier; the demonstration load is its own submodel in the MPD.

| LEGO color | BrickLink / Rebrickable name | LDraw |
|---|---|---:|
| Bright Yellow | Yellow | 14 |
| Black | Black | 0 / 256 |
| Medium Stone Grey | Light Bluish Gray | 71 |
| Dark Stone Grey | Dark Bluish Gray | 72 |
| Bright Blue | Blue | 1 |
| Bright Red | Red | 4 |
| Brick Yellow | Tan | 19 |
| Transparent Bright Orange | Trans-Orange | 57 |

These are naming and code cross-references, not RGB equivalence claims. Trans-Orange is Rebrickable color `182` but LDraw color `57`; the [Rebrickable color endpoint](https://rebrickable.com/api/v3/lego/colors/) keeps the systems distinct.

## Mechanisms to verify in a motion model

- **Steering:** Couple the four axles to the hand-of-God control. Front and rear steer in opposite directions, with the outer axles turning more than the inner axles. Compare the four actual angle curves and check tires against fenders at the travel limits.
- **Outriggers:** Check each of the four legs independently, including its stowed and deployed poses. The manual illustrates different front and rear control arrangements. Do not infer load sharing from the CAD pose.
- **Turntable and elevation:** Separate manual slew from boom elevation. The extra-long linear actuator raises the boom; it is not the telescoping stage. Rebrickable `40918`, BrickLink `40918c01`, and LEGO element `6240630` refer to that item, while LDraw `40918-f1` and `40918-f2` represent different pose files.
- **Telescope and hoist:** The rack-driven inner boom and the hoist drum have separate controls and locking levers. Map the telescope rack and pinion, the drum, tip sheaves, hook block, and hoist cord before sweeping poses. The cord (`37597c300` / BrickLink `x77cc300`) is one physical item even though its rendered route uses many segments. Do not use the CAD path length as a cutting specification.

Consult the [BrickLink set inventory](https://www.bricklink.com/catalogItemInv.asp?S=42108-1&viewCodes=Y) and the [Rebrickable set inventory](https://rebrickable.com/api/v3/lego/sets/42108-1/parts/) for part names and catalog variants.
