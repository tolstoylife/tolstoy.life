---
name: physical-foundations
description: Physical and chemical foundations of physiology - pressure-driven flow, electrical forces, diffusion, chemical energy, and thermodynamics
parent: quantitative-physiology
unit: 1
---

# Physical and Chemical Foundations of Physiology

## Overview

This sub-skill covers the quantitative physical and chemical principles underlying all physiological processes. These foundations are essential for understanding transport, signaling, and energy transformations in biological systems.

## Core Concepts

### 1. Pressure-Driven Flow

#### Flow and Flux Definitions

**Volume Flux** (J_V): Volume flowing per unit area per unit time
```
J_V = Q_V / A    [m³/(m²·s) = m/s]
```

**Solute Flux** (J_S): Amount of solute per unit area per unit time
```
J_S = Q_S / A    [mol/(m²·s)]
```

#### Continuity Equation

The fundamental conservation law for transport:
```
∂C/∂t = -∂J/∂x
```

**Physical meaning**: If flux varies spatially (∂J/∂x ≠ 0), concentration must change temporally.

**Steady state** (∂C/∂t = 0) requires uniform flux → linear concentration gradient.

#### Hydrostatic Pressure

Pressure at depth h in fluid:
```
P = ρgh
```
Where:
- ρ = fluid density (kg/m³)
- g = gravitational acceleration (9.8 m/s²)
- h = height of fluid column (m)

**Clinical relevance**: Blood pressure measurement, CSF dynamics, edema formation.

#### Poiseuille's Law

For laminar flow through a cylindrical tube:
```
Q_V = (πr⁴/8η) × (ΔP/L)
```

**Key insights**:
- Flow ∝ r⁴ (doubling radius → 16× flow)
- Flow ∝ 1/η (viscosity impedes flow)
- Flow ∝ ΔP (pressure gradient drives flow)
- Flow ∝ 1/L (longer tubes = more resistance)

**Hydraulic resistance**: R = 8ηL/(πr⁴)
```
Q_V = ΔP/R    (analogous to Ohm's law: I = V/R)
```

#### Law of Laplace

Relates wall tension to transmural pressure:

**Cylinder** (blood vessels):
```
ΔP = T/r    or    T = ΔP × r
```

**Sphere** (alveoli, cells):
```
ΔP = 2T/r    or    T = ΔP × r/2
```

**Clinical implications**:
- Aneurysms: Larger radius → more wall tension → risk of rupture
- Alveoli: Surfactant reduces surface tension, preventing collapse
- Heart: Dilated ventricle requires more wall tension for same pressure

### 2. Electrical Forces

#### Coulomb's Law

Electrostatic force between point charges:
```
F = (q₁q₂)/(4πε₀r²)
```

Where:
- q₁, q₂ = charges (C)
- ε₀ = 8.85×10⁻¹² C²/(J·m) (permittivity of free space)
- r = separation distance (m)

In a medium with dielectric constant ε:
```
F = (q₁q₂)/(4πεε₀r²)
```

#### Electric Potential

Work per unit charge to move from reference to point A:
```
U_A = -∫(F·ds)/q_test
```

Units: Volts (V) = Joules per Coulomb (J/C)

#### Electric Field

Force per unit charge:
```
E = F/q = -∇U
```

The field points from high to low potential (downhill for positive charges).

#### Capacitance

Definition:
```
C = Q/V    [Farads = C/V]
```

Parallel plate capacitor:
```
C = εε₀A/d
```

**Membrane as capacitor**:
- Typical membrane capacitance: 1 μF/cm²
- Lipid bilayer thickness: ~4 nm
- Membrane acts as insulator between two conductors

### 3. Diffusion

#### Fick's First Law

Diffusive flux is proportional to concentration gradient:
```
J_S = -D(∂C/∂x)
```

Where D = diffusion coefficient (m²/s)

**Negative sign**: Flux goes from high to low concentration (down the gradient).

#### Fick's Second Law

Time evolution of concentration during diffusion:
```
∂C/∂t = D(∂²C/∂x²)
```

Derived from Fick's First Law + Continuity Equation.

#### Diffusion Coefficient

**Einstein relation**:
```
D = kT/ζ
```
Where ζ = frictional coefficient

**Stokes-Einstein equation** (spherical particle):
```
D = kT/(6πηa)
```
Where:
- k = 1.38×10⁻²³ J/K (Boltzmann constant)
- T = temperature (K)
- η = viscosity (Pa·s)
- a = particle radius (m)

**Typical values**:
| Molecule | D in water (m²/s) |
|----------|-------------------|
| Na⁺ | 1.3×10⁻⁹ |
| K⁺ | 2.0×10⁻⁹ |
| Glucose | 6.7×10⁻¹⁰ |
| Albumin | 6×10⁻¹¹ |

#### Diffusion Time

Characteristic time for diffusion over distance x:
```
t = x²/(2D)
```

