# TEM3P

TEM3P adds thermal and mechanical analysis to the electromagnetic solvers. It takes RF wall loss from Omega3P or S3P as a heat source, solves for temperature, then for the resulting mechanical deformation, and finally reports the frequency shift of the cavity from that deformation.

## Typical applications

- RF heating and cooling-channel design
- Lorentz-force detuning
- Thermal stress in windows and couplers
- Frequency sensitivity to mechanical deformation

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.tem3p` input file uses `EMHeating` pointing at an Omega3P or S3P results directory, thermal material properties and boundary conditions, elastic material properties and constraints, and `LFDetuning` for the frequency-shift calculation.

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full TEM3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/tem3p` and `exercises/tem3p`. Contributions welcome; see [Contributing](../contributing.md).
