# TEM3P command syntax

Block-by-block description of the `.tem3p` input file. Worked cases are in the [TEM3P module guide](../../modules/tem3p/index.md).

Problem blocks: `ThermostaticProblem`, `ElasticProblem`, `ThermoElasticProblem`. Within a problem: `MeshFile`, `BasisOrder`, `CurvedSurfaces`, solver blocks, materials, `Shell`, `HeatSource`, `Boundary`, `MeshDump`, `EigenSolver`, `HarmonicAnalysis`, `Transient`.

## Problem types

```text
ThermostaticProblem : { ... }       // steady-state thermal, linear or nonlinear

ElasticProblem : { ... }            // static elasticity, eigenmodes, or harmonic response

ThermoElasticProblem : { RunId: 3 } // marker: run the following thermal then elastic
ThermostaticProblem : { ... }       // problems in sequence, passing temperature
ElasticProblem : { ... }
```

Each problem block begins with the mesh:

```text
MeshFile:       RfGunBody.ncdf
BasisOrder:     2
CurvedSurfaces: on
```

## Solvers

```text
LinearSolver : {
  Solver:            CG            // CG, GMRES, MUMPS
  Verify:            yes           // compute the residual; default no
  SaveDOFs:          yes           // keep DOFs for post-processing; default yes
  Preconditioner:    DIAGONAL      // DIAGONAL, CHOLESKY, SSOR, ILU
  AbsoluteTolerance: 1.0e-18
  Tolerance:         1.0e-10
  MaxIterations:     100000
}

PicardSolver : { ... same keys ... }      // used for Picard steps in nonlinear solves

NonlinearSolver : {
  Solver:          Newton
  PicardIteration: 10              // Picard steps before switching to Newton
  MaxIterations:   40
  AbsTolerance:    2.33e-10
  RelTolerance:    1.0e-8
}

EigenSolver : {                    // in ElasticProblem: mechanical eigenmodes
  NumEigenvalues: 5
  FrequencyShift: 1.0              // Hz
}

HarmonicAnalysis : {               // in ElasticProblem: forced response
  Start:    50                     // Hz, scan
  End:      250
  Interval: 50
  Frequency: 50                    // single frequency instead of a scan
  StiffnessDamping: 0.01           // Rayleigh damping coefficients
  MassDamping:      100000
}
```

Picard iteration first, then Newton, stabilizes nonlinear thermal solves. The eigensolver needs homogeneous boundary conditions and `Density` in the material. Harmonic analysis treats `Neumann` loads as amplitudes at each frequency; with damping the system is complex and the linear solver must handle it.

!!! note
    `AbsoluteTolerance` inside `LinearSolver` is from the command reference. The example inputs spell it `AbsoluteTolerante`, and neither string is read by `tem3p/src/LinearSolverMan.C`, which reads `Tolerance` (default 1e-10). The only absolute tolerances the code reads are `ThermalAbsoluteTolerance` and `ElasticAbsoluteTolerance` in `ThermoElasticProblem`.

## Materials

```text
ThermalConductivity : { Id: 1  Value: 391 }                  // W/(m·K)
ThermalConductivity : { Id: 3  Function: functions/ss304 }   // k(T) from a file

VolumeMaterial : {
  Id: 1
  ElasticLambda: 8.1244e+10        // Pa; or give
  ElasticMu:     4.3363e+10        // Pa
  // YoungsModulus: 17e6           // Pa, with
  // PoissonsRatio: 0.36
  ElasticAlpha:  1.70000e-5        // 1/K; not used by the eigensolver
  Density:       8960              // kg/m³; eigensolver only
}
```

`Id` is the Cubit block. Either the Lamé pair or Young's modulus with Poisson's ratio may be given; the conversion is $\mu = E/2(1+\sigma)$ and $\lambda = E\sigma/(1+\sigma)(1-2\sigma)$.

### Function files

A nonlinear property is a text file of piecewise expressions in `T`:

```text
Tstart   Tend     f(T)
-1000.0  2.8322   2.8800
2.8322   2.9743   3.0832*T+(-5.8522)
...
```

Used by `ThermalConductivity.Function`, `Boundary.SurfaceResistance`, `Boundary.RobinFactor`, and `Boundary.RobinValue`.

## Shell

```text
Shell : {
  Bd:         6                    // sideset carrying the shell
  Material:   221                  // a ThermalConductivity Id
  BasisOrder: 1
  Thickness:  1e-5                 // m
}
ThermalConductivity : { Id: 221  Function: functions/CURRR100 }
```

A thin conducting layer on a surface, for platings and coatings, without meshing it. `Material` refers to a `ThermalConductivity` block, not a mesh block.

## HeatSource

Volumetric heating, two kinds:

```text
HeatSource : {                     // dielectric loss from an RF field
  Id:                  5           // block
  ConditionType:       RFHeating
  WhichMode:           0
  DielectricConstantE: 9
  LossTangentE:        0.0001
  Directory:           s3p_results
  Method:              Powerinput
  TargetPowerinput:    437.5       // W
}

HeatSource : {                     // external heating map, FLUKA format
  Id:              9
  ConditionType:   ExtVHeating
  ExtVHeatingFile: heating_file.dat
}
```

The FLUKA file has six header lines, then `r1 r2 nr dr`, `theta1 theta2 ntheta dtheta`, `z1 z2 nz dz`, a power scaling factor, a dummy line, and nr × ntheta × nz power densities with r varying fastest.

