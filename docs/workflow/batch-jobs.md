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

**Track3P** parallelizes over particles and is OpenMP-parallel within each rank. Because every rank holds the whole mesh and field, run it in hybrid mode: one or two MPI ranks per node and OpenMP threads across the rest of the cores. Scripts are in [Hybrid MPI and OpenMP](#hybrid-mpi-and-openmp-track3p) below.

**T3P** scales to many nodes for large time-domain problems. Rank count should be proportional to element count; a rule of thumb is 5,000 to 20,000 elements per rank.

**acdtool** is serial. Run it with `-n 1`.

## Hybrid MPI and OpenMP (Track3P)

Track3P is the only ACE3P solver that uses OpenMP threads. The layout below puts two ranks on each node and lets threads fill the cores: 2 x 60 threads on an S3DF `milano` node (128 cores, 8 left for the system), 2 x 64 on a Perlmutter CPU node (128 cores). `OMP_PROC_BIND=spread` and `OMP_PLACES=cores` pin the threads so they do not migrate between sockets. The second argument to `track3p` is the results directory.

=== "S3DF"

    ```bash title="run-track3p-hybrid.sh"
    #!/bin/bash -l
    #SBATCH -p milano
    #SBATCH -A rfar:regular
    #SBATCH -q normal
    #SBATCH -N 1
    #SBATCH --exclusive
    #SBATCH -t 02:00:00
    #SBATCH -J track3p-omp
    #SBATCH -o track3p_omp_%j.log
    #SBATCH -e track3p_omp_%j.log

    source /sdf/group/rfar/ace3p/ace3p.sh

    RANKS_PER_NODE=2
    NTHREADS=60
    TOTAL_RANKS=$((SLURM_JOB_NUM_NODES * RANKS_PER_NODE))

    export OMP_NUM_THREADS=${NTHREADS}
    export OMP_PROC_BIND=spread
    export OMP_PLACES=cores

    srun --overlap --cpu-bind=none -n ${TOTAL_RANKS} --ntasks-per-node=${RANKS_PER_NODE} -c ${NTHREADS} \
         track3p Pillbox.track3p track3p_results
    ```

=== "Perlmutter"

    ```bash title="run-track3p-hybrid.batch"
    #!/bin/bash -l
    #SBATCH -C cpu
    #SBATCH -q regular
    #SBATCH -A m349
    #SBATCH -N 1
    #SBATCH --exclusive
    #SBATCH -t 02:00:00
    #SBATCH -J track3p-omp
    #SBATCH -o track3p_omp_%j.log
    #SBATCH -e track3p_omp_%j.log

    RANKS_PER_NODE=2
    NTHREADS=64
    TOTAL_RANKS=$((SLURM_JOB_NUM_NODES * RANKS_PER_NODE))

    export OMP_NUM_THREADS=${NTHREADS}
    export OMP_PROC_BIND=spread
    export OMP_PLACES=cores

    srun -n ${TOTAL_RANKS} --ntasks-per-node=${RANKS_PER_NODE} -c ${NTHREADS} --cpu-bind=cores \
         $CFS/ace3p/perlmutter/CPU/track3p Pillbox.track3p track3p_results
    ```

Raise `-N` for more nodes; the rank count scales with it. Add ranks rather than threads only when one rank's share of the particles takes too long, keeping the per-node memory of the replicated mesh in mind. For a quick test, one rank with 16 threads is enough:

```bash
export OMP_NUM_THREADS=16
srun -n 1 -c 16 track3p Pillbox.track3p
```

The end of `track3p.log` prints a function-by-function timing report (emission, push, material interaction) that shows whether more threads would help.

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

A full campaign chains mesh conversion, several solves, and post-processing, often across many parameter values. Writing that as a sequence of hand-submitted scripts is error prone. The [ACE3P GUI](../interfaces/gui.md) has a workflow-orchestration mode for parameter sweeps and optimization chains, and [lume-ace3p](https://github.com/slaclab/lume-ace3p) does the same from Python.
