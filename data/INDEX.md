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
