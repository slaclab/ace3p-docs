# Local tools: Cubit and ParaView

Geometry, meshing, and visualization run on your own computer.

## Cubit

[Cubit](https://cubit.sandia.gov/) from Sandia National Laboratories is the geometry and meshing tool used throughout the ACE3P workflow. It requires a license. The tutorials were written with Cubit 16.x.

ACE3P uses Cubit through **journal files** (`.jou`), which are scripts of Cubit commands. Two ways to run one:

1. Click the **Play** button in the toolbar, browse to the `.jou` file, and open it.
2. Open **Tools, then Journal Editor**, load the file, and press Play. The editor lets you step through and modify commands.

A full walkthrough of building and meshing a cavity is on the [Cubit page](../workflow/cubit.md). The export command that ACE3P needs is Genesis format with all blocks:

```
export Genesis "model4.gen" block all overwrite
```

Mesh elements must be quadratic tetrahedra (`tetra10`) and the model must be scaled to meters before export. See [Mesh preparation](../workflow/mesh.md).

### Cubit on S3DF

A licensed Cubit is installed at `/sdf/group/rfar/software/Cubit-16.12/`. Use it through a NoMachine remote desktop, through `ssh -X`, or in batch mode without a GUI:

```bash
/sdf/group/rfar/software/Cubit-16.12/cubit -batch -nographics -input step2-Mesh-pillbox.jou
```

## ParaView

[ParaView](https://www.paraview.org/) is free. Install version 5.11 or later to match the SLAC plugin.

### Enable the SLAC toolbar

1. Open **Tools, then Manage Plugins**.
2. Select **SLACTools** and click **Load Selected**.
3. Expand the entry and check **Auto Load** so it is active on every start.

The SLAC toolbar adds a reader that loads an ACE3P mesh (`.ncdf`) together with mode or field files (`.mod`) in one step.

### Load the ACE3P macros

The CW23 materials include Python macros for common ACE3P plots. Add each one through **Macros, then Add new macro**:

| Macro | Used with | Purpose |
|---|---|---|
| `nextmode.py` | Omega3P, S3P, T3P, TEM3P | Step through modes or time steps |
| `enhancement.py` | Track3P | Plot the enhancement counter |
| `resonant.py` | Track3P | Plot resonant particles |
| `trajectory.py` | Track3P | Animate particle trajectories |
| `wakeplot.py` | T3P | Plot wake potentials |
| `timeFFT.py` | T3P | FFT of a time signal |

The macros are in the `macros/` directory alongside the examples.

### ParaView on S3DF

A ParaView 5.11.1 build with web components is installed at `/sdf/group/rfar/software/ParaView-5.11.1-MPI-Linux-Python3.9-x86_64/`. It can serve the ParaView Web Visualizer so you can look at results in a browser through an SSH tunnel without copying files to your laptop. See [Web dashboard](../interfaces/dashboard.md).
