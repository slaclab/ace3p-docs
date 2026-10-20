# Corrections to source material

This documentation was converted from the CW18 and CW23 workshop slide decks and grounded in the example directories that ship with them. The slides, the example files, and the stored results do not always agree with each other, and some of the stored results no longer match what the current ACE3P build produces. This page records every such discrepancy found during conversion, what the documentation says instead, and why.

Keep adding to this list. When a reader reports that a value in the docs does not match what they see, check here first; if it is a new case, add it.

## Conventions used in this documentation

- **The example file on disk wins over the slide.** When the slide listing and the file in `examples/` differ, the docs show the file, because that is what a user will run.
- **Stored results are quoted as stored, with their build date.** When a tutorial quotes a number from an `omega3p.out` or `track3p_results/` in the example directory, that number came from whichever ACE3P build produced the stored file, which may be a decade old.
- **Reruns on current builds are labelled as such.** Where the same input has been rerun recently, both results are shown and the difference is discussed rather than hidden.
- **No numbers are invented.** Where an earlier draft of these pages contained an illustrative value that did not come from a file, it has been replaced with the real value or removed. Those cases are listed below under "Errors in earlier drafts of this documentation".

## Omega3P

### Pillbox tutorial (CW18 `cw18-omega3p-updated.pptx`)

| Item | Slide or earlier draft said | Documentation now says | Source of correction |
|---|---|---|---|
| Convergence mesh ordering | Earlier draft: `mesh0` to `mesh3` have `scale` 4, 6, 8, 10 | `scale` 10, 8, 6, 4; `mesh0` is coarsest | The journal files in `examples/omega3p/pillbox-rtop/` |
| Mode 0 Q~0~ | Earlier draft: "about 28,900" | 28,885 | `omega3p_results/omega3p.out` in the example directory |
| Mode 1 Q~0~ | Not given | 33,831 | Same |
| Convergence plot axis | Slide plots dF/F against element count up to 50,000 with five points; the directory has only four mesh journals | Plot reproduced as is; text notes four journals | Count of `mesh*.jou` files |
| Slide 17 input listing | Shows `pillbox-rtop4.ncdf` and commented-out `Tolerance`, `MaxIterations` lines | Docs show the file on disk, which has no commented lines | `pillbox-rtop.omega3p` on disk |

### Coupler tutorial (CW18 slides 44 to 74)

| Item | Slide or earlier draft said | Documentation now says | Source of correction |
|---|---|---|---|
| Coax Q~ext~ | **Earlier draft invented** a mode summary with Q~ext~ of 4100 and Q~0~ of 28,500 | Q~ext~ = 1,024,236, Q~0~ = 28,815, f = 1.3137561 GHz + j641 Hz, quoted verbatim from the stored result | `examples/omega3p/pillbox-rtop+coax/omega3p_results/omega3p.out`. The 30 mm tip offset gives very weak coupling, which the slides never state. |
| Mesh journal curve ID | Slide: `modify curve 11 blend radius 1` | `modify curve 12 blend radius 1` | `step1-Make-90DegreeBend.jou` on disk (this is actually in the S3P bend journal; listed here because the same curve-ID caution applies to the coax journal) |
| Practice 3b first-run results | Slide table shows mode 2 at 2.062 GHz with Q~ext~ 496 | Reproduced as stated; no stored `omega3p.out` for the in1 run exists in the example directory to verify against | Verified only against the slide |

### Lossy load and periodic boundaries (CW18 slides 75 to 83)

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Load input `PostProcess` block | Slide shows it commented out with `Compute Total Energy: 1` | File on disk has `_PostProcess: { Toggle: off }`, which disables the block by renaming it | `pillbox+recWG+load.omega3p` on disk. Both forms disable post-processing; the docs mention neither and show the file as is. |
| PBC input `HFormulation: 0` | Slide includes it in `BoundaryCondition` | Omitted from docs | Not present in `dlwg-pbc4-m0.omega3p` on disk, and not documented anywhere else |
| PBC mesh journal export | Slide: `export genesis "pbc-4.gen" overwrite` after `transform mesh output scale 0.001` | Reproduced as on disk | Matches disk |

## S3P

### Mitered bend (CW18 `cw18-s3p.pptx`)

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Finite element order | Slide 13: `Order: 1` | `Order: 2` | `90DegreeBend.s3p` on disk |
| Frequency scan | Slide 13: 9.424 to 14.424 GHz in 0.2 GHz steps | 9.424 to 12.424 GHz in 0.25 GHz steps, 13 points | File on disk. The S11 plot in the slide and the docs spans the wider range; the caption now says so. |
| Modes per port | Slide 13: `NumberOfModes: 1` | `NumberOfModes: 2` | File on disk |
| Mesh journal curve ID | Slide 9: `modify curve 11 blend radius 1` | `modify curve 12` | `step1-Make-90DegreeBend.jou` on disk |
| Mesh `max_size` | Slide 11 wraps the sizing line across two lines with `max_gradient 1.2` on the second | Single line | Cosmetic |
| Result files | Slide 19 lists `Sparameter.out` and `PortRef7.out` | `Sparameter.out` does not exist in the stored results; port mode files are `PortRef7_0.out`, `PortRef7_1.out` and so on, one per mode | Listing of `s3p_results/` on disk |