## Thermal Boundary

```text
Boundary : { Id: 2  ConditionType: Dirichlet  DirichletValue: 2 }          // K
Boundary : { Id: 4  ConditionType: Neumann    NeumannValue: 0. }           // W/m² into the surface
Boundary : {
  Id: 5
  ConditionType: Robin                                                       // convection
  RobinConstantFactor: 20000.0                                               // h, W/(m²·K)
  RobinConstantValue:  440000.0                                              // h × T_ambient
}
Boundary : {
  Id: 5
  ConditionType: Robin
  RobinFactor: functions/He2p2f                                              // nonlinear h(T)
  RobinValue:  functions/He2p2v
}
```

### RFHeating

Heat flux from a field solution. Four ways to scale it:

=== "Powerinput (S3P)"

    ```text
    Boundary : {
      Id: 8
      ConditionType:     RFHeating
      WhichMode:         0
      Directory:         s3p_results
      Method:            Powerinput
      TargetPowerinput:  437.5             // W
      SurfaceResistance: functions/SRinnerCU
    }
    ```

=== "Gradient (Omega3P)"

    ```text
    Boundary : {
      Id: 6
      ConditionType:  RFHeating
      WhichMode:      0
      Sigma:          5.8e7
      Directory:      omega3p_results
      Method:         Gradient
      TargetGradient: 60e6                 // V/m
      DutyFactor:     0.00036
      StartPoint:     0.0001, 0.0001, -0.017018
      EndPoint:       0.0001, 0.0001,  0.017018
    }
    ```

=== "PowerLoss"

    ```text
    Boundary : {
      Id: 6
      ConditionType:   RFHeating
      WhichMode:       0
      Directory:       omega3p_results
      Method:          PowerLoss
      TargetPowerloss: 500                 // W total on metal
      Sigma:           5.8e7
    }
    ```

=== "RFHeatingMap"

    ```text
    Boundary : {
      Id: 6
      ConditionType: RFHeatingMap
      InputFile:     power.txt             // ix iy theta phi F, W/m²
    }
    ```

| Key | Meaning |
|---|---|
| `WhichMode` | Mode index, from 0 |
| `Directory` | Field solver results |
| `Method` | `Powerinput`, `Gradient`, or `PowerLoss` |
| `TargetPowerinput`, `TargetGradient`, `TargetPowerloss` | The target in W, V/m, or W |
| `StartPoint`, `EndPoint` | Gradient integration line, m |
| `Sigma` | Conductivity for computing loss from the surface H, S/m |
| `SurfaceResistance` | Function file R~s~(T) instead of `Sigma` |
| `DutyFactor` | Multiplies the load for pulsed operation |
| `SymmetryFactor` | Reference says 1 full, 0 half for heating; 0 full, 1 half, 2 quarter for detuning. Inconsistent in the reference document. `EMHeating.C` reads it with default 0 and a warning when absent; check `tem3p.out` for the value applied. |

## Mechanical Boundary

```text
Boundary : { Id: 1  ConditionType: Dirichlet  DirichletValue: 0. }         // all components fixed, m
Boundary : { Id: 4  ConditionType: Neumann    NeumannValue: 0. }           // normal traction, Pa; positive pushes into the surface
Boundary : {
  Id: 2
  ConditionType: Mixed
  MixedType:  DIRICHLET NEUMANN NEUMANN                                      // per direction x y z
  MixedValue: 0., 0., 0.
}
```

### LFDetuning

Radiation pressure from a field solution:

```text
Boundary : {
  Id:             6
  ConditionType:  LFDetuning
  WhichMode:      0
  Directory:      omega3p_results
  Omega3PId:      6                       // wall sideset in the vacuum mesh
  Method:         Gradient                // Gradient, Voltage, or Powerinput
  TargetGradient: 60e6
  GradientDirection: 0, 0, 1              // default
  SymmetryFactor: 2
  StartPoint:     0.0001, 0.0001, -0.017018
  EndPoint:       0.0001, 0.0001,  0.017018
}
```

`Method: Voltage` takes `TargetVoltage` in V and `VoltageDirection`; `Method: Powerinput` takes `TargetPowerinput` in W.

## MeshDump

```text
MeshDump : {
  WriteDeformedMesh:   on          // body mesh with displacements
  WriteDeformedEMMesh: on          // vacuum mesh with mapped displacements
  MeshDeformScale:     1.0         // multiply displacements; for mode shapes
  EMMeshInputDir:      omega3p_results
  WriteStressStrain:   on
}
```

## Transient

Time-dependent thermal analysis inside `ThermostaticProblem`:

```text
Transient : {
  TimeStepping : {
    Type:        Thermal
    Scheme:      BackwardEuler
    MaximumTime: 8.e1              // s
    DT:          4.e-1
    InitialT:    0.                // start time
    InitialTemp: 25.               // °C
  }
  Excitation : {
    Power: 1.
    Pulse : {
      Type:         Monochromatic
      Frequency:    1.
      Rise periods: 10
      T0:           0.
    }
  }
}
```

The `Excitation` block reuses T3P's pulse machinery to modulate the heat load in time; `Fall periods` and `TMax` are optional as in T3P.

## Post-processing

`acdtool mesh deform` exaggerates a deformed mesh for viewing, and `acdtool postprocess project` decomposes a static or harmonic displacement field onto a set of mechanical eigenmodes. See the [acdtool command syntax](acdtool.md).
