# Gun3P command syntax

Block-by-block description of the `.gun3p` input file. The [Gun3P module guide](../../modules/gun3p/index.md) explains the iteration and the sheet beam gun example.

Top-level blocks: `DCGunProblem`, `ElectrostaticProblem`, `MagnetostaticProblem`, `Tracker`.

## DCGunProblem

```text
DCGunProblem : {
  RunId:          test
  SymmetryFactor: 1                        // 1 full, 2 half, 4 quarter
  // JustGenerateTreecotree: On
  ElectricAbsoluteTolerance:  0.
  ElectricRelativeTolerance:  1.00e-12
  ElectricAbsoluteTolerance2: 0.
  ElectricRelativeTolerance2: 1.00e-12
  MagneticAbsoluteTolerance:  0.
  MagneticRelativeTolerance:  1.00e-12
  MaxIterations: 32
  // FirstIterationForMagnetostaticProblem: 1
  Save iteration data: On
}
```

| Key | Meaning |
|---|---|
| `RunId` | Run label |
| `SymmetryFactor` | Scales emitted current to the full gun |
| `JustGenerateTreecotree` | Run on one core to build the tree-cotree gauge for the magnetostatic solve; needed if that solve does not converge. Does not create output. |
| `ElectricRelativeTolerance` | Convergence on the E-field change between iterations with the magnetic solver off |
| `ElectricRelativeTolerance2`, `MagneticRelativeTolerance` | The same with the magnetic solver on |
| `...AbsoluteTolerance` | Always 0 |
| `MaxIterations` | Hard stop |
| `FirstIterationForMagnetostaticProblem` | Iteration at which the beam's self-magnetic field is first included. Commented out means never. |
| `Save iteration data` | Keep per-iteration fields and particles under `OUTPUT/ITER_<n>/` |

## ElectrostaticProblem

```text
ElectrostaticProblem : {
  AnodeBoundaryId: 12
  MeshFile:        dcgun.ncdf
  BasisOrder:      2
  CurvedSurfaces:  on
  Charge averaging factor: 0.1

  VolumeMaterial : {
    Id:         1
    MediumName: Vacuum
    PhysicalParameter : { Name: Permittivity  ConstantValue: 1. }
  }

  Write dofs to disk:     on
  Debug bd dofs mapping:  Off
  Debug matrix assembly:  Off
  Use reduced solver:     On

  Outputs : {
    Dofs for vizualization: On
    ElectrostaticFieldToken: On          // export on a Cartesian grid for Track3P
    FileName: test.data
    Nx: 40  Ny: 50  Nz: 60
    XRange: -0.02 0.02                   // optional, metres; default: mesh bounding box
    YRange: -0.01 0.01
    ZRange:  0.0  0.10
  }

  Boundary : { Id: 1   ConditionType: Dirichlet  DirichletValue: 0. }
  Boundary : { Id: 2   ConditionType: Dirichlet  DirichletValue: -500. }
  Boundary : { Id: 3   ConditionType: Neumann    NeumannValue: 0. }
  Boundary : { Id: 12  ConditionType: Dirichlet  DirichletValue: 115000. }

  Compute non zero initial guess: On
  LinearSolver : {
    Solver:            CG                // CG for large, MUMPSFLOAT for small problems
    Preconditioner:    CHOLESKY
    PrintFrequency:    50
    QuietMode:         0
    AbsoluteTolerance: 1.00e-99
    Tolerance:         1.00e-16
    MaxIterations:     5000
  }
}
```

| Key | Meaning |
|---|---|
| `AnodeBoundaryId` | Anode sideset |
| `MeshFile`, `BasisOrder`, `CurvedSurfaces` | As in TEM3P |
| `Charge averaging factor` | Under-relaxation: new = (1 − f) × previous + f × computed |
| `VolumeMaterial.PhysicalParameter` | `Name` is `Permittivity`, `Permeability`, or `Sigma`; `ConstantValue` its value |
| `Write dofs to disk` | Save the field for the output converter |
| `Use reduced solver` | Eliminate constrained DOFs; keep on |
| `Debug ...` | Developer output; keep off |
| `Outputs.Dofs for vizualization` | Needed for `gun3pOutputConverter` |
| `Outputs.ElectrostaticFieldToken`, `FileName`, `Nx`, `Ny`, `Nz` | Also write E on a structured grid, for `ElectroStaticFieldMap` in Track3P |
| `Outputs.XRange`, `YRange`, `ZRange` | **New in v2026.11.** Optional. Two values each, `min max` in metres, setting the grid extent per axis. Omitted axes use the mesh bounding box. Exactly two values are required and `min` must be below `max`. Points outside the mesh are written as zero. |
| `Boundary` | `Dirichlet` fixes the potential in V; `Neumann` fixes the normal derivative, usually 0 on symmetry and open boundaries |
| `Compute non zero initial guess` | Warm-start each iteration from the previous solution |
| `LinearSolver` | Keep as shown |

## MUMPS

