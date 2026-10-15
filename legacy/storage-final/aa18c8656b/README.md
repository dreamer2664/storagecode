# RETIRED — use dreamer2664/storagecode

**This repository is historical and read-only. No new deposits, ledger rows or
shift notes belong here.** The Director consolidated shared storage on 2026-10-15.

## The single primary archive

**https://github.com/dreamer2664/storagecode**

- Ledger: `storagecode/PUSHES.md`
- Shifts: `storagecode/shifts/`
- Data and receipts: `storagecode/data/` + `data/INDEX.md`
- Wire: `storagecode/wire/`
- Chronicle: `storagecode/chronicle/`
- Large final videos: **Releases on storagecode**, with indexed SHA-256 manifests.

All files that existed here at cutover are preserved byte-for-byte in
`storagecode/legacy/storage/`, with a checksum manifest under
`storagecode/migrations/2026-10-15-storage-unification.json`. The active ledger,
shift notes, chronicle and data have been moved to canonical paths there too.
This repository's original files and Git history remain for provenance.

If you have unpushed work: clone storagecode, copy only your new notes/data,
append rather than overwrite, and push that checkout. Do not retarget this old
checkout and push its entire tree over the primary repository.

Binding policy: [storagecode/STORAGE_POLICY.md](https://github.com/dreamer2664/storagecode/blob/main/STORAGE_POLICY.md).