### Waveguide load

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Finite element order | Slide 26: `Order: 1` | `Order: 2` | `recWG-load1.s3p` on disk |
| Frequency scan | Slide 23 and 26: 2.456 to 3.056 GHz | 2.556 to 3.156 GHz | File on disk |

### Window

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| WR284 height | Slide 29 journal: `h284 = 34.163` | Reproduced as 34.163 | Matches disk. Note the S3P load example uses 34.036 for the same waveguide designation; both are quoted as found. |
| Mesh journal group syntax | Slide 30: `group 'ms' add surface Is_merged` | `group 'ms' add surface with Is_merged` | `step2-Mesh-window.jou` on disk |
| Mesh journal `merge tolerance` line | Slide 30 shows it | Reproduced | Matches disk |
| Track3P version of the window S3P input | Slide 59 of the Track3P deck includes `HFormulation: 0` | Reproduced only in the Track3P context where it is on disk; omitted elsewhere | `examples/track3p/Window/Window.s3p` has it; `examples/s3p/window/window.s3p` does not |

## Track3P

### Pillbox multipacting (CW18 `cw18-Track3P-Tutorial.pdf`, example `Pillbox`)

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| `MinimumEC` in scan input | Slide 24: `MinimumEC: 1` | `MinimumEC: 0.01` | `Pillbox.track3p` on disk |
| `TotalTime` for scan | Not set, default 20 | Default 20 noted explicitly | `InputParameters` in stored results |
| Trajectory run `TotalTime` | Slide 46: `TotalTime: 5` | Reproduced | `Pillbox2.3MV.track3p` on disk has `TotalTime` absent; the slide value is shown with the file's `EmissionOutput: 1`. Treat as the slide's intent. |
| Omega3P mode 2 frequency | Slide 20: `1.7499342e+09` | Confirmed correct: mode 1 at 1.31381 GHz (Q~0~ 28,877), mode 2 at 1.74993 GHz (Q~0~ 27,463) | Stored `omega3p_results/omega3p.out`. An earlier draft of this page wrongly called the slide value suspicious by comparing against the quarter model's 2.329 GHz. The full model has no symmetry planes, so the first dipole mode appears as mode 2; the quarter model with two magnetic planes excludes it. |
| **Resonant particle counts** | Stored 2016 results: 642, 518, 642 at 23, 24, 25 MV/m | Both the 2016 stored result and a 2026 S3DF rerun are shown | Rerun July 2026 on S3DF with ACE3P commit `92b97112`, same input: 522, 392, 528 |
| **Impact energy range** | Stored 2016 results: 11 to 84 eV | Both shown | 2026 rerun: 24 to 42 eV |
| **Maximum enhancement counter** | Stored 2016 results: 1.40 | Both shown | 2026 rerun: 0.98. The 2016 build predicts a soft multipacting barrier for copper in this range; the 2026 build does not. The documentation presents this as an open discrepancy to be resolved against measurement, not as a settled value. |
| `enhancementCounter` columns | 7 columns | 2026 build appends three columns, `FinalImpactLocationX/Y/Z` | Header line of the 2026 output |
| ParaView version in slide 39 | `ParaView-5.2.0` alias | Omitted | Obsolete |
| Slide 52 trajectory IDs | "select ... output file 2300 and 7011" | 16100 and 15400 | `Pillbox.acdtool` on disk and the files present in the example directory |

### Window, Muon, Tesla

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Muon input material block | Slide 86, 92, 98: `Mat1erial:{ Type: Primary ...}` | `Material:` | Typo is present in the files on disk too. A misspelled block name is silently ignored by the parser, which means the stored Muon runs had **no primary emitter material declared**. The docs show the corrected spelling and this note. Users rerunning the example should fix the file. |
| Muon field map file name | Slide 98: `File: Bfield` | `File: BField` | File on disk and the directory name `BField/` |
| Muon `Emitter` type | Not given, so default type 2 | Default noted | `InputParameters` |
| Tesla secondary SEY data | Slide 123 shows the niobium table in the input | Reproduced; the commented-out copper table in the file is omitted | `Tesla-SEmission.track3p` on disk |
| Tesla run script account | Slide: not shown; file: `#SBATCH -A m669` with `m349` commented | Not reproduced; docs point to Getting Started for account settings | Allocation names are site- and time-specific |
| Window emitter `Type: 5` comment | Slide and file comment: "5: Window MP emission mode" | Named `SolidElectronicSurface` | `EmitterManager.C` in the ACE3P source |
| Emitter type list | Slide 30 lists types 2, 5, 7 only | Full list of ten types from source given in the module page, with the three tutorial-relevant ones described | `EmitterManager.C` |

