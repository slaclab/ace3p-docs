# Batch jobs

ACE3P solvers are MPI programs and run under Slurm. The structure of a batch script is the same on every system; only the partition, account, and binary path change.

## Anatomy of a script

```bash
#!/bin/bash -l
#SBATCH <resource and queue options>
#SBATCH -J <job name>
#SBATCH -o <stdout file>
#SBATCH -e <stderr file>

<load ACE3P environment>
srun -n <ranks> <solver> <project>.<module>
```

System-specific headers are in [Running on S3DF](../getting-started/s3df.md) and [Running on Perlmutter](../getting-started/perlmutter.md).

## Choosing resources

**Omega3P and S3P** are memory-bound sparse eigenvalue and linear solves. Start with 16 MPI ranks on one node for meshes up to a few hundred thousand elements. Add nodes when the solver reports high memory use per node in its `.out` file:

```text
used mem per node in GB : min:   4.97 GB, max:   4.97 GB, avg:   4.97 GB
used mem per node in %  : min:   40.7  %, max:   40.7  %, avg:   40.7  %
```

Keep the percentage under about 70 to leave room for the direct solver's fill-in.

**Track3P** parallelizes over particles and runs well in hybrid mode: one MPI rank per socket, OpenMP threads across the cores. See the [Track3P guide](../modules/track3p.md).

**T3P** scales to many nodes for large time-domain problems. Rank count should be proportional to element count; a rule of thumb is 5,000 to 20,000 elements per rank.

**acdtool** is serial. Run it with `-n 1`.

## Walltime

| Problem | Typical time |
|---|---|
| Omega3P, 2 modes, 15k elements, order 2 | 1 to 2 minutes |
| Omega3P, 10 modes, 500k elements, order 2 | 30 to 60 minutes |
| S3P, 20 frequency points, 100k elements | 10 to 30 minutes |
| Track3P multipacting scan, 30 field levels | 10 minutes to several hours depending on particle count |

Use a short debug queue for the first run of a new model and check the `.out` file before committing to a long queue.

## Output files

Each solver writes into a results directory next to the input file, `omega3p_results/` for Omega3P and similar for the others. Common files:

| File | Content |
|---|---|
| `<module>.out` | Full log including parsed input, mesh statistics, convergence history, and the mode summary |
| `<module>.log` | Shorter progress log |
| `<module>.warn` | Warnings only. Check this first when results look wrong. |
| `*.mod` | Field files for ParaView, one per mode or time step |
| `VECTOR/` | Raw eigenvectors for restart or post-processing |

The Slurm `.out` and `.err` files capture the same console output plus any MPI runtime messages.

## Chaining steps

A full campaign chains mesh conversion, several solves, and post-processing, often across many parameter values. Writing that as a sequence of hand-submitted scripts is error prone. The [AI workflow assistant](../interfaces/workflow-assistant.md) page describes the Maestro-based workflow tooling developed for ACE3P on S3DF, which expresses the whole chain as one YAML specification with dependencies and parameter sweeps.
