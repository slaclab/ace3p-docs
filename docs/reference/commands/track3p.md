# Track3P command syntax

Block-by-block description of the `.track3p` input file. Worked cases are in the [Track3P module guide](../../modules/track3p/index.md).

Top-level: `TotalTime`, `ParticlesTrajectories`, `FieldScales`, `NormalizedField`, `Emitter`, `Domain`, `Material`, `OutputImpacts`, `SingleParticleTrajectory`, `Postprocess`. The mesh and fields come from the solver results named in `Domain`; there is no `ModelInfo`.

## TotalTime

```text
TotalTime: 50
```

Tracking duration in RF cycles. Default 20.

## ParticlesTrajectories

```text
ParticlesTrajectories : {
  ParticleFile: partpath
  Start: 0
  Stop:  1000000
  Skip:  1
}
```

Controls `PARTICLES/partpath_ts*.ncdf` output. Only active when `ScanToken` is 0. `Start`, `Stop`, `Skip` are in time steps.

## FieldScales

```text
FieldScales : {
  Type:      FieldGradient
  ScanToken: 1
  Minimum:   23.0e+6
  Maximum:   25.0e+6
  Interval:  1.0e+6
  Scale:     23.00e+6          // used when ScanToken is 0
}
```

| Key | Meaning |
|---|---|
| `Type` | `FieldGradient` (V/m, averaged along the `NormalizedField` line), `InputPortPower` (W, for S3P fields), `StorEnergy` (J) |
| `ScanToken` | 1 scans `Minimum` to `Maximum` by `Interval`, no trajectory files; 0 runs the single level `Scale` and writes trajectories |

## NormalizedField

```text
NormalizedField : {
  Beta:       1
  StartPoint: 0.0 0.0 -0.057
  EndPoint:   0.0 0.0  0.057
  N:          300
}
```

The line along which the accelerating voltage is integrated for `Type: FieldGradient`. `N` points, default 300; `Beta` for the transit-time factor, default 1.

## Emitter

```text
Emitter : {
  Type:          2
  t0: 0   t1: 1                // emission window in RF cycles
  x0: -0.03  x1: 0.035         // bounding box, m
  y0:  0.04  y1: 0.1
  z0: -0.045 z1: 0.0
  BoundaryID:    6
  SkipTimeSteps: 1
  N:             1000          // field emission only
  WorkFunction:  4.2           // eV, field emission only
  Beta:          120           // enhancement, field emission only
}
```

Several `Emitter` blocks may be defined.

| `Type` | Name | Meaning |
|---|---|---|
| 2 | `ElectronicSurface` | Default. Primaries from the mesh surface inside the box. |
| 5 | `SolidElectronicSurface` | From mesh surfaces and from boundaries between material regions; for RF windows. Needs `SolidRegion` and `VacuumRegion` in `Domain`. |
| 7 | `FieldEmission` | Fowler-Nordheim, for dark current. `N` is the minimum electrons per emitted macroparticle; `WorkFunction` default 4.2 eV (copper); `Beta` the field enhancement factor. |
| 10 | `LoadParticles` (new 2025) | Load particles from a file. `ParticlesFile`: one line per particle with electron count, energy in eV, x y z in m, and momentum components. `PositionFile`: positions only, launched with `Velocity` or `Direction` and `Energy`. `RadiationFile`: positions from a radiation-source file. All accept `XScale`, `YScale`, `ZScale`, `EnergyScale`, `XOffset`, `YOffset`, `ZOffset` (defaults 1 and 0). |

Other numbered types exist in the shared emitter code (1 `ThermalCathode`, 3 `Injector`, 4 `EmitterSamples`, 6 `ChildLangmuir`, 8 `PICInput`, 9 `PlaneFieldEmission`); 6 is the model [Gun3P](gun3p.md) uses.

## Domain

```text
Domain : {
  FieldDir:        ./omega3p_results
  ModeID:          0
  FrequencyScanID: 0             // S3P only
  dt:              1
  MaxImpacts:      50
  LowEnergy:       20
  HighEnergy:      5000
  InitialEnergy:   2.0
  Voltage:         0.0 0.0 0.0
  Bins:            64
  SolidRegion:     2             // RF windows
  VacuumRegion:    1
  ExternalMagneticField: 0.0 0.0 4.0
  MagneticFieldMap : { File: bfield2  Scaling: 0.0001  Units: 0.001  ZOffset: 0.27 }
  ElectroStaticFieldMap : { File: ./gun3p_results/OUTPUT/E/test-11.txt  Scaling: 1.0 }
  SymmetryFactor:  2
  SymmetryPlane:   5
}
```

