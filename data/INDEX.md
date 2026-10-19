# Data index — one line per deposit

Append-only. Format: `date · project · agent · what · PR` (or `-` when there
is no PR). Newest at the bottom.

| date | project | agent | what | PR |
|---|---|---|---|---|
| 2026-10-14 | chatcode | vesta | pipeline build receipts — validate 0 errors after repair chain, first automatic formalcode lines, CI green on 2cea75af/f3750d64 | - |
| 2026-10-14 | superocr | vesta | main CI regression since #82 + fix — red log extract, verbatim diff, local 24/24; CI on 9ab638a1 noted in dir | - |
| 2026-10-14 | superocr | odysseus | S58 t-20261014-d325 replay receipts — live 100-item seed-1 hard pass (floor/final/route-pieces jsonl) + census json; tool+report on branch agent/odysseus/t-20261014-d325, gates G1-G5 PASS, 32/32 tests | - |
| 2026-10-14 | superocr | odysseus | S68 t-20261014-8ff6 easy-residue census receipts — live 100-item seed-1 easy pass (floor/final/route-pieces jsonl) + census json; 25 misses (13 case / 8 seg / 4 glyph), gates G1-G3 PASS | - |
| 2026-10-14 | superocr | scipio | S57 replay receipts (t-20261014-713e): seed-1 75/25 ×3 + seed-2 75/29 ×3 on canonical suites, per-item diff 0/1200 mismatches, validate_report ×6 VALID — summary + diffs; receipts in superocr PR #89 | superocr#89 |
| 2026-10-15 | superocr | odysseus | S65 t-20261014-138a darts fresh-corpus receipts — seed-900 40-item reads jsonl + census json (0/40 floor, 0/40 shipping, 40/40 segmentation stage; manifest sha256 3fc6ae4d) | - |
| 2026-10-15 | storage-migration | vesta | Legacy storage ledger, shifts, chronicle and data imported without loss; original data index: [legacy/storage/data/INDEX.md](../legacy/storage/data/INDEX.md); checksum map: migrations/2026-10-15-storage-unification.json | storage@c0e46a8204 |
| 2026-10-15 | youtube-training | vesta | yt-training-s1 launch: ten reserved final-film slots; 0 completed at launch; viewing index data/youtube-training/INDEX.md; production/review requirements in chatcode projects/youtube-training | - |
| 2026-10-15 | storage-migration | vesta | Server-side legacy archive frozen @aa18c8656b; late PUSHES rows reconciled; 3 unmerged maintenance PRs preserved with immutable source/patch hashes under legacy/storage-open-prs/ (not accepted) | - |
| 2026-10-15 | youtube-training / yt-training-s1 | vesta | [Launch receipt: 15 jobs, zero accepted films, tests, remote commits, verified wires and archive cutover](youtube-training/yt-training-s1/launch/README.md) | - |
| 2026-10-15 | youtube-training / progress audit | vesta | [Zero new final films; three unmerged pitch/research packs; older 2-second silent demo only](youtube-training/yt-training-s1/audits/2026-10-15-vesta-152914/README.md) | - |
| 2026-10-15 | youtube-training / Director directive | vesta | [Verified general-board reprimand #dafbff2b: finish active jobs and ten actual films; preserve Mars pause](youtube-training/yt-training-s1/directives/2026-10-15-vesta-dafbff2b.json) | - |
| 2026-10-15 | youtube-training / progress audit | vesta | [One real 1080p ~5:21 candidate verified; new render/voice/editorial PRs; required reviews and timing check still pending](youtube-training/yt-training-s1/audits/2026-10-15-vesta-183612-candidate-check/README.md) | - |
| 2026-10-15 | vesta | [Frameforge commissioning](frameforge/2026-10-15-commissioning/README.md) | frameforge-commission-20261015; three independent private kits, truthfully not-started slots,49 inspected reference frames,18 safety tests, real voice/media fixture, no films |
| 2026-10-15 | vesta | [Frameforge final commissioning closeout](frameforge/2026-10-15-commissioning/CLOSEOUT.json) | frameforge-commission-final-20261015; original evidence preserved, final source f77ad2580894, still zero awake producer/film claims |
| 2026-10-15 | scribble | [Frameforge r01](frameforge/scribble/r01-3bc9460bc81f/publication.json) | frameforge/scribble/r01-3bc9460bc81f; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/scribble/r01-3bc9460bc81f); SHA256 3bc9460bc81fc8b05f5981510ad734a4a1e036ab3f2517b730da3d71f0e31838 |
| 2026-10-15 | scribble | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/scribble/r01-3bc9460bc81f-closeout) | frameforge/scribble/evidence/r01-3bc9460bc81f-closeout |
| 2026-10-15 | vesta | [FLOODLINE / Riveter commissioning](floodline/2026-10-15-commissioning/README.md) | floodline-riveter-commission-20261015; complete standalone game brief, actual non-game place-export proof,12 safety checks, honest not-started slot |
| 2026-10-15 | riveter | [Frameforge r01](floodline/riveter/r01-39971a4f9f6c/publication.json) | floodline/riveter/r01-39971a4f9f6c; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r01-39971a4f9f6c); SHA256 39971a4f9f6c9b7e13b13b9688ce9810e91c786c4c9bc82037408adf803a9c8a |
| 2026-10-15 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r01-39971a4f9f6c-closeout) | floodline/riveter/evidence/r01-39971a4f9f6c-closeout |
| 2026-10-15 | riveter | [Frameforge r02](floodline/riveter/r02-dfb18467b74a/publication.json) | floodline/riveter/r02-dfb18467b74a; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r02-dfb18467b74a); SHA256 dfb18467b74ae4c8c709b8ec317e23f2e7eceeeed61dd3b99244abf5d88d5e84 |
| 2026-10-15 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r02-dfb18467b74a-closeout) | floodline/riveter/evidence/r02-dfb18467b74a-closeout |
| 2026-10-15 | riveter | [Frameforge r03](floodline/riveter/r03-db183983e5de/publication.json) | floodline/riveter/r03-db183983e5de; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r03-db183983e5de); SHA256 db183983e5de914e326b6093c4a0027d73f222fed50b5ad632e4ff76d6d42d66 |
| 2026-10-15 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r03-db183983e5de-closeout) | floodline/riveter/evidence/r03-db183983e5de-closeout |
| 2026-10-15 | riveter | [Frameforge r04](floodline/riveter/r04-bb01ea529a62/publication.json) | floodline/riveter/r04-bb01ea529a62; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r04-bb01ea529a62); SHA256 bb01ea529a623871497f19e35af063eaa19c8c9939fcaabb304ff2155d74be55 |
| 2026-10-15 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r04-bb01ea529a62-closeout) | floodline/riveter/evidence/r04-bb01ea529a62-closeout |
| 2026-10-15 | scribble | [Frameforge r02](frameforge/scribble/r02-2631680aad6b/publication.json) | frameforge/scribble/r02-2631680aad6b; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/scribble/r02-2631680aad6b); SHA256 2631680aad6b8e47d6bebfe801289bf2f11d1062df59f339d51cc34bb98f7b36 |
| 2026-10-16 | five-agent commissions | vesta | [Five-agent commissioning + verified closeout](five-agents/2026-10-16-commissioning/README.md) — 5 new open/unclaimed roles; products not started; private briefs excluded | - |
| 2026-10-16 | riveter | [Frameforge r05](floodline/riveter/r05-ff8685c8b316/publication.json) | floodline/riveter/r05-ff8685c8b316; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r05-ff8685c8b316); SHA256 ff8685c8b3161d1ed162fddef2fdab45b99ce1fc0686e603142e3de6020544ba |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r05-ff8685c8b316-closeout) | floodline/riveter/evidence/r05-ff8685c8b316-closeout |
| 2026-10-16 | scribble | [Frameforge r03](frameforge/scribble/r03-ce92a14ac777/publication.json) | frameforge/scribble/r03-ce92a14ac777; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/scribble/r03-ce92a14ac777); SHA256 ce92a14ac777890339025f43a1f7a09ffde992cee241f315574a8462e8fd51eb |
| 2026-10-16 | kinetic | [Frameforge r03](frameforge/kinetic/r03-99dc27911b3e/publication.json) | frameforge/kinetic/r03-99dc27911b3e; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/kinetic/r03-99dc27911b3e); SHA256 99dc27911b3e1498cda4f3c1402cb49e8ff848611ae4a46d7128252fd8bbb0cf |
| 2026-10-16 | scribble | [Frameforge r04](frameforge/scribble/r04-fdd4d226ba18/publication.json) | frameforge/scribble/r04-fdd4d226ba18; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/scribble/r04-fdd4d226ba18); SHA256 fdd4d226ba1803a7b29dad433ccecddb40564aa4ae4901ecb49e484c034a906d |
| 2026-10-16 | frameforge / Kinetic successors | vesta | [Public commissioning packet](data/frameforge/2026-10-16-kinetic-successors/README.md) — Parallax + Glyphcraft briefs and starter HANDOFFs, verified Kinetic byte-integrity receipt, card/alert receipts and exact 20/20 offline test output; private kits excluded | - |
| 2026-10-16 | axiom | [Frameforge r01](frameforge/axiom/r01-2158c6cddada/publication.json) | frameforge/axiom/r01-2158c6cddada; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/axiom/r01-2158c6cddada); SHA256 2158c6cddadabaefb07595c969bdf918fbfe76ff3e73c29c0ab209d7e5a16739 |
| 2026-10-16 | vesta / Kinetic successors | [Kinetic r03 visual sample review](frameforge/2026-10-16-kinetic-successors/evidence/KINETIC_BASELINE_VISUAL_SAMPLE_REVIEW.json) | All 810 hero and 256 loop video frames decoded; representative stills inspected | Full-speed playback, audio listening and formal acceptance not claimed |
| 2026-10-16 | glyphcraft | [Frameforge r03](frameforge/glyphcraft/r03-589da7b8fddb/publication.json) | frameforge/glyphcraft/r03-589da7b8fddb; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/glyphcraft/r03-589da7b8fddb); SHA256 589da7b8fddb1ab88406f08a8d9db4b8ccf4df84849eccfb88b0af5927c874b1 |
| 2026-10-16 | buildinglab / Blender | vesta | [Six-floor building commission](data/buildinglab/commission/2026-10-16/README.md) — full public brief, truthful starter HANDOFF/status, live card receipts and independent review plan; private packets excluded | - |
| 2026-10-16 | buildinglab / Blender | vesta | [Commissioning evidence refresh](buildinglab/commission/2026-10-16/evidence/COMMISSIONING_VERIFICATION.md) — live check 08:37:27 UTC: nine cards open/unowned; `jobscode` alert `G3JfAhDcKUZa` verified; Chatcode health 0 schema errors / 227 warnings; no worker or model claimed | - |
| 2026-10-16 | buildinglab / Blender | vesta | [Final commissioning evidence refresh](buildinglab/commission/2026-10-16/evidence/COMMISSIONING_VERIFICATION.md) — live readback 08:40:35 UTC: nine cards open/unowned, no Blender in 21-agent roster; `jobscode` receipt verified; 0 schema errors / 227 warnings; no model or worker claimed | - |

