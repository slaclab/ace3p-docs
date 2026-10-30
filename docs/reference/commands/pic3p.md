# Pic3P command syntax

Block-by-block description of a `.pic3p` input, which is run by the `t3p` executable. The [Pic3P module guide](../../modules/pic3p/index.md) explains the physics and the LCLS gun example.

Top-level blocks: `ModelInfo`, `FiniteElement`, `PRegion`, `Loading`, `TimeStepping`, `Monitor`, `LinearSolver`, `CheckPoint`.

## ModelInfo, FiniteElement, TimeStepping, LinearSolver, CheckPoint

As in [T3P](t3p.md). Boundary types used in PIC: `Electric`, `Magnetic`, `Exterior`, `Absorbing` (beam entry and exit, coax), `Waveguide`.

## PRegion

The causal moving window:

```text
FiniteElement : { Order: 0  CurvedSurfaces: on }
PRegion : { Type: PICCausality  Order: 1 }
PRegion : { Type: PICDomain     Order: 1 }
```

`PICCausality` is the region reachable from the particles within the light cone; `PICDomain` is the sub-region enclosing the particles themselves and may take a higher order, with 2 or above recommended for accuracy. Outside both, the order is 0.

## Loading

```text
Loading : {
  SymmetryFactor: 4
  SymmetryOrigin: 0 0 0

  Particles : {
    TrackingOnly: no
    z0:           -6.0325e-2
    TotalCharge:  -1e-9              // per bunch when NumBunches > 1
    NumBunches:      1               // optional; > 1 injects a train (new 2026)
    BunchSeparation: 8.85426e-11     // s between bunches, required when NumBunches > 1
    Gaussian macroparticle sigma in h/p: 0.5     // finite macroparticle size, noise control
    Gaussian macroparticle width in sigmas: 2
    Distribution : {
      Beta:              0 0 0.003
      NumberOfParticles: 1e3
      Radial :       { rMin: 0  rMax: 1e-3 }
      Longitudinal : { Type: Flattop  DeltaT: 10e-12  RiseTime: 2e-12 }
    }
    Monitors : {
      DumpInterval:            2e-11
      DumpPhases:              18 64
      DumpPositions:           0 1e-2
      ObserverPlaneZPositions: -2e-2 2e-2          // legacy flat list: forward crossings only
      // or, new since 2026, per-plane direction:
      // ObserverPlaneZPositions : { Z: -2e-2 2e-2   Direction: Forward Both }
    }
  }

  ConstantField : { E: 0 0 0  B: 0 0 0 }

  DriveField : {
    FieldValueAtPhase0:       -120e6
    FieldComponent:           2
    SamplePoint:              0,0,-6.0325e-2
    CentroidPhaseBeforeCrest: -58
    RisePeriods:              20                 // optional ramp-up over 20 RF periods (new 2026)
    T0:                       0.                 // ramp start, s
    Omega3PMap : { Directory: omega3p_results  ModeNumber: 1 }
  }
}
```

| Key | Meaning |
|---|---|
| `SymmetryFactor` | 2 for half, 4 for quarter model |
| `SymmetryOrigin` | Point the symmetry planes pass through, m |

### Particles

| Key | Meaning |
|---|---|
| `TrackingOnly` | `yes` disables space charge |
| `z0` | Injection plane, m |
| `TotalCharge` | C; negative for electrons. With `NumBunches` above 1 this is the charge of each bunch. |
| `NumBunches`, `BunchSeparation` | Bunch train: `NumBunches` identical copies of the `Distribution` template injected at `z0` every `BunchSeparation` seconds. Default 1. Only a few bunches are live at once, so hundreds are affordable. Checkpoint-aware. |
| `Gaussian macroparticle sigma in h/p`, `Gaussian macroparticle width in sigmas` | Deposit each macroparticle as a Gaussian of width sigma in units of the local element size over basis order, cut at the given number of sigmas. About 50 % less on-axis field noise at no cost; the log confirms with `Setting finite macroparticle size`. |
| `Distribution` | Built-in generator or `File` |
| `Monitors` | Phase-space output control, below |

**Built-in distribution**: `Beta` (initial v/c vector), `NumberOfParticles`, `Radial` with `rMin` and `rMax` (uniform), `Longitudinal` with:

| `Type` | Keys |
|---|---|
| `Flattop` | `DeltaT` duration, `RiseTime` for each edge, both in s |
| `Gaussian` | `SigmaT`, `NumSigma` |
| `Ellipsoid` | `DeltaT` |

**File distribution**: `Distribution : { File: dist.ncdf }`. Create the file from a text table whose first line is the particle count and each following line is `x px y py z pz` in m and normalized momentum, converted with `acdtool postprocess pic3pconvert dist.txt`.