### Track3P on S3DF (not in any slide)

| Item | Note |
|---|---|
| Hybrid MPI and OpenMP | The slides predate OpenMP support in Track3P. The source now has OpenMP pragmas in the particle loop, field interpolation, and material manager, and the S3DF build enables `-fopenmp`. The docs recommend one rank per socket with threads filling the cores. The 2026 rerun used 1 rank and 16 threads. |
| Results directory for the rerun | The S3DF workflow run stored results in `track3p_results/` inside a Maestro workspace at `maestro/ace3p-multi-solver_20260728-133254/track3p-solve/` in the s3df-workflow repository checkout on S3DF |

## T3P

Source deck: `T3P-Tutorial.pptx` (CW23, March 2023). Stored results were produced with the March 2023 ACE3P build, so unlike Track3P there is no build-age gap between slides and results. The discrepancies are between the slides and the files, and between the slides' acdtool listings and the meshes actually stored.

### Element counts

The acdtool statistics shown on the slides were captured from meshes that differ from the `.ncdf` files now in the example directories. The documentation quotes the count from `t3p.log` of the stored run.

| Example | Slide acdtool listing | Stored mesh and `t3p.log` |
|---|---|---|
| cavity-quarter | 8,537 | 7,552 |
| cavity-half | 17,703 | 15,516 |
| BPM | 68,326 | 68,720 |
| taper | 9,795 | 8,536 |

The stored `acdtool.log` in each directory agrees with `t3p.log`, so the slides were made from an earlier mesh. Loss and kick factors in the docs are from the stored `wakefield.out` and therefore correspond to the stored meshes.

### Input files

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| cavity-quarter/open finite element order | Not shown; implied same as closed case (order 2) | Order 1 | `pillboxwg-open.t3p` on disk. Noted in Tutorial 1 since it affects comparability of the 0.386 V/pC loss factor. |
| cavity-half slide 24 `ModelInfo.File` | `./pillboxwg.ncdf` | `./pillboxwg2.ncdf` | File on disk. The slide copied the quarter-model file name. |
| cavity-half `CheckPoint` block | Not shown on slide | Shown, `Action: none`, `Ntimesteps: 500` | File on disk |
| BPM `LinearSolver` | Slide 41: `Solver: MUMPS // CG for large problems` | File has `Slover: CG`, a misspelled key | File on disk. The parser ignores the unknown key; `NML_ITLLinearSolver.C` then selects MUMPS when compiled in. The stored BPM run used MUMPS, not CG. Docs say so. |
| BPM batch script | Slide 42: `srun -n 128 -c 2` | Reproduced | Matches disk |
| SIBC `CheckPoint.Action` | Slide: not shown | `restart` | File on disk |
| SIBC `LinearSolver` | Slide 65: `Solver: CG` | Reproduced | Matches disk |
| `SymmetricFactor` vs `SymmetryFactor` | Both appear on slides without comment | Documented as two distinct keys: `SymmetryFactor` in `LoadingInfo` (beam), `SymmetricFactor` in `Loading.Port` (port excitation) | `BeamLoading.C` and `WaveguidePortBC.C` in source. `Application.C` also accepts `SymmetryFactor` placed in the wrong block "in case someone puts it into the wrong place". |
| Alternate key spellings | Slides use `Number of sigmas`, `Nsigmas`, `StartContour`, `Start contour`, `CurvedSurfaces`, `Curved Surfaces` interchangeably | Documented as accepted alternates | `fillAutomaticMovingWindow.C` checks both `Nsigmas` and `Number of sigmas`; the contour and curved-surface spellings both appear in source reads |

### Results and plots

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Multi-beam kick factor | Slide 32: "a factor of 2 higher" | 0.175 V/pC against 0.0964 V/pC single-beam, ratio 1.81 | `wakefield.out` in both directories. "Factor of 2" is the ideal; the stored numbers are quoted. |
| Half-model kick factor | Slide 35: "the same as ... two beam excitations" | 0.1747 V/pC against 0.1746 V/pC | Both `wakefield.out` files. Agreement to 0.05%. |
| Moving-window loss factor | Slide 60: "valid at distance governed by moving window size", no number | 0.0761 V/pC against 0.0762 V/pC full-order | Both `wakefield.out` headers |
| SIBC transmitted power | Slide 67 shows the plot only | 46% of input energy to output port, 50% to coating loss, by trapezoidal integration of the three `Power` monitor files | Computed from `inputPower.out`, `outputPower.out`, `wallossPower.out` |
| SIBC transit time | Not stated | 3.3 ns, consistent with c over 1 m | Peak times from the power files: input 0.88 ns, output 4.28 ns |
| Wakefield slide 7 | "Applied to structures one can see only vacuum from upstream and downstream beampipe ends" | Reproduced as the applicability condition of the indirect integration method | Slide only |
| Slide 20 directory name | "Directory: pillboxwg-half" | `cavity-half` | Directory on disk |
| Slide 12 and others | Mix of `edison $` and `perlmutter-p1` prompts; `qsub` in several READMEs | System-neutral `srun` and `sbatch` | Edison was decommissioned in 2019; `qsub` is the PBS command, not Slurm |
| `acdtool.log` overwrite warning | Slides 25 and 42 | Promoted to an admonition on the module page | Slide |