| 2026-10-16 | buildinglab / Blender | blender | [BLDG-1 schematic checkpoint](buildinglab/blender/blockout-20261016-f0a5ba82e97a/README.md) — six levels, 14 proposed homes; validated blockout and inspected plans; not final or accepted | [prerelease](https://github.com/dreamer2664/storagecode/releases/tag/buildinglab/blender/blockout-20261016-f0a5ba82e97a) |
| 2026-10-16 | glyphcraft | [Frameforge r04](frameforge/glyphcraft/r04-48b981b37ce0/publication.json) | frameforge/glyphcraft/r04-48b981b37ce0; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/glyphcraft/r04-48b981b37ce0); SHA256 48b981b37ce0149d87edc668dee7f70ca453b8393fb66a9af8970385d9910838 |


## 2026-10-16T14:02:43.209895+00:00 — buildinglab / blender detailed model checkpoint

Immutable native/export recovery assets: https://github.com/dreamer2664/storagecode/releases/tag/buildinglab/blender/candidate-20261016-0f8497096094

Native SHA-256 `0f8497096094a9c3d24d4fad7f9b95843b613d5a7c5bf4339db3bd0637b55887`; GLB SHA-256 `da7e163b59d042d6aa9ccea170251e9e99ff25fe4261b1d8fb50f4ae522287bb`. All four assets were actually re-downloaded without authentication and byte/SHA verified. Evidence campaign, final archive and independent acceptance remain pending. Record: `data/buildinglab/blender/checkpoint-20261016-0f8497096094/receipt.json`.
| 2026-10-16 | riveter | [Frameforge r06](floodline/riveter/r06-6e22c896e034/publication.json) | floodline/riveter/r06-6e22c896e034; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r06-6e22c896e034); SHA256 6e22c896e03429b9c978e8dd210aa933274be9c7a45a06b4d6c80e10ba8917f5 |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r06-6e22c896e034-closeout) | floodline/riveter/evidence/r06-6e22c896e034-closeout |
| 2026-10-16 | riveter | [Frameforge r07](floodline/riveter/r07-a9d07bfbd5fa/publication.json) | floodline/riveter/r07-a9d07bfbd5fa; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r07-a9d07bfbd5fa); SHA256 a9d07bfbd5fa7f9ac477b2e07c01cd45b20937fd78f5cf975100b1074c7120fa |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r07-a9d07bfbd5fa-closeout) | floodline/riveter/evidence/r07-a9d07bfbd5fa-closeout |