!!! tip "New since CW23"
    **Per-particle charge** (2026). A seventh column `q` (macroparticle charge in C, signed) gives each particle its own weight, so an upstream tracking code can hand over a modulated bunch. `pic3pconvert` detects the seventh column and writes a `particleCharge` variable into the NCDF file; six-column files behave as before. `TotalCharge` rescales all charges by one common factor, so relative weights are preserved. Set `TotalCharge` equal to the file's sum to use the file values unchanged.

    ```text
    N
    x1 px1 y1 py1 z1 pz1 q1
    x2 px2 y2 py2 z2 pz2 q2
    ```


**Self-consistent emission** instead of `Distribution`:

| Block | Keys |
|---|---|
| `FieldEmission` | `BoundaryID`, `Work Function` (eV), `FieldEnhancement`, `MaxCurrentDensity` (A/m²) |
| `ThermionicEmission` | `BoundaryID`, `A`, `B` for J = A exp(B √E), `MaxCurrentDensity` |
| `DCEmission` (new 2026) | `BoundaryID`, `BeamCurrentDensity` (A/m²), `Beta0` |

**Monitors**:

| Key | Meaning |
|---|---|
| `DumpInterval` | Phase-space dump every this many seconds |
| `DumpPhases` | Dump at these drive-field phases, degrees |
| `DumpPositions` | Dump when the bunch centroid reaches these z, m |
| `ObserverPlaneZPositions` | Record every particle crossing of these z planes. Flat list: forward (+z) crossings only. Container form (new 2026) `{ Z: z1 z2 ...  Direction: Forward Backward Both ... }` sets the direction per plane; one `Direction` entry per `Z`, default `Forward`. Crossing position and time are interpolated to the plane. |

Output goes to `<jobname>/OUTPUT/Particles/`.

### ConstantField

Uniform external `E` in V/m and `B` in T.

### DriveField

The RF field. Several `DriveField` blocks may be given.

| Key | Meaning |
|---|---|
| `FieldValueAtPhase0` | Field at RF phase zero at `SamplePoint`, V/m. Sign convention follows `TotalCharge`. |
| `FieldComponent` | 0, 1, 2 for x, y, z |
| `SamplePoint` | Normalization point, m |
| `CentroidPhaseBeforeCrest` | Injection phase of the bunch centroid, degrees before crest |
| `Omega3PMap` | `Directory` and `ModeNumber` (from 0) |
| `PoissonMap` | `File` and `Frequency` for a Superfish map instead |

| `RisePeriods`, `T0` | Ramp the drive from zero to `FieldValueAtPhase0` over `RisePeriods` RF periods starting at `T0` (s), with a smooth envelope that keeps the drive a clean single tone. Default 0: no ramp. Restart-safe. New 2026. |

A `Solenoid` block with a `PoissonMap` adds a static focusing field. `SolenoidStrength` (T), `Component` and `SamplePoint` renormalize the map to that value at that point; since 2026 they are optional, and when omitted the map is used with its native field values.

## Monitor

`Point` and `Volume` monitors as in T3P; `WakeField` is available but rarely used in PIC. See the [T3P command syntax](t3p.md#monitor).

!!! tip "New since CW23"
    Three particle monitors were added in 2026. Each is a top-level `Monitor` block, one per surface or point, next to the other `Monitor` blocks (not inside `Loading.Particles.Monitors`).

    ```text
    Monitor : {
      Type: EmittedCurrent
      Name: cathode_current          // optional, default emitted_ref<N>
      ReferenceNumber: 5             // the emitter BoundaryID
    }
    Monitor : {
      Type: AbsorbedParticle
      Name: cavity_wall              // optional, default absorbed_ref<N>
      ReferenceNumber: 6
      DumpSteps: 1000                // flush OUTPUT/<Name>.ncdf every N steps; 0 = end of run only
    }
    Monitor : {
      Type: DriveFieldPoint
      Name: drive_on_axis
      Coordinate: 0. 0. 0.02
    }
    ```

    | `Type` | Records | Notes |
    |---|---|---|
    | `EmittedCurrent` | `<Name>.out`: t, I in A, cumulative charge in C | Works for `FieldEmission`, `ThermionicEmission` and `DCEmission`. Values are for the computational domain; multiply by `SymmetryFactor` for the full device. Continues across a checkpoint restart. |
    | `AbsorbedParticle` | `OUTPUT/<Name>.ncdf`: x y z, px py pz, arrival time interpolated within the step, macroparticle charge, for every particle leaving through `ReferenceNumber` | Diagnostic only; the charge is not deposited. Checkpointed. |
    | `DriveFieldPoint` | `<Name>.out`: the applied `DriveField` at `Coordinate` vs t | Shows the ramp and the drive itself; the `Point` monitor records only the scattered field. |


## Outputs

See the [module guide](../../modules/pic3p/index.md#output) for the particle files and the columns of `particles.stat`. Post-processing with `acdtool postprocess pic3pconvert` and `pic3pstats` is in the [acdtool command syntax](acdtool.md#pic3pstats-and-pic3pconvert).