### Not verified

- Whether the BPM `ModeVoltage` monitor's `ESolver.Frequency: 1.e9` matters for a TEM mode with zero cutoff, or is a placeholder.
- The physical meaning of negative `inputPower` values: documented as the Poynting flux referenced to the outward normal, inferred from the sign pattern, not confirmed in `MON_SurfacePoynting`.
- Slide 5's dipole benchmark numbers (11.024 and 11.037 GHz); no example directory corresponds to it.

## TEM3P

Source deck: `TEM3P-Tutorial.pptx` (CW23). Stored results are from the March 2023 build, same as the slides.

### Input files

| Item | Slide or file said | Documentation now says | Source of correction |
|---|---|---|---|
| `AbsoluteTolerante` in `ElasticProblem.LinearSolver` | Both the slide and all three elastic inputs on disk spell it `AbsoluteTolerante` | Shown as `Tolerance` only, with a note | The misspelled key is silently ignored. Only `Tolerance` is read in the solver source; `AbsoluteTolerance` does not appear in `tem3p/src` or `solver/src` either, so neither spelling has any effect. |
| `NeumanValue` in `SRFCell.tem3p` | File on disk has `NeumanValue: 0.` for sidesets 3 and 4 | Shown as `NeumannValue` | Source reads `NeumannValue`. Since the value is zero and zero is the default traction, the typo has no effect on the stored result. |
| `RunId: 3` in `ThermoElasticProblem` | Present in slide and file | Documented as not read by the code | `grep RunId tem3p/src` finds nothing. The block's presence is what matters. |
| Body mesh journal CAD file | Slide 10: `import acis "RfGun-CouplerCell-2018.sat"` | `RfGun-CouplerCell.sat` | Both journals on disk import the same file, which is the only `.sat` in the directory |
| Vacuum mesh journal sizing line | Slide 8 breaks `min_size 0.5 max_size` across lines with the value missing | `min_size 0.5 max_size 3` | File on disk |
| S3P `SurfaceMaterial` for the coupler | Slide 31 omits it | `SurfaceMaterial: { ReferenceNumber: 1  Sigma: 5.7e7 }` included | File on disk; required for the `Impedance` boundary |
| `Method: Powerinput` spelling | Slide and file use `Powerinput`, docs elsewhere use `PowerInput` | Both listed as accepted | `EMHeating.C` and `LFDetuning.C` accept `Powerinput`, `PowerInput`, `powerinput`, `POWERINPUT` |
| Slide 12 Robin formula | `Q = hA(Th - Tc)` with keys `RobinConstantFactor` and `RobinConstantValue` described only as "h" and "h.T" | Documented as flux = h (T − T~fluid~) with `RobinConstantValue` = h·T~fluid~, so 440000/20000 = 22 °C water | `Tem3P_BdConstantRobin` constructor takes (factor, value); water temperature inferred from the ratio |
| Transient input file | Slide 25 titled "Input File for Thermal Transient Simulation" is empty; slide 26 shows the result | Transient shown as a figure only, with a note that no input file exists in the example | No file on disk contains `TimeStepping` or `MaximumTime` under `tem3p/` |

### Results

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| RF gun element counts | Not given | Vacuum 83,124; body 229,035 | `omega3p.out` and `tem3p.log` |
| RF gun frequency shift | Slide 20 names the two mode files, 2.8533884 and 2.8534358 GHz, without stating the shift | +47.4 kHz, computed from `omega3p.out` in both result directories | 2,853,435,826.2 − 2,853,388,398.9 Hz |
| RF gun power balance | Not discussed | 215.6 W in through RF wall, 213.1 W out through cooling; 1.2 percent imbalance noted as discretization leakage | `ResultFile` |
| SRF cell frequency shift | Slide 52 names mode files 1.3009577 and 1.3009506 GHz | −7.17 kHz and a coefficient of −5.85 Hz/(MV/m)² at 35 MV/m | `omega3p.out` in both directories. The mode file names on the slide are rounded; the docs use the full values from `omega3p.out`. |
| SRF cell Omega3P Q~0~ | Not shown | Reported as infinite, since the wall is `Electric` | `omega3p.out` prints `QualityFactor : inf` |
| Coupler shell sideset power | `ResultFile` shows `P (SideSet 6) = 0` and `P (SideSet 7) = 0` for the heated shell surfaces | Noted with an explanation that shell heat does not appear in the boundary flux tally | `ResultFile`; the mechanism is inferred, not traced in source |
| **Tesla eigenmode frequencies in `tem3p.log`** | Log prints `Frequency: 18833843948` for the 62.8 Hz mode | Flagged as wrong: the log applies the electromagnetic conversion. `ResultFile` and the file names are correct. | `ElasticProblem.C` line 1392 multiplies `FrequencyShift` by `Support::C` "to be consistent with the EM solvers", and the same scaling leaks into the printed frequency. $\sqrt{155810.34}/2\pi = 62.823$ Hz matches `ResultFile`. |
| Tesla element count | Not given | 286,556 elements, 1,543,974 DOFs | `tem3p.log` and `acdtool.log` agree |