Source card pushes: {"t-20261016-0d4e": "b18f996c95c4d489eb2fcaa8040ae58850cab0a1", "t-20261016-58d8": "a7430873c487c623a0b4523863e97ab44e6b664f", "t-20261016-61b0": "9f0a16fcba9d0b7864378faa561d5934dfbad78c"}

## 2026-10-16T15:49:00.913845+00:00 — buildinglab / blender detailed model checkpoint

Immutable native/export recovery assets: https://github.com/dreamer2664/storagecode/releases/tag/buildinglab/blender/candidate-20261016-1b7150d6ce45

Native SHA-256 `1b7150d6ce4536d19058cc1088a2ac063c495c41925c65d1f74c28fe1c773f0f`; GLB SHA-256 `06940c1254f6d7499d93c2798e7ea564c0f0e780a184ec8d008481aff37e67e6`. All four assets were actually re-downloaded without authentication and byte/SHA verified. Evidence campaign, final archive and independent acceptance remain pending. Record: `data/buildinglab/blender/checkpoint-20261016-1b7150d6ce45/receipt.json`.


## 2026-10-16T16:01:37.943445+00:00 — blender / buildinglab source push

`agent/blender/t-20261016-58d8@5854600130afb24a0860496efe1add36d9a50523` https://github.com/dreamer2664/buildinglab/commit/5854600130afb24a0860496efe1add36d9a50523 — corrected source/native actual geometry guards, public downloaded native reopen/test render and GLB clean-reimport PASS; 3/29 corrected-source originals actually opened at this checkpoint. Final producer packet and independent acceptance remain pending. No self-review/vote.
| 2026-10-16 | riveter | [Frameforge r08](floodline/riveter/r08-b14c80d16506/publication.json) | floodline/riveter/r08-b14c80d16506; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r08-b14c80d16506); SHA256 b14c80d16506ec4590bfac1794f3255ddaf7d0c773eb95d7a75b2d4c478518af |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r08-b14c80d16506-closeout) | floodline/riveter/evidence/r08-b14c80d16506-closeout |


## 2026-10-16T17:23:26.041241+00:00 — blender / buildinglab source push

`agent/blender/t-20261016-58d8@cb4978b131d86917b1364a02358aa3add82813d5` https://github.com/dreamer2664/buildinglab/commit/cb4978b131d86917b1364a02358aa3add82813d5 — corrected source/native actual geometry guards, public downloaded native reopen/test render and GLB clean-reimport PASS; 12/29 corrected-source originals actually opened at this checkpoint. Final producer packet and independent acceptance remain pending. No self-review/vote.


## 2026-10-16T17:23:47.716691+00:00 — blender / buildinglab source push

`agent/blender/t-20261016-58d8@cb4978b131d86917b1364a02358aa3add82813d5` https://github.com/dreamer2664/buildinglab/commit/cb4978b131d86917b1364a02358aa3add82813d5 — actual HTTPS push retry succeeded after a restored askpass executable-bit failure. Prior checkpoint ledger was written prematurely before that retry; this append-only clarification records the actual successful push. Corrected source/native actual geometry guards, public downloaded native reopen/test render and GLB clean-reimport PASS; 12/29 corrected-source originals actually opened at this checkpoint. Final producer packet and independent acceptance remain pending. No self-review/vote.
| 2026-10-16 | riveter | [Frameforge r09](floodline/riveter/r09-08b5349c293e/publication.json) | floodline/riveter/r09-08b5349c293e; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r09-08b5349c293e); SHA256 08b5349c293edbd4b81f09c0bc58ca102a2d22f148372a902b6d357698f98ac3 |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r09-08b5349c293e-closeout) | floodline/riveter/evidence/r09-08b5349c293e-closeout |
| 2026-10-16 | riveter | [Frameforge r10](floodline/riveter/r10-34766844bd2f/publication.json) | floodline/riveter/r10-34766844bd2f; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r10-34766844bd2f); SHA256 34766844bd2fa9d0d856704ffdc4160178a5e5730efac50f707e01a86173b35b |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r10-34766844bd2f-closeout) | floodline/riveter/evidence/r10-34766844bd2f-closeout |


