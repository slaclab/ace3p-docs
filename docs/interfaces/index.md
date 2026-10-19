# Interfaces

The command line is the primary way to run ACE3P, and everything in this documentation can be done from a terminal. Three higher-level interfaces are being developed around the same solvers and input files.

| Interface | What it does | Where it runs | Status |
|---|---|---|---|
| [ACE3P GUI](gui.md) | Desktop application for building input files and launching jobs | Perlmutter (Linux), Windows | First release, v1.4.15 |
| [Web dashboard](dashboard.md) | Browser-based input generators, workflow documentation, job monitoring | S3DF, via SSH tunnel | Prototype |
| [AI workflow assistant](workflow-assistant.md) | Natural-language generation of multi-step workflow specifications, executed by Maestro on Slurm | S3DF | Prototype, validated on Omega3P and Track3P |

All three produce the same `.omega3p`, `.s3p`, and other input files described in this manual, and all three submit the same solver binaries. Learning the input format here carries over to any of them.
