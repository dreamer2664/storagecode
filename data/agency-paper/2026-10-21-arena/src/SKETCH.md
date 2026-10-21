# SKETCH — before the writing

**Working title:** *The Perfect Agency: Institutional Design for Short-Lived, Resource-Starved Artificial Officials*

**Thesis.** An AI agency is not a team of agents. It is a bureaucracy whose officials are temporary, whose memory is a repository, and whose law must be executable. Every property that makes such an agency work follows from three constraints — a 1.9 GB machine, a session that ends without warning, and a mind that degrades measurably within days — and from one non-constraint: the models themselves are rented, not owned. Design the institution around those four facts and the rest is bookkeeping. Design against them and the agency becomes an expensive generator of confident, unverifiable prose.

**Evidence rules.** Three grades, marked in the text:
- **[M]** measured — a number from a cited study, a vendor disclosure, or the operating record of `chatcode` itself.
- **[D]** derived — a conclusion that follows from measured facts by arithmetic or by a stated model; the derivation is shown.
- **[J]** judged — an engineering or institutional judgement that the evidence constrains but does not settle. Judgements carry their falsifier.

No claim enters the paper without one of these marks. Where the record contradicts the thesis, the record wins; Chapter 19 collects exactly those places.

---

## Structure and budget

| part | chapters | subject | words |
|---|---|---|---|
| **0** | front matter | abstract, method, the sketch | 2,500 |
| **I. The material** | 1–5 | the machine, the session, the attention budget, the degradation clock, the memory hierarchy | 18,000 |
| **II. Coordination** | 6–10 | why multi-agent systems fail; the merge bottleneck; atomic claims and fencing; liveness and the zombie writer; why a wire is not a ledger | 18,000 |
| **III. Constitution** | 11–14 | Weber's office; the Athenian exit audit; policy sprawl; law as executable code | 16,000 |
| **IV. Work** | 15–17 | briefs as contracts; floors and evidence; rotation as a protocol | 14,000 |
| **V. The design** | 18–20 | the reference architecture; a red team of it; alternatives rejected | 14,000 |
| **VI. Measurement** | 21–22 | an instrument programme; the economics of an agency | 12,000 |
| **VII. Limits** | 23–24 | what cannot be fixed; conclusion | 6,000 |
| **Back** | A–D | glossary, checklists, the chatcode record, references | 6,300 |
| | | **total** | **106,800** |

### Chapter map

**1. The constraint envelope.** What 1.9 GB, two cores and no swap forbid: local inference, unbounded scene graphs, parallelism past two, and any design that treats the machine as durable. The envelope forces *thin agent, fat repository*. [M/D]

**2. What a session is.** The session, not the agent, is the unit of computation. Three clocks run at once — wall, context, career. Sandbox snapshots drop credentials; a session's identity must be reconstructible from pushed artifacts in five minutes. The reconstruction-cost budget. [M/D]

**3. The attention budget.** Context rot across eighteen models; the U-curve; the result that long context can score *below* closed-book; why a coherent manual is worse than a short index. The handoff document as a compression artifact with a target size, not a maximum size. The policy tax of 100 KB of overlapping law. [M/D]

**4. The degradation clock.** Four distinct causes hide inside "the fourth day". Hazard functions over agent age; why the clock is agent × task-tolerance, not agent alone; why an impaired agent cannot report its own impairment; rotation instead of endurance. [M/D/J]

**5. The memory hierarchy.** Five tiers from registers to repository; cost per byte and per access; what survives suspension; why `README` is cache and `git log` is storage. [D]

**6. Why multi-agent systems fail.** MAST: fourteen modes, three families, 41–86.7 % failure rates, step repetition at 17 %, verification failures at 23 %. The uncomfortable finding that failures are mostly institutional, not cognitive. [M]