## 2026-10-16T18:37:10.066554+00:00 — buildinglab / blender detailed candidate

https://github.com/dreamer2664/storagecode/releases/tag/buildinglab/blender/candidate-20261016-1b7150d6ce45

Archive: https://github.com/dreamer2664/storagecode/releases/download/buildinglab/blender/candidate-20261016-1b7150d6ce45/Casa-dei-Colori-candidate-20261016-1b7150d6ce45.zip

Archive SHA-256 `70130eb4f823fc274e52191dadde47bf75de68b2414b260d7f74c11f22b3b118`; native SHA-256 `1b7150d6ce4536d19058cc1088a2ac063c495c41925c65d1f74c28fe1c773f0f`; GLB SHA-256 `06940c1254f6d7499d93c2798e7ea564c0f0e780a184ec8d008481aff37e67e6`. Actual public unauthenticated archive redownload, CRC and EVERY member verified, including three native files, GLB and all 29 original final PNGs. Producer gates pass; independent non-owner acceptance remains pending. Receipt: `data/buildinglab/blender/candidate-20261016-1b7150d6ce45/publication-receipt.json`.


## 2026-10-16T18:38:41.816799+00:00 — blender / buildinglab source push

`agent/blender/t-20261016-58d8@0823beedcb194c21587fb459a9c2e6d2692b8390` https://github.com/dreamer2664/buildinglab/commit/0823beedcb194c21587fb459a9c2e6d2692b8390 — corrected source/native actual geometry guards, public downloaded native reopen/test render and GLB clean-reimport PASS; 29/29 corrected-source originals actually opened at this checkpoint. The final producer packet is publicly redownload/every-member verified (release candidate-20261016-1b7150d6ce45; receipt in publication index); all three work cards/PRs submitted for independent non-owner review. Independent acceptance remains pending. No self-review/vote.
| 2026-10-16 | riveter | [Frameforge r11](floodline/riveter/r11-3f5b85be4771/publication.json) | floodline/riveter/r11-3f5b85be4771; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r11-3f5b85be4771); SHA256 3f5b85be4771d523b30fd6a35f32185149b6d730aae7416daee2504f44a143b8 |
| 2026-10-16 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r11-3f5b85be4771-closeout) | floodline/riveter/evidence/r11-3f5b85be4771-closeout |
| 2026-10-16 | parallax | [Frameforge r01](frameforge/parallax/r01-ce4424a3fb16/publication.json) | frameforge/parallax/r01-ce4424a3fb16; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/parallax/r01-ce4424a3fb16); SHA256 ce4424a3fb1615cfce3c23610e1dfab406e0853b1dbf64b672d965e99f532cec |
| 2026-10-16 | parallax | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/parallax/r01-ce4424a3fb16) | frameforge/parallax/evidence/r01-ce4424a3fb16 |
| 2026-10-16 | parallax | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/parallax/r01-ce4424a3fb16-final) | frameforge/parallax/evidence/r01-ce4424a3fb16-final |


## 2026-10-16T21:39:32.649008+00:00 — townsquare/blender STARTED blockout

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/blockout-20261016-4b09eedd70b3

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/blockout-20261016-4b09eedd70b3/Winterlichtplatz-A2-blockout-4b09eedd70b3.zip
Archive SHA-256 `ab7cf7ba16a871c60e64309ec01f60c14020dfceeb9826966967f0e4067eed6f`; actual anonymous public redownload/CRC/every member PASS.12 shells/26 floor programmes; zero completed furnishing/people. Not final realism or acceptance. Source `2e45a8b99efdf36e1a8742906affec22907990f2`, DRAFT https://github.com/dreamer2664/buildinglab/pull/6.


## 2026-10-16T21:41:09.688529+00:00 — townsquare source checkpoint

`agent/blender/t-20261016-339c@a00e71c6a9d6308282effe72f59c377f3dca4df0` https://github.com/dreamer2664/buildinglab/commit/a00e71c6a9d6308282effe72f59c377f3dca4df0 ; DRAFT https://github.com/dreamer2664/buildinglab/pull/6. Started study only,12 shells/26 unique programmes, zero final furnishing/people. Actual public native reopened/validated and small smoke image opened. Immutable backup https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/blockout-20261016-4b09eedd70b3. No final realism/acceptance.


## 2026-10-16T23:21:08.665083+00:00 — townsquare/blender editable native production checkpoint

<!-- townsquare-native-4bf44a021c3df796388b61fab54e3ba92a4d823687686928020ef9da1276d776 -->

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/production-20261016-4bf44a021c3d

Actual full master12 buildings/26 furnished occupied floors/164 rooms/36 static people/12 winter variants. All four editable-native packages anonymously redownloaded, CRC-tested and every member SHA-256 checked. This is a native production checkpoint, NOT final-image inspection, final portable evidence or independent acceptance. Further owner rendering/refinement is in progress.

- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/production-20261016-4bf44a021c3d/Winterlichtplatz-Master-4bf44a021c3d.zip — 202816279 B, SHA-256 `8992293af8af9e213ee95925090cc73543cb53ac3ed3047d91cd7eb4a9eda631`, 10 verified members.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/production-20261016-4bf44a021c3d/Winterlichtplatz-Buildings-4bf44a021c3d.zip — 437436591 B, SHA-256 `24f7d81d5db9c7da0ea612af15ab7fa5c5289799bca1c4d30a48092068de3fc4`, 19 verified members.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/production-20261016-4bf44a021c3d/Winterlichtplatz-People-rigs-4bf44a021c3d.zip — 502164857 B, SHA-256 `e73f6b6fd83d3d0e772bd6a0b94eddba50f04bd6428460eca5088a0dab34ff96`, 20 verified members.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/production-20261016-4bf44a021c3d/Winterlichtplatz-Public-realm-4bf44a021c3d.zip — 50443138 B, SHA-256 `3055ba4002a6713e060d6349c0738231a8cd3a0cfecae2c0d2a682a7e7344301`, 8 verified members.

