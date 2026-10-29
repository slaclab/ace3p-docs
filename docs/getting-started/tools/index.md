# Pre- and post-processing tools

Two graphical programs bracket every ACE3P run: **Cubit** builds the geometry and the mesh before the solver, and **ParaView** displays the fields and particles after it. Both are installed on Perlmutter and on S3DF. You do not need to install them yourself; run them in a remote desktop on the HPC system, next to your meshes and results.

| | Cubit | ParaView |
|---|---|---|
| Role | Pre-processing: geometry, meshing, sidesets and blocks, `.gen` export | Post-processing: fields, modes, particle trajectories, wake plots |
| On Perlmutter | Cubit 16.16 under `$CFS/ace3p/tools/`, run in a [ThinLinc desktop](../index.md#connecting-with-thinlinc) | ParaView 5.11.0 under `$CFS/ace3p/tools/`, run in a ThinLinc desktop; NERSC client-server mode for large data |
| On S3DF | Installed, run in a NoMachine desktop or with `ssh -X` | Installed, run in a NoMachine desktop or through the web visualizer |
| On your own computer | Possible; needs a license | Possible; free download |
| Page | [Cubit](cubit.md): interface, pillbox walkthrough, journal files, meshing, sidesets and blocks, export, where to run it | [ParaView](paraview.md): starting it, SLAC toolbar, ACE3P macros, installing locally |

Each tool has its own page. If you have never used Cubit, start with the [Cubit page](cubit.md); it builds and meshes a pillbox cavity step by step and every module tutorial assumes that walkthrough. The [ParaView page](paraview.md) is short: enable the SLAC toolbar once, load the macros, and you can open any ACE3P result.
