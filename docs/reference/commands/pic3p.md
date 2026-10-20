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
    TotalCharge:  -1e-9
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
      ObserverPlaneZPositions: -2e-2 2e-2
    }
  }

  ConstantField : { E: 0 0 0  B: 0 0 0 }

  DriveField : {
    FieldValueAtPhase0:       -120e6
    FieldComponent:           2
    SamplePoint:              0,0,-6.0325e-2
    CentroidPhaseBeforeCrest: -58
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
| `TotalCharge` | C; negative for electrons |
| `Distribution` | Built-in generator or `File` |
| `Monitors` | Phase-space output control, below |

**Built-in distribution**: `Beta` (initial v/c vector), `NumberOfParticles`, `Radial` with `rMin` and `rMax` (uniform), `Longitudinal` with:

| `Type` | Keys |
|---|---|
| `Flattop` | `DeltaT` duration, `RiseTime` for each edge, both in s |
| `Gaussian` | `SigmaT`, `NumSigma` |
| `Ellipsoid` | `DeltaT` |

**File distribution**: `Distribution : { File: dist.ncdf }`. Create the file from a text table whose first line is the particle count and each following line is `x px y py z pz` in m and normalized momentum, converted with `acdtool postprocess pic3pconvert dist.txt`.

**Self-consistent emission** instead of `Distribution`:

| Block | Keys |
|---|---|
| `FieldEmission` | `BoundaryID`, `Work Function` (eV), `FieldEnhancement`, `MaxCurrentDensity` (A/m²) |
| `ThermionicEmission` | `BoundaryID`, `A`, `B` for J = A exp(B √E), `MaxCurrentDensity` |
| `DCEmission` | `BoundaryID`, `BeamCurrentDensity` (A/m²), `Beta0` |

**Monitors**:

| Key | Meaning |
|---|---|
| `DumpInterval` | Phase-space dump every this many seconds |
| `DumpPhases` | Dump at these drive-field phases, degrees |
| `DumpPositions` | Dump when the bunch centroid reaches these z, m |
| `ObserverPlaneZPositions` | Record every particle crossing of these z planes |

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

A `Solenoid` block with `SolenoidStrength` (T), `Component`, `SamplePoint`, and a `PoissonMap` adds a static focusing field.

## Monitor

`Point` and `Volume` monitors as in T3P; `WakeField` is available but rarely used in PIC. See the [T3P command syntax](t3p.md#monitor).

## Outputs

See the [module guide](../../modules/pic3p/index.md#output) for the particle files and the columns of `particles.stat`. Post-processing with `acdtool postprocess pic3pconvert` and `pic3pstats` is in the [acdtool command syntax](acdtool.md#pic3pstats-and-pic3pconvert).