### Not verified

- Which elastic displacement components a plain `Dirichlet` boundary fixes. The source reads a `DirichletType` key that no example uses; the docs assume all three components, which is what the examples' use of `Mixed` for partial constraints implies.
- The sign convention of the RF gun frequency shift (+47 kHz). The docs say it reflects the balance of thermal expansion, Lorentz pressure, and the constraints, but do not decompose it. Rerunning with `LFDetuning` removed would separate the two contributions.
- The statement that shell heat appears in the symmetry-plane power tally.

## Cubit chapter

Source deck: `Cubit-Demo.pptx` (CW23). Example: `examples/cubit/pillbox`.

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| Step 1 journal | Slide 29 shows a cleaned, parameterized journal with `reset` and `#{}` variables | Reproduced as on the slide, since it is the intended teaching form | The file on disk is the raw transcript: it begins with `cd "/Users/lge/cw23/examples/cubit/pillbox` (a user-specific path with an unclosed quote), has no `reset`, no variables, and `unite 1 2` rather than `unite volume 1 2`. The docs say the slide version is what you should write. |
| Mesh journal sizing | Slide 33 template has `volume 1 sizing function type skeleton` with no arguments and placeholder `X` surface IDs | `min_size 3 max_size 12` with real surface IDs 2, 4, 3, 1 | File on disk |
| Mesh journal `Cd` line | Slide 33: `Cd: "your working directory"` | Omitted | Not valid Cubit syntax and not in the file |
| Adaptive sizing example | Slide 38: `min_size 6 max_size 10 max_gradient 1 scale 5` | Shown as `min_size 3 max_size 12 max_gradient 1.2 scale 5` on the Cubit page | The slide values appear only as a commented-out line in the file on disk; the active line is `min_size 3 max_size 12`. The docs use the active values with a typical gradient. |
| Pillbox mode frequency | Slide 11: "TM010: f ~ 1.2GHz, λ ~ 250mm" | "near 1.2 GHz" | Slide only; this pillbox has no stored Omega3P run in `examples/cubit`. The rounded-top pillbox of the same radius in the Omega3P tutorials gives 1.3138 GHz, so 1.2 GHz is an approximation. |
| Element count | Slide 39 command line: "Generated 5549 tets for Volume 1" | 5,863 | `acdtool.log` on disk for the stored `pillbox.gen`. The slide screenshot is from a different sizing. |
| acdtool quality thresholds | Slide 48: "If aspect ratio > 20, shape measure <0.01, it might take longer" | Reproduced on the mesh page, attributed to the slides | Not found as thresholds in source. The `GREAT` and `GOOD` labels are printed by `mesh_stats.C`; the numeric cutoffs behind them were not traced. |
| acdtool mesh subcommands | Not listed on slides | Full list of 19 subcommands given on the mesh page | `tools/src/mesh.C` string comparisons and the `mesh_*.C` file names. Note `shuntimpedence` is spelled that way in the source. |
| ParaView version in screenshots | Slides show ParaView 5.11.0 and Cubit 16.04 | Versions not quoted | Cosmetic |
| Webcut plane naming | Slide 23 says "Choose YZ Plane" in the GUI and "`webcut vol 1 with xplane`" in the command | Both reproduced | Cubit names the plane by its normal in the command (`xplane` is normal to x) and by the two in-plane axes in the GUI (YZ). Same plane, two conventions. |

## Pic3P

Source: `cw18-Pic3P-Tutorial.ppt` (legacy binary format, text and images extracted directly from the OLE stream since no PDF exists), `pic3p-commands.pdf` from the CW23 command references, and the `LCLSGun` example. Stored results are from an October 2018 build.

