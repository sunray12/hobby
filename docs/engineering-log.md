# Engineering log

This log preserves the decisions and public research evidence behind each build. It is a curated record, not a verbatim transcript.

## 42108 Mobile Crane baseline | 2026-11-20

### Scope and sources

The dry run was to reproduce and analyze the 1,292-piece LEGO Technic Mobile Crane, document the mechanisms and color mappings, and produce an MPD with reproducible CAD checks. Use [LEGO's set instructions](https://www.lego.com/en-us/service/building-instructions/42108) for the original build steps and physical operation, [Rebrickable v3](https://rebrickable.com/api/v3/docs/) for inventory and color mappings, [BrickLink](https://www.bricklink.com/catalogItemInv.asp?S=42108-1&viewCodes=Y) for catalog cross-references, and [Brickognize](https://api.brickognize.com/docs) as an optional identification aid, not authoritative mold evidence.

### Decisions

- Use Max Martin Richter's [exact-set OMR model](https://library.ldraw.org/omr/sets/1113) as the attributed geometry baseline. Do not claim a clean-sheet reconstruction. Keep the original MPD untouched; make an identified review adaptation and retain original credit and license headers.
- The downloaded source was rejected by strict Nova validation for its legacy rope encoding and rounded rotations. Treat generated cord and chain geometry as two physical items, remove only fully collapsed cord references, and use proper rotations for the static assembly placements. Use the OMR source when editing the original LDCad path mechanics.
- Use LEGO step 134 to resolve the turntable's colors. The black toothed half and light bluish gray plain half in the reviewed MPD follow [the LEGO manual](https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6310950.pdf), not the reversed assignment in the source MPD.
- The Rebrickable endpoints are under `/api/v3/lego/`, not legacy `get_set_parts` routes. Store the authorization header outside this public repository and never put an API key in a URL.

### Outcomes

- The [CAD review](../builds/42108-mobile-crane/LEGO-42108-CAD-Review.md) records a standard Nova pass, five inspected LeoCAD views, and a Nova-to-LeoCAD count match at 1,291 modeled physical placements.
- The [inventory comparison](../builds/42108-mobile-crane/LEGO-42108-Inventory-Check.csv) counts 1,292 retail items excluding spares. The remaining differences are the omitted sticker sheet, one extra black `18654`, and one missing black `87082`. Mold-family normalization is explicit in the comparison.
- The stricter Nova contact pass found one unresolved seating error between `32073.dat` and `32524.dat`, plus overlap and disconnected-group warnings. It did not establish a physical assembly defect or demonstrate mechanism travel.

### Lessons and next checks

- A visual fit, a tool-to-tool BOM match, and a retail inventory match are three different checks. Equal totals can hide part substitutions. An actuator pose or generated cord segment is not an additional retail item.
- Use the official instructions to check seating before translating a part to silence an automated diagnostic. First resolve the 5L axle and 7L beam finding and locate the `18654` / `87082` discrepancy.
- Create a separate kinematic study for four-axle steering, each of the four outriggers, the turntable, the actuator, telescoping rack, and hoist. Inspect end stops, cord routing/payout, and the two locks in each relevant pose. Do not infer clearance, clutch, or load capacity from a static model.
