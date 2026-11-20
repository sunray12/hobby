# Working in this repository

1. Read the [engineering log](docs/engineering-log.md) and the relevant build index. Start a topic branch from `develop` and identify the baseline MPD revision or checksum.
2. Keep one change or investigation per branch. Use `build/<set>-<topic>` for CAD work, `fix/<set>-<topic>` for a focused correction, and `docs/<topic>` for documentation.
3. Keep each build's model, review, and inventory comparison in `builds/<set>-<name>/`. Record source URLs, part-library and CAD-tool revisions, commands, hash of the reviewed MPD, and checks that failed or did not run. Add renders for geometry changes.
4. In the pull request to `develop`, state what changed, what was tested, and what remains uncertain. For geometry changes, include before-and-after views and distinguish catalog equivalence, geometric fit, and mechanical motion.
5. After review, promote the accepted batch from `develop` to `main` by pull request. Do not force-push or rewrite shared history. AI contributors should not push changes, merge, or change repository settings without the owner's explicit approval.

## Review checklist

- The MPD opens, references resolve, and visible parts are present in the expected pose.
- The inventory comparison separates LDraw aliases and assembly poses, catalog mold-family substitutions, actual differences, flex assets, and spares.
- Primary visuals agree with the official instructions. Any proposed change to a fit, axle, or connector is checked against the applicable instruction step before it is accepted.
- Contact findings, collisions, clearance, travel, clutch, and load capacity are not treated as interchangeable.
- Do not upload private prompts, secure-form screenshots, secrets, or credential-bearing URLs. Fetch data with credentials stored outside the repository. For a published inventory snapshot, retain only the part and color data needed to repeat the comparison.
- Preserve upstream credit and license terms in third-party files and add an explicit note about modifications.