**Example**: For D = 10⁻⁹ m²/s
- 1 μm: t ≈ 0.5 ms
- 10 μm: t ≈ 50 ms
- 100 μm: t ≈ 5 s
- 1 mm: t ≈ 500 s ≈ 8 min
- 1 cm: t ≈ 50,000 s ≈ 14 hours

**Implications**: Diffusion works for cells, fails for whole organisms → need circulation.

### 4. Chemical Energy and Thermodynamics

#### Enthalpy

Heat content at constant pressure:
```
H = E + PV
```

#### Entropy

Measure of disorder/randomness:
```
ΔS = Q_rev/T
```

#### Gibbs Free Energy

Maximum useful work from a process:
```
G = H - TS
ΔG = ΔH - TΔS
```

**Spontaneity**:
- ΔG < 0: Spontaneous (exergonic)
- ΔG > 0: Non-spontaneous (endergonic)
- ΔG = 0: Equilibrium

#### Standard Free Energy

At 1 M concentrations, 1 atm, 25°C:
```
ΔG° = -RT ln(K_eq)
```

Actual free energy change:
```
ΔG = ΔG° + RT ln(Q)
```
Where Q = reaction quotient (actual concentration ratio)

#### ATP Hydrolysis

```
ATP + H₂O → ADP + Pᵢ
```

**Standard**: ΔG° ≈ -30.5 kJ/mol
**Cellular conditions**: ΔG ≈ -54 kJ/mol

The higher magnitude in cells is due to:
- Low ADP concentration
- Low Pᵢ concentration
- High ATP concentration

### 5. Electrochemical Potential

Unifying electrical and chemical driving forces:
```
μ̃ = μ° + RT ln(C) + zFψ
```

Where:
- μ° = standard chemical potential
- RT ln(C) = concentration term
- zFψ = electrical term (z = valence, F = Faraday, ψ = potential)

**Equilibrium condition**: Δμ̃ = 0

This leads to the **Nernst equation**:
```
E = (RT/zF) ln(C_out/C_in)
```

At 37°C (310 K):
```
E = (26.7 mV/z) ln(C_out/C_in)
E ≈ (61.5 mV/z) log₁₀(C_out/C_in)
```

## Computational Models

### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Physical constants
R = 8.314       # J/(mol·K)
F = 96485       # C/mol
k_B = 1.38e-23  # J/K
N_A = 6.02e23   # mol⁻¹

class PhysicalFoundations:
    """Quantitative models for physical foundations of physiology"""

    @staticmethod
    def poiseuille_flow(delta_P, r, L, eta):
        """
        Calculate flow through cylindrical tube (Poiseuille's Law)

        Parameters:
        -----------
        delta_P : float - Pressure difference (Pa)
        r : float - Tube radius (m)
        L : float - Tube length (m)
        eta : float - Viscosity (Pa·s)

        Returns:
        --------
        Q : float - Volume flow rate (m³/s)
        """
        return (np.pi * r**4 * delta_P) / (8 * eta * L)

    @staticmethod
    def laplace_cylinder(T, r):
        """Transmural pressure for cylinder (blood vessel)"""
        return T / r

    @staticmethod
    def laplace_sphere(T, r):
        """Transmural pressure for sphere (alveolus)"""
        return 2 * T / r

    @staticmethod
    def diffusion_coeff(T, eta, a):
        """
        Stokes-Einstein diffusion coefficient

        Parameters:
        -----------
        T : float - Temperature (K)
        eta : float - Viscosity (Pa·s)
        a : float - Particle radius (m)

        Returns:
        --------
        D : float - Diffusion coefficient (m²/s)
        """
        return (k_B * T) / (6 * np.pi * eta * a)

    @staticmethod
    def diffusion_time(x, D):
        """Characteristic time for diffusion over distance x"""
        return x**2 / (2 * D)

    @staticmethod
    def nernst_potential(z, C_out, C_in, T=310):
        """
        Nernst equilibrium potential

        Parameters:
        -----------
        z : int - Ion valence
        C_out : float - Extracellular concentration
        C_in : float - Intracellular concentration
        T : float - Temperature (K), default 37°C

        Returns:
        --------
        E : float - Equilibrium potential (V)
        """
        return (R * T) / (z * F) * np.log(C_out / C_in)

    @staticmethod
    def gibbs_free_energy(delta_G0, Q, T=310):
        """
        Actual Gibbs free energy change

        Parameters:
        -----------
        delta_G0 : float - Standard free energy change (J/mol)
        Q : float - Reaction quotient
        T : float - Temperature (K)

        Returns:
        --------
        delta_G : float - Free energy change (J/mol)
        """
        return delta_G0 + R * T * np.log(Q)

    @staticmethod
    def diffusion_1d(C0, x, t, D):
        """
        1D diffusion from point source (Gaussian spreading)

        Parameters:
        -----------
        C0 : float - Initial amount
        x : array - Position array (m)
        t : float - Time (s)
        D : float - Diffusion coefficient (m²/s)

        Returns:
        --------
        C : array - Concentration profile
        """
        return (C0 / np.sqrt(4 * np.pi * D * t)) * np.exp(-x**2 / (4 * D * t))