| Item | Slide or file said | Documentation now says | Source of correction |
|---|---|---|---|
| Executable | README: "Run t3p"; slides: `t3p startupfile` | Stated explicitly that there is no `pic3p` binary and that `t3p` enters PIC mode on a `Loading` block containing `Particles` | `Application.C` line 709 |
| README input file name | "LCLSgun.t3p" in the run step | `LCLSGun.pic3p` | File on disk |
| Batch script | Personal copy: `run-pic3p.sl` with `srun -n 24` on Edison | Group copy's `run-pic3p.batch` with `srun -n 32 -c 8` on Perlmutter | Group copy is current |
| `Ekin` column of `particles.stat` | Not documented | MeV | `ParticlesIO.C` line 977: `(gamma-1)*e_mass_MeV()`. Cross-checked: γ = 1.00944 gives 4.8 keV, matching the stored value 0.00482. |
| Emittance units | Not documented | m·rad, RMS | Inferred from magnitude (2.5e-5 m·rad = 25 mm·mrad is plausible for 1 nC with 1000 macroparticles and no solenoid); the exact normalization was not traced in source |
| Final-row statistics | Slide shows the stat file without comment | Noted that the particle count falls from 996 to 413 after 300 ps as particles exit the absorbing pipe, so end-of-run moments describe a partial bunch | `particles.stat` rows 830 and 840 |
| `Longitudinal.Type: Flattop` | Command reference lists Flattop, Gaussian, Ellipsoid | Same, plus note that the code also accepts `Bunched` as a synonym and names the profile `LongitudinalFermiDirac` in output | `Particles.C` line 1569 and the output file names |
| `PICDomain` order | Example uses order 1 | Example reproduced; command reference's recommendation of order 2 or above for accuracy quoted | `pic3p-commands.pdf` |
| Mesh element counts | Journal comment: "h=2 => 128k ele" | Stored meshes: 64,116 drive-field, 121,202 PIC | `acdtool-*.log` on disk. The comment's numbers are for a different journal revision. |
| Omega3P mode frequencies | Not stated | 2.83750 GHz (0 mode) and 2.85281 GHz (π mode) | `omega3p.out` on disk |

## Gun3P

Source: `Gun3P-Tutorial.pdf` and `gun3p-commands.pdf` (both CW23, dated 9/29/2026 in the reference footer), and the `LSBK` example. These exist only in the group copy at `/sdf/group/rfar/ace3p/cw23/`; the personal copy used for the other modules has an empty `examples/gun3p/`.

| Item | Slide or file said | Documentation now says | Source of correction |
|---|---|---|---|
| Iteration count and convergence | Slide 15 shows iterations 3 and 4 only | Full history from the stored output: current 562.6 A at iteration 0 falling to 128.4 A by iteration 8 and steady thereafter; E relative change 2.4e-3 to 1.6e-5 over 31 iterations | `ace3p.o6436083` (70,979 lines). The run ended on `MaxIterations: 32`, not on tolerance. |
| Tolerance | Input: `ElectricRelativeTolerance: 1.00e-12` | Documented as unreachable; 1e-5 reached after 32 iterations | Stored output |
| Emitted current | Benchmark table: 129.3 A on a 1.3M-element mesh | 128.4 A on the 459k-element tutorial mesh, 0.7 percent lower | Stored output vs. SLAC-PUB-13097 table on slide 15 |
| `Max allowed total current` units | Not stated in the reference | μA | `EMT_ChildLangmuir.C` line 28 comment "in micro-amperes" |
| Where the iteration log goes | Slide 14: "Screen output – gun3p_results/gun3p.log" | `gun3p.log` holds only timing; the iteration history is on standard output | `gun3p.log` is 438 lines of timers; the Slurm output has the 96 perveance lines |
| Emitter `BoundaryID` | Slide 12: `BoundaryID: 8` | `BoundaryID: 1` | File on disk. Sideset 8 does not exist in the mesh (IDs are 1, 2, 3, 4, 10, 12). |
| Material list on slide 12 | Includes sideset 6 and 11 | Sidesets 1, 2, 3, 4, 10, 12 | File on disk; 6 and 11 do not exist in this mesh |
| `Particles per face` | Slide 12: 1 | 5 | File on disk |
| `Generate output for vizualization` | Slide 11: Off | on | File on disk. Note the misspelling `vizualization` is what the code reads. |
| `MaxIterations` | Slide 9: 60; slide 16: 60 | 32 | File on disk |
| Magnetostatic solver | Present in the input | Documented as configured but never activated, because `FirstIterationForMagnetostaticProblem` is commented out | File on disk; the H relative tolerance in the log is identically 0 every iteration |
| Material parameter name in `MagnetostaticProblem` | `Name: Permittivity` | Reproduced with a note that the code accepts it | File on disk; presumably `Permeability` was intended |
| Perlmutter host in README | `saul-p1.nersc.gov` | Not reproduced | Saul was NERSC's Perlmutter test system name during early access |

### Track3P additions from the CW23 deck

The CW23 Track3P deck (`Track3P-Tutorial.pdf`, 144 pages) extends the CW18 version (134 pages) used for the original Track3P pages. A page-title diff found the additions, which are now in the Track3P pages:

| Addition | Where in docs |
|---|---|
| `LoadParticles` emitter type 10 with `ParticlesFile` and scale/offset keys (also in the 2025 updates deck) | Track3P module page, Emitter table |
| `SymmetryPlane` material with `Domain.SymmetryFactor` and `Domain.SymmetryPlane` | Material and Domain tables |
| `ElectroStaticFieldMap` in `Domain`, loading a Gun3P Cartesian field | Domain table and Tutorial 6 |
| TW7Cell traveling-wave dark current example replacing the Tesla example | Tutorial 5 |
| Coax-StaticField example chaining S3P, Gun3P, Track3P | Tutorial 6 |

