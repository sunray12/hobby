# LEGO Technic Dev Builds

A shared engineering workspace for LEGO Technic reverse engineering, CAD models, and original builds. It gives human contributors, Perplexity, and Ninja Tech AI employees the same baseline, references, and open questions.

## Start here

| Build | What to open | Current status |
|---|---|---|
| LEGO 42108 Mobile Crane | [Build index](builds/42108-mobile-crane/README.md) · [LDraw model](builds/42108-mobile-crane/LEGO-42108-Mobile-Crane.mpd) · [CAD review](builds/42108-mobile-crane/LEGO-42108-CAD-Review.md) | Static baseline. Nova's standard checks passed; the full contact scan flagged one unresolved axle-seating issue. |

Read [Working in this repository](CONTRIBUTING.md) before changing a model. The [engineering log](docs/engineering-log.md) records the project's decisions, results, and lessons without private conversation history or credentials.

## Branches

- `main`: Reviewed baselines and documentation. A reviewed baseline can have clearly documented open issues.
- `develop`: Shared integration branch for changes under review.
- `build/<set>-<topic>`, `fix/<set>-<topic>`, or `docs/<topic>`: Short-lived work branches, created from `develop` as needed.

Open a pull request into `develop` for work that needs review. Promote reviewed batches to `main` by pull request. An automated checker passing is not hardware validation.

## Public repository

Use public sources and publishable engineering material only. Do not add API credentials, private transcripts, account screenshots, or content without redistribution rights. Model and part licenses are declared in their LDraw headers and build documentation; the repository does not relicense third-party work.