# Example usage and visualization
if __name__ == "__main__":
    pf = PhysicalFoundations()

    # Example: Diffusion time scaling
    distances = np.logspace(-6, -2, 100)  # 1 μm to 1 cm
    D = 1e-9  # m²/s (typical small molecule)
    times = pf.diffusion_time(distances, D)

    plt.figure(figsize=(10, 6))
    plt.loglog(distances * 1e6, times, 'b-', linewidth=2)
    plt.xlabel('Distance (μm)')
    plt.ylabel('Diffusion Time (s)')
    plt.title('Diffusion Time vs Distance')
    plt.grid(True)
    plt.axhline(1, color='r', linestyle='--', label='1 second')
    plt.axhline(60, color='g', linestyle='--', label='1 minute')
    plt.legend()
    plt.savefig('diffusion_scaling.png', dpi=150)
```

### Julia Implementation

```julia
using Plots
using DifferentialEquations

# Physical constants
const R = 8.314       # J/(mol·K)
const F = 96485       # C/mol
const k_B = 1.38e-23  # J/K
const N_A = 6.02e23   # mol⁻¹

"""
    poiseuille_flow(ΔP, r, L, η)

Calculate volume flow through cylindrical tube.

# Arguments
- `ΔP`: Pressure difference (Pa)
- `r`: Tube radius (m)
- `L`: Tube length (m)
- `η`: Viscosity (Pa·s)

# Returns
- Volume flow rate (m³/s)
"""
function poiseuille_flow(ΔP, r, L, η)
    return (π * r^4 * ΔP) / (8 * η * L)
end

"""
    stokes_einstein(T, η, a)

Calculate diffusion coefficient for spherical particle.
"""
function stokes_einstein(T, η, a)
    return (k_B * T) / (6π * η * a)
end

"""
    nernst_potential(z, C_out, C_in; T=310)

Calculate Nernst equilibrium potential.
"""
function nernst_potential(z, C_out, C_in; T=310)
    return (R * T) / (z * F) * log(C_out / C_in)
end

"""
    diffusion_1d!(du, u, p, t)

1D diffusion equation for DifferentialEquations.jl

∂C/∂t = D × ∂²C/∂x²

Uses finite differences on grid.
"""
function diffusion_1d!(du, u, p, t)
    D, dx = p
    N = length(u)

    # Boundary conditions: no flux at edges
    du[1] = D * (u[2] - u[1]) / dx^2
    du[N] = D * (u[N-1] - u[N]) / dx^2

    # Interior points
    for i in 2:N-1
        du[i] = D * (u[i+1] - 2*u[i] + u[i-1]) / dx^2
    end
end

# Example: Simulate 1D diffusion
function run_diffusion_example()
    # Grid setup
    L = 1e-3  # 1 mm domain
    N = 100
    x = range(0, L, length=N)
    dx = L / (N-1)

    # Initial condition: point source at center
    u0 = zeros(N)
    u0[N÷2] = 1.0

    # Parameters
    D = 1e-9  # m²/s
    p = (D, dx)

    # Solve
    tspan = (0.0, 100.0)  # 100 seconds
    prob = ODEProblem(diffusion_1d!, u0, tspan, p)
    sol = solve(prob, Tsit5(), saveat=10.0)

    # Plot
    plt = plot(xlabel="Position (mm)", ylabel="Concentration (arb)",
               title="1D Diffusion Over Time")
    for (i, t) in enumerate(sol.t)
        plot!(plt, x*1e3, sol.u[i], label="t=$(t)s")
    end
    return plt
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the process**: Flow, diffusion, electrical, or combination?
2. **List known quantities** with units
3. **Select appropriate equation**
4. **Check dimensional consistency**
5. **Calculate and interpret**
6. **Validate reasonableness**

### Typical Problems

**Type 1: Flow calculations**
- Given: Pressure, dimensions, viscosity
- Find: Flow rate, resistance, or required pressure

**Type 2: Diffusion problems**
- Given: Distances, time, or concentrations
- Find: Diffusion time, steady-state profiles, or D values

**Type 3: Electrical problems**
- Given: Charges, distances, or potentials
- Find: Forces, fields, or capacitance

**Type 4: Thermodynamic problems**
- Given: Concentrations, temperatures, or ΔG°
- Find: ΔG, equilibrium constants, or spontaneity

## Key Relationships Summary

| Quantity | Driving Force | Conductance |
|----------|---------------|-------------|
| Volume flow | ΔP | 1/R_hydraulic |
| Current | ΔV | 1/R_electrical |
| Diffusive flux | ΔC | D/Δx |
| Heat flow | ΔT | k/Δx |

All follow the general pattern:
```
Flux = Conductance × Driving Force
```
