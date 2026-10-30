# S3P command syntax

Block-by-block description of the `.s3p` input file. Worked cases are in the [S3P module guide](../../modules/s3p/index.md).

Top-level blocks: `ModelInfo`, `FiniteElement`, `FrequencyScan` (or `WaveguideFrequency`), `Port`, `Loading`, `LinearSolver`, `PostProcess`.

## ModelInfo

Identical in form to [Omega3P's](omega3p.md#modelinfo), including `Material` with `EpsilonImag` and `MuImag`, `PML`, `SurfaceMaterial`, and the [`Plasma`](omega3p.md#plasma-material) material. Boundary types available: `Electric`, `Magnetic`, `Exterior`, `Impedance`, `Absorbing`, `Waveguide`. Periodic boundaries are not available in S3P.

Two extensions to `SurfaceMaterial` matter in S3P:

```text
SurfaceMaterial : {
  ReferenceNumber: 3
  Sigma:     5.8e7
  Frequency: 5e9                 // frequency at which Sigma applies
  Coating : {
    Type:      ThinLossyDielectric
    Epsilon:   56
    Sigma:     12
    Thickness: 1.e-3
  }
}
```

`Frequency` fixes the frequency at which the surface impedance is evaluated for an `Impedance` boundary. `Coating` adds a thin lossy dielectric layer on the conductor without meshing it; see the [T3P surface impedance tutorial](../../modules/t3p/tutorials.md#tutorial-5-surface-impedance-with-a-thin-lossy-coating) for the physics.

### Lorentz dispersion

!!! tip "New since CW23"
    A `Material` may be frequency dependent through a Lorentz model. S3P re-evaluates the permittivity at every scan frequency. Validated against HFSS on a dielectric-loaded waveguide.

    ```text
    Material : {
      Attribute: 1
      Epsilon:   4.0
      Dispersion : {
        Type:    Lorentz
        Omega_0: 6.2832e+10        // resonance angular frequency, rad/s
        Omega_p: 3.7698e+10        // oscillator strength, rad/s
        Gamma:   3.0159e+09        // damping rate, 1/s
        Eps_inf: 4.0               // high-frequency permittivity
      }
    }
    ```

    The same block drives the time-domain model in [T3P](t3p.md#modelinfo).

## FiniteElement

As in Omega3P: `Order` 1 to 6 and `CurvedSurfaces`.

## FrequencyScan

```text
FrequencyScan : {
  Start:    9.424e+9
  End:      14.424e+9
  Interval: 0.2e+9
}
```

Frequencies in Hz. If `Interval` exceeds `End − Start`, only `Start` is computed. For a single frequency the shorthand `WaveguideFrequency: 1.3e+9` at top level is equivalent.

## Port

```text
Port : {
  ReferenceNumber: 7
  NumberOfModes:   2
}
```

One per `Waveguide` surface; absent, one mode is loaded. Load every mode that propagates anywhere in the scan range.

## Loading

!!! tip "New since CW23"
    `DipoleLoading` (2024, strength key 2026) drives the structure from a point dipole instead of a port, for antenna-style and near-field problems or for identifying modes.

Dipole excitation as an alternative to port excitation, for mode identification:

```text
Loading : {
  Type:       DipoleLoading
  Coordinate: 0., 2., 0.         // m
  Direction:  0.0, 1.0, 0.0
  Tolerance:  0.001
  Power:      1.                 // dipole moment, A·m
  Frequency:  30.e3              // Hz
}
```

`Tolerance` sets how closely the dipole direction must align with the nearest element edge.

## LinearSolver

The default is the MUMPS direct solver. For large problems use an iterative solver with the multilevel preconditioner, which requires `Order: 2`:

```text
LinearSolver : {
  Solver:         GMRES          // MUMPS, GMRES, CG, QMR
  Preconditioner: MP
  MaxIterations:  5000
  Tolerance:      1e-10
  PrintFrequency: 50
  QuietMode:      0              // 1 suppresses iteration output
}
```

`MP` first solves at order 1 with MUMPS to build a preconditioner, then iterates at order 2. The 2025 release notes give a resource table for this configuration on Perlmutter: 7 million elements on 4 nodes in 10 minutes, 47 million on 32 nodes in 2 hours.

!!! tip "New since CW23"
    PETSc CG with the `MP` preconditioner (2026) is an alternative to the in-house iterative solvers for very large problems.

PETSc solvers are also available with the same `Solver: PETSc` and `PETScOption` syntax as in [Omega3P](omega3p.md#linear-solver-inside-the-eigensolver). Use `-ksp_type cg` only for lossless problems and `-ksp_type gmres` for lossy ones; complex problems need the `bin-petsc-complex` binaries.

## MUMPS

!!! tip "New since CW23"
    Optional top-level `MUMPS` block, read by every module that factorizes with MUMPS (Omega3P, S3P, T3P, Pic3P, TEM3P, Gun3P). Since v2026.11 a factorization that runs out of workspace (MUMPS error -9) is retried automatically with a doubled memory margin, 45 to 90 to 180 to 200 percent, instead of aborting. The block tunes that behaviour; without it only the retry is active.

    ```text
    MUMPS : {
      MemoryRelaxation:    90      // starting margin, percent (default 45)
      MaxMemoryRelaxation: 200     // stop retrying above this (default 200)
      MemoryPerRank:       14000   // optional cap on workspace per rank, MB
      ICNTL_35: 1                  // any raw MUMPS ICNTL(k), applied last
    }
    ```

    If a log shows a retry line, set `MemoryRelaxation` to the value that succeeded to skip the wasted first attempt. Results do not depend on the margin.

## PostProcess

```text
PostProcess : {
  Toggle:     on
  PortNumber: 7                  // save fields only for this excitation port
  ModeFile:   rec                // default s3p
  WriteLoss:  on
}
```

Without `PortNumber`, fields are written for every port excitation at every frequency, which multiplies the output. `WriteLoss` is read by the shared post-processor in `emfem/src/NewPP.C` and writes `.loss` surface power density files.

## Output files

See the [S3P module guide](../../modules/s3p/index.md#output) for `Reflection.out`, `2dports.log`, and the per-mode port files. acdtool's `rf` post-processor reads S3P results with `FreqScanID` selecting the scan point; see the [acdtool command syntax](acdtool.md).
