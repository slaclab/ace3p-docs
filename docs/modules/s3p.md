# S3P

S3P computes scattering parameters of RF structures in the frequency domain. Given one or more waveguide ports and a drive frequency, it solves the driven Maxwell problem and reports the S-matrix, port mode fields, and 3D field distributions. A frequency scan runs many solves and produces S-parameters versus frequency.

## Typical applications

- Coupler matching and bandwidth
- Transmission through multi-cell structures
- Waveguide components: bends, tapers, mode converters
- Loaded Q of a cavity from the width of a transmission peak

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.s3p` input file uses `SParameter` with the drive frequency or scan range, `Port` blocks defining each waveguide port and the number of modes to load, and `ModelInfo` with `Waveguide` boundary conditions on the port surfaces.

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full S3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/s3p` and `exercises/s3p`. Contributions welcome; see [Contributing](../contributing.md).
