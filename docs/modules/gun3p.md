# Gun3P

Gun3P solves electrostatic and magnetostatic fields together with space-charge-limited electron emission and beam optics. It is used to design DC and RF electron guns and to compute emitted current and beam envelope.

## Typical applications

- Thermionic and photoemission guns
- Space-charge-limited current
- Beam optics through focusing electrodes and solenoids
- Starting distributions for downstream tracking

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.gun3p` input file uses `ElectrostaticProblem` or `DCGunProblem`, emission model and cathode surface, electrode potentials by boundary ID, and monitors on planes, circles, or segments that record beam properties.

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full Gun3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/gun3p` and `exercises/gun3p`. Contributions welcome; see [Contributing](../contributing.md).
