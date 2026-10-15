# Storage cutover receipt

The Director requested that the fuller of the two archives become primary.
Tracked files on current main were inventoried, excluding Git history.
Winner: storagecode (29 files, 291728 bytes; even excluding generated app/,
232428 bytes); storage (22 files, 127592 bytes). All 22 old files are preserved
byte-for-byte with SHA-256s in migrations/2026-10-15-storage-unification.json.
Canonical root PUSHES, shifts, chronicle and data were installed in storagecode.
Old storage is to be made historical/read-only after verified remote cutover.
No secrets or old data were removed.