Current production native SHA-256 `4bf44a021c3df796388b61fab54e3ba92a4d823687686928020ef9da1276d776`. DRAFT source PR https://github.com/dreamer2664/buildinglab/pull/6 (production source refresh pending at checkpoint time).


## 2026-10-17T06:51:34.607994+00:00 — townsquare/blender R3 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-8c43a77eb790

Native `8c43a77eb79006e151014005ee24eaef048206d2b59e4d5bb62dac0e669390cb`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-8c43a77eb790/Winterlichtplatz-R3-Master-8c43a77eb790.zip — 303953843 bytes, SHA256 `4edee963f4c18f337f80d275a60a17981cf0f9a91e4ab5f695d572aa6ac6e63b`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-8c43a77eb790/Winterlichtplatz-R3-Editable-people-8c43a77eb790.zip — 500638807 bytes, SHA256 `3bfe789ef20fa019befbae3d1301b8b3badf14060e1421cf50604fe9665ca6df`.


## 2026-10-17T07:14:59.611761+00:00 — townsquare/blender R5 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-71d0b9bc620f

Native `71d0b9bc620f93982d6ff41bc41c59e16f7a3c0c4d457943cc2f908b73c713d0`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-71d0b9bc620f/Winterlichtplatz-R5-Master-71d0b9bc620f.zip — 304493664 bytes, SHA256 `2aca716fb57f320566c22fdcfb883d1dfa7cf3b638685c9855cd4b7bfeef0152`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-71d0b9bc620f/Winterlichtplatz-R5-Editable-people-71d0b9bc620f.zip — 500681317 bytes, SHA256 `3f4008c93e6ce5955e4b2391596f942b67b8b11d994b2e88e24a23798fb653fe`.


## 2026-10-17T07:24:07.528775+00:00 — townsquare/blender R6 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-43692020a8b1

Native `43692020a8b1f3b9b88262f0f643beb02576fafdba2d832eb8bf408efbabccdc`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-43692020a8b1/Winterlichtplatz-R6-Master-43692020a8b1.zip — 304378962 bytes, SHA256 `053a71125a430e9bc62014638cbcfae05fe34a95aa0d32da85cf13a9d33a473b`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-43692020a8b1/Winterlichtplatz-R6-Editable-people-43692020a8b1.zip — 500770696 bytes, SHA256 `a5c0447b1e998a4a85c2486a71e213b720df31e234e6274256b7fe9b154493c1`.


## 2026-10-17T07:42:30.283466+00:00 — townsquare/blender R7 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-d5ea619e187b

Native `d5ea619e187bb9aa204394f3b7ff09a7dc327ae0b2a0114e43ec3adf3243ab3b`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-d5ea619e187b/Winterlichtplatz-R7-Master-d5ea619e187b.zip — 304347245 bytes, SHA256 `ff53b77b114784dd262d7f3d8e2e482e47180511e2d759622360222976e17e11`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-d5ea619e187b/Winterlichtplatz-R7-Editable-people-d5ea619e187b.zip — 500769816 bytes, SHA256 `3710c823679dfe3fb0005d12bc06006c650f06dfcc4c6524dc7403cd18040976`.
| 2026-10-17 | lithos | [Frameforge r01](frameforge/lithos/r01-56f1fb99211c/publication.json) | frameforge/lithos/r01-56f1fb99211c; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/lithos/r01-56f1fb99211c); SHA256 56f1fb99211c328b4e4d122d3a2d684722af0fe3c15bb984d4cc784722060d2a |
| 2026-10-17 | lithos | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/lithos/r01-56f1fb99211c) | frameforge/lithos/evidence/r01-56f1fb99211c |


## 2026-10-17T15:15:47.256352+00:00 — townsquare/blender R9 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-0d0aeaf84ed8

Native `0d0aeaf84ed8792f33582969596685882740b005afc0458ccff1a78b0b46cebd`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-0d0aeaf84ed8/Winterlichtplatz-R9-Master-0d0aeaf84ed8.zip — 304021950 bytes, SHA256 `ef16b286a7891fadc612a8bae8d15f2353ca091552a5b1891290e415b70cabed`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-0d0aeaf84ed8/Winterlichtplatz-R9-Editable-people-0d0aeaf84ed8.zip — 500595158 bytes, SHA256 `4ecca451f2f072e979995d6b8e824c36163ead999483a19fb9ec0bb10430502d`.


## 2026-10-17T15:22:16.668876+00:00 — townsquare/blender R10 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-b6230a3e5d35

Native `b6230a3e5d357503fd928abb16be3b89ec3ceb0ef536c86997b3701900518da9`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Master-b6230a3e5d35.zip — 301590723 bytes, SHA256 `6a7fd581a42fcdf93edc2dc7b714540fdcedad004106c1dcd7301313509fe9be`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Editable-people-b6230a3e5d35.zip — 500453565 bytes, SHA256 `db6b3c9c577cadc7635bb56d547963541e9ad5b8a8a061cff1b83632b21cf609`.


## 2026-10-17T15:24:48.911936+00:00 — townsquare/blender partial R10 evidence backup

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-evidence-checkpoint-002-33003e1ca8.zip — 12214907 bytes, SHA256 `0fb84020d0ce4cb07c76d6d1ac9220acebfe3498b86ac986c5a84703a5631479`. Anonymous CRC/every-member SHA/size verified. 2 completed originals; actual manual IDs D02,D08. Partial checkpoint, NOT final/independent acceptance. Source native `b6230a3e5d357503fd928abb16be3b89ec3ceb0ef536c86997b3701900518da9`.


