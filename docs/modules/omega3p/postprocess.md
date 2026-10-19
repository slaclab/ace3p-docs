# Post-processing with acdtool

ParaView shows field patterns. For numbers such as shunt impedance, kick factor, and peak surface fields, use the RF post-processor built into acdtool:

```bash
acdtool postprocess rf <project>.rfpost
```

It runs serially and reads the mode files that Omega3P or S3P wrote. Running it with no file argument writes a `sample.rfpost` template containing every available function with default values, which is the easiest way to start.

## The .rfpost file

The file is a sequence of named blocks. The first must be `RFField`, which selects the mode and sets scaling. Every other block is a calculation that is enabled with `ionoff = 1`.

```text title="pillbox-rtop.rfpost"
RFField
{
   ResultDir   = omega3p_results   // where the .mod files are
   FreqScanID  = 0                 // S3P only: frequency scan index
   ModeID      = 0                 // which mode, when a block uses modeID = -1
   xsymmetry   = magnetic          // [none, electric, magnetic]
   ysymmetry   = magnetic
   gradient    = 2.0e7             // V/m; -1 keeps normalized fields
   cavityBeta  = 1.0               // particle beta for V and R/Q integrals
   reversePowerFlow = 0            // [1 = charging, 0 = decaying]
   x0 = 0.0                        // integration axis x
   y0 = 0.0                        // integration axis y
   gz1 = -0.057                    // integration start z, m
   gz2 =  0.057                    // integration end z, m
   npoint = 300                    // points along the axis
   fmnx = 10                       // field map resolution
   fmny = 10
   fmnz = 50
}

RoverQ
{
   ionoff = 1
   modeID1 = -1                    // -1, -1: all modes
   modeID2 = -1
   x1 = 0.0
   x2 = 0.0
   y1 = 0.001
   y2 = 0.001
   z1 = 1e8                        // 1e8: use the model bounding box
   z2 = 1e8
}

maxFieldsOnSurface
{
   ionoff = 1
   surfaceID = 6
}
```

### RFField keys

| Key | Meaning |
|---|---|
| `ResultDir` | Results directory from the solver |
| `ModeID` | Mode used by single-mode functions |
| `xsymmetry`, `ysymmetry` | Tell the post-processor which symmetry planes were used so volume integrals are scaled to the full cavity |
| `gradient` | Accelerating gradient in V/m used to scale fields. With `-1`, fields keep the solver's normalization of 1 J stored energy. |
| `cavityBeta` | Particle velocity for the transit-time factor in V and R/Q |
| `gz1`, `gz2` | Axial integration range for the voltage. Set to the cavity length, not the whole beam pipe, to define the gradient consistently. |

### Functions

| Block | Computes |
|---|---|
| `RoverQ` | Voltage along a line and R/Q = V²/(ωU) per mode |
| `RoverQT` | Transverse R/Q |
| `kickFactor` | Transverse kick factor |
| `FieldMap` | Field on a 3D grid of nx × ny × nz points in the given box |
| `FieldAtPoint`, `ALLFieldAtPoint` | Field at one point, for one or all modes |
| `FieldOnLine`, `ALLFieldOnLine` | Field along a line with `npoint` samples at a given `rfphase`, written to `filename` |
| `fieldOn2DBoundary` | Field on a boundary surface, written to file |
| `fieldOnSurface` | Field on a surface as components or amplitude |
| `maxFieldsOnSurface` | Peak E and H on a surface with their locations |
| Multipole analysis | Multipole decomposition of the field on axis |

Coordinates are in meters. A coordinate of `1e8` means "use the bounding box of the model," which is convenient for line integrals along the full axis.

## Output

acdtool writes to standard output and to `rfpost.out`. It begins with a mode summary:

```text
** Omega3P/S3P Mode Summary:
**   Total number of modes :      2
**      ModeID         Frequency(r,i)                       Qext
**         0           1.31381e+09, 0.00000e+00           0.00000e+00
**         1           2.32914e+09, 0.00000e+00           0.00000e+00
**   Model bounding box: ( 0.00000e+00,  0.00000e+00 -1.50000e-01)
**                       ( 1.00005e-01,  1.00123e-01  1.50000e-01)
```

followed by a `[scaling]` block giving the voltage and the factor used to scale the normalized fields to the requested gradient, then one block per enabled function:

```text
[RoverQ]
{  // RoverQ=V^2/(omega*U)
 ModeID  Frequency           (V_r, V_i)                      |V|            RoQ(ohm/cavity)
    0   1.31381e+09  ( 2.2980e+00,  3.4925e+00)    4.18073e+00      1.19567e+02
    1   2.32914e+09  (-7.2671e-04,  6.2729e-04)    9.59998e-04      3.55621e-06
}

[maxFieldsOnSurface]
{
   surfaceID :   6
      ModeID :   0
        Emax :  4.22488e+07 (V/m)   at ( 3.9627e-02,  1.8486e-02, -4.5454e-02)
        Hmax :  5.80786e+04 (A/m)   at ( 3.3116e-02,  7.9193e-02,  3.2771e-02)
}
```

Surface field values correspond to the `gradient` in `RFField`. The ratio E~peak~/E~acc~ is a standard figure of merit and comes straight from `Emax` divided by `gradient`.

!!! note "R/Q convention"
    acdtool reports R/Q in the circuit convention V²/(ωU) in ohms per cavity, where V is the full on-axis voltage after the transit-time factor. For a symmetric model the `xsymmetry` and `ysymmetry` settings restore the full-cavity stored energy. Divide by 2 for the linac convention if your comparison uses it.

## S3P results

The same tool works on S3P output. Set `FreqScanID` to pick a frequency point from the scan and `ModeID` to pick the excited port mode.
