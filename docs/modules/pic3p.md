# Pic3P

Pic3P is a particle-in-cell code that solves Maxwell's equations and particle motion self-consistently, including the space-charge fields of the beam. It is used for devices where the beam strongly modifies the fields: klystrons, guns with high bunch charge, and beam-loading transients.

## Typical applications

- Klystron and RF source simulation
- Space-charge-dominated electron bunches
- Beam loading with self-consistent fields
- Noise and instability studies in PIC

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.pic3p` input file uses particle injection and emission, field solver settings, time stepping, and diagnostics. Pic3P shares infrastructure with T3P.

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full Pic3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/pic3p` and `exercises/pic3p`. Contributions welcome; see [Contributing](../contributing.md).
