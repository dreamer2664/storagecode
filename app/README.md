# app/state.json \u2014 frozen tombstone

The live state moved to the push-driven rolling branch:
`raw.githubusercontent.com/dreamer2664/chatcode/vigil-state/app/state.json`
(see CONTRACT.md \u00A71). This frozen copy exists for one reason only: a client that
still holds the pre-2026-10-15 app shell fetches this path, and without it that
client would fall back to the sample and show a banner. It is NOT updated and
will be deleted once the old shells have rotated out.
