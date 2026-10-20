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
| [Shared EM keywords](emfem.md) | The `emfem/` library used by all electromagnetic solvers: `ModelInfo`, boundary conditions, materials, coatings, `FiniteElement` |
| [Eigensolver keywords](solver.md) | The `solver/` library: Arnoldi, Lanczos, ESIL, CORK and SOAR nonlinear solvers, linear solver and preconditioner options |

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

ACE3P solvers read input through one uniform call:

```cpp
const int nev = Get(kvc, "NumEigenvalues", InitOrFallback<int>(1) or quiet);
```

The script `tools/extract_keywords.py` in this repository scans the source for such calls, extracts the keyword, type, default, and severity, and writes these Markdown pages. It runs in continuous integration whenever an ACE3P release is tagged. See [Contributing](../contributing.md).

!!! note "Coverage"
    Modules whose parsing uses a different pattern, notably T3P and Pic3P, are not yet covered by the extractor. Their keywords will be added as the script learns those patterns.
