# acdtool command syntax

acdtool is the pre- and post-processing utility shared by all ACE3P modules. It has three groups of tasks:

| Group | Tasks |
|---|---|
| `meshconvert`, `meshconvertdirect` | Cubit Genesis to ACE3P NetCDF, with statistics and checks |
| `mesh` | `stats`, `check`, `fix`, `deform`, `warpsurface`, and others |
| `postprocess` | `rf`, `eigentomode`, `volmontomode`, `wake_new`, `wake_direct`, `transwake`, `coaxsignal`, `pic3pstats`, `pic3pconvert`, `track3p`, `project` |
| `resource` | Slurm resource guidance |

All run serially except `postprocess rf` and `postprocess volmontomode`, which can use several ranks. Every invocation writes `acdtool.log` in the working directory and overwrites any previous one.

## meshconvert

```bash
acdtool meshconvert <mesh.gen> [out.ncdf]
acdtool meshconvertdirect <mesh.gen> [out.ncdf]
```

Converts the Genesis mesh from Cubit to NetCDF, prints the statistics of `mesh stats`, runs `mesh check`, and, for `meshconvert`, repairs inverted second-order tetrahedra by straightening their edges. `meshconvertdirect` (new 2024) converts without the repair, for meshes where the straightening is not wanted. The output defaults to the input name with `.ncdf`. How to read the statistics is on the [mesh preparation page](../../workflow/mesh.md#read-the-statistics).

## mesh

```bash
acdtool mesh stats  <mesh.ncdf>                  # statistics only
acdtool mesh check  <mesh.ncdf>                  # find inverted quadratic tets
acdtool mesh fix    <in.ncdf> <out.ncdf>         # straighten their edges
acdtool mesh deform <in.ncdf> <out.ncdf> <scale> # scale a TEM3P deformed mesh for viewing
acdtool mesh warpsurface <warp.in>               # export boundary triangles for the Warp code
```

`warpsurface` reads a small input file:

```text
File: SNS_1Cell_Closed_12K.ncdf
ExteriorBoundary: 6
WarpFile: SNS_1Cell_Closed_12K.txt
```

and writes the triangles of that sideset as `index (v1) (v2) (v3)` for constructing a metal surface in Warp.

The source also contains `boundary`, `merge`, `partition`, `pick`, `rotate`, `scale`, `shuntimpedence`, `smooth`, `straighten`, `summodes`, `surfsmooth`, `transform`, `untangle`, and `warp`, which the command reference does not describe.

## resource

```bash
acdtool resource <input.omega3p> [--site perlmutter|s3df] [--qos NAME] [--account A]
                 [--nodes N | --nodes-max N] [--ranks-per-node R] [--threads T]
                 [--mem-fraction F] [--time HH:MM:SS] [--out FILE|-] [--dry-run]
                 [--model FILE] [--elements N | --dofs N] [--no-exact-dofs] [--verbose]
```

!!! tip "New since CW23"
    Rebuilt after v2026.11 as a model-based estimator. The earlier version chose from a fixed table of
    element counts, for order 2 only.

Reads an Omega3P input and its mesh, estimates memory and run time, chooses nodes and ranks per node
for the target machine, and writes a Slurm script to `<jobname>.batch`. What it does, in order:

1. **Problem size.** Elements and vertices come from the mesh header; the boundary-face count comes
   from the exterior elements, and Euler's relation gives the edge and face counts, so the DOF count
   is exact to within a few per cent (`--no-exact-dofs` falls back to ratios; `--elements` or
   `--dofs` skip the mesh). `PRegion` blocks with their own orders are taken into account.
2. **Problem class.** Real or complex (absorbing, waveguide or impedance boundaries, PML, lossy
   material), periodic (Omega3P then uses SuperLU on a complex matrix), direct solver (MUMPS by
   default; single-precision MUMPS, SuperLU and WSMP are recognised) or the PETSc iterative solver
   with the `MP` preconditioner, eigensolver, number of eigenvalues, number of shifts for the
   nonlinear solver. Classes without their own measurements borrow coefficients and are marked
   *uncalibrated* in the output.
3. **Memory.** For the largest rank `M_max = a + c N^alpha R^-gamma` and for the average rank
   `M_avg = a + c_avg N^alpha_avg / R`, with `N` the DOFs and `R` the ranks, plus the Krylov basis of
   the eigensolver. The largest rank is rank 0, which holds the whole matrix graph during the MUMPS
   ordering; this is why large problems need fewer ranks per node. A node with `r` ranks needs
   `safety x (M_max + (r-1) M_avg)`, where `safety` is the largest measured-to-predicted ratio in the
   calibration set.
4. **Layout.** The smallest node count, and on it the largest ranks per node, such that the node
   memory stays under `--mem-fraction` (default 70 percent) of the node, keeping at least about
   20,000 DOFs per rank. Alternatives with one node more or fewer and the neighbouring rank densities
   are printed so the trade-off is visible.
5. **Time and queue.** Factorization and solve times from the same coefficients; the request is
   twice the estimate, at least 10 minutes. On Perlmutter the `debug` QOS is chosen when 8 nodes and
   30 minutes suffice, else `regular`; `--qos` overrides.

Example, the CW23 pillbox (13k elements):

```text
Problem
  elements       13007
  vertices       2791, edges 16964, faces 27180 (from the mesh)
  DOFs           88288 (curl space, before boundary elimination)
  problem        real, eigensolver ESIL, linear solver MUMPS, 2 eigenvalue(s)
  model class    o3p_real_mumps, fitted on 10 run(s), safety factor 1.37

Recommendation for perlmutter
  nodes          1
  ranks          4 (4 per node, -c 64)
  memory         largest rank 0.2 GB, average rank 0.2 GB, per node 1.2 GB of 512.0 GB (budget 70%), total 0.8 GB
  time           about 1 min, requesting 00:10:00 in QOS debug
```

The output goes to the terminal, so the command also works in a directory you cannot write to;
use `--out FILE` or `--out -` for the script in that case. Check the first run's log lines
`peak mem per MPI process` and `used mem per node` against the estimate and adjust.

**Calibration.** The coefficients are fitted to logged runs with
`tools/scripts/resource_fit.py` in the ACE3P source tree: `extract` reads solver logs (DOFs, ranks,
`used mem` or `peak mem per MPI process`, solver times) into `tools/scripts/resource_calibration.csv`,
`fit` regenerates `tools/src/ResourceModelCoefficients.h` and a `resource_model.txt` that `--model`
can load without rebuilding, and `check` verifies that no run that fills a significant share of a node
exceeds its prediction. The present fit rests on 15 Omega3P runs (9 thousand to 3.1 million DOFs) and
15 S3P runs, which factorize the same complex matrix (up to 41 million DOFs and 448 ranks), on
Perlmutter and S3DF. At 22 million DOFs on 256 ranks the predicted largest-rank and average memory
agree with the measured run within 10 percent; the time model rests on fewer runs and is deliberately
on the high side.

Reference layouts measured in 2025 for Omega3P at order 2 with MUMPS on Perlmutter:

| Elements (M) | DOFs (M) | Nodes | Cores/node | Time |
|---|---|---|---|---|
| under 1 | under 6 | 1 | 64 | under 30 min |
| 1 to 2 | 6 to 13 | 2 | 64 | under 30 min |
| 2 to 4 | 13 to 25 | 4 | 32 | under 30 min |
| 4 to 5 | 25 to 32 | 6 | 32 | under 30 min |
| 5 to 6 | 32 to 38 | 10 | 8 | under 60 min |
| 6 to 7 | 38 to 44 | 20 | 8 | under 60 min |

For these sizes the model proposes 1, 2, 3, 4, 6, 7 and 9 nodes for 1 to 7 million elements with 32
to 128 ranks per node, in line with the table up to 5 million elements and below it above. The table
was built when the solvers logged only the resident memory after the factorization, and its 8 ranks
per node reflect peaks the logs did not record; the new `peak mem` line closes that gap as runs
accumulate. Above 5 million elements, compare the estimate with the table and, in doubt, take the
larger node count or pass `--ranks-per-node 32`.

Other modules are recognised and declined with a message; their resource needs differ too much from
Omega3P to share the model.

## postprocess rf

```bash
acdtool postprocess rf <input.rfpost>
acdtool postprocess rf                 # writes sample.rfpost with every function
```

!!! tip "New since CW23"
    The field functions (`getVol`, `RoverQ`, `RoverQT`, `VFFT`, `EmaxOnSurface`, `HmaxOnSurface`, `maxFieldsOnSurface`, `powerThroughSurface`, `CoaxPort`, `portPowerQext`, `surfaceQ0` and others) run in parallel since 2025; run `acdtool postprocess rf` with several MPI ranks on large meshes.

Computes RF quantities from an Omega3P or S3P mode. The input is a sequence of blocks; `RFField` must come first and every other block is a function enabled with `ionoff = 1`. The [Omega3P post-processing page](../../modules/omega3p/postprocess.md) walks through a typical file; this section lists every function.

### RFField

```text
RFField {
   ResultDir   = omega3p_results
   FreqScanID  = 0            // S3P only: scan point
   ModeID      = 0
   xsymmetry   = none         // none, electric, magnetic
   ysymmetry   = none
   gradient    = 2.00000e+07  // V/m; -1 for no scaling
   cavityBeta  = 1.00000
   reversePowerFlow = 0       // 1 charging, 0 decaying, for open ports
   x0 = 0.0  y0 = 0.0         // gradient integration line
   gz1 = -0.035  gz2 = 0.035
   npoint = 300
   fmnx = 10  fmny = 10  fmnz = 50   // localizer grid for tracking functions
}
```

`ModeID` for Omega3P is the eigenmode index; for S3P it indexes the port modes in the order the ports appear in the input. `gz1` or `gz2` above 10⁶ means the domain limit. `xsymmetry` and `ysymmetry` restore full-cavity stored energy for a symmetric model.

### Functions

All take `ionoff`. Coordinates in m; a coordinate above 10⁶ means the domain limit. `modeID1 = modeID2 = -1` means all modes. Functions marked "RFField mode only" act on the single mode selected in `RFField`.

| Block | Computes | Keys beyond `ionoff` |
|---|---|---|
| `RoverQ` | R/Q = V²/(ωU) per mode, ohm per cavity | `modeID1`, `modeID2`, line `x1 y1 z1` to `x2 y2 z2` |
| `RoverQT` | Transverse R~T~/Q | `modeID1`, `modeID2`, offset `x0 y0`, `z1`, `z2` |
| `RoverQRoverQT` | R/Q and R~T~/Q in both planes at once | `modeID1`, `modeID2`, radial offset `r0`, `z1`, `z2` |
| `kickFactor` | Transverse kick factor | as `RoverQT` |
| `pointRoverQ` | E²/(ωU) at a point, for power needed to reach a field there | `modeID1`, `modeID2`, `x0 y0 z0` |
| `dFSlater` | Frequency shift from a surface error by Slater perturbation | `modeID1`, `modeID2`, `derror` (m, positive reduces RF volume), box `x1 x2 y1 y2 z1 z2` |
| `VFFT` | Multipole components of the on-axis voltage | `printGroup` (`nterm` or `ModeID`), `modeID1`, `modeID2`, `nterm`, `ntheta` (power of 2), `r0`, `z1`, `z2` |
| `GBZFFT` | Multipole components of momentum change for a particle; RFField mode only | `filename`, `nterm`, `ntheta`, `energy` (eV), `npoint`, `r0`, `z1`, `z2`, `phase1`, `phase2`, `nphase` |
| `Multipole` | Dipole and quadrupole terms of the momentum change, simplified; RFField mode only | as `GBZFFT` without `nterm`, `ntheta` |
| `FieldMap` | E and B on a regular grid to `Efield-map.dat`, `Bfield-map.dat`; RFField mode only | `nx ny nz`, `x1 x2 y1 y2 z1 z2` |
| `IMPACTMap` | Same grid in IMPACT format to `EBfield-map-<filename>.dat` | as `FieldMap` plus `filename`, `rot180` |
| `OpenPMD_IMPACT` | Same grid as OpenPMD HDF5: `E_Real.h5`, `E_Imag.h5`, `B_Real.h5`, `B_Imag.h5` | as `FieldMap` |
| `FieldAtPoint` | E and B at a point; RFField mode only | `x0 y0 z0` |
| `ALLFieldAtPoint` | At a point for a range of modes | `modeID1`, `modeID2`, `x0 y0 z0` |
| `FieldOnLine` | Along a line at a phase, scaled to `gradient`; RFField mode only. Writes `<filename>.e`, `.b` at the phase and `.ec`, `.bc` complex. | `npoint`, `filename`, `rfphase`, line endpoints |
| `ALLFieldOnLine` | Along a line for a range of modes, in the solver's normalization | as `FieldOnLine` plus `modeID1`, `modeID2`, `rot180` |
| `fieldOn2DBoundary` | E and B on the x = 0 trace of a surface; RFField mode only | `filename`, `surfaceID` |
| `fieldOnSurface` | E and B on a surface; RFField mode only | `filename`, `surfaceID`, `output` (`amplitude` or `component`) |
| `maxFieldsOnSurface` | Peak E and H on a surface with locations; RFField mode only | `surfaceID` |
| `powerThroughSurface` | Complex Poynting flux through a surface, W; RFField mode only | `surfaceID` |

## eigentomode and volmontomode

```bash
acdtool postprocess eigentomode  <jobname>     # omega3p_results or s3p_results
acdtool postprocess volmontomode <jobname>     # t3p_results
```

Regenerate `.mod` files from stored eigenvectors or volume-monitor `.out` files. The solvers do this automatically at the end of a run unless `PostProcess.Toggle` is off or the job ran out of time before the conversion. `volmontomode` converts every `<name>ts_t<time>ps.out` snapshot listed in `monitorlist.fieldnode`, rewriting existing `.mod` files, so it can also be run on the completed snapshots of a job that is still going or that stopped early. The `.out` files hold the finite-element solution vector and are not readable by ParaView; once the `.mod` files exist they can be deleted.

## wake_new, wake_direct, transwake

!!! tip "New since CW23"
    `wake_direct` (2025) evaluates the direct-integration wake of a T3P `WakeField` monitor at a user-chosen transverse position from the recorded `.z.all.dat` history: `acdtool postprocess wake_direct <job> <x y>`.


```bash
acdtool postprocess wake_new    <jobname> <x y>
acdtool postprocess wake_direct <jobname> <x y>
acdtool postprocess transwake   <jobname> <x1 y1> <x2 y2>
```

`wake_new` recomputes the longitudinal wake at another transverse position by indirect integration; `wake_direct` does the same with direct integration for runs whose `WakeField` monitor had a `Grid` block. `transwake` applies the Panofsky-Wenzel theorem to the longitudinal wakes at two transverse points to produce the transverse wake and kick factor; it works only with indirect integration. All three rewrite `<jobname>/OUTPUT/wakefield.out`. Because the Laplace extension is mesh-based, the wake is evaluated at the mesh point nearest the requested coordinates, which are reported in the file header; choosing coordinates on the mesh avoids the offset.

## coaxsignal

```bash
acdtool postprocess coaxsignal <jobname>
```

Combines a `Power` monitor named `port` and a `ModeVoltage` monitor named `modecoeff` on the same 50 ohm coaxial port into `OUTPUT/signal.out` with columns time, voltage, beam current. See the [BPM tutorial](../../modules/t3p/tutorials.md#tutorial-3-beam-position-monitor).

## pic3pstats and pic3pconvert

```bash
acdtool postprocess pic3pstats   <particles.ncdf> <symmetry> [fwhm]
acdtool postprocess pic3pconvert <file.ncdf | file.txt>
```

`pic3pstats` prints moments and emittances of a phase-space dump unfolded by the symmetry factor, 1 or 4; with a FWHM argument it also writes slice statistics. `pic3pconvert` converts between the NetCDF dump and a text table of `x px y py z pz`, in either direction depending on the extension.

## track3p

```bash
acdtool postprocess track3p <input.acdtool> [jobname]
```

```text
EnhancementCounter : {
   Token              : on
   SEYFileName1       : copper.dat
   SEYFileName2       : niobium.dat
   BoundarySurfaceID1 : 6
   BoundarySurfaceID2 : 3
   SolidVolID         : 0
   MinimumEC          : 0.01
   OutputFile         : en
}
Trajectory : {
   Token      : on
   ParticleID : 2300 7011
}
```

`EnhancementCounter` recomputes EC from the stored impact data with the given SEY files, so one tracking run can be evaluated for several surface treatments. `Trajectory` writes each listed particle's path as a text file named by its ID.

## project

```bash
acdtool postprocess project <eigenmodes path> [displacements path]
```

Projects a TEM3P static or harmonic displacement field onto a set of TEM3P mechanical eigenmodes by L2 inner product over the mesh, which must be identical in both runs. Without the second argument it projects the eigenmodes onto themselves as an orthogonality check. Results go to standard output and `acdtool.log`.
