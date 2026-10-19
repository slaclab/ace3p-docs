# T3P

T3P solves Maxwell's equations in the time domain with an implicit, unconditionally stable scheme on the same high-order finite-element mesh. It is used for wakefield calculation, transient response of couplers, and beam-driven fields. A moving-window option follows a short bunch through a long structure.

## Typical applications

- Short-range and long-range wakefields
- Transient fill and decay of cavities and couplers
- Beam-loading studies with prescribed bunch trains
- Time-domain S-parameters by Fourier transform of port signals

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.t3p` input file uses time-stepping block with `DT` and total time, an excitation block describing the beam or port drive, `Port` blocks for absorbing boundaries, and monitors that record fields or port signals versus time.

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full T3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/t3p` and `exercises/t3p`. Contributions welcome; see [Contributing](../contributing.md).
