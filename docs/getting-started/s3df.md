# Running on S3DF

!!! note "SLAC users only"
    S3DF, SLAC's Shared Scientific Data Facility, is reachable only with a SLAC computing account. Users elsewhere should use [NERSC Perlmutter](perlmutter.md), which is the main ACE3P platform. The rest of this manual applies to both systems.

ACE3P is installed under the `rfar` group area and runs on the Rocky 9 nodes of the `milano` partition. Cubit and ParaView are installed as well; see [Pre- and post-processing tools](tools/index.md).

!!! info "Rocky 9 build, November 2026"
    S3DF moved its nodes to Rocky Linux 9. The current ACE3P binaries are built for Rocky 9 (GCC 11.5, PETSc 3.25, MUMPS 5.9, OpenMPI 4.1.8) and run only on nodes with that OS, which the `--constraint=OS_VER:9.6` line in the batch script selects. The previous RHEL 8 installation is kept under `/sdf/group/rfar/ace3p/rocky8/` for jobs that still need it.

## Log in

```bash
ssh <username>@s3dflogin.slac.stanford.edu
ssh iana
```

The second command moves you to an interactive node (`sdfiana0xx`). Use these nodes for editing, job submission, and the GUI tools in a NoMachine desktop. Do not run solvers on them. The `iana` nodes still run RHEL 8 while the `milano` compute nodes run Rocky 9, which matters for the environment script below.

## Load the ACE3P environment

One command sets up everything, on the login nodes and inside batch scripts alike:

```bash
source /sdf/group/rfar/ace3p/ace3p.sh
```

It loads three module files from `/sdf/group/rfar/ace3p/modulefiles`: `ace3p` (the solvers, `acdtool`, and the OpenMPI they were built with), `cubit`, and `paraview`. Nothing else is needed, and no `module load openmpi`: ACE3P ships its own OpenMPI 4.1.8, and the `ace3p` module makes a plain `srun -n N` use PMIx, which is what works on the Rocky 9 nodes. `mpirun` works as well.

!!! note "What the script does not do"
    The solvers run only on the Rocky 9 `milano` nodes, so on an `iana` login node `omega3p` or `acdtool` will not start. Put them in a batch script. The script sets no `LD_LIBRARY_PATH`, so Cubit and ParaView started from the same shell work normally. If you use ACE3P regularly, the `source` line can go in `~/.bashrc`.

The same script serves developers: the `ace3p` module also sets `SPACK_ENV` and `MPI_HOME`, which the ACE3P CMake build reads. Build on a Rocky 9 node.

## Partitions and accounts

| Setting | Value | Notes |
|---|---|---|
| Partition | `milano` | AMD Milan nodes, 128 cores per node |
| Constraint | `OS_VER:9.6` | Rocky 9 nodes, required by the current binaries |
| Account | `rfar:regular` | Replace `rfar` with your own allocation if different |
| QOS | `normal` | Non-preemptable; use `preemptable` for lower-priority throughput |

Check your allocations with `sacctmgr show assoc user=$USER format=account,partition,qos`.

## A minimal batch script

The reference script is `/sdf/group/rfar/ace3p/run.sl`; copy it and change the job name, resources and solver line.

```bash title="run.sl"
#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=rfar:regular
#SBATCH --constraint=OS_VER:9.6
#SBATCH --job-name=omega3p
#SBATCH --output=output-%j.txt
#SBATCH --error=error-%j.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=16gb
#SBATCH --time=0-00:45:00

# ACE3P environment (modules: ace3p, cubit, paraview)
source /sdf/group/rfar/ace3p/ace3p.sh

srun -n 16 --cpu-bind=cores omega3p pillbox.omega3p
```

Multi-node jobs work the same way: raise `--nodes` and give `srun -n` the total rank count. `mpirun -n 16 omega3p pillbox.omega3p` is an equivalent last line.

Submit, monitor, and cancel with the usual Slurm commands:

```bash
sbatch run-omega3p.sh
squeue -u $USER
scancel <jobid>
```

## Interactive sessions

For short tests, allocate an interactive shell on a compute node:

```bash
srun --partition=milano --account=rfar:regular --constraint=OS_VER:9.6 -n 16 --time=01:00:00 --pty /bin/bash
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
