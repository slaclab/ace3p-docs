# Faster particle localization and startup

!!! info "From the ACE3P source tree"
    Written by the ACE3P developers in `docs/user/track3p/localization-and-startup.md` and copied here for release `v2026.11` on 2026-10-28. Propose changes in the ACE3P repository, not on this page.

## Problem

Track3P (multipacting / dark-current tracking) spent almost all of its step-loop time finding
the element that contains a particle, not pushing it. On the KEK 56-cell field-emission case
(3.4M tetrahedra, 2.1 GB S3P field) a 30-RF-cycle run took **1794 s** on one S3DF ampere node
(16 threads), of which 1674 s was the step loop; with 4 MPI ranks it still took 1332 s. The
Pillbox multipacting test (12K nodes) is small enough that the same cost only shows as a 1.3x
to 1.8x slowdown.

Two causes, both in the localizer (`LocalizerCurved`, emfem):

1. **Grid resolution.** The localizer is a uniform grid of bins along the longest mesh axis;
   each bin lists the elements whose bounding box overlaps it. The default was 64 bins (and
   production inputs carried `Bins: 256`). On a 3.4M-element mesh that is thousands of elements
   per bin, so every from-scratch search scanned hundreds of candidates with a barycentric test.
2. **Every search was from scratch.** A particle moves a small fraction of an element per step,
   yet each step localized it twice (before and after the push) with the grid, and the boundary
   bisection in `MaterialManager` localized ~14 interior points per dead particle the same way.

A third, independent cost was startup: every rank ran `DM_Numbering` (DOF numbering, 64 s on
KEK) although Track3P never uses DOFs, and every rank re-did the emission sampling for all
emitting faces on N ranks.

## What changed

### 1. Automatic `Domain.Bins` (`LocalizerCurved::autoNumBins`)

`Bins` not given, or `<= 0`, now means automatic: the number of bins along the longest axis is
`ceil(extent / h)` where `h` is the mean element bounding-box extent (sampled), so a bin is about
one element wide. Clamped to at least 16 and to at most 64M bins in total (the cap is applied
through the box shape, so a long thin cavity keeps a fine axial resolution). KEK: 1382 bins,
45 x 114 x 1382 grid, 279 MB, built in 2.3 s. The chosen value is logged:

```
Localizer: Bins not given, using 1382 (about one element per bin along the longest axis; 3398056 elements)
Localizer: 45 x 114 x 1382 bins, 278.8 MB, built in 2.3 s
```

`Bins: N` in the input still overrides. **Existing inputs with `Bins: 256` (the KEK inputs) must
drop the line to get the gain**; 256 is now a pessimization on large meshes.

Results are not affected by the bin count: the grid only decides which candidates are tested,
and a point inside an element is inside it in every bin that overlaps the element.

### 2. Hinted localization (`MeshInterface::localize(position, hint)`)

