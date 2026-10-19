# Track3P

Track3P tracks charged particles in the electromagnetic fields computed by Omega3P, S3P, or T3P, including secondary electron emission at surfaces. Its primary use is multipacting analysis: finding the field levels at which resonant electron trajectories grow. It also handles dark current from field emission.

## Typical applications

- Multipacting barriers in cavities, couplers, and windows
- Enhancement counter and impact energy versus field level
- Dark current trajectories and impact locations
- Field-emission current from high-gradient surfaces

## Input blocks

In addition to the [common blocks](../workflow/input-format.md), the `.track3p` input file uses emission settings for primary and secondary particles, the surface secondary-emission yield model, the list of field files and the scan of field levels, tracking duration and time step, and monitors that record resonant particles and the enhancement counter.

### Hybrid execution

Track3P runs well with one MPI rank per socket and OpenMP across the cores:

```bash
export OMP_NUM_THREADS=16
srun -n 1 -c 16 track3p pillbox.track3p
```

### Post-processing

`acdtool postprocess track3p` summarizes resonant particles and the enhancement counter. The ParaView macros `enhancement.py`, `resonant.py`, and `trajectory.py` plot them. See [local tools](../getting-started/local-tools.md).

## Documentation status

!!! warning "Under construction"
    This page is an outline. The full Track3P tutorial from the CW23 workshop has not yet been converted. The source slides and example files are in the CW23 materials under `examples/track3p` and `exercises/track3p`. Contributions welcome; see [Contributing](../contributing.md).
