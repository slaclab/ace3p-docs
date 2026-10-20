# Reference

Two kinds of reference material, serving different questions.

## Command syntax

One page per module describing every input block with a complete example and the meaning, units, and default of each key. These are converted from the ACE3P command reference documents distributed with the CW23 materials (dated September 2026) and cross-checked against the source where possible. Use them when you know which block you need and want to know what goes in it.

| Page | Blocks |
|---|---|
| [Omega3P](commands/omega3p.md) | `ModelInfo` with PML, `FiniteElement`, `PRegion`, `EigenSolver` incl. PETSc and CORK, `Port`, `PostProcess` |
| [S3P](commands/s3p.md) | `FrequencyScan`, `Port`, dipole `Loading`, `LinearSolver` with the multilevel preconditioner, `PostProcess` |
| [T3P](commands/t3p.md) | Time-domain materials incl. Lorentz dispersion, `PRegion` moving window, `LoadingInfo` bunch shapes and trains, `Loading` dipole/port/surface with pulse types, all `Monitor` types incl. direct wake integration, `CheckPoint` |
| [Pic3P](commands/pic3p.md) | PIC `PRegion`, `Loading` with `Particles`, distributions, emission models, `DriveField` |
| [Track3P](commands/track3p.md) | `FieldScales`, `Emitter` types incl. particle files, `Domain` incl. field maps and symmetry, `Material` incl. secondary emission models, `Postprocess` |
| [TEM3P](commands/tem3p.md) | Problem types, solvers incl. nonlinear, eigen, and harmonic, materials and function files, `Shell`, `HeatSource`, thermal and mechanical `Boundary` incl. all RF heating methods, `MeshDump`, `Transient` |
| [Gun3P](commands/gun3p.md) | `DCGunProblem`, static field problems, `Tracker` with Child-Langmuir emission, `gun3pOutputConverter` |
| [acdtool](commands/acdtool.md) | Mesh conversion and repair, `resource`, every `postprocess rf` function, wake and signal post-processing, PIC and Track3P utilities, `project` |

## Keyword tables

These pages list the input-file keywords that each ACE3P module reads. They are **generated from the source code**, not written by hand. Keyword names, types, and default values therefore always match the release the documentation is built for. Use them to check spelling and defaults, and to find keywords the command syntax pages do not mention.

| Page | Covers |
|---|---|
| [Omega3P keywords](omega3p.md) | Everything read in the `omega3p/` source tree: eigensolver selection, frequency targets, adaptive mesh refinement, matrix output |
| [S3P keywords](s3p.md) | `FrequencyScan`, ports, dipole loading, S-parameter output |
| [T3P and Pic3P keywords](tfe3p.md) | The `tfe3p/` tree: beam and port loading, monitors, moving window, particles, drive fields |
| [Track3P keywords](multipacting.md) | The `multipacting/` tree: `Domain`, `Emitter`, `Material`, field maps, post-processing |
| [TEM3P keywords](tem3p.md) | Thermal and mechanical problems, boundaries, solvers, `Transient`, `HarmonicAnalysis` |
| [Gun3P keywords](gun3p.md) | `DCGunProblem`, static field problems, `Tracker`, Child-Langmuir emitter |
| [acdtool keywords](tools.md) | Mesh utilities and the Track3P post-processor input |
| [acdtool rf post-processor keywords](omega3p-postprocess.md) | Every function and parameter name the `.rfpost` parser recognizes |
| [Shared EM keywords](emfem.md) | The `emfem/` library used by all electromagnetic solvers: `ModelInfo`, boundary conditions, materials, coatings, `FiniteElement` |
| [Eigensolver keywords](solver.md) | The `solver/` library: Arnoldi, Lanczos, ESIL, CORK and SOAR nonlinear solvers, linear solver and preconditioner options |
| [Excitation pulse keywords](excitation.md) | `Pulse` types shared by T3P loading and TEM3P transients |
| [Waveguide port keywords](waveguide.md) | Port mode solvers, including imported (`Interpolative`) modes |
| [Bunch shape keywords](slacsupport.md) | Gaussian, BiGaussian, Flattop, and profiled bunches, plus the input-file reader itself |

## How to read the tables

| Column | Meaning |
|---|---|
| **Keyword** | The name as it appears in the input file. Grouped under the block that contains it when the code reads a dotted path such as `EigenSolver.SolverMode`. |
| **Type** | `int`, `double`, `string`, or blank when the code reads the value into a pre-typed variable |
| **Default** | The value used when the keyword is absent. Blank means the code checks for presence with `find()` and handles absence in its own logic, or the entry is a block name rather than a scalar. |
| **Presence** | `optional` when a default exists; `required` when the solver aborts without it |
| **Read in** | Source file and line number, for developers tracing behavior |

The tables are deliberately terse. Explanations of what each keyword does belong in the [module guides](../modules/index.md), which link back here.

## How the pages are generated

ACE3P solvers read input through a small family of calls on a key-value container:

```cpp
const int nev = Get(kvc, "NumEigenvalues", InitOrFallback<int>(1) or quiet);   // typed, with default
if (!domainkvc.find("MaxImpacts", m_maxImpacts)) { m_maxImpacts = 50; }       // default assigned after
if (!kvc.find("JobName", name)) { kvcError(); }                                // required
kvc.find("StartPoint", 0, x);                                                  // indexed list value
kvc.findSwitch("Toggle");                                                      // on/off switch
kvc.findContainer("Domain", domainkvc);                                        // a block
```

The script `tools/extract_keywords.py` in this repository scans the source for all six forms, extracts the keyword, type, default, and presence, and writes these Markdown pages. Block membership comes from dotted keys or from the `findContainer` binding of the variable the key is read from. The `acdtool postprocess rf` input uses a separate string-compare parser, which the script also reads.

A workflow in the ACE3P source repository runs the script whenever a release tag `v*` is pushed and opens a pull request here with the regenerated pages. See [Contributing](../contributing.md).

!!! note "Coverage"
    Keys the code reads from a container whose block cannot be inferred are listed under *top level or unspecified block* at the end of each page. The source location column tells you where to look.
