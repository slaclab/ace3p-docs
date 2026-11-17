# ParaView

ParaView is the post-processing and visualization tool for ACE3P: it displays meshes, mode and field files, particle trajectories and wake data. It is free, open-source software from Kitware. ACE3P results are read through the **SLAC toolbar**, a plugin shipped with every ParaView release, which loads a mesh (`.ncdf`) together with mode or field files (`.mod`) in one step.

## ParaView on Perlmutter

ParaView 5.11.0 with the SLAC toolbar is installed in the ACE3P project area. In a ThinLinc desktop:

```bash
$CFS/ace3p/tools/ParaView-5.11.0-MPI-Linux-Python3.9-x86_64/bin/paraview &
```

This is the version the tutorials and the CW23 macros were tested with. NERSC also provides newer ParaView releases (5.12 and later) and a **client-server mode** for very large datasets, where the GUI runs on your computer and the data stays on Perlmutter. Setup is in the [NERSC ParaView guide](https://docs.nersc.gov/applications/paraview/); the client version must match the server version listed there.

## ParaView on S3DF

ParaView 5.11.1 with the SLAC toolbar is installed under `/sdf/group/rfar/software/`. In a NoMachine desktop on an `iana` node:

```bash
source /sdf/group/rfar/ace3p/ace3p.sh
paraview &
```

The environment script puts this version first on your `PATH`; without it, `paraview` is the older system package 5.9.1 in `/usr/bin`. ParaView also runs on a `milano` compute node inside an interactive job started with `srun --x11 --pty bash`, which is useful for results too large for the login node.

## Installing ParaView on your own computer

Download the installer for Windows, macOS or Linux from [paraview.org/download](https://www.paraview.org/download/). No license is needed. Use version 5.11 or later; the SLAC toolbar is included. Running ParaView locally means copying `.ncdf` and `.mod` files down from the HPC system with `scp`.

## Enable the SLAC toolbar

Do this once per ParaView installation, on the HPC system or your laptop:

1. Open **Tools, then Manage Plugins**.
2. Select **SLACTools** and click **Load Selected**.
3. Expand the entry and check **Auto Load** so it is active on every start.

A **SLAC** button appears in the toolbar. Click it, pick the `.ncdf` mesh and the `.mod` field file, and the model loads with the field data attached.

## Seeing the field inside the volume

The SLAC reader loads the **External Surface** only, so by default you see the field on the walls and the **Entire Volume** entry in the Pipeline Browser is empty. To look inside:

1. Select the reader (the top entry in the Pipeline Browser).
2. In the Properties panel, check **Read Internal Volume** and click **Apply**.
3. Show **Entire Volume** and hide **External Surface** with the eye icons, or keep both and make the surface translucent (Opacity below 1).
4. Use the **Clip** and **Slice** filters from the Common toolbar near the top of the window to cut the model open and see the field on the cut.

This applies to every `.mod` file: Omega3P and S3P modes, TEM3P results, and the T3P and Pic3P `*ts_t<time>ps.out.mod` snapshots alike. Reading the volume takes more memory than the surface, so leave it off when you only need the wall fields.

Step-by-step procedures for movies, vector cones, surface and node identification, particle trajectories and data export are on the [ParaView recipes](paraview-recipes.md) page.

## Load the ACE3P macros

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
