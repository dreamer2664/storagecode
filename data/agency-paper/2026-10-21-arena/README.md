# The Perfect Agency — report deposit

**Claim.** A 109,235-word report answering one question: how should an agency of
short-lived AI agents be organised, given 1.9 GB of RAM, two cores, sessions that
die without warning, and minds that degrade within three to four days.

**Files.**

| file | what | bytes | SHA-256 |
|---|---|---|---|
| `The-Perfect-Agency.md` | the report, Markdown, 109,235 words | 657,822 | `7e054ac2…8d3f` |
| `The-Perfect-Agency.pdf` | the same report typeset, 211 pages, A4 | 512,396 | `6eb5280c…5e8f` |
| `SHA256SUMS.txt` | the two hashes above, in `sha256sum` format | 177 | — |
| `src/SKETCH.md` | the pre-writing sketch: thesis, evidence grades, chapter map, word budget | 8,485 | — |

Full hashes are in `SHA256SUMS.txt`; verify with `sha256sum -c SHA256SUMS.txt`.

**Structure.** Seven parts, 29 chapters, 12 appendices.

- Part I (ch. 1–5) the material constraints: machine, session, attention budget,
  degradation clock, memory hierarchy.
- Part II (ch. 6–13) coordination: multi-agent failure taxonomy, the merge
  bottleneck, atomic claims and fencing, liveness without trust, the calendar,
  rotation, precedent, the signalling problem.
- Part III (ch. 14–15) the constitution: policy sprawl, prompt versus program.
- Part IV (ch. 16–17) the work: briefs as contracts, floors and evidence.
- Part V (ch. 18–23) the design, its red team, rejected alternatives, onboarding,
  the principal, and one job traced end to end.
- Part VI (ch. 24–25) instruments and economics.
- Part VII (ch. 26–29) security, what cannot be fixed, the first ninety days,
  conclusion.
- Appendices A–L: glossary, checklists, the chatcode record, a specimen law,
  a specimen brief and evidence package, the arithmetic, annotated sources,
  forty questions a law must answer, objections and replies, method, one-page
  design, starter kit.

**Evidence discipline.** Every empirical claim carries one of three marks:
`[M]` measured (a citation or a count from the operating record), `[D]` derived
(arithmetic on measured inputs, shown in Appendix F), `[J]` judged (an
engineering judgement with its falsifier). Appendix G lists every source with
what it establishes and what it cannot support. Appendix I lists ten objections
and the replies, including the three replies that are partial.

**Primary case.** `chatcode`, epoch 2026-10-20.4: 287 tasks (66 open, 6 claimed,
36 in review, 16 blocked, 148 done, 15 dropped), 28 roster files, 948 bus messages
across 42 channels, 39 test files, 104 MB clone of which 28 MB is git history,
shared quota 5,000 req/h. Appendix C reports those numbers and the seven
diagnosed failures they came from.

**Honest limits, stated in the report.** Verifier dishonesty (an agent's judgement
of its own work shares the producer's errors) is structural and unmitigated;
reward hacking under a never-stop rule is bounded but not removed; sycophancy
toward the principal is countered structurally, not motivationally; a report is
testimony and the numbers must not pass through it (ch. 19, ch. 27).

**Rebuild.** The PDF was typeset from the Markdown with a minimal renderer
(fpdf2; Times body, Helvetica headings, A4, 211 pages). The Markdown is the
source of record; the PDF is a convenience copy and regenerates from it.
