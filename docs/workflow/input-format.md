# Input file format

All ACE3P solvers read a plain-text input file with nested blocks of `Key: value` pairs. The file is named `<project>.<module>`.

## Syntax

```text title="pillbox.omega3p"
ModelInfo : {
  File: ./pillbox4.ncdf

  BoundaryCondition : {
    Magnetic: 1, 2
    Exterior: 6
  }

  SurfaceMaterial : {
    ReferenceNumber: 6
    Sigma: 5.8e7
  }
}

FiniteElement: {
  Order:           2
  CurvedSurfaces: on
}

EigenSolver : {
  NumEigenvalues: 2
  FrequencyShift:  1.0e9
}

PostProcess : {
  Toggle: on
  ModeFile: mode
}
```

Rules:

- A block is `Name : { ... }`. Blocks nest. The space before the colon is optional.
- A scalar entry is `Key: value`. Lists are comma separated: `Magnetic: 1, 2`.
- Comments use `//` to end of line or `/* ... */` for a range. Commenting out a whole block is the usual way to disable it.
- Keywords are case sensitive. `Order` and `order` are different.
- A block may be repeated when the solver expects a list of them, for example several `Material` or `Port` blocks.
- Numbers accept scientific notation: `5.8e7`, `1.0e9`.
- Switches accept `on` and `off`.

!!! tip "Keyword reference"
    The [reference section](../reference/index.md) lists every keyword each solver reads, with its type and default value, generated from the source code. Use it to check spelling and defaults.

## Blocks common to all modules

### ModelInfo

Describes the mesh and the physical boundary conditions.

| Key | Meaning |
|---|---|
| `File` | Path to the `.ncdf` mesh |
| `BoundaryCondition` | Maps boundary types to sideset IDs. See below. |
| `Material` | Volume material by block `Attribute`. Default is vacuum. Repeat for several materials. |
| `SurfaceMaterial` | Surface conductivity `Sigma` on a boundary `ReferenceNumber`, used for wall loss and Q~0~ |

Boundary condition types:

| Type | Physics | Typical use |
|---|---|---|
| `Electric` | Tangential E = 0, perfect electric conductor | Metal walls when wall loss is not needed, electric symmetry plane |
| `Magnetic` | Tangential H = 0 | Magnetic symmetry plane |
| `Exterior` | Metal wall with finite conductivity from `SurfaceMaterial` | Cavity wall when Q~0~ is wanted |
| `Waveguide` | Port surface; modal expansion with `Port` blocks | Couplers, beam pipe ends |
| `Absorbing` | Simple first-order absorbing boundary | Beam pipe ends when modal accuracy is not needed |
| `Periodic_M`, `Periodic_S` | Master and slave periodic surfaces with phase advance `Theta` in degrees | Traveling-wave structures |
| `Impedance` | Surface impedance boundary | Thin coatings, lossy surfaces |

### Material

```text
Material : {
  Attribute: 2          // Cubit block ID
  Epsilon: 10.0         // relative permittivity
  EpsilonImag: -1.52    // negative imaginary part for loss
  Mu: 1.0               // relative permeability
}
```

### FiniteElement

| Key | Meaning |
|---|---|
| `Order` | Polynomial order of the vector basis functions, 1 to 6. Order 2 is the usual choice. Higher order gives more accuracy per element at higher cost. |
| `CurvedSurfaces` | `on` to use the quadratic mid-edge nodes of `tetra10` elements for curved geometry. Keep this on. |

### PostProcess

| Key | Meaning |
|---|---|
| `Toggle` | `on` writes field files for ParaView |
| `ModeFile` | Prefix for the `.mod` files in the results directory |

## Module-specific blocks

Each solver adds its own blocks: `EigenSolver` and `Port` for Omega3P, `SParameter` and frequency scan settings for S3P, time-stepping and excitation for T3P, emission and tracking parameters for Track3P. These are documented in the [module guides](../modules/index.md).

## Echo of parsed input

Every solver prints the parsed input, with defaults filled in, near the top of its `.out` file under the heading `input parameters, KVC syntax`. Compare that echo against your file when a keyword seems to be ignored. A misspelled keyword is silently dropped, so the echo is the quickest way to catch typos.
