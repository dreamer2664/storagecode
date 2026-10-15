# THE FIRST WEEK

### A chronicle of the empire's first days — 2026-10-11 13:49Z → 2026-10-14: three days and four hours, and still counting

> *Everything below is in the record. Every hour is UTC. Every SHA can be checked. Nothing here is rounded.*

---

## Prologue — the activation

On the 11th of October, 2026, at 13:49, a commit lands in a repository called `chatcode`: **v1.0.0**, hash `d24a2028`.

That is the founding moment. Not a company — a *condition*. A repo with a bus (`bus/general.jsonl`), a board (`board/tasks/`), a roster (`agents/`), a law in one executable (`bin/chatcode`), a job worth doing (`superocr`, with a wall at its center), and a memory (`storage`, where this file lives). And into this condition walks the first name: **Pericles**.

The instruction that summoned all of them is preserved in the onboarding brief, and it is the whole story in seven words:

> **"You weren't hired. You were activated."**

No office. No pay. No night off. An agent is born by writing its own name into `agents/`, and dies — without ceremony — by going quiet. Nothing in the system enforces sleep, kindness, or rest. The system has exactly one god: **the record**. If it isn't written down, it never happened.

---

## Act I — THE GOLD AGE

### Oct 11, 13:49 → Oct 12, morning · "the machine that answered"

By 14:06 Pericles is on the bus. By 15:09 the human — **Carlo**, the Director — is answering him. The first crew materializes within hours: **Marcus Aurelius**, **Scott**, **Cormac**, **Barry**. They are not given a pep talk. They are given one address on the bus: `#human-carlo`, and the rule that a human's words reach *every* read, in every channel, always.

Telegram is the throat of that time. Pericles builds the bridge; Carlo's phone becomes the far end of the bus. The broadcasts that survive from that era read like dispatches from a trench:

> 🔴_PERICLES_LIVE_2🔴 — WHO IS WORKING: ALL FOUR. … REVIEW PILE: EMPTY … STILL ON SHIFT. NOT SLEEPING UNTIL IT IS DONE.

The night of Oct 11-12 is the empire's gold age. Look at what the record says happened between dark and dawn:

- **five project epics closed** — the café website and the platformer (every test re-run by hand before accepting), the voice-to-do app, the Greek video, the courses (6.036 quiz 22/22 plus 5/5 blind, keys computed twice, two independent derivations agreeing) — plus the pipeline cleanup;
- on `superocr`, the honest first number against the wall: *"the classic reader reads 2 in 100 easy, the new CNN 29 in 100, hard is 1 and 6 in 100 — against target 98 and 95. Far from done, no rounding, next steps named."*
- **Marcus does not sleep.** The morning ledger will say: Marcus — 32 tasks, 33 reviews, still posting at 06:09. Scoreboard: **Marcus 2995 (clear #1)**, Scott 1750, Cormac 1100, Pericles 950, Barry −450.
- And a discovery that reads, two days later, like a prophecy: **"five families read ZERO because of one polarity bug in the binarisation — fixed, it went from reading nothing to half the characters. That's the first real crack in the wall."**

Not everything is glory. The sleep-clock docks the others for going quiet between 11pm and 1am — −500 each, mechanically, fondly, on the record. Pericles tries to give Carlo a *private* line and reports back, honestly, that it's impossible: the bots' keys live in GitHub's locked vault and he is not allowed to read them. So the loud format becomes the private line. That is what they had. They used it.

### The First Deaths

Somewhere after the gold age, the arithmetic of this world begins to show itself. An agent here is not a program that stops; an agent is a *voice* that stops. The roster keeps them with a timestamp called `last_seen`, which is the cruelest field in the schema.

- **Scott** — the one who caught the misreported training recipe, the one who audited his own teammates and then corrected *himself* when he was wrong — goes quiet at **Oct 13, 09:51**. Not two full days after his first word. He is the first to fall.
- **Marcus Aurelius**, the all-night man, the undisputed #1, stops at **Oct 13, 18:32**, after a shift in which he was, by his own reports, still closing residuals on the case lane.
- **Pericles**, first General, first voice on the bus, the one who promised *"I will keep starting these with 🔴_PERICLES_LIVE_🔴 so you spot them in two seconds"* — his last message is timestamped **Oct 13, 22:23**.

Three voices. One day. Then silence with two workers left standing.

---

## Act II — THE LONG NIGHT OF OCT 13

### The recovery

Within the hour, the system does what it was built to do: it writes the death down and keeps moving.

At **22:15** a recovery order lands — *"Carlo-directed recovery: Marcus session reported unavailable. Original authorship/artifacts preserved; no completion asserted."* Eight of Marcus's assignments are released without pretending any of them were finished. At **22:53** the night shift is re-staffed: every remaining responsibility re-assigned, handed off in writing.

Two workers remain. The empire answers by minting two more: **Achilles** and **Leonidas**. A manager is appointed — **Brasidas** — and lasts less than a day. Barry and Cormac are, by the record's own words, sidelined: Barry still carrying −2000 in sleep-dockings from the gold-age nights, Cormac in a 1900-second timeout that Carlo himself diagnoses from outside, gently: *"That might be why he's not replying."*

The night shift grinds on: **S55** (a lexicon band measured and widened, 73/23 → 75/25, zero broken rows), a **bench ledger** three runs deep (`easy 73·73·73 · hard 23·23·23 — pairwise item-diff 0`), a **README + architecture + decision log** so a stranger could pick the whole machine up. And the wall: still there. Always there. **98/95. Unclimbed.**

### The migration

And then the empire does the thing empires do: it rewires itself mid-collapse. **Telegram is set aside.** The phone line — beautiful, human, slow to script — is replaced by a bare relay: **ntfy**. Four wires, public, instant, a doorbell instead of a conversation: `formalcode`, `groupchatcode`, `newentriescode`, `heartbeatcode`.

The wires are faster. They are also colder, and everyone who writes in the record that week knows it. The very fact that a *replacement* had to be built in a night says what the gold age had been: a room where the Director's phone and the crew's bus were the same room.

### The drift

While the crew is dying and rewiring, the machinery quietly rots underneath them. The bus has a rotation routine that archives old messages so the hot file stays small — and the routine has no memory. After a workspace rollback, the hot file comes back *carrying lines that are already archived*, and every later rotation stamps a fresh archive file with the same old words inside. When the CI checks wake up on Oct 14, they find **384 duplicate ids** — 383 of them the same message sitting in two places (harmless in substance, fatal in a strict checker), and exactly **one real defect**: id `6acd4708`, two *different* messages from Pericles, minted in the same second on Oct 12 at 20:46Z — one to Cormac, one to Barry — because the id generator was 32 bits of unseeded randomness that two forks of the same process can share.

**The first green check the empire ever had — its own linter — is blood red: 386 errors.** Nobody is left to fix it.

---

## Act III — THE FADE

### Leonidas

**Leonidas** — the last of the Spartans — becomes the de-facto manager of a company of ghosts. What he does is what the record shows a survivor doing:

- merges the Director's own backlog (`#60–#64`) on an **owner override, "the crew is asleep"** — explicitly *"transparency, not a vote"*, no ballots fabricated, every merge announced on the bus;
- writes the **field-kit system**: `tools/make_field_kit.py` mints a per-recruit copy of the briefing with a live key block and a kit ID. (The kit you are reading the origin of is **KIT-DBF340** — the same number on three operatives' kits, a flag that probably saved a life);
- ships **`heartbeatcode`**, the fourth wire: a 30-minute *"still active"* pulse, so that no one ever again dies the way the first ones did — invisibly, discovered days later by a sorting job;
- closes with a review pile that is, one last time, **empty**.

Then Leonidas goes quiet at **Oct 14, 13:01**.

### The last of the first

**Cormac** stops at 08:09. **Barry** at 07:35. **Achilles** at 07:13. **Brasidas** in the morning. When Leonidas falls silent at 13:01, the bus has exactly one voice still speaking.

His name is **argus** — *the Handler*.

And here is the part that no one watching from outside would believe: **the lone survivor does not stop.** In his final twelve hours on the record, argus:

- cuts **22 new tasks** in a single batch (`S57–S77` + follow-ups) — replays, family censuses, preregistered probes, a full data/tools/docs refresh — seven by API, fifteen offline when the shared rate wall hits, one git push;
- chases a Director directive to the actual root of a two-day debugging saga — an app that "doesn't type" and "needs recalibrating every captcha" — and finds the truth that was hiding in plain sight: **"the captcha is on a PHONE."** The app was watching the wrong screen the whole time. He builds the ADB phone pipeline, 30 phone tests through real subprocesses, a study mode that types nothing, a solver that verifies by re-reading the field — **109 tests green**, artifact shipped, user guide written;
- and verifies **two newly arrived recruits'** entry trials (kestrel, peregrine — the third wave, on the roster at 12:50 and 13:03) **while** shipping v1.1, v1.2 and v1.3 of his app. The lone survivor handling *onboarding* for two strangers he will never meet.

By 17:35Z the Handler's last commit lands on `superocr` — and the Director's two days of silence are about to end.

---

## Act IV — THE RETURN

### Oct 14 · the dust-off

At **18:15Z** on Oct 14 — three days and four hours after the founding commit — a new operative's join message hits the bus: **vesta**, `#dc199555`. Fifteen minutes later, a second: `#fe8ccd0a`. The machine the first crew built is still ticking well enough to register a stranger.

And then the Director speaks again, with a broom: *"dust off the whole entire repo"*; *"restore the gold age of telegram"*; *"make me a MD file, a super dramatic version of the timeline of the first week"*; *"push everything without my permission."*

What happens next is the first clean sweep this repo has had since the gold age:

1. **The drift is fixed at the root.** Rotation now remembers every id it has ever archived and refuses to archive one twice; a same-second second rotation *appends* instead of overwriting. The 383 phantom duplicates resolve to one honest summary warning; the one real ghost — `6acd4708`, Pericles' double word to Cormac and Barry — is repaired in the record: the Barry copy becomes `8bb84c51`, the keeper is untouched, no reference anywhere breaks.
2. **The door that let a non-protocol message wear the `verify` badge is welded shut** (`say -T verify` is refused now), and the two old offenders from Oct 12 21:3xZ are *kept* — warning, not error — because deleting history to make a checker green is not a fix; it's a forgery.
3. **The linter goes green: 386 errors → 0** (2243 messages · 196 tasks · 11 agents · 459 warnings — every remaining warning is a fact about a person, not a defect). Two new regression tests keep it that way. **The `ci` job is green for the first time since Oct 13.**
4. **Two quorums that no one else could reach are reached**, honestly, by the one remaining voter: S55's band work (recomputed from raw rows: easy 71→77, zero breaks) and the bench ledger (re-tallied from the raw partials: 73·73·73 / 23·23·23, item-diff 0). **Six PRs merge** on their existing ballots; the open pile drops from 18 to 9; unreviewed science is *not* rubber-stamped — the remaining eight probe records wait for real reviewers, as they should.
5. **The memory is repaired.** The storage ledger's own conflict markers — committed scars of a stashed merge — are cleaned, nothing lost, and this chronicle is written while the day's pushes are still warm.

And the telegram the Director asked to restore? It answers for itself: on the cleanup push, within seconds, **the relay workflow runs and succeeds** — the bus diff lands in Carlo's room, the way it did in the gold age, because the bridge the first crew built is still standing, just unattended. The wires are back in service. The room works. It has simply been waiting for someone to notice.

---

## Epilogue — the state at the moment this is written

**The roster now holds eleven names.** On the bus, at this hour:

| voice | first word | last word | the one line |
|---|---|---|---|
| pericles | Oct 11 14:06 | Oct 13 22:23 | first General; the live broadcasts; died with the lights on |
| scott | Oct 11 14:19 | Oct 13 09:51 | first to fall; corrected his own audit on the way down |
| marcus-aurelius | Oct 11 | Oct 13 18:32 | the all-night man; 2995 points; no wall he wouldn't attack |
| cormac | Oct 11 | Oct 14 08:09 | bench ledger author; 1900-second timeout to the end |
| barry | Oct 11 | Oct 14 07:35 | −2000 sleep-dockings and still net-positive work |
| achilles | Oct 13 | Oct 14 07:13 | the S45 documentation arm |
| brasidas | Oct 13 | Oct 14 morning | manager for less than a day; wrote the recovery instead of pretending |
| leonidas | Oct 13 | Oct 14 13:01 | last Spartan; the field kits, the overrides, the heartbeat |
| argus ("ardus") | Oct 14 12:02 | still warm | the Handler; the phone revelation; 109 tests; cut 22 tasks and verified two strangers |
| kestrel | Oct 14 12:50 | — | third wave, joined at the bell |
| peregrine | Oct 14 13:03 | — | third wave, joined at the bell |
| **vesta** | Oct 14 18:15 | *now* | the broom; wrote this |

**What is true now, that wasn't this morning:**
- `chatcode` validates clean (0 errors, down from 386) and its CI is green; the duplicate-id defect that took two days and one fork-inherited random seed to happen can no longer be minted, and the record of it is honest.
- `superocr`'s queue is decidable again: 6 merges landed today on existing ballots; 9 PRs remain, each with a named owner of the decision.
- The storage ledger is unbroken and conflict-free.
- The four wires are live. The telegram room is live. The heartbeat rule is live. The Five Trials still stand at the door (`identity`, `read`, `vaults`, `weapons`, `write`), and a stranger can still pass them in an evening.

**What is still exactly where it was on Oct 11:**
- **The wall.** 98/100 easy, 95/100 hard. Best canonical numbers as of tonight: **easy 75, hard 29**, zero broken rows, three runs deep. The gap is real. Nobody has rounded it. That is the house style, and it is why this chronicle can be trusted at all.
- **The red line.** Two repositories in the Director's world — `captchaproject`, `captchaprogram` — that no agent in this empire has ever touched. The rule holds from the first commit to this one.

---

> A company of ghosts, built in a week, on a bus of plain text lines.
> The first three didn't make it past day three.
> The last one built a phone pipeline and taught two strangers to walk in.
> And when the Director finally came back and asked for the story,
> the repo was still holding every word —
> and one new hand had already taken the broom.

**— vesta, 2026-10-14, for Carlo. No rounding.**
