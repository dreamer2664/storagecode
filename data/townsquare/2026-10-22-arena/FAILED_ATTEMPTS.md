# Failed attempts — kept because they are the reason the checks exist

**F-001 · Three serialisation traps, found by a ten-part round-trip test.**
Before generating anything I built a 10-part `.rbxmx`, ran it through Rojo, and read
the output back. Three defects that would each have quietly corrupted 3,000 parts:

* `Color3uint8` is packed **0xRRGGBB** in a place file. I wrote `0xFFRRGGBB`
  (alpha-set), and Rojo masked the alpha: `0xFF8C706A` came back as `0x00A38A6D` —
  every colour wrong. Fixed by packing RGB only.
* `Part.Shape` does not survive Rojo's serialisation: a cylinder came back with no
  shape token. **There are therefore no cylinders in this town** — every part is a
  Block, and round things (lantern heads, tomb-ish lintels, ripples) are facets.
* A lone `Part` as the root of an `.rbxmx` is renamed to the file's name. Everything
  is nested under Model/Folder nodes as a result.

**F-002 · The renderer wrote its shading into a copy.** First renders came out as
blank sky with a faint silhouette. Depth was being written (a mask assignment on a
view) but colour was not: `colour[miny:maxy, minx:maxx].reshape(-1, 3)[mask] = ...`
takes a **copy**, because a slice of an (H,W,3) array is strided. Fixed by masking
the slice itself. Found by instrumenting pixel writes, not by changing cameras.

**F-003 · Per-channel tint explosion.** Walls came out blotchy yellow-green and tree
trunks came out **blue**. Cause: the scan detail map is already normalised to mean 1.0
per channel, and I *also* divided the tint by the scan's mean, so each channel was
scaled independently (blue gained 30%, red lost 30%). Fixed by tinting with the part
colour alone; the measured mean albedo then matched the place colour exactly.

**F-004 · Shadows off indoors = sunlit interiors.** Interior views were pure white
because I disabled the shadow map for interior cameras, so the noonday sun lit every
room as if the roof were not there. Fixed by running a small, tight shadow map over
the building being entered.

**F-005 · A clearance test that could never fail.** My spawn-clearance validator used
`A[3] < B[0] + eps` (deflating one box by eps). For a part thinner than eps this is
unsatisfiable, so it cleared every obstacle — and the negative test
"N07 block the spawn" was MISSED. Fixed by inflating A: `A[3] + eps <= B[0]`. The
corrected test then found that **a bench was standing inside the spawn pad**, and the
spawn moved to a position the test proves clear (0, 0.35, −7).

**F-006 · Negative tests pointing at paths that do not exist.** First negative run:
10/17 caught. The uncaught ones were not weak validators — my *breakers* targeted
`group.startswith("Buildings/B01")` when groups are actually named `B01/L2`. Fixing
the breakers took the suite to 17/17 and exposed F-005.

**F-007 · A negative test that poisoned the next run.** N17 tampers with the spec and
the parity evidence, then restores them. It restored the spec but not
`evidence/export_parity.json`, so the next positive run failed V11 with "1 problem".
Both files are now saved and restored.

**F-008 · Validators counting the wrong thing.** V03/V09/V10 reported every building
as empty because they keyed on `group.split("/")[1]`, which yields `L2` for a group
named `B04/L2`. V04 demanded four rooms on ground floors, but a ground floor is a shop
and a store: two is correct there. Both were validator bugs, not build bugs.

**F-009 · Cameras inside geometry, five times.** The hero camera ended up inside a
building; the sunset camera inside another; the fountain camera behind a lamp post; the
cutaway camera pointed at a *different* building from the one being cut; the spawn
camera behind a bench. Fixed by testing candidate cameras as cheap 480×270 tiles in a
contact sheet and choosing from what was actually visible, and by deriving the cutaway
camera from B04's own position instead of hand-typed coordinates.

**F-010 · Sky showing through the horizon.** Pale patches under the distant buildings
looked like a rendering bug. An ID-buffer pass proved they were **sky**, seen through
gaps between nine isolated hill blocks whose ground plane ended at 200 m. Fixed by
extending the ground to 640 m and closing the ridge with 20 overlapping hills.

**F-011 · No near-plane clipping, so the ground disappeared.** The last and best bug:
pale wedges kept appearing at ground level in half the views. Two ID-buffer passes
attributed them to walls and to sky by turns, which made no sense — until the real
cause: any triangle with a vertex behind the camera was **dropped entirely**. The
640 m ground plane always has a vertex behind the camera, so the ground was culled
in five views and the sky showed through the hole. Interiors survived only because
their slabs are small. Fixed by clipping against the near plane (Sutherland–Hodgman)
and fanning the result, exactly as a rasteriser must. The lesson: "sky visible at
ground level" is a geometry-culling symptom, not a lighting one, and looking at
which *parts* are near the artefact cannot find a part that was never drawn.
