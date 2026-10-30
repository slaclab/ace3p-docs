# Kly3P command syntax

!!! tip "New since CW23"
    Kly3P is a new module (2024 to 2025). It computes the large-signal operating point of a klystron cavity: the RF mode amplitude and phase that are self-consistent with the beam loading, by iterating a Pic3P tracking run against a circuit model of each cavity mode. There is no user guide or tutorial yet; this page documents the input file from the source and the test case in `kly3p/test/`.

```bash
kly3p <project>.kly3p [jobname]
```

Kly3P is built on the T3P and Pic3P libraries and reads a `.kly3p` input file that is a Pic3P input plus two blocks, `LargeSignalProblem` and `RFProblem`. The mesh, boundary conditions, finite-element order, time stepping, linear solver, particle loading and drive-field map are exactly as in [Pic3P](pic3p.md). `kly3pOutputConverter` writes the field files for ParaView and, like `gun3pOutputConverter`, can export the field on a structured grid.

## LargeSignalProblem

```text
LargeSignalProblem : {
  SymmetryFactor: 1

  ElectricAbsoluteTolerance: 0.
  ElectricRelativeTolerance: 1.00e-12
  MagneticAbsoluteTolerance: 0.
  MagneticRelativeTolerance: 1.00e-12

  PowerAbsoluteTolerance:    1.e-6
  PowerRelativeTolerance:    1.00e-12

  MaxIterations:  10
  PrintFrequency: 10
  Save iteration data: On
}
```

| Key | Default | Meaning |
|---|---|---|
| `SymmetryFactor` | 1 | 1 full, 2 half, 4 quarter model |
| `PowerAbsoluteTolerance`, `PowerRelativeTolerance` | | Convergence test on the power balance between iterations |
| `ElectricAbsoluteTolerance`, `ElectricRelativeTolerance`, `MagneticAbsoluteTolerance`, `MagneticRelativeTolerance` | | Convergence tests on the field coefficients |
| `MaxIterations` | | Stop after this many large-signal iterations regardless |
| `PrintFrequency` | 10 | Progress print interval |
| `Save iteration data` | Off | Keep the particle and field output of every iteration |

Each iteration tracks the bunch through the drive fields, computes the beam-induced current in each mode, updates the mode coefficients from the circuit model, and rescales the drive fields for the next pass.

## RFProblem

One `DriveField` entry per cavity mode. Several may be given, one for each mode in the `Loading.DriveField` list, in the same order.

```text
RFProblem : {
  FrequencyDetuned: 1.e9
  DriveField : {
    Frequency:              11.382e9      // mode frequency, Hz
    FrequencyDetuned:       0.5e9         // detuning of the drive from the mode, Hz
    Qloss:                  4539.9        // wall-loss Q of the mode
    Qext:                   156.5         // external Q through the output coupler
    WallLoss:               6.974e-05     // wall loss per unit stored energy, from Omega3P
    InputPower:             0.            // drive power into the cavity, W; 0 for an output cavity
    InputPhase:             0.            // degrees
    InitialModeCoefficient: 1.e5          // starting amplitude of the mode
    Scale:                  1.            // optional multiplier on the Omega3P map
    Phase:                  0.            // optional phase offset, degrees
  }
}
```

| Key | Meaning |
|---|---|
| `Frequency` | Mode frequency in Hz; matches the Omega3P mode used in `Loading.DriveField` |
| `FrequencyDetuned` | Offset of the drive or beam frequency from the mode frequency, Hz. The top-level value is the default for every mode. |
| `Qloss`, `Qext`, `WallLoss` | Circuit-model parameters of the mode, taken from the Omega3P post-processing of the cavity |
| `InputPower`, `InputPhase` | External drive for an input or gain cavity; zero for an output cavity, which is excited only by the beam |
| `InitialModeCoefficient` | Starting value of the complex mode amplitude for the iteration |
| `Scale`, `Phase` | Optional rescaling of the field map before the first iteration |

## Pic3P blocks

`ModelInfo`, `FiniteElement`, `PRegion`, `TimeStepping`, `LinearSolver`, `CheckPoint` and `Loading` with `Particles`, `ConstantField` and `DriveField` are as described on the [Pic3P page](pic3p.md). `TrackingOnly: yes` in `Particles` runs without space charge, which is the usual setting for a klystron cavity where the beam is prescribed. `ElectrostaticProblem` and `MagnetostaticProblem` blocks may be present but empty.

## Output

Per iteration, the particle dumps and field monitors of Pic3P under `<jobname>/`, plus the power balance and the converged mode coefficients in the log. `kly3pOutputConverter <project>.kly3p e` converts the stored fields to `.mod` files and accepts the same `Outputs` keys as the [Gun3P converter](gun3p.md#gun3poutputconverter), including `XRange`, `YRange`, `ZRange`.

## Example

The test model is an XC8 output cavity in the first quadrant, `kly3p/test/` in the source tree: `input.kly3p`, the Cubit journal `mesh-xc8.jou`, and `o3p.in` for the Omega3P run that produces the drive-field map.
