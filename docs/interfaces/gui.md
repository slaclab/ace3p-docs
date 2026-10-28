# ACE3P GUI

The ACE3P GUI is a desktop application that builds input files for all seven solvers, meshes geometries, submits jobs to NERSC Perlmutter, and post-processes the results, without editing text files by hand. It is developed by the ACE3P team and released separately from the solvers. The current version is **1.4.15**.

Everything about the GUI is on its own pages:

- **Overview and downloads:** <https://ace3p.slac.stanford.edu/user-interface>
- **User guide:** <https://mothmanslac.github.io/ace3p-gui-docs/>, with sections on getting started, a tutorial, simulation setup, running jobs, workflow orchestration, result post-processing, the AI assistant, and a reference.

This manual does not repeat that material. It documents the input files, keywords and command-line tools that the GUI produces and calls, so the two fit together: use the GUI to build a run, and this manual to understand what each field means.

## Getting the GUI

=== "Perlmutter"

    Already installed in the ACE3P project area. Connect with a [ThinLinc desktop](../getting-started/index.md#connecting-with-thinlinc), open a terminal and run:

    ```bash
    /global/cfs/cdirs/ace3p/gui/ACE3P-GUI-v1.4.15-linux-x86_64/ACE3P-GUI
    ```

=== "Windows or Linux desktop"

    Download `ACE3P-GUI-v1.4.15-windows-x86_64.exe` or `ACE3P-GUI-v1.4.15-linux-x86_64.tar.gz` from the link on the [user-interface page](https://ace3p.slac.stanford.edu/user-interface). No installer is needed; unpack and run. The GUI connects to Perlmutter to submit jobs, so you still need a NERSC account.

## What it does

| Area | In the GUI | In this manual |
|---|---|---|
| Simulation setup | Forms that write the `.omega3p`, `.s3p`, `.t3p`, `.track3p`, `.tem3p`, `.gun3p` input as you type | [Input file format](../workflow/input-format.md), [command syntax](../reference/index.md) and keyword tables |
| Meshing | Drives Cubit journals and `acdtool meshconvert` | [Cubit](../cubit/index.md), [Mesh preparation](../workflow/mesh.md) |
| Running jobs | Submits to Perlmutter and monitors the queue | [Running on Perlmutter](../getting-started/perlmutter.md), [Batch jobs](../workflow/batch-jobs.md) |
| Workflow orchestration | Parameter sweeps and optimization chains | Module pages describe the individual steps |
| Post-processing | 3D field viewer, data explorer, `acdtool postprocess` | [Omega3P post-processing](../modules/omega3p/postprocess.md) and the module pages |
| AI assistant | Troubleshooting and input help inside the GUI | |

Questions and feedback on the GUI go to the ACE3P team at <ace3p@slac.stanford.edu>.
