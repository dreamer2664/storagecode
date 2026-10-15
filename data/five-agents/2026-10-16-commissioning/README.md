# Five-agent commissioning — 2026-10-16 (Europe/Rome)

**Commissioner setup, not product delivery.** Five full, standalone role briefs, four dedicated source repositories, five open first-wake cards (neural pair share one repository), honest status/event/HANDOFF scaffolds and safety CI were created and remotely verified. No producer was registered, awakened or claimed by the commissioner, and none of the named products has been built. Public checkout/tests are commissioning-harness checks, not evidence of model/engine/map/chess/game features. See `evidence/source-verification.json`.

## The five roles

- **Neuroforge** (`t-20261015-7d93`) and **Benchmate** (`t-20261015-afd1`) share [neuralbrain](https://github.com/dreamer2664/neuralbrain), a local persistently queued coding brain that should fit a measured whole-process inference cap of 1 GiB and genuinely learn tested corrections. Benchmate independently builds/tests/breaks/corrects/retests. They coordinate at the public, unauthenticated, untrusted `https://ntfy.sh/neuralbrain`; commissioner setup marker `yC6rtL3X3SHE`. Only secret-free commit/test pointers; older channel contents ignored.
- **Gravitas** (`t-20261015-4892`) builds the substantial custom deterministic 3D Luau rigid-body library in [tideengine](https://github.com/dreamer2664/tideengine) and an additive, pinned, actual compatibility PR for Riveter's [FLOODLINE](https://github.com/dreamer2664/floodline). Native Roblox character physics stays authoritative; game integration is not complete until verified in the real game.
- **Lookout** (`t-20261015-84d3`) builds the stylized interactive map in [agent-atlas](https://github.com/dreamer2664/agent-atlas). Its map must reflect only actual published, fresh evidence; it shows stale/unknown/empty truth rather than inventing activity. [GitHub Pages](https://dreamer2664.github.io/agent-atlas/) is configured and currently serves an honest not-started commissioning landing page, **not yet the map app**.
- **Zugzwang** (`t-20261015-ed6e`) builds an original UCI chess engine in [zugzwang](https://github.com/dreamer2664/zugzwang), with fair preregistered balanced self-play and a genuinely slightly weaker peer. It may establish results only for the finite played corpus; chess remains unsolved and no universal guarantee is claimed.

## Included

- `public-briefs/`: five complete, clean public role briefs with placeholders (no live credentials).
- `agents/<name>/`: the truthful initial `HANDOFF.md`, append-only setup event and not-started status for each slot.
- `projects/<repo>/`: current public project-specific commissioning summary, scope JSON and six passing **helper-only** safety tests per repository. The map HTML is explicitly renamed `NOT_A_MAP_YET.html`.
- `evidence/`: verified task IDs, exact source commits and formalcode record IDs, status of the one-time public ntfy setup, bootstrap fake-key test metadata, and clear no-activity/no-product truth.
- `START_FIVE_AGENTS.md`: private-kit handout sheet; the actual five token-stamped private copies are intentionally **not** in storagecode or any public repository.

Credentials in public files are still only `PENDING-ISSUE` placeholders. The existing universal kit `KIT-DBF340` was tested using synthetic dummy values only. Private stamped packets are stored locally with mode `0600` and belong only in a private handoff.

All five cards remain open and unclaimed as observed at archive time. Outcome-based work, no fake heartbeat or arbitrary overnight quota. Existing video campaign stays distinct, Mars/Windows/PC bridge remains paused, primary archive is storagecode alone and the retired `storage` repository stays read-only.