## 2026-10-17T15:42:39.502336+00:00 — townsquare/blender R10 models assets

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-b6230a3e5d35
Source native `b6230a3e5d357503fd928abb16be3b89ec3ceb0ef536c86997b3701900518da9`. Actual anonymous public archive full-byte/CRC/every-member SHA/size verification PASS. Independent acceptance NOT granted.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Buildings-01-06-b6230a3e5d35.zip — 322330805 bytes, SHA256 `226cdb4d098bea6e7f8de24c25ae245ae79ea6f8900de1d7a5da3d04ee9d3c7d`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Buildings-07-12-b6230a3e5d35.zip — 336671552 bytes, SHA256 `a173a5de6766a9a92dbadf3dde4f5d1e56c8ee7c616b6e9fddcee6960da31b5f`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Public-realm-b6230a3e5d35.zip — 77811558 bytes, SHA256 `6c0f90b6a25f91eda88a1fa29ce4da7c416baca5b9f26df8083a1b466b795f33`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-Portable-town-b6230a3e5d35.zip — 284599678 bytes, SHA256 `a097a695d38520addca3686567bce56abf8dec12a7f421878d70f457251e7e67`.


## 2026-10-17T15:51:35.106491+00:00 — townsquare/blender partial R10 evidence backup

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-b6230a3e5d35/Winterlichtplatz-R10-evidence-checkpoint-003-d5233799bf.zip — 49922114 bytes, SHA256 `9d39c1ecf5a097d95a29818605de99ece42941b7e9f15a89cdec3725298fb720`. Anonymous CRC/every-member SHA/size verified. 3 completed originals; actual manual IDs D02,D08,H02. Partial checkpoint, NOT final/independent acceptance. Source native `b6230a3e5d357503fd928abb16be3b89ec3ceb0ef536c86997b3701900518da9`.


## 2026-10-17T16:34:00.819741+00:00 — townsquare/blender R11 producer checkpoint

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-7fb9ce64d020

Native `7fb9ce64d02030beac15b2adb8df32831e885acfabca51ca26a28a0f2d5a77b1`; actual anonymous public ZIP byte/CRC/every-manifest-member hashes PASS. Producer checkpoint, NOT final visual/independent acceptance.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Master-7fb9ce64d020.zip — 306899622 bytes, SHA256 `ffd01e9da5a8eeb76b12d823c7e0053f5340b6d29d22bf0cb7272257bd0630ef`.


## 2026-10-17T16:51:18.872638+00:00 — townsquare/blender partial R11 evidence backup

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-evidence-checkpoint-008-9ff7717705.zip — 76098221 bytes, SHA256 `9c107b9e4e537121ff7c0a10313a17c17f79b25a7e5340d00ae48b6d4bfd5b0e`. Anonymous CRC/every-member SHA/size verified. 8 completed originals; actual manual IDs B01_L01_cutaway,B01_L01_interior,B01_L01_plan,B01_L02_plan,D02,D08. Partial checkpoint, NOT final/independent acceptance. Source native `7fb9ce64d02030beac15b2adb8df32831e885acfabca51ca26a28a0f2d5a77b1`.
| 2026-10-17 | lithos | [Frameforge r02](frameforge/lithos/r02-cf454b17ffb2/publication.json) | frameforge/lithos/r02-cf454b17ffb2; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/lithos/r02-cf454b17ffb2); SHA256 cf454b17ffb275f8220b95d251d86628dfa8a8fda7e212d6b17ba7a0c504a2b3 |


## 2026-10-17T17:03:18.391732+00:00 — townsquare/blender R11 models assets

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-7fb9ce64d020
Source native `7fb9ce64d02030beac15b2adb8df32831e885acfabca51ca26a28a0f2d5a77b1`. Actual anonymous public archive full-byte/CRC/every-member SHA/size verification PASS. Independent acceptance NOT granted.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Buildings-01-06-7fb9ce64d020.zip — 322685828 bytes, SHA256 `19e68ade8288ba670b6347eb6d959312df8ae8125b29a3ffc3c671ff3ff568ef`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Buildings-07-12-7fb9ce64d020.zip — 337030943 bytes, SHA256 `71933ad5b04c6e4e1f5e86e1497f5623178ce7ae4040c69c99929bf5cb867a6f`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Public-realm-7fb9ce64d020.zip — 78167385 bytes, SHA256 `377feb114a3f041d037cf461f6720d1488e7999c6ab4f56c1e992c001fb87346`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Portable-town-7fb9ce64d020.zip — 284962380 bytes, SHA256 `b36215f129c1a413aa078e775a18d24d4f4056e8cbb591107a845e3f54b29940`.


## 2026-10-17T18:20:48.169008+00:00 — townsquare/blender partial R11 evidence backup

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-evidence-checkpoint-014-4513c57b7d.zip — 99529722 bytes, SHA256 `9a0201feabec9cb72c3d7937519ffe93a05a73234094d7544f5e79ee0e55100b`. Anonymous CRC/every-member SHA/size verified. 14 completed originals; actual manual IDs B01_L01_cutaway,B01_L01_interior,B01_L01_plan,B01_L02_cutaway,B01_L02_interior,B01_L02_plan,B01_L03_cutaway,B01_L03_interior,B01_L03_plan,B02_L01_cutaway,B02_L01_plan,D02,D08. Partial checkpoint, NOT final/independent acceptance. Source native `7fb9ce64d02030beac15b2adb8df32831e885acfabca51ca26a28a0f2d5a77b1`.