!!! tip "New since CW23"
    Optional top-level `MUMPS` block, read by every module that factorizes with MUMPS; in Gun3P that is the `MUMPSFLOAT` solver of the static problems. Since v2026.11 a factorization that runs out of workspace (MUMPS error -9) is retried automatically with a doubled memory margin, 45 to 90 to 180 to 200 percent, instead of aborting. The block tunes that behaviour; without it only the retry is active.

    ```text
    MUMPS : {
      MemoryRelaxation:    90      // starting margin, percent (default 45)
      MaxMemoryRelaxation: 200     // stop retrying above this (default 200)
      MemoryPerRank:       14000   // optional cap on workspace per rank, MB
      ICNTL_35: 1                  // any raw MUMPS ICNTL(k), applied last
    }
    ```

    If a log shows a retry line, set `MemoryRelaxation` to the value that succeeded to skip the wasted first attempt. Results do not depend on the margin.

## MagnetostaticProblem

Same structure as `ElectrostaticProblem` with all `Boundary` blocks `Dirichlet` 0. The examples keep `Name: Permittivity` in the material, which the code accepts. `Solver: MUMPSFLOAT` is typical.

## Tracker

```text
Tracker : {
  JobName:      ./gun3p_results/OUTPUT     // must match the results directory on the command line
  Particlefile: partpath
  t:            6.0e-6                     // forward tracking time, s
  Generate output for vizualization: on
  Print emission statistics:         On

  Backward : {
    t: 6.0e-6
    Generate output for vizualization: on
  }

  Domain : {
    t0: 0.0
    dt: 1.0e-12
    Window_Vol: 0
    MaxImpacts: 2
    LowEnergy:  0.0
    HighEnergy: 1.0e+99
    InitialEnergy: 0.0
    dt backward: 1.0e-12
    Backward velocity pattern: 0
    Minimum backward velocity factor: 0.01
    Strategy for dt: 0
    Emission Nx: 200   Emission Ny: 100   Emission Nz: 300
    Tracking Nx: 200   Tracking Ny: 100   Tracking Nz: 300
    Tracking box x min: -0.11   Tracking box x max: 0.11
    Tracking box y min: -0.04   Tracking box y max: 0.04
    Tracking box z min: -0.001  Tracking box z max: 0.18
  }

  Monitor : {
    Type: PlaneCrossingsVsT
    Name: screen
    Plane point:  0., 0., 0.15999
    Plane normal: 0., 0., 1.
    Compute densities: On
    Max x for densities: 0.110   X number of densities: 11
    Max y for densities: 0.004   Y number of densities: 80
  }

  MeshInterface : { Type: pd  Localizer : { Type: USS_Curve } }

  Emitter : {
    Type:       6                          // Child-Langmuir
    BoundaryID: 1
    t0: -1.0e-12   t1: 1.0e-12
    N: 1.0e+0                              // electrons per macroparticle
    M: 9.10938e-31                         // kg
    Q: -1.60218e-19                        // C
    d: 0.1e-3                              // macroparticle radius, m
    Sample Type: 1                         // 1 face centers, 2 stochastic
    Child Langmuir : {
      Whole boundary is emitter: On
      Use electric field direction for initial forward velocity: On
      Strategy: 6
      Use average J: On
      Backward velocity factor: 0.66666667
      Forward velocity factor: 1.
      Min allowed distance: 0.01e-3
      Max allowed distance: 5.00e-3
      Given delta phi: 100.0
      Max allowed emission distance wrt z axis: 1.000000
      First inter cycle factor: 1.0
      Inter cycle averaging factor: 1.0
      Max allowed total current: 1.35e+9     // μA
      Reference z for emission surface: 1.50e-3
      Particles per face: 5
    }
  }

  Material : { BoundarySurfaceID: 1  Type: 2 }   // 1 Reflector, 2 Absorber, 3 Secondary, 4 Test, 5 SymmetryPlane
  Material : { BoundarySurfaceID: 2  Type: 2 }
}
```

| Key | Meaning |
|---|---|
| `JobName` | Output path; agree with the second command-line argument |
| `t` | Forward tracking duration. Long enough for the slowest particles to reach the screen. |
| `Backward` | Backward tracking from the emission reference plane to the cathode, used to set launch conditions |
| `Domain.Emission N*`, `Tracking N*` | Localizer grid resolution in the emission and tracking regions |
| `Domain.Tracking box` | Region outside which particles are dropped |
| `Monitor.PlaneCrossingsVsT` | One plane; reports emittances and, with `Compute densities`, current density on a grid of `X number` by `Y number` cells out to `Max x` and `Max y` |
| `Monitor.PlanesCrossing` | A stack: `First plane point`, `Common plane normal`, `Distance between first and last planes`, `Number of planes` |
| `MeshInterface` | Localizer; keep as shown |
| `Emitter.Type` | 6 for Child-Langmuir, the usual gun model. Types 1 to 5 are shared with Track3P. |
| `Emitter.Child Langmuir` | `Reference z for emission surface` is where the field is sampled to set the current; `Particles per face` controls emission granularity and can be tuned for convergence; `Max allowed total current` is a cap in μA. The rest are iteration-strategy settings documented as "keep as default". |
| `Material` | Particle behavior per sideset, numbered 1 to 5 |

## gun3pOutputConverter

```bash
gun3pOutputConverter dcgun.gun3p e [iter]     # electric field
gun3pOutputConverter dcgun.gun3p m [iter]     # magnetic field
```

Converts the stored DOFs of the final iteration, or of iteration `iter`, into `OUTPUT/E/staticDofs.ncdf.mod` or `OUTPUT/M/...` for ParaView, and writes the Cartesian-grid field file when `ElectrostaticFieldToken` was on.
