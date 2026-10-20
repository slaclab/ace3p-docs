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
| Omega3P mode 2 frequency | Slide 20: `1.7499342e+09` | Not quoted | Stored `omega3p_results` for this full pillbox gives 1.3138 GHz for mode 1; mode 2 frequency was not independently checked and the slide value is suspicious given the quarter-model result of 2.329 GHz |
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
5. **Module index.** S3P and Track3P were listed as outline stubs after their guides were written. Fixed when each guide landed.

## Still unverified

Items the documentation states that have not been checked against source code or a fresh run. Contributions welcome.

- acdtool R/Q convention (see above).
- Omega3P Practice 3b first-run table (in1.omega3p); no stored output exists.
- Default values quoted for `Port.NumberOfModes` (one mode when the block is absent), from the slide comment only.
- `FrequencyScan.Interval` default of one tenth of the range: from `SParameter.C` line 1674, but the warning path was not traced.
- The Track3P `Voltage` keyword format `a ra rb` with V = a / log(rb/ra): from the `InputParameters` comment only.
- Whether the Muon example results in the directory (`RF-*.png`, `RL-*.png`) were produced with the misspelled `Mat1erial` block and therefore without a declared primary surface, or with a corrected file.