The particle's previous element is tested first, then its four face neighbours, and only then
the grid. The hint is accepted only when **all barycentric coordinates are >= +1e-3**, ten times
the grid search's own tolerance of 1e-4. Any point that passes is unambiguously inside that
element, so the grid search would return the same element; the result is bit-identical. Points
near a face (where the grid's tie-break between candidates matters) fall through to the grid.

Used in both CPU push overloads (`ParticleManager`), in the boundary bisection of
`MeshInterface::findBoundaryIntersect` (the dead particle's pre-push element, then the element
found at the previous bisection level, are passed as hints), and for new secondaries
(`MAT_SecondaryEmitter`, hit element as hint). Face neighbours are resolved by element id
(`fi.elementid()` via `findContiguous`), because the postprocess mesh stores adjacency ids, not
connected pointers; the pointer form is used when available. On KEK ~81% of lookups skip the
grid. Survivors keep their post-push element as the hint for the next step.

An earlier variant that accepted the hint with the grid's own tolerance inside the bisection
("decision-identical" by argument) was **not** identical in practice: a bisection point within
tolerance of a boundary face but outside the element's bounding box is found by the hint test and
missed by the grid, which moved 4 of 88,246 Pillbox impact rows. It was removed; only the
margin-safe hint is used anywhere.

### 3. One shared vertex field pass for `InterpolationMethod: Linear`

The LINEAR mode (vertex-interpolated fields, the same evaluation the GPU kernel uses) built its
per-vertex E/B cache lazily, by one thread, inside the OpenMP region (~90 s on KEK). It is now
built once by `EMWrap::prepareForTracking()`, called from `genptab` after `setScale()` from the
serial context, and invalidated by the field-gradient scan (generation counter). The vertex values
are the group-averaged point evaluators (volume-weighted over the elements sharing the vertex);
evaluating from a single owner element changes the physics and was rejected.

This also fixes the LINEAR path on master, which aborted with `Error in Domain kvc!` on
`FieldDir` (postprocess) inputs because it still demanded `Meshfile`/`Modefile`.

### 4. Startup

- `EMWrap_Omega3p` inserts `SkipDOFNumbering: on` into the postprocess KVC;
  `DiscreteDomain::setModel` then skips `DM_Numbering::apply` (64 s per rank on KEK).
- Adjacency face hash presized; right-orientation loop parallel (small gains).
- `[STARTUP]` timers (rank 0) in `genptab`, `NewPP`, `DiscreteDomain`.

### 5. Per-rank emitting-face ownership (`EMT_FieldEmission`)

Rank `r` owns faces with `fIdx % commSize == r` and creates all their particles, instead of
every rank sampling every face and keeping every N-th sample. Same particle set, N times less
emission work on N ranks; `Total Emitted Particles` is the `MPI_Allreduce`d global count.

### 6. Reporting

The loop function-by-function timing report is always printed on rank 0 (was `TRACK3P_DEBUG`):

```
  FUNCTION-BY-FUNCTION TIMING REPORT (OMP_NUM_THREADS=8)
  emitterManager.run():          6.771 s ( 29.3%)
  pushParticles():              13.507 s ( 58.5%)
  materialManager.run():         2.427 s ( 10.5%)
  removeDeadParticles():         0.384 s (  1.7%)
  Total loop time:              23.099 s (100.0%)
```

`MM_PHASES[...]` lines (rank 0, every 200 calls, stderr) split `MaterialManager` into bisection,
face lookup and material handling.

## Performance

Measured on S3DF against a build of the pre-change master, same nodes and inputs. EIGEN is the
default exact FEM field evaluation; LINEAR is the vertex-interpolated mode.

**Pillbox multipacting** (12K nodes, 2000 steps; milano node, 1 rank)

| Mode | Threads | before | after | after: loop (push / material) |
|---|---|---|---|---|
| EIGEN | 16 | 7.7 s | 6.1 s | 3.2 s (2.2 / 0.9) |
| EIGEN | 1 | 42.9 s | 24.1 s | 21.0 s (14.6 / 6.3) |
| LINEAR | 16 | aborts | 5.9 s | 3.8 s (2.7 / 1.0) |

**KEK 56-cell field emission** (3.4M elements; ampere node). "before" inputs have `Bins: 256`,
"after" inputs have no `Bins` key (automatic, 1382).

| Run | Mode | before wall (loop) | after wall (loop) | after: push / emission / material |
|---|---|---|---|---|
| 5 cycles, 1 x 16 | EIGEN | 295 s (175 s) | 65.9 s (5.9 s) | 3.3 / 1.5 / 1.0 |
| 5 cycles, 1 x 16 | LINEAR | aborts | 73.2 s (8.0 s) | 4.9 / 2.1 / 0.8 |
| 30 cycles, 1 x 16 | EIGEN | 1794 s (1674 s) | 121.6 s (54.7 s) | 33.3 / 13.8 / 6.4 |
| 30 cycles, 4 x 8 | EIGEN | 1332 s (1207 s) | 82.7 s (23.1 s) | 13.5 / 6.8 / 2.4 |
| 30 cycles, 4 x 8 | LINEAR | aborts | 112.5 s (38.6 s) | 28.3 / 7.9 / 2.1 |

Loop speedup 30x (1 rank) to 52x (4 ranks); walltime 15x to 16x. Of the 30-cycle 4x8 walltime,
~60 s is startup replicated on every rank (mesh read and adjacency ~30 s, 2.1 GB field read
12-16 s), which is now the dominant cost.

**Standard regression suite** (`regression/ace3ptest.py --regex track3p`, milano): 12/12 GOOD
before and after. Wall per test, before -> after:

| Case | 1 MPI | 8 MPI | 1 MPI x 8 OMP |
|---|---|---|---|
| Coax | 27 -> 21 s | 37 -> 33 s | 15 -> 13 s |
| CoaxTWWithReflection | 34 -> 26 s | 8 -> 6 s | 10 -> 8 s |
| PillboxLosslessTenDSlice | 56 -> 17 s | 12 -> 5 s | 11 -> 5 s |
| Window | 19 -> 16 s | 37 -> 32 s | 15 -> 12 s |

## Validation

- Pillbox EIGEN, 1 thread: `ImpactsInfo` and `OUTPUT/resonantparticles` byte-identical to master
  (88,246 impacts, 3,173 resonant).
- Pillbox EIGEN, 16 threads: identical row set ignoring the particle-id column (ids are assigned
  in thread order; master's own 1- and 16-thread files differ the same way).
- KEK 5 and 30 cycles, 1 rank and 4 x 8, EIGEN: `particles.data` (27,534 and 282,178 rows)
  identical to master as a set; Faraday-cup files identical as sets; survived particles identical
  ignoring ids. 4 ranks == 1 rank.
- LINEAR has no master baseline (master aborts); its results are unchanged by the final commits
  and match the GPU kernel to 1e-9 m on the GPU development branch.

How to check "identical" for future changes: compare against a **master build**, at 1 thread for
byte identity; for multi-thread or multi-rank runs sort and drop the id column.

## Where the time goes now, and what is left

KEK 30 cycles, 4 x 8: walltime 83 s = ~60 s startup + 23 s loop (push 13.5, emission 6.8,
material 2.4). Candidates, none done here:

- **Startup replication**: every rank reads, orients and adjacency-hashes the full mesh and reads
  the field. Rank 0 could build and broadcast, or a prepared mesh/coefficient cache could be
  written per mesh+mode.
- **Boundary search**: `MaterialManager` still runs a golden-section bisection with ~14
  localizations per dead particle (now mostly hint hits). A face walk from the pre-push element
  (`findBoundaryIntersect2` exists, unused) would need 1-3 face tests but returns the exact plane
  crossing instead of a point within 1e-6 m of it, so it changes impact positions and emission
  times slightly. Needs a decision and a validation plan beyond bit-identity.
- Remove `Bins: 256` from production inputs.

## Files

`emfem/src/LocalizerCurved.{C,h}` (autoNumBins, findElementWithHint), `emfem/src/NewPP.{C,h}`,
`emfem/src/DiscreteDomain.C` (SkipDOFNumbering, timers), `distmesh/src/DM_AdjacencyManager.C`,
`multipacting/src/MeshInterface.{C,h}` (hinted localize, hinted bisection),
`multipacting/src/ParticleManager.C`, `MaterialManager.C`, `MAT_SecondaryEmitter.C`,
`EMT_FieldEmission.C` (face ownership), `EMT_MPEmission.C`, `EMWrap.h`, `EMWrap_Omega3p.{C,h}`
(Bins default, vertex pass, SkipDOFNumbering), `genptab.C` (prepareForTracking, timers, report).

The same changes are on the `Track3p-GPU` development branch, where the push and emission field
evaluation additionally run on the GPU (OpenACC); the full session log is in
`multipacting/docs/Track3p-GPU-Progress.md` on that branch, and the PR text with the measurement
details is `multipacting/docs/PR-track3p-cpu-localization.md`.