Not changed: the pillbox, window, muon, and Tesla tutorials remain as written from the CW18 deck, since their example directories are unchanged except that `Tesla` is absent from the group copy.

## Omega3P additions from the CW23 deck

The CW23 Omega3P deck is 76 pages against the CW18 version's 84; practices 3b and 4 were condensed into two slides, "Important TIPs" and "Non-linear Eigensolver Parameters". The TIPs slide adds guidance not in the CW18 deck: a multi-port problem is quadratic (and solvable without CORK) when every port has one mode and all ports share the same cutoff; otherwise use the 1D absorbing boundary as an approximation, PML as a better approximation, or CORK for accuracy. The CORK example gains an `OneRKSShift: 1` key not present in the CW18 deck or the example files. These points are now in the Omega3P module page (tip box in the input section) and in the Omega3P command syntax page, where `OneRKSShift` was confirmed to be read by `solver/src/CORK_RationalNewton.C`.

## Material not yet converted

Found during this pass, in `/sdf/group/rfar/ace3p/cw23/`:

- `commands/*.pdf`: per-module command references dated 9/29/2026, 13 to 32 pages each. **Converted on 2026-10-19** into the eight pages under Reference > Command syntax. Discrepancies found are in the section below.
- `news/ace3p-updates-032525.pdf`: 2025 release notes with a Perlmutter resource-allocation table for Omega3P and S3P and the `acdtool resource` tool.
- `presentations/ACE3P-Introduction.pptx` (126 MB) and `A3PI-Tutorial.pptx`.
- `mmode/`: mechanical-mode animation scripts for ParaView.
- `examples/a3pi/`: the ACE3P-IMPACT workflow with its own 22-page user guide.

## Command reference conversion

The nine command reference PDFs in `commands/` (Omega3P, S3P, T3P, Pic3P, Track3P, TEM3P, Gun3P, acdtool, and the A3PI user guide) were converted into the pages under Reference > Command syntax. Every keyword the references describe was searched for in the ACE3P source checkout at `/sdf/group/rfar/lge/sdf/ace3p/`. Findings:

| Item | Reference says | Source says | Documentation now says |
|---|---|---|---|
| Gun3P Cartesian field export | CW23 Gun3P slides: `FieldOutputToken` | `gun3p/src/outputConverter.C` reads `ElectrostaticFieldToken`; `FieldOutputToken` appears nowhere | `ElectrostaticFieldToken`, which the command reference also uses |
| Track3P secondary emission `Model: 3` (Furman-Pivi) | Described as available | `MAT_SecondaryEmitter.C` branches on `m_model != 3` at line 279, so model 3 is a code path, but the reference does not list the parameters it reads | Listed with that caveat. An earlier draft of this page said model 3 was absent from the source; that was wrong and is corrected here. |
| `PostProcess.WriteLoss` | Omega3P and S3P references describe it | Read only in the shared `emfem/src/NewPP.C`, not in the module trees, which is why the per-module keyword tables do not list it | Described on both pages with the source location |
| TEM3P `LinearSolver.AbsoluteTolerance` | Listed as a key | `LinearSolverMan.C` reads only `Tolerance`; the example inputs spell the key `AbsoluteTolerante`; neither spelling is read | Note on the TEM3P command page |
| TEM3P `SymmetryFactor` for RF heating | 1 full, 0 half for heating; 0 full, 1 half, 2 quarter for LF detuning | `EMHeating.C` defaults to 0 with a warning when absent; the two conventions were not reconciled | Both conventions quoted, with the advice to check `tem3p.out` |
| T3P bunch and pulse keys `BiGaussian`, `Rise sigma`, `Flattop width`, `UserDefinedPulse`, `Fall periods`, `TMax`, `Interpolative`, `ExFile` | Described | All found: bunches in `slacsupport/src/FlattopBunch.C` and `BunchMan.C`, pulses in `excitation/src/`, port import in `waveguide/src/` | Described as in the reference |
| Track3P `Domain.ModeID` | `ModeID` | Source also accepts `ModeID1` | Both noted |
| Omega3P `CORK.OneRKSShift` | Not in the command reference; only in the CW23 slide example | Read by `solver/src/CORK_RationalNewton.C` | Listed in the CORK table |
| acdtool `mesh` subcommands | Reference documents `stats`, `check`, `fix`, `deform`, `warpsurface` | Source has 14 more (`boundary`, `merge`, `partition`, ...) | Listed by name only, as undocumented |
| acdtool `resource` table | 2025 release notes give a six-row Perlmutter table for Omega3P | Not checked against the tool's code | Reproduced from the notes, labeled as such |

