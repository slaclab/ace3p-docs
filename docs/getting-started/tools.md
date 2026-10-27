# Pre- and post-processing tools: Cubit and ParaView

Two graphical programs bracket every ACE3P run: **Cubit** builds the geometry and the mesh before the solver, and **ParaView** displays the fields and particles after it. Both are installed on Perlmutter and on S3DF. You do not need to install them yourself; run them in a remote desktop on the HPC system, next to your meshes and results.

| | Cubit | ParaView |
|---|---|---|
| Role | Pre-processing: geometry, meshing, sidesets and blocks, `.gen` export | Post-processing: fields, modes, particle trajectories, wake plots |
| On Perlmutter | Installed, run in a [ThinLinc desktop](index.md#connecting-with-thinlinc) | Installed, run in a ThinLinc desktop or in client-server mode |
| On S3DF | Installed, run in a NoMachine desktop or with `ssh -X` | Installed, run in a NoMachine desktop or through the web visualizer |
| On your own computer | Possible; needs a license | Possible; free download |
| Learn more | [Cubit chapter](../cubit/index.md) | [Omega3P tutorial](../modules/omega3p/tutorial-pillbox.md), module pages |

## Cubit

Cubit from Sandia National Laboratories is the geometry and meshing tool used throughout the ACE3P workflow. ACE3P drives it mostly through **journal files** (`.jou`), scripts of Cubit commands that make a mesh reproducible. The [Cubit chapter](../cubit/index.md) walks through building and meshing a pillbox cavity, first interactively, then by journal, and ends with the export rules. The short version:

```
export Genesis "model4.gen" block all overwrite
```

Mesh elements must be quadratic tetrahedra (`tetra10`) and the model must be scaled to meters before export. See [Mesh preparation](../workflow/mesh.md).

### Cubit on Perlmutter

Connect with [ThinLinc](index.md#connecting-with-thinlinc), open a terminal and start Cubit from the ACE3P project area under `$CFS/ace3p/`:

```bash
ls $CFS/ace3p/            # the Cubit directory is listed here
<path-to-cubit>/cubit &
```

<!-- TODO: replace <path-to-cubit> with the installed Perlmutter path and version once confirmed. -->

The GUI opens on the ThinLinc desktop. Set the working directory to your scratch area (**File, then Set Directory**) so the `.gen` file lands where `acdtool meshconvert` will read it.

### Cubit on S3DF

Cubit 16.12 is installed at `/sdf/group/rfar/software/Cubit-16.12/`. Start it from a NoMachine desktop or an `ssh -X` session:

```bash
/sdf/group/rfar/software/Cubit-16.12/cubit &
```

A journal can also be played with no display, which is what automated workflows do:

```bash
/sdf/group/rfar/software/Cubit-16.12/cubit -batch -nographics -input step2-Mesh-pillbox.jou
```

### Installing Cubit on your own computer

Cubit requires a license. Two routes:

- **Sandia Cubit** is free for U.S. government use: government agencies and laboratories, and companies working under a direct U.S. government contract. Request a license through the [ASC software request form](https://www.sandia.gov/ascsoftware/asc-software-request/); approval takes a few weeks. Downloads and the licensing rules are at [cubit.sandia.gov/licensing](https://cubit.sandia.gov/licensing/) and [cubit.sandia.gov/downloads](https://cubit.sandia.gov/downloads/).
- **Coreform Cubit** is the commercial version for everyone else, with trial and academic licenses from [coreform.com](https://coreform.com/products/coreform-cubit/). Journal files written for one run in the other.

The tutorials were written with Cubit 16.x. Running Cubit locally means copying `.gen` files up to the HPC system with `scp`.

## ParaView

ParaView is free, open-source software from Kitware. ACE3P results are read through the **SLAC toolbar**, a plugin shipped with every ParaView release, which loads a mesh (`.ncdf`) together with mode or field files (`.mod`) in one step.

### ParaView on Perlmutter

NERSC maintains ParaView on Perlmutter; versions 5.12, 5.13 and 6.0 are available at the time of writing. In a ThinLinc desktop:

```bash
module avail paraview        # list the installed versions
module load paraview         # pick one, e.g. module load paraview/5.13.3
paraview &
```

For very large datasets NERSC also supports **client-server mode**, where the ParaView GUI runs on your computer and the data stays on Perlmutter. Setup is in the [NERSC ParaView guide](https://docs.nersc.gov/applications/paraview/). The client version must match the server version listed there.

### ParaView on S3DF

ParaView 5.11.1 is installed at `/sdf/group/rfar/software/ParaView-5.11.1-MPI-Linux-Python3.9-x86_64/`. Start `bin/paraview` from a NoMachine desktop, or use the ParaView Web Visualizer through an SSH tunnel as described on the [Web dashboard](../interfaces/dashboard.md) page.

### Installing ParaView on your own computer

Download the installer for Windows, macOS or Linux from [paraview.org/download](https://www.paraview.org/download/). No license is needed. Use version 5.11 or later; the SLAC toolbar is included. Running ParaView locally means copying `.ncdf` and `.mod` files down from the HPC system with `scp`.

### Enable the SLAC toolbar

Do this once per ParaView installation, on the HPC system or your laptop:

1. Open **Tools, then Manage Plugins**.
2. Select **SLACTools** and click **Load Selected**.
3. Expand the entry and check **Auto Load** so it is active on every start.

A **SLAC** button appears in the toolbar. Click it, pick the `.ncdf` mesh and the `.mod` field file, and the model loads with the field data attached.

### Load the ACE3P macros

The CW23 materials include Python macros for common ACE3P plots. Add each one through **Macros, then Add new macro**:

| Macro | Used with | Purpose |
|---|---|---|
| `nextmode.py` | Omega3P, S3P, T3P, TEM3P | Step through modes or time steps |
| `enhancement.py` | Track3P | Plot the enhancement counter |
| `resonant_lineplot.py`, `resonant_location.py` | Track3P | Resonant particles: energy vs field level, impact locations |
| `trajectory.py` | Track3P | Animate particle trajectories |
| `wakeplot.py` | T3P | Plot wake potentials |
| `timeFFT.py` | T3P | FFT of a time signal |

The macros are in `$CFS/ace3p/cw23/macros` on Perlmutter and `/sdf/group/rfar/ace3p/cw23/macros` on S3DF. If you run ParaView on your laptop, copy that directory down first.