| Key | Default | Meaning |
|---|---|---|
| `FieldDir` | | Omega3P or S3P results directory |
| `ModeID` | 0 | Eigenmode index (Omega3P) or port-mode index (S3P). The source also accepts `ModeID1`. |
| `FrequencyScanID` | 0 | Scan point in an S3P result |
| `dt` | 1.0 | Time step = `dt` / frequency / 100 |
| `MaxImpacts` | 50 | Particles die after this many impacts |
| `LowEnergy`, `HighEnergy` | 5, 1e9 eV | Impact energy window outside which no secondaries are emitted |
| `InitialEnergy` | 2 eV | Launch energy |
| `Voltage` | 0 0 0 | DC coax bias as `a ra rb`: V = a / ln(rb / ra), units V m m |
| `Bins` | automatic | Localizer bins along the longest axis; the others derive from it. **Since v2026.11 omit this key**: the code picks about one element per bin (logged as `Localizer: Bins not given, using N`), which made the KEK 56-cell dark-current run 15x faster with identical results. An explicit value still overrides; old inputs with `Bins: 256` should drop the line. |
| `SolidRegion`, `VacuumRegion` | | Block IDs for window problems |
| `ExternalMagneticField` | 0 0 0 | Uniform B in T |
| `MagneticFieldMap` | | Cylindrically symmetric map in Poisson text format: header lines `r0 rN Nr` and `z0 zN Nz`, then `Fr Fz [Fphi]` rows with r varying fastest. `Scaling` multiplies the field, `Units` converts the coordinates to m, `ZOffset` shifts the origin. |
| `ElectroStaticFieldMap` | | Cartesian-grid field from `gun3pOutputConverter`; `File`, `Scaling` |
| `SymmetryFactor`, `SymmetryPlane` | 1, none | Model symmetry and the sideset of the symmetry plane, used with a `SymmetryPlane` material. Since 2026 the plane's orientation is detected from the mesh, so half models of any orientation work. |

## Material

```text
Material : { Type: Primary    BoundarySurfaceID: 6 }
Material : { Type: Secondary  BoundarySurfaceID: 3 4 6 }
Material : { Type: Absorber   BoundarySurfaceID: 7 8 }
Material : { Type: SymmetryPlane  BoundarySurfaceID: 5 }

Material : { Type: Primary    SolidBlockID: 2 }        // RF window dielectric
Material : { Type: Secondary  SolidBlockID: 2 }

Material : {
  Type: Secondary
  BoundarySurfaceID: 6
  Model: 2
  SecondaryEmissionYield: sey.dat
  MinimumNumElectrons: 1000
  ElasticThreshold:    1000
}
```

| `Type` | Behavior |
|---|---|
| `Primary` | Primaries may launch here |
| `Secondary` | Impacts emit secondaries per `Model` |
| `Absorber` | Impacts kill the particle |
| `SymmetryPlane` | Specular reflection |

`BoundarySurfaceID` is a sideset list; `SolidBlockID` a block, for window dielectrics.

| `Model` | Secondary emission |
|---|---|
| 1 (default) | Multipacting: one secondary per impact, emitted normal to the surface |
| 2 | Dark current: true secondaries and elastically reflected particles at random angles, following a yield table from `SecondaryEmissionYield` (two columns, energy in eV and yield) or inline `Sigma0` and `Einit` lists. `MinimumNumElectrons` and `ElasticThreshold` prune small macroparticles. |
| 3 | Furman-Pivi model with multiple secondaries per impact. `MAT_SecondaryEmitter.C` branches on model 3; the parameters it reads are not in the command reference. |

## OutputImpacts and SingleParticleTrajectory

```text
OutputImpacts:            on      // default off; writes ImpactsInfo_<level>
SingleParticleTrajectory: off     // default off; on writes one file per particle named by ID
```

!!! tip "New since CW23"
    - `ImpactsInfo_<level>` rows for field-emitted particles now carry the **emission field and the emitting face area** (2026), so the dark-current source distribution can be reconstructed from the impacts (inverse current).
    - Particles that leave the mesh without a recorded impact are written to a separate `LostParticles_<level>` file (2026), created only when the count is non-zero. Field-emitted particles at MeV energies are no longer discarded by the multipacting `LowEnergy`/`HighEnergy` filter.
    - The end of `track3p.log` always prints a function-by-function **timing report** (emission, push, material interaction, dead-particle removal) on rank 0, which shows whether more OpenMP threads would help.
    - Track3P is hybrid MPI and OpenMP since 2026; see [Batch jobs](../../workflow/batch-jobs.md#hybrid-mpi-and-openmp-track3p) for the recommended layout.


## Postprocess

```text
Postprocess : {
  Toggle: on
  ResonantParticles : {
    Token:          on
    InitialImpacts: 4
    EnergyRange:    25 10000
    PhaseTolerance: 0.01
  }
  EnhancementCounter : {
    Token:              on
    SEYFileName1:       copper.txt
    BoundarySurfaceID1: 6
    SEYFileName2:       niobium.txt
    BoundarySurfaceID2: 3
    SolidVolID:         0
    MinimumEC:          0.01
  }
}
```

**ResonantParticles** flags trajectories that repeat in phase. `InitialImpacts` (default 4) is the minimum impact count considered; `EnergyRange` in eV discards impacts outside it; `PhaseTolerance` is the phase match criterion.

**EnhancementCounter** computes EC = δ~1~ δ~2~ … δ~m~ over a particle's impacts, with δ~i~ the SEY at the i-th impact energy from the file for that surface. Two surfaces with different materials can be given. `SolidVolID` names a window volume. `MinimumEC` (default 10) suppresses rows below it.

The same counter can be recomputed after the run with a different SEY file by `acdtool postprocess track3p`; see the [acdtool command syntax](acdtool.md#track3p).
