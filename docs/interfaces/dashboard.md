# Web dashboard

The ACE3P Workflow Dashboard is a browser application that documents the simulation workflow, generates solver input files from forms, produces Slurm scripts, and monitors running workflows.

Source: <https://github.com/lge0303/ace3p-dashboard>

## Features

| Area | Pages |
|---|---|
| Input generators | Omega3P, S3P, T3P, Track3P, TEM3P. Fill in boundary conditions and solver parameters in a form, preview the generated file, download it. |
| Slurm script generator | Omega3P batch scripts for Perlmutter and S3DF |
| Post-processing | `.rfpost` file generator for `acdtool postprocess rf` |
| Workflow monitor | Live status of Maestro workflows, reading Slurm `squeue` and Maestro output directories, refreshed every few seconds |
| AI generator | Front end for the [workflow assistant](workflow-assistant.md) |

The dashboard is built with Next.js and runs on S3DF. Users reach it through an SSH tunnel:

```bash
ssh -L 3000:localhost:3000 <username>@s3dflogin.slac.stanford.edu
# then open http://localhost:3000
```

No data leaves S3DF. Form logic runs in the browser and generated files are downloaded locally.

## Visualization in the browser

ParaView 5.11 on S3DF includes the ParaView Web Visualizer, which renders 3D data server-side and streams it to a browser:

```bash
PVDIR=/sdf/group/rfar/software/ParaView-5.11.1-MPI-Linux-Python3.9-x86_64
$PVDIR/bin/pvpython $PVDIR/share/paraview-5.11/web/visualizer/server/pvw-visualizer.py \
  --data /path/to/omega3p_results --port 8080
```

Tunnel port 8080 and open `http://localhost:8080`. This avoids copying large `.mod` files to a laptop. Integrating the visualizer into the dashboard is planned.
