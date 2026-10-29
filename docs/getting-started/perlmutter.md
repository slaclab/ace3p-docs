# Running on NERSC Perlmutter

Perlmutter is NERSC's flagship system. ACE3P is installed in the `ace3p` project directory on the Community File System (CFS) and currently runs on the CPU nodes. Each CPU node has two AMD EPYC 7763 processors, 128 cores in total, and 512 GB of memory.

## Log in

The recommended way to work is through a **ThinLinc remote desktop**, which gives you a terminal, Cubit and ParaView in one window on Perlmutter. Setup is described on the [Getting started page](index.md#connecting-with-thinlinc). ThinLinc needs an sshproxy key, so do the [sshproxy step](#avoid-repeated-otp-prompts-with-sshproxy) below first.

For a terminal only:

```bash
ssh <username>@perlmutter.nersc.gov
```

Enter your password followed immediately by your six-digit one-time password, with no space between them.

### Avoid repeated OTP prompts with sshproxy

NERSC provides `sshproxy` to generate a key that is valid for 24 hours.

=== "Linux and macOS"

    ```bash
    scp <username>@dtn01.nersc.gov:/global/cfs/cdirs/mfa/NERSC-MFA/sshproxy.sh .
    ./sshproxy.sh -u <username>
    ssh -l <username> -i ~/.ssh/nersc perlmutter.nersc.gov
    ```

=== "Windows"

    ```powershell
    scp <username>@dtn01.nersc.gov:/global/cfs/cdirs/mfa/NERSC-MFA/sshproxy.exe .
    .\sshproxy.exe -u <username> --format openssh -o nersc
    ssh -l <username> -i nersc perlmutter.nersc.gov
    ```

    For PuTTY or WinSCP, omit `--format openssh` to get a `.ppk` key.

## Load the ACE3P environment

```bash
cp $CFS/ace3p/perlmutter/CPU/perlmutter-ace3p.sh ~/
source ~/perlmutter-ace3p.sh
```

The ACE3P binaries live in `$CFS/ace3p/perlmutter/CPU/`. `$CFS` expands to `/global/cfs/cdirs`.

## Cubit and ParaView

Both are installed on Perlmutter and run in a ThinLinc desktop, so meshes and results never have to leave the system. See [Pre- and post-processing tools](tools.md) for how to start them and for the ParaView SLAC toolbar.

## Working directory

Run jobs from scratch, not from your home directory:

```bash
mkdir -p $SCRATCH/ace3p
ln -s $SCRATCH/ace3p ~/ace3p
cd ~/ace3p
```

## Transfer files

Use the data transfer nodes `dtn01` through `dtn04`:

```bash
# laptop -> Perlmutter
scp pillbox4.gen <username>@dtn01.nersc.gov:ace3p/pillbox/
# Perlmutter -> laptop
scp '<username>@dtn01.nersc.gov:ace3p/pillbox/omega3p_results/*.mod' .
```

Windows users can do the same in WinSCP with protocol SCP, host `dtn01.nersc.gov`, port 22.

## A minimal batch script

```bash title="run-omega3p.batch"
#!/bin/bash -l
#SBATCH -C cpu
#SBATCH -q debug
#SBATCH -A m349
#SBATCH -N 1
#SBATCH -t 00:10:00
#SBATCH -J omega3p
#SBATCH -e ace3p.e%j
#SBATCH -o ace3p.o%j

srun -n 16 -c 16 --cpu-bind=cores $CFS/ace3p/perlmutter/CPU/omega3p pillbox.omega3p
```

| Line | Meaning |
|---|---|
| `-C cpu` | Request CPU nodes |
| `-q debug` | Short test queue, 30 minute limit. Use `regular` for production. |
| `-A m349` | The ACE3P allocation |
| `-n 16 -c 16` | 16 MPI ranks, 16 cores each, filling one 128-core node |

```bash
sbatch run-omega3p.batch
squeue -u $USER       # or: sqs
scancel <jobid>
tail -f ace3p.o<jobid>
```

See the [NERSC job documentation](https://docs.nersc.gov/jobs/) for queue policies and more options. Track3P runs best with few ranks and OpenMP threads; its batch script is in [Batch jobs](../workflow/batch-jobs.md#hybrid-mpi-and-openmp-track3p).
