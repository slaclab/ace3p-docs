# Running on S3DF

!!! note "SLAC users only"
    S3DF, SLAC's Shared Scientific Data Facility, is reachable only with a SLAC computing account. Users elsewhere should use [NERSC Perlmutter](perlmutter.md), which is the main ACE3P platform. The rest of this manual applies to both systems.

ACE3P is installed under the `rfar` group area and runs on the `milano` partition. Cubit and ParaView are installed as well; see [Pre- and post-processing tools](tools.md).

## Log in

```bash
ssh <username>@s3dflogin.slac.stanford.edu
```

Login nodes are for editing and job submission only. Do not run solvers on them.

## Load the ACE3P environment

Source the environment script once per session. It loads the matching OpenMPI module and puts the ACE3P binaries on your `PATH`.

```bash
source /sdf/group/rfar/ace3p/ace3p.sh
which omega3p acdtool
```

!!! tip
    Add the `source` line to your `~/.bashrc` if you use ACE3P regularly.

## Partitions and accounts

| Setting | Value | Notes |
|---|---|---|
| Partition | `milano` | AMD Milan nodes, 128 cores per node |
| Account | `rfar:regular` | Replace `rfar` with your own allocation if different |
| QOS | `normal` | Non-preemptable; use `preemptable` for lower-priority throughput |

Check your allocations with `sacctmgr show assoc user=$USER format=account,partition,qos`.

## A minimal batch script

```bash title="run-omega3p.sh"
#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=rfar:regular
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:30:00
#SBATCH --job-name=omega3p
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

source /sdf/group/rfar/ace3p/ace3p.sh
srun --overlap --cpu-bind=none -n 16 omega3p pillbox.omega3p
```

Submit, monitor, and cancel with the usual Slurm commands:

```bash
sbatch run-omega3p.sh
squeue -u $USER
scancel <jobid>
```

## Interactive sessions

For short tests, allocate an interactive shell on a compute node:

```bash
srun --partition=milano --account=rfar:regular -n 16 --time=01:00:00 --pty /bin/bash
source /sdf/group/rfar/ace3p/ace3p.sh
mpirun -n 16 omega3p pillbox.omega3p
```

## Storage

| Location | Use |
|---|---|
| `$HOME` | Scripts and small inputs. Quota is limited. |
| `/sdf/group/rfar/<user>` | Project space for inputs and results. |
| `/sdf/scratch/<group>/<user>` | Large temporary output. Purged periodically. |

!!! warning "Temporary files"
    Some ACE3P tools write scratch files to `$TMPDIR`. If `/lscratch` on a node is full, set `export TMPDIR=/sdf/scratch/<group>/<user>/tmp` before running.

## Hybrid MPI and OpenMP (Track3P)

Track3P is OpenMP-parallel inside each MPI rank, and every rank holds the whole mesh, so it runs best with few ranks and many threads. Request one or two ranks per node and let OpenMP fill the cores:

```bash
export OMP_NUM_THREADS=16
srun -n 1 -c 16 track3p input.track3p
```

Complete S3DF and Perlmutter batch scripts for the hybrid layout are in [Batch jobs](../workflow/batch-jobs.md#hybrid-mpi-and-openmp-track3p). The field solvers (Omega3P, S3P, T3P, TEM3P) are pure MPI; run them with one rank per core.
