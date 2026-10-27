# Mesh preparation

ACE3P reads meshes in its own NetCDF format (`.ncdf`). You produce them by exporting a Genesis file (`.gen`) from Cubit and converting it with `acdtool`. Building and meshing the model in Cubit is covered on the [Cubit page](../cubit/index.md); this page covers what the exported mesh must contain and how to check it.

## Cubit export checklist

A typical meshing journal ends like this:

```text title="step2-Mesh-pillbox.jou"
reset
import acis "pillbox4.sat"

volume all scheme Tetmesh
volume all sizing function type skeleton scale 5 time_accuracy_level 2 min_size auto max_size 12 max_gradient 1.2
mesh volume all

Sideset 1 surface 7                      # symmetry plane
Sideset 2 surface 1                      # symmetry plane
Sideset 6 surface all except 7 1         # exterior wall

block 1 volume all
block 1 element type tetra10             # quadratic tets, required

volume all scale 0.001                   # mm to m
export Genesis "pillbox4.gen" block all overwrite
```

Check each item before export:

- [x] **Tetrahedral mesh** with the `Tetmesh` scheme. Hex meshes are not supported.
- [x] **Element type `tetra10`** on every block. Linear `tetra4` elements lose the curved-surface information.
- [x] **Every boundary surface in a sideset.** Surfaces that belong to no sideset get boundary ID 0 and are treated as interior, which is almost never what you want. The idiom `Sideset 6 surface all except ...` catches everything you did not name explicitly.
- [x] **Every volume in a block.** Blocks become material attributes.
- [x] **Scaled to meters.**
- [x] **Multiple volumes imprinted and merged** so shared faces are a single surface. Otherwise the volumes are disconnected in the mesh. See the [lossy load tutorial](../modules/omega3p/tutorial-advanced.md).

### Sizing function

The skeleton sizing function adapts element size to local geometry. The parameters that matter most:

| Parameter | Effect |
|---|---|
| `scale` | Overall density. Smaller is finer. |
| `max_size` | Largest edge length allowed, in model units |
| `max_gradient` | How fast element size may change between neighbors. 1.2 to 1.5 is typical. |

Refine around small features such as coupler irises and rounded edges, and do a convergence study before trusting results. See the [pillbox tutorial](../modules/omega3p/tutorial-pillbox.md#convergence-study).

## Convert with acdtool

Copy the `.gen` file to the HPC system and run:

```bash
acdtool meshconvert pillbox4.gen
```

This writes `pillbox4.ncdf` and prints statistics. It is a serial program and finishes in seconds for meshes with fewer than a million elements, so it can run on a login node or in a one-task batch job.

### Read the statistics

```text
Input: pillbox4.gen (contains quadratic 10-point elements)
Output: pillbox4.ncdf
TOTALS:
  elements: 13382
  coordinates: 2955
EULER CHARACTER:
  Surf Euler Char = 2
  Vol Euler Char = 1
  Euler Char is OK.
ASPECT RATIO:
  min      = 1.03213
  max      = 2.53273 <- GREAT
SHAPE MEASURE:
  min      = 0.26181 <- GREAT
Existing boundary IDs:
1 2 6
Material IDs 	 Number of Elems:
1:	 	 13382
Total Number of invalid second order tetrahedral elements (ISOTE) is: 0
```

What to look for:

- **Euler characteristic OK.** A closed, simply connected volume has surface Euler characteristic 2. Anything else means a hole or a disconnected piece.
- **Existing boundary IDs** must match the sidesets you expect. A missing ID means a sideset was never created; an unexpected `0` means a surface was left out.
- **Material IDs** must match your blocks.
- **Invalid second-order elements** must be zero. A nonzero count means some mid-edge nodes fold the element inside out, usually from an aggressive sizing function on a curved surface. Refine the mesh or relax `max_gradient`.
- **Aspect ratio and shape measure** are quality indicators. acdtool prints `GREAT`, `GOOD`, or a warning next to them. The CW23 slides give rough limits: aspect ratio above 20 or shape measure below 0.01 will slow the solvers noticeably.

### Other acdtool mesh commands

```bash
acdtool mesh stats pillbox4.ncdf     # statistics only
acdtool mesh check pillbox4.ncdf     # validity check only
acdtool mesh fix in.ncdf out.ncdf    # replace invalid curved tets with straight ones
acdtool mesh deform in.ncdf out.ncdf 5000   # exaggerate a deformed mesh for viewing
```

The full list of `acdtool mesh` subcommands in the current source is: `boundary`, `check`, `deform`, `fix`, `merge`, `partition`, `pick`, `rotate`, `scale`, `shuntimpedence`, `smooth`, `stats`, `straighten`, `summodes`, `surfsmooth`, `transform`, `untangle`, `warp`, `warpsurface`. Most are undocumented beyond their source files; `meshconvert` already calls `check` and `fix` for you. The full acdtool command set, including every `postprocess` function and the `resource` tool, is in the [acdtool command syntax](../reference/commands/acdtool.md).