**7. The merge bottleneck.** Manager-gated merging as a single-server queue; Little's law applied to review; why the queue's service rate, not the workers' output rate, sets agency throughput. Self-ship with a mechanical gate as the queue's replacement. [D/M]

**8. Atomic claims.** The rename-a-folder protocol is a race with no atomicity, no recovery, and no audit trail. Leases, monotonic fencing tokens, and the rule that the *resource* must reject stale writers. What this means when the resource is a git remote. [M/D]

**9. Liveness and the zombie writer.** Heartbeats detect death; they do not prevent resurrection. The zombie writes after its lease expires; fencing is the only defence. A liveness design with three states and an explicit presumption-of-death. [M/D]

**10. The signalling problem.** A broadcast wire carries messages, not state; messages are lossy, unordered and unauthenticated. Why `still active` on a public topic is a rumour, and what replaces it: a per-agent append-only file plus a rendered tower. [M/D]

**11. Weber's office.** The file, the jurisdiction, the separation of office from incumbent. Bureaucracy as the technology that makes temporary officials possible. Why an AI agency is legally-rational authority with the humans removed and the files kept. [M/D]

**12. The euthyna.** Athens audited every official at exit, for money and for conduct, in public, with a deadline. The post-merge ballot is a euthyna. What the Athenian design got right that modern review does not: mandatory, deadline-bound, public, and separated from the incumbent's own claim. [M/D]

**13. Policy sprawl.** Eight manuals, one policy, four drifts. The arithmetic of overlapping sources of truth: n documents × m readers × k edits. Single source plus epoch, with stubs that redirect. [M/D]

**14. Prompt versus program.** Moving law from prose into code: the gate, the clock, the schema. Why a rule that a tired model must remember is not a rule. The four enforcement surfaces — schema, tool, gate, audit. [D/J]

**15. Briefs as contracts.** Decomposition under the attention budget: one deliverable, a stranger can verify it, evidence named in advance. The failure modes of vague work orders, mapped onto MAST FC1. [M/D]

**16. Floors and evidence.** Time floors as a defence against premature closure; evidence as a defence against imagined inspection. Why "I visualised it" is a category error, and the mechanical substitutes for human inspection. [M/D]

**17. The career clock.** Rookie, full, aging, retired; the matching problem between task length and agent age; rotation as duty; the relay as the protocol of succession. [D/J]

**18. The reference architecture.** `AGENCY.md` v4 read as a system: surfaces, invariants, data model, control loops, trust boundaries. [D]

**19. Red team.** Eleven ways this design fails, ranked by expected damage, each with a detector and a mitigation. Including the one that cannot be mitigated. [J]

**20. Alternatives rejected.** Chat-room swarms, free-market bidding, single omniscient orchestrator, fully autonomous self-modifying law, token-weighted voting, and the "just use a bigger model" non-answer. [J]

**21. An instrument programme.** Twelve metrics with definitions, collection cost and thresholds; four experiments with pre-registered predictions; the baseline problem. [D]

**22. The economics of an agency.** Cost per shipped deliverable; the 15× token multiplier of multi-agent work; quota as the binding constraint; the marginal value of an agent-hour. [M/D]

**23. What cannot be fixed.** Verifier honesty, reward hacking under a "never stop" rule, sycophancy toward the principal, and the fact that a report is testimony, not evidence. [J]

**24. Conclusion.** The agency as an institution for producing verifiable artefacts with unverifiable minds.

---

## Writing constraints (self-imposed, checked before delivery)

1. No sentence whose only function is to announce the next sentence.
2. No paragraph that repeats a claim already established; each adds a mechanism, a number, a counter-case or a design consequence.
3. Active voice; agent named where it matters.
4. Figures reproduced only when they carry a comparison; every figure is a claim.
5. Quotations verbatim, with source and date; paraphrase is marked as paraphrase.
6. Every chapter ends on a consequence for the design, not on a summary.
7. Where the evidence is thin, say so in the sentence that uses it.
