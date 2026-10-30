# New since CW23: capabilities and where they are documented

ACE3P gained a number of capabilities between the August 2023 Code Workshop (CW23) and release v2026.11. This page lists them by module and records, for each, whether its input syntax is on the matching [command syntax](index.md#command-syntax) page. Every item marked *added 2026-10* was missing from the command pages and has been added, highlighted there with a **New since CW23** box.

## Capabilities by module

| Module | Capability | Input keys | Since |
|---|---|---|---|
| Omega3P, S3P | PETSc Krylov solvers with the multilevel (`MP`) preconditioner; complex PETSc build for lossy and periodic problems | `LinearSolver: { Solver: PETSc  Preconditioner: MP  PETScOption: {...} }`; `bin-petsc-complex` binaries | 2026-05 |
| all | MUMPS workspace auto-retry and runtime options | top-level `MUMPS: { MemoryRelaxation  MaxMemoryRelaxation  MemoryPerRank  ICNTL_<k> }` | 2026-09 |
| Omega3P, S3P | Plasma material with expression-valued density and collision frequency | `Material.Plasma: { Type: Ionosphere  Frequency  ReferenceHeight  Sharpness  Density  CollisionFreq  Epsilon  Sigma }` | 2025-06 |
| Omega3P, S3P | Spherical PML with shifted origin; PML parallel fix | `Material.PML` | 2025-04 |
| S3P | Dipole point-source excitation | `Loading: { Type: DipoleLoading  Coordinate  Direction  Tolerance  Power }` | 2024-12 |
| S3P, T3P | Lorentz dispersive material | `Material.Dispersion: { Type: Lorentz  Omega_0  Omega_p  Gamma  Eps_inf }` | 2025-12 |
| T3P | Nonlinear material with saturation; PETSc SNES or re-linearization | `Chi2  Chi3  Esat2  Esat3`; `TimeStepping.PETScOption.Jacobian`; `LinearSolver.PETScOption.BuildMatrix` | 2023-10 to 2024-03 |
| T3P | Time-varying permittivity | `Omegam  Epsm` | 2025-10 |
| T3P | User-defined excitation pulse from a file | `Pulse: { Type: UserDefinedPulse  File  Frequency  T0  Scaling }` | 2023-10 |
| T3P, acdtool | Direct wake integration at any transverse position | `acdtool postprocess wake_direct <job> <x y>` | 2025-03 |
| T3P | Moving window stable at 512 ranks; `MaximumTime` rule | `PRegion: { Type: AutomaticMovingWindow }` | 2026-09 |
| Pic3P | DC emission model | `Loading.Particles.DCEmission` | 2026-01 |
| Pic3P | Multibunch trains | `NumBunches  BunchSeparation` | 2026-07 |
| Pic3P | Per-particle charge in file-loaded distributions | 7-column file, `particleCharge` NCDF variable, `pic3pconvert` | 2026-07 |
| Pic3P | Drive-field ramp-up | `DriveField.RisePeriods  T0` | 2026-07 |
| Pic3P | Solenoid map without renormalization | `SolenoidStrength`, `SamplePoint`, `Component` optional | 2026-08 |
| Pic3P | Emitted-current monitor | `Monitor: { Type: EmittedCurrent  ReferenceNumber }` | 2026-08 |
| Pic3P | Absorbed-particle monitor | `Monitor: { Type: AbsorbedParticle  ReferenceNumber  DumpSteps }` | 2026-07 |
| Pic3P | Drive-field point monitor | `Monitor: { Type: DriveFieldPoint  Coordinate }` | 2026-07 |
| Pic3P | Observer planes with per-plane direction | `ObserverPlaneZPositions: { Z  Direction }` | 2026-05 |
| Pic3P | Finite macroparticle size for noise control (documented) | `Gaussian macroparticle sigma in h/p`, `Gaussian macroparticle width in sigmas` | 2026 |
| Track3P | Hybrid MPI and OpenMP; automatic localizer grid; hinted localization (15x on KEK 56-cell) | omit `Domain.Bins` | 2023-09 to 2026-10 |
| Track3P | Particles loaded from a file | `Emitter: { Type: 10  ParticlesFile | PositionFile | RadiationFile  XScale ... ZOffset }` | 2025-02 |
| Track3P | Impact records with emission field and area; lost-particle file; automatic symmetry plane | `OutputImpacts`, `LostParticles_<level>`, `SymmetryPlane` | 2026-01 to 2026-08 |
| Track3P | Function-by-function timing report | always on rank 0 | 2026-10 |
| Gun3P | Structured-grid field export on a chosen region | `Outputs: { XRange  YRange  ZRange }` | 2026-10 |
| Kly3P | New module: klystron large-signal solver | `LargeSignalProblem`, `RFProblem.DriveField` | 2024-06 to 2025-05 |
| acdtool | Parallel field functions in `postprocess rf` | run with several ranks | 2025-06 |
| acdtool | Mesh conversion without the fix-up pass | `acdtool meshconvertdirect` | 2024-08 |

## Command-syntax coverage before and after this audit

| Page | Was already documented | Missing before 2026-10-29, now added |
|---|---|---|
| [Omega3P](commands/omega3p.md) | PETSc + MP linear solver, complex build, PML | `Plasma` material, `MUMPS` block, spherical-PML note |
| [S3P](commands/s3p.md) | `DipoleLoading`, PETSc + MP | Lorentz `Dispersion`, `Plasma` pointer, `MUMPS` block |
| [T3P](commands/t3p.md) | `Chi2`/`Chi3`, `Dispersion`, `UserDefinedPulse`, `AutomaticMovingWindow`, `wake_direct` pointer | `Esat2`/`Esat3`, `Omegam`/`Epsm`, SNES `Jacobian`, `BuildMatrix`, the three new monitor types, `MUMPS` block |
| [Pic3P](commands/pic3p.md) | `DCEmission`, `ObserverPlaneZPositions` (flat form), `Solenoid` keys | `NumBunches`/`BunchSeparation`, per-particle charge file format, `RisePeriods`/`T0`, `ObserverPlaneZPositions` container form, `EmittedCurrent`, `AbsorbedParticle`, `DriveFieldPoint`, macroparticle-size keys, optional solenoid renormalization |
| [Track3P](commands/track3p.md) | `Bins` (as a fixed value), `ParticlesFile` | automatic `Bins`, `PositionFile`/`RadiationFile`, impact-record columns, `LostParticles` file, symmetry-plane detection, timing report, hybrid-run pointer |
| [TEM3P](commands/tem3p.md) | (no post-CW23 input changes) | `MUMPS` block |
| [Gun3P](commands/gun3p.md) | `XRange`/`YRange`/`ZRange` | highlight only; `MUMPS` block |
| [Kly3P](commands/kly3p.md) | nothing: the module had no page | whole page |
| [acdtool](commands/acdtool.md) | `meshconvertdirect`, `wake_direct` | highlights; note that `postprocess rf` functions run in parallel |

Items not tied to an input key, and therefore not on the command pages, are described elsewhere: the Track3P speedup and startup changes on the Track3P [notes from the source tree](../modules/track3p/from-source/index.md); hybrid batch scripts under [Batch jobs](../workflow/batch-jobs.md#hybrid-mpi-and-openmp-track3p); build, platform and regression changes in the [releases](../releases/index.md).

## Still to do

- User guides for the Kly3P module and for the T3P nonlinear, time-varying and dispersive materials (the command pages carry the syntax; worked examples exist in `tfe3p/testsuites/` and `kly3p/test/` in the source tree).
- The three Gun3P range keys and the Pic3P macroparticle-size keys are read in a form the keyword extractor does not recognise, so they are absent from the generated keyword tables; they are documented on the command pages.