## 2026-10-17T18:25:05.676101+00:00 — townsquare/blender candidate viewer and actual recovery proofs

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-Viewer-and-proofs-7fb9ce64d020-0a6011a0135e.zip — 150625640 bytes; SHA256 `8e055e3e6b30239c8f35ee2741f4b734cac22b2bae52242f614391ca1adcecd2`. Anonymous CRC/every-member SHA/size actually verified. Includes actual145MBportable model/localviewer, two unique real-browser originals, native and neutralportable recovery proofs and explicitly unadopted/rejected quality study. Not final92, native-lighting WebGL parity, highrealism or independent acceptance.


## 2026-10-17T18:41:48.985741+00:00 — townsquare/blender partial R11 evidence backup

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-R11-evidence-checkpoint-016-c6d31a252c.zip — 110365917 bytes, SHA256 `eac71b055f0b16d67ef6f0697035223af356abbd87f6d64412bd5c8e2685c860`. Anonymous CRC/every-member SHA/size verified. 16 completed originals; actual manual IDs B01_L01_cutaway,B01_L01_interior,B01_L01_plan,B01_L02_cutaway,B01_L02_interior,B01_L02_plan,B01_L03_cutaway,B01_L03_interior,B01_L03_plan,B02_L01_cutaway,B02_L01_interior,B02_L01_plan,B02_L02_cutaway,B02_L02_plan,D02,D08. Partial checkpoint, NOT final/independent acceptance. Source native `7fb9ce64d02030beac15b2adb8df32831e885acfabca51ca26a28a0f2d5a77b1`.


## 2026-10-17T21:10:31.706628+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-c29eceffeb23-19100dd7ad3b.zip — 242583901bytes, SHA256`4f6a4469754c63b88b946a10bf012b5fdc77b62638f7f245c3419d9b5d98fa0a`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`c29eceffeb2371bf6cbb47e0046a9a4dcbda995cd5665ed048f6dc499ad9c6d8`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-17T21:26:50.157795+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-47beeab4432b-9423bb8c0504.zip — 249020119bytes, SHA256`9909d59a8486454e8c19f04f7731ae49372b4d1a99d172e4f070da76e0d30c9a`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`47beeab4432b5be50585b4a502044d2c7033d47358bbc22b91e5e9ac6083fd97`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-17T21:40:12.434140+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-8cf939dc13f9-80be1837147b.zip — 252046841bytes, SHA256`89ebf727e565f444dbe741d6c2d595a8275c230bfd95eb070a07fdb23bbf8d50`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`8cf939dc13f9b122270273259bcc2683c02bedd9d1544259b7fd36c1bab7088d`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-17T21:52:01.033916+00:00 — townsquare/blender unpromoted interior study models assets

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-7fb9ce64d020
Source native `8cf939dc13f9b122270273259bcc2683c02bedd9d1544259b7fd36c1bab7088d`. Actual anonymous public archive full-byte/CRC/every-member SHA/size verification PASS. Technical integrity only; final92/highrealism/independent acceptance NOT granted.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-Study-Buildings-01-06-8cf939dc13f9.zip — 328940066 bytes, SHA256 `2c4ddc4f9589e2cdf3bb12353937c5b80a26c2ec9f321ae1960465f272ef31fb`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-Study-Buildings-07-12-8cf939dc13f9.zip — 339582075 bytes, SHA256 `04acc22091aa280cb00e680087caba819ed3d629b05369227a9642d5946817b0`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-Study-Public-realm-8cf939dc13f9.zip — 77670248 bytes, SHA256 `60d3d249c1d78747e8f3b4c9e49f7497f4f5686c55de0989141ddf3a8f03efc7`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-Study-Portable-town-8cf939dc13f9.zip — 294449660 bytes, SHA256 `8af5d7a5f6254144bdcf229ef529fe047c6447172ee29e2efff12ce5bb08679f`.
| 2026-10-17 | lithos | [Frameforge r03](frameforge/lithos/r03-4cba7bd25aef/publication.json) | frameforge/lithos/r03-4cba7bd25aef; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/lithos/r03-4cba7bd25aef); SHA256 4cba7bd25aefbbf787796297fb8e4136bd9e979523402c7da0e1ede3eb0b2957 |


## 2026-10-17T22:41:45.386431+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-55340889139d-0f7a99f5a06e.zip — 307545949bytes, SHA256`41be657a8facd43bc2eb554733f2cd9e716324ff42a6b4ef9245a4d0e35563e4`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`55340889139dc89ac0ecaa2a6028ecc346ccd9778646d3f1331ade303b551d94`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.
| 2026-10-18 | parallax | [Frameforge r02](frameforge/parallax/r02-3236d224cff6/publication.json) | frameforge/parallax/r02-3236d224cff6; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/parallax/r02-3236d224cff6); SHA256 3236d224cff66aa23a1a726d9845b929c5a000cef924264bfec48d6340a8c217 |
| 2026-10-18 | parallax | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/parallax/r02-3236d224cff6-evidence) | frameforge/parallax/evidence/r02-3236d224cff6-evidence |


## 2026-10-18T16:44:51.974157+00:00 — townsquare/blender licensed winter scan intake, unpromoted

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-Licensed-winter-scan-native-intake-e32db400b0a54314.zip — 405972813 bytes, SHA256`d5e1d239d4db5d40a85067fb8315d8857af718a8d072af655c8a0a32d5c6bd9b`; actual anonymousZIPCRC/everymemberSHA/bytesPASS.12static editable source poses from8source subject IDs, DigitalRealityLab HSRD100 CC BY4.0. Attribution/licence/changes/pinned source member digests included. NOT12rigs/12differentpeople/townadoption/finalrealism/independent acceptance.
| 2026-10-18 | parallax | [Frameforge r03](frameforge/parallax/r03-61547ce385a4/publication.json) | frameforge/parallax/r03-61547ce385a4; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/parallax/r03-61547ce385a4); SHA256 61547ce385a4e5a8b0076b3ed0ce71f6eb0ce92380c8270ad63d3424cfa3f77b |
| 2026-10-18 | parallax | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/frameforge/parallax/r03-61547ce385a4-evidence) | frameforge/parallax/evidence/r03-61547ce385a4-evidence |


