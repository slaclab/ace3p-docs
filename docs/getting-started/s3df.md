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

The environment script sets up the libraries and the OpenMPI that ACE3P was built with and puts the binaries on your `PATH`. No `module load` is needed, and none should be added: ACE3P uses its own OpenMPI 4.1.8, built so that both `srun` and `mpirun` work, not the site module.

```bash
source /sdf/group/rfar/ace3p/ace3p.sh
```

Source it **inside your batch script**, as the reference script below does, or in an interactive `srun` shell on a `milano` node. Do not source it on the `iana` login nodes and do not put it in `~/.bashrc`: the script places Rocky 9 libraries first on `LD_LIBRARY_PATH`, and on a RHEL 8 login node that breaks every program started afterwards, including ParaView and Cubit, with errors such as

```
/lib64/libc.so.6: version `GLIBC_2.34' not found
```

The ACE3P binaries themselves do not run on the login nodes either, so a tool such as `acdtool` goes into a batch script or an interactive shell on a compute node. If a login shell already has the script sourced, open a new one, or start the GUI tools with a clean library path:

```bash
env -u LD_LIBRARY_PATH /sdf/group/rfar/software/paraview &
```

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

# ACE3P environment (libraries, OpenMPI, PATH)
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
