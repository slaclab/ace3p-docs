# Interfaces

The command line is the primary way to run ACE3P, and everything in this documentation can be done from a terminal. The **[ACE3P GUI](gui.md)** is a desktop application built around the same solvers and input files: it writes the `.omega3p`, `.s3p` and other inputs described in this manual, submits the same binaries to Perlmutter, and adds a 3D field viewer and an AI assistant. Its own pages are at <https://ace3p.slac.stanford.edu/user-interface>.

Two Python toolkits drive ACE3P programmatically and are not yet documented here:

- **[lume-ace3p](https://github.com/slaclab/lume-ace3p)**, public on GitHub, wraps Cubit, acdtool, and the ACE3P solvers in the LUME interface for design parameter scans.
- **A3PI**, the ACE3P-IMPACT integration, chains Cubit, Omega3P, acdtool field extraction, and the IMPACT-T beam dynamics code under libEnsemble for gun optimization. Its user guide and an example are in the `commands/` and `examples/a3pi/` directories of the CW23 materials.

Learning the input format in this manual carries over to all of them.