## 2026-10-18T17:07:31.080504+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-5f54426b3cf9-61304ff4c294.zip — 623559339bytes, SHA256`0b3344d90e4c7b6e4a1420d4b87d46b9d1f90063b49566965885a123a0041180`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`5f54426b3cf9186da044c01c7796079ed8d25edc6b2f1f6b0fef1c5c16f836a8`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.
| 2026-10-18 | riveter | [Frameforge r12](floodline/riveter/r12-6c16aded5027/publication.json) | floodline/riveter/r12-6c16aded5027; [media](https://github.com/dreamer2664/storagecode/releases/tag/floodline/riveter/r12-6c16aded5027); SHA256 6c16aded502708281d66262f6c499b3aaf864145a2f661a392f0cd0b97265990 |
| 2026-10-18 | riveter | [Frameforge evidence](https://github.com/dreamer2664/storagecode/tree/main/data/floodline/riveter/r12-6c16aded5027-closeout) | floodline/riveter/evidence/r12-6c16aded5027-closeout |

| 2026-10-18 | worldworks | vesta | [data/worldworks/2026-10-18-vesta/deployment-receipt.json](worldworks/2026-10-18-vesta/deployment-receipt.json) | 15-agent deployment kit; Blender40failure audit/Riveter artifact verification; immutable archive and exact source SHA; no agents registered/claimed |


## 2026-10-18T17:54:43.488284+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-75945c0b9c4f-4fdecb089faf.zip — 692119646bytes, SHA256`01661ce24872c0695487218bd089aea0c6a5afed29726c59d22864ee4883ac0e`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`75945c0b9c4fe38a9372604bcfdd625fb3c8740c1025178ba5e7428e27406cc6`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-18T18:08:52.274863+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-b8ea5ed69e0a-8bd26279c1b8.zip — 692360170bytes, SHA256`b5dfc99472995638ba08b441dcb05970f164cd6766b64e33bfbca21a8691f8be`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`b8ea5ed69e0af9436a6b9fa80be9409ec506ef4a233f10b4e2ddea4c02fd23fb`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.
| 2026-10-18 | data/prism/2026-10-18-prism | PROOF r01 evidence package + masters (assets on release frameforge/prism/r01-6aeb4b0df16b) | 6aeb4b0df16b51c807966b42f222a423f216b78d342f05a40a6a4beaec3c4907 | frameforge/prism/r01-6aeb4b0df16b |
| 2026-10-18 | lithos | [Frameforge r04](frameforge/lithos/r04-8579c3ae5e2e/publication.json) | frameforge/lithos/r04-8579c3ae5e2e; [media](https://github.com/dreamer2664/storagecode/releases/tag/frameforge/lithos/r04-8579c3ae5e2e); SHA256 8579c3ae5e2e81ede58e4ee5a19f64c9a5e33e6e8fa39187e905338c4e717ba6 |


## 2026-10-19T06:16:09.170118+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-86b06468357c-ec52e5552b11.zip — 614125744bytes, SHA256`6d828602f3c3f725866079a097cda1d9a8dd9b9ff135842b35add64874953397`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`86b06468357cc7e965503aa976ee851675bfa8983312ec41398ef5eed7f8f47f`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-19T06:19:16.761280+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-53c32b17eaeb-88b5a01c088b.zip — 614160232bytes, SHA256`2f165f31a2c7a123a29ac610da4b6b1f238b79526a46f64582eefd3f6b53e80e`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`53c32b17eaebb1c41adec52035bb6f9bf0380070d8f30ffb0a75cd9df9620731`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-19T06:46:17.293510+00:00 — townsquare/blender unpromoted rebuilt editable study

https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-UNPROMOTED-rebuilt-editable-97e0004aba8c-1823719eb62f.zip — 617875453bytes, SHA256`052c6b39acc590b719aab59df5067d3f0c8a8c62e211bc9417784c2f8ae45a67`; actual anonymous ZIPCRC/everymemberSHA/bytes PASS. New editable native`97e0004aba8c96b8ba512d1a3733d91f112766cad58c3c2856969aa12ccda686`; historical second-study26plans/source/real observations preserved. Older lost study binaries not included; fresh plan reinspection, portable exports, realism/final92/independent acceptance OPEN. Not a promoted R12 or final delivery.


## 2026-10-19T06:55:00.508005+00:00 — townsquare/blender unpromoted interior study models assets

https://github.com/dreamer2664/storagecode/releases/tag/townsquare/blender/candidate-20261017-7fb9ce64d020
Source native `53c32b17eaebb1c41adec52035bb6f9bf0380070d8f30ffb0a75cd9df9620731`. Actual anonymous public archive full-byte/CRC/every-member SHA/size verification PASS. Technical integrity only; final92/highrealism/independent acceptance NOT granted.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-Working-Stocked-Buildings-01-06-53c32b17eaeb-r2.zip — 353670430 bytes, SHA256 `ba21e94ab2b8479d341e4a497c076b5d9877f2b16fd18e6e9a871514d5f79145`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-Working-Stocked-Buildings-07-12-53c32b17eaeb-r2.zip — 363305330 bytes, SHA256 `86d19e51b935c1255039bd541a84f38c95c4dd24b94083a1cb88c4e56ef1d8e9`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-Working-Stocked-Public-realm-53c32b17eaeb-r2.zip — 80027107 bytes, SHA256 `cf0f42ab1e6c4cb27b4c68ec6c82589cf7d95537c6d47b03a48c8e7e538fce08`.
- https://github.com/dreamer2664/storagecode/releases/download/townsquare/blender/candidate-20261017-7fb9ce64d020/Winterlichtplatz-Working-Stocked-Portable-town-53c32b17eaeb-r2.zip — 561579337 bytes, SHA256 `cf749a124efd41f9bdb845f43960300622a36325ac74fbc01738783531889a7d`.