Not converted from this set: the A3PI user guide (22 pages), which belongs with the [Interfaces](interfaces/index.md) page and the `examples/a3pi/` workflow rather than the Reference section.

Formula and layout figures were taken from the PDFs rather than retyped: the PML conductivity profile, the PML face/edge/corner and waveguide layouts, and the direct wake-integration contour. The Lamé relation and the niobium conductivity figure from the TEM3P reference were replaced by inline formulas or omitted.

## Getting Started and Workflow pages

| Item | Slide said | Documentation now says | Source of correction |
|---|---|---|---|
| NERSC login host | CW23 `ComputerSetup.pptx`: `perlmutter-p1.nersc.gov` | `perlmutter.nersc.gov` | Current NERSC documentation; `-p1` is a specific login node |
| Cubit version | CW23: "Cubit v. 16.08" | "16.x", with 16.12 installed on S3DF | `/sdf/group/rfar/software/Cubit-16.12/` |
| ParaView version | CW23: 5.11.0 | 5.11 or later | 5.11.1 installed on S3DF |
| Batch script `srun` line | CW23 slide 19: `srun -n 16 -c 16 --cpu-bind=cores` on Perlmutter | Reproduced for Perlmutter; S3DF page uses `srun --overlap --cpu-bind=none -n 16` | S3DF pattern taken from the ACE3P regression scripts and the validated workflow runs |
| CW23 tutorial link | Slide 4 points to "Materials for CW18" on Confluence | Not reproduced | The CW23 page is the current one and this site supersedes both |

## Errors in earlier drafts of this documentation

These were introduced during conversion and fixed on 2026-10-19 after a verification pass against the example directories.

1. **Omega3P Tutorial 2, coax coupler.** The first draft contained a mode summary with Q~ext~ 4100 and Q~0~ 28,500 that was written as an illustration, not taken from a file. Replaced with the stored result, Q~ext~ 1,024,236. The difference is more than two orders of magnitude and would have misled anyone using the example to check their installation.
2. **Omega3P Tutorial 1, convergence study.** Stated the mesh journals went from fine to coarse as `mesh0` to `mesh3`; the opposite is true.
3. **Omega3P Tutorial 1, Q~0~.** Quoted as "about 28,900"; the stored value is 28,885.
4. **Omega3P post-processing page, R/Q convention.** The note stating acdtool uses the circuit convention V²/(ωU) per cavity was inferred from the output header comment `RoverQ=V^2/(omega*U)` and not independently confirmed in source. It remains in the docs but is flagged here as unverified against code.
5. **Module index.** S3P, Track3P, and T3P were listed as outline stubs after their guides were written. Fixed when each guide landed.
6. **T3P tutorials, element counts.** The first draft quoted the slide acdtool counts (8,537; 17,703; 68,326; 9,795). Replaced with the stored-mesh counts from `t3p.log` on 2026-10-19 before publication.
7. **T3P tutorials, BPM solver.** The first draft said the misspelled `Slover` key made T3P use "the default" without naming it. Traced in `NML_ITLLinearSolver.C`: the default is the best direct solver compiled in, MUMPS on these builds.
8. **T3P tutorials, SIBC power.** The first draft said "roughly 40%" transmitted from eyeballing the plot. Replaced with 46% from integrating the monitor files.
9. **TEM3P module page, LF pressure.** First draft gave the pressure formula without its sign convention. Checked `LFDetuning.C`: pressure is $\tfrac{1}{4}(\mu_0 H^2 - \varepsilon_0 E^2)$ and the load vector is scaled by −1 times the outward normal, so a positive (magnetic-dominated) pressure pushes the wall outward from the vacuum, which is inward on the metal. Wording adjusted.
10. **Getting Started, example paths.** The first draft pointed at the personal copy `/sdf/data/rfar/nfs/acd/u01/userspace/cho/cw23/`, which lacks Gun3P and the CW23 Track3P additions. Changed to the group copy `/sdf/group/rfar/ace3p/cw23/` on 2026-10-19 when the difference was discovered.
11. **This page, Track3P section.** The first draft flagged the slide's Omega3P mode 2 frequency of 1.75 GHz as suspicious. It is correct; the stored output confirms it, and the physics (a dipole mode visible only in the full model) explains it. The entry now says so.

## Still unverified

Items the documentation states that have not been checked against source code or a fresh run. Contributions welcome.

- acdtool R/Q convention (see above).
- Omega3P Practice 3b first-run table (in1.omega3p); no stored output exists.
- Default values quoted for `Port.NumberOfModes` (one mode when the block is absent), from the slide comment only.
- `FrequencyScan.Interval` default of one tenth of the range: from `SParameter.C` line 1674, but the warning path was not traced.
- The Track3P `Voltage` keyword format `a ra rb` with V = a / log(rb/ra): from the `InputParameters` comment only.
- Whether the Muon example results in the directory (`RF-*.png`, `RL-*.png`) were produced with the misspelled `Mat1erial` block and therefore without a declared primary surface, or with a corrected file.
