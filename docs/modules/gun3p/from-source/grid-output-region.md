# Structured-grid E-field export on a user-chosen region

!!! info "From the ACE3P source tree"
    Written by the ACE3P developers in `docs/user/gun3p/grid-output-region.md` and copied here for release `dev` on 2026-10-28. Propose changes in the ACE3P repository, not on this page.

Applies to `gun3pOutputConverter` and to the identical code in `kly3pOutputConverter`.
Added October 2026 (PR #240).

## Summary

`gun3pOutputConverter <input>.gun3p e` can export the electrostatic E field of a Gun3P
solution on a Cartesian grid. Track3P reads that file back as `ElectroStaticFieldMap`
(class `FieldMap3D` in slacsupport) to superimpose a DC gun field on an RF mode, for
example in the `Coax-StaticField` Track3P example.

Until now the grid always spanned the full bounding box of the mesh. For a gun whose
cathode and anode occupy a small fraction of the model, most of the `Nx x Ny x Nz`
points landed outside the mesh and were written as zero, and the useful region was
sampled coarsely. The `Outputs` block now accepts optional `XRange`, `YRange`,
`ZRange` keys that set the grid extent per axis. Axes not given keep the bounding
box, so existing inputs produce exactly the same file as before.

## What was wrong before

- The grid extent was hard-wired to the mesh bounding box
  (`DM_StatisticsManager::boundingBox`). The only user control was the point count.
- For the LSBK sheet-beam gun (model 44 x 44 x 18 cm, gun region about
  4 x 2 x 10 cm) a 12 x 12 x 20 grid put 77 % of its points outside the mesh.
- A missing `Ny` wrote its default into `nx` instead of `ny`, so `ny` stayed
  uninitialised.
- The `Nz` fallback message said 50 while the code used 100.

## Input syntax

The keys live in the `Outputs` block of `ElectrostaticProblem` (for `e`) or
`MagnetostaticProblem` (for `m`), next to the existing export keys.

```
ElectrostaticProblem: {
  ...
  Outputs: {
    Dofs for vizualization: On      // needed by the converter in any case
    ElectrostaticFieldToken: On     // turn the grid export on
    FileName: efield.txt            // written as gun3p_results/OUTPUT/E/<FileName>
    Nx: 50                          // points along x over the chosen region
    Ny: 50
    Nz: 200
    XRange: -0.02  0.02             // optional, metres, min max
    YRange: -0.01  0.01             // optional
    ZRange:  0.0   0.10             // optional
  }
}
```

| Key | Type | Default | Meaning |
|---|---|---|---|
| `ElectrostaticFieldToken` | `On`/`Off` | `Off` | Enable the grid export |
| `FileName` | string | `test.txt` | Output name under `gun3p_results/OUTPUT/E/` |
| `Nx`, `Ny`, `Nz` | int | 50, 50, 100 | Grid points per axis over the region. A value of 1 is raised to 2. |
| `XRange`, `YRange`, `ZRange` | two doubles | mesh bounding box | Grid extent per axis, `min max`, metres. Independent per axis. |

Rules:

- A range may be smaller or larger than the mesh. Points outside the mesh are written
  as zero field, as before. `FieldMap3D::FieldCartesian` also returns zero outside the
  map, so Track3P behaviour is continuous either way.
- Exactly two values per range key. One or three values abort with
  `XRange must have exactly two values (min max), found N. Exiting...`
- `min` must be less than `max`, else
  `XRange: min must be less than max (got 0.02 -0.02). Exiting...`
- The region in use is echoed once:
  `output grid region: x [-0.02, 0.02]  y [-0.01, 0.01]  z [0, 0.1]`

Run the converter as before, on one or more ranks:

```
mpirun -n 1 gun3pOutputConverter dcgun.gun3p e
```

## Output format (unchanged)

Three header lines, then one line per grid point with x varying fastest, then y,
then z. Values are Ex Ey Ez in V/m.

```
<xmin> <xmax> <Nx>
<ymin> <ymax> <Ny>
<zmin> <zmax> <Nz>
<Ex> <Ey> <Ez>
...
```

The header now carries the chosen region rather than the bounding box, which is what
`FieldMap3D` uses to place the map, so no change is needed on the Track3P side.

## How it works

The grid section of `outputConverter.C` builds a `LocalizerCurved` over the local mesh,
then for each grid point finds the containing tetrahedron and interpolates the
node-averaged field `vectField_av` linearly inside it. The change only replaces the
`x1..z2` extents, taken from the bounding box, with the user values when a range key is
present; the localization and interpolation are untouched. That is why a ranged grid
whose points coincide with points of another grid gives identical values (see the
validation).

## Validation

Reproducible test: `gun3p/testsuites-new/grid-region/run.sh` (see its README). It uses
the converged electrostatic DOFs of the CW23 LSBK example
(`/sdf/group/rfar/ace3p/cw23/examples/gun3p/LSBK`, 421 714 tetrahedra, basis order 2),
so no gun3p solve is needed. Five converter runs, then `check.py`:

| Case | Grid | Checks |
|---|---|---|
| `full` (no range keys) | 12 x 12 x 20 over the bounding box | header equals the bounding box in the log; 2880 rows |
| `rangeA` | x +-0.02, y +-0.01, z 0 to 0.10 m, 11 x 11 x 21 | header equals the requested ranges; 2541 rows |
| `rangeB` | same x, y; z 0 to 0.05 m, 11 x 11 x 11 | every point coincides with a rangeA point; field identical there |
| `bad_reversed` | `XRange: 0.02 -0.02` | aborts with the min/max message |
| `bad_single` | `XRange: 0.02` | aborts with the two-values message |

Result on 2026-10-26, converter built from commit 9db95cc83: 15 checks, 0 failures.

| Quantity | full box | rangeA |
|---|---|---|
| points inside the mesh | 22.9 % | 90.5 % |
| max abs E | 7.1e6 V/m | 3.0e6 V/m |
| rangeA vs rangeB at coincident points | | max difference 0.0 |

A trilinear interpolation of the full-box grid onto the rangeA points differs from
rangeA by tens of percent. That is expected: the full-box spacing is 4 cm in x and y
on a gun a few centimetres across, so the coarse grid cannot represent the field
there. It is the reason the region keys are useful.

## Files changed

- `gun3p/src/outputConverter.C`: range keys, region echo, `Ny` fix, `Nz` message.
- `kly3p/src/outputConverter.C`: same change (the file is a verbatim copy of the
  Gun3P converter; a shared helper would remove the duplication but was out of scope).
- `gun3p/testsuites-new/grid-region/`: `README.md`, `run.sh`, `make_inputs.py`,
  `check.py`.

## Follow-up

- `ace3p-docs`: add `XRange`, `YRange`, `ZRange` to the `Outputs` rows in
  `docs/modules/gun3p/index.md` and `docs/reference/commands/gun3p.md`. The generated
  keyword table in `docs/reference/gun3p.md` is refreshed by the docs workflow on the
  next release tag.
- The magnetostatic (`m`) path shares the same code and keys, but was not exercised in
  the validation because the LSBK example has no converged magnetostatic DOFs.
