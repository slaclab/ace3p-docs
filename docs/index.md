# ACE3P Documentation

**ACE3P** (Advanced Computational Electromagnetic 3D Parallel) is a suite of parallel finite-element codes developed at SLAC National Accelerator Laboratory for the design and analysis of particle accelerator components. It solves Maxwell's equations and coupled multiphysics problems on unstructured tetrahedral meshes with high-order basis functions, and runs on HPC systems using MPI.

<div class="grid cards" markdown>

-   :material-rocket-launch: **Getting started**

    ---

    Get a NERSC account, connect to Perlmutter with a ThinLinc desktop, and run your first job. Cubit and ParaView are already installed there.

    [:octicons-arrow-right-24: Getting started](getting-started/index.md)

-   :material-cube-scan: **Cubit**

    ---

    Geometry and meshing for ACE3P: the pillbox walkthrough, journal files, sidesets and blocks, mesh quality.

    [:octicons-arrow-right-24: Cubit chapter](cubit/index.md)

-   :material-sitemap: **Workflow**

    ---

    The common ACE3P pipeline: geometry and meshing in Cubit, mesh conversion with acdtool, solving, and post-processing.

    [:octicons-arrow-right-24: Workflow overview](workflow/index.md)

-   :material-cube-outline: **Modules**

    ---

    User guides and tutorials for each solver: Omega3P, S3P, T3P, Track3P, Pic3P, TEM3P, and Gun3P.

    [:octicons-arrow-right-24: Module guides](modules/index.md)

-   :material-book-open-variant: **Reference**

    ---

    Input-file keyword tables generated directly from the ACE3P source, so they always match the released code.

    [:octicons-arrow-right-24: Keyword reference](reference/index.md)

</div>

## Solver modules

| Module | Domain | Typical use |
|---|---|---|
| **Omega3P** | Frequency domain, eigenmodes | Cavity resonant modes, Q factors, R/Q, mode damping with couplers |
| **S3P** | Frequency domain, driven | S-parameters of couplers, waveguides, and multi-port structures |
| **T3P** | Time domain | Wakefields, transient response, beam-driven fields |
| **Track3P** | Particle tracking | Multipacting, dark current, field emission |
| **Pic3P** | Particle-in-cell | Self-consistent beam dynamics with space charge |
| **TEM3P** | Multiphysics | Thermal and mechanical analysis coupled to RF fields |
| **Gun3P** | Electrostatic / beam optics | Electron guns, space-charge-limited emission |
| **acdtool** | Utility | Mesh conversion and statistics, RF post-processing, field extraction |

## About these docs

This site replaces the CW23 workshop slide decks that were distributed as PDFs. The content is organized as a manual rather than as lecture notes, it is searchable, and it is versioned alongside ACE3P releases. Use the version selector in the header to view documentation for a specific release.

The keyword reference pages are regenerated from the ACE3P source tree whenever a release is tagged, and the [Releases](releases/index.md) section carries the developers' notes for each one. See [Contributing](contributing.md) for how that works and how to propose changes.

!!! note "Citing ACE3P"
    Please cite ACE3P when publishing results obtained with it. Contact the development team at <ace3p@slac.stanford.edu>.
