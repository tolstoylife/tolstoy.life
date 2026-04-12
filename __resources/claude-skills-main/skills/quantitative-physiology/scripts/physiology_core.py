#!/usr/bin/env python3
"""
Quantitative Physiology Core Computational Models

This module provides foundational equations and calculations for quantitative
human physiology. Extract from the Quantitative Human Physiology skill system.

Source: Feher JJ. Quantitative Human Physiology: An Introduction, 3rd Edition.
"""

import numpy as np
from typing import Union, Tuple, Optional
from dataclasses import dataclass

# Physical Constants
R = 8.314       # Gas constant, J/(mol·K)
F = 96485       # Faraday constant, C/mol
k_B = 1.38e-23  # Boltzmann constant, J/K
N_A = 6.02e23   # Avogadro's number, mol⁻¹
BODY_TEMP = 310 # Body temperature, K (37°C)


# =============================================================================
# TRANSPORT EQUATIONS
# =============================================================================

def poiseuille_flow(delta_P: float, r: float, L: float, eta: float) -> float:
    """
    Calculate laminar flow through cylindrical tube (Poiseuille's Law).

    Q = (π × r⁴ × ΔP) / (8 × η × L)

    Parameters
    ----------
    delta_P : float
        Pressure difference (Pa)
    r : float
        Tube radius (m)
    L : float
        Tube length (m)
    eta : float
        Fluid viscosity (Pa·s)

    Returns
    -------
    float
        Volume flow rate (m³/s)

    Notes
    -----
    Flow ∝ r⁴: Doubling radius increases flow 16-fold.
    Clinical relevance: Vasoconstriction/dilation effects on blood flow.
    """
    return (np.pi * r**4 * delta_P) / (8 * eta * L)


def hydraulic_resistance(r: float, L: float, eta: float) -> float:
    """
    Calculate hydraulic resistance of cylindrical tube.

    R = 8ηL / (πr⁴)

    Parameters
    ----------
    r : float
        Tube radius (m)
    L : float
        Tube length (m)
    eta : float
        Fluid viscosity (Pa·s)

    Returns
    -------
    float
        Hydraulic resistance (Pa·s/m³)
    """
    return (8 * eta * L) / (np.pi * r**4)


def laplace_cylinder(T: float, r: float) -> float:
    """
    Transmural pressure for cylindrical vessel (Law of Laplace).

    ΔP = T/r

    Parameters
    ----------
    T : float
        Wall tension (N/m)
    r : float
        Vessel radius (m)

    Returns
    -------
    float
        Transmural pressure (Pa)

    Notes
    -----
    Clinical: Aneurysms - larger radius requires more wall tension.
    """
    return T / r


def laplace_sphere(T: float, r: float) -> float:
    """
    Transmural pressure for spherical structure (Law of Laplace).

    ΔP = 2T/r

    Parameters
    ----------
    T : float
        Surface tension (N/m)
    r : float
        Sphere radius (m)

    Returns
    -------
    float
        Transmural pressure (Pa)

    Notes
    -----
    Clinical: Alveoli - surfactant reduces T to prevent collapse.
    """
    return 2 * T / r


# =============================================================================
# DIFFUSION EQUATIONS
# =============================================================================

def diffusion_coefficient(T: float, eta: float, a: float) -> float:
    """
    Stokes-Einstein diffusion coefficient for spherical particle.

    D = kT / (6πηa)

    Parameters
    ----------
    T : float
        Temperature (K)
    eta : float
        Solvent viscosity (Pa·s)
    a : float
        Particle radius (m)

    Returns
    -------
    float
        Diffusion coefficient (m²/s)
    """
    return (k_B * T) / (6 * np.pi * eta * a)


def diffusion_time(x: float, D: float) -> float:
    """
    Characteristic time for diffusion over distance x.

    t = x² / (2D)

    Parameters
    ----------
    x : float
        Distance (m)
    D : float
        Diffusion coefficient (m²/s)

    Returns
    -------
    float
        Diffusion time (s)

    Notes
    -----
    Key insight: Diffusion time scales with square of distance.
    - 1 μm: ~0.5 ms
    - 1 mm: ~500 s (~8 min)
    - 1 cm: ~50,000 s (~14 hours)
    """
    return x**2 / (2 * D)


def fick_flux(D: float, dC_dx: float) -> float:
    """
    Diffusive flux (Fick's First Law).

    J = -D × (∂C/∂x)

    Parameters
    ----------
    D : float
        Diffusion coefficient (m²/s)
    dC_dx : float
        Concentration gradient (mol/m⁴)

    Returns
    -------
    float
        Solute flux (mol/(m²·s))
    """
    return -D * dC_dx


# =============================================================================
# MEMBRANE TRANSPORT
# =============================================================================

def permeability_coefficient(D: float, K: float, delta: float) -> float:
    """
    Membrane permeability coefficient.

    P = D × K / δ

    Parameters
    ----------
    D : float
        Diffusion coefficient in membrane (m²/s)
    K : float
        Partition coefficient (dimensionless)
    delta : float
        Membrane thickness (m)

    Returns
    -------
    float
        Permeability coefficient (m/s)
    """
    return (D * K) / delta


def passive_flux(P: float, C_out: float, C_in: float) -> float:
    """
    Passive solute flux across membrane.

    J = P × (C_out - C_in)

    Parameters
    ----------
    P : float
        Permeability coefficient (m/s)
    C_out : float
        External concentration (mol/m³)
    C_in : float
        Internal concentration (mol/m³)

    Returns
    -------
    float
        Solute flux (mol/(m²·s))
    """
    return P * (C_out - C_in)


def nernst_potential(z: int, C_out: float, C_in: float, T: float = BODY_TEMP) -> float:
    """
    Nernst equilibrium potential for an ion.

    E = (RT/zF) × ln(C_out/C_in)

    Parameters
    ----------
    z : int
        Ion valence (e.g., +1 for Na⁺, -1 for Cl⁻)
    C_out : float
        Extracellular concentration
    C_in : float
        Intracellular concentration
    T : float, optional
        Temperature in K (default: 310 K = 37°C)

    Returns
    -------
    float
        Equilibrium potential (V)

    Notes
    -----
    At 37°C: E ≈ (61.5 mV/z) × log₁₀(C_out/C_in)

    Typical values:
    - E_K ≈ -90 mV (K⁺: 140 mM in, 4 mM out)
    - E_Na ≈ +67 mV (Na⁺: 10 mM in, 145 mM out)
    - E_Cl ≈ -89 mV (Cl⁻: 10 mM in, 110 mM out)
    """
    return (R * T) / (z * F) * np.log(C_out / C_in)


def goldman_hodgkin_katz(
    P_K: float, P_Na: float, P_Cl: float,
    K_o: float, K_i: float,
    Na_o: float, Na_i: float,
    Cl_o: float, Cl_i: float,
    T: float = BODY_TEMP
) -> float:
    """
    Goldman-Hodgkin-Katz equation for resting membrane potential.

    V_m = (RT/F) × ln[(P_K×K_o + P_Na×Na_o + P_Cl×Cl_i) /
                       (P_K×K_i + P_Na×Na_i + P_Cl×Cl_o)]

    Parameters
    ----------
    P_K, P_Na, P_Cl : float
        Relative permeabilities (dimensionless ratios)
    K_o, K_i : float
        Extracellular and intracellular [K⁺]
    Na_o, Na_i : float
        Extracellular and intracellular [Na⁺]
    Cl_o, Cl_i : float
        Extracellular and intracellular [Cl⁻]
    T : float, optional
        Temperature (K), default 310 K

    Returns
    -------
    float
        Membrane potential (V)

    Notes
    -----
    Typical resting permeability ratios: P_K : P_Na : P_Cl ≈ 1 : 0.04 : 0.45
    """
    numerator = P_K * K_o + P_Na * Na_o + P_Cl * Cl_i
    denominator = P_K * K_i + P_Na * Na_i + P_Cl * Cl_o
    return (R * T / F) * np.log(numerator / denominator)


def osmotic_pressure(sigma: float, C: float, T: float = BODY_TEMP) -> float:
    """
    Van't Hoff equation for osmotic pressure.

    π = σ × C × RT

    Parameters
    ----------
    sigma : float
        Reflection coefficient (0 to 1)
    C : float
        Solute concentration (mol/m³)
    T : float, optional
        Temperature (K), default 310 K

    Returns
    -------
    float
        Osmotic pressure (Pa)
    """
    return sigma * C * R * T


# =============================================================================
# ENZYME KINETICS
# =============================================================================

def michaelis_menten(S: float, J_max: float, K_m: float) -> float:
    """
    Michaelis-Menten enzyme kinetics.

    J = J_max × [S] / (K_m + [S])

    Parameters
    ----------
    S : float
        Substrate concentration
    J_max : float
        Maximum reaction velocity
    K_m : float
        Michaelis constant (substrate concentration at half-maximal velocity)

    Returns
    -------
    float
        Reaction velocity

    Notes
    -----
    At [S] = K_m: J = J_max/2
    At [S] >> K_m: J → J_max (saturation)
    At [S] << K_m: J ≈ (J_max/K_m) × [S] (first-order)
    """
    return J_max * S / (K_m + S)


def hill_equation(S: float, J_max: float, K_half: float, n: float) -> float:
    """
    Hill equation for cooperative binding.

    J = J_max × [S]ⁿ / (K₀.₅ⁿ + [S]ⁿ)

    Parameters
    ----------
    S : float
        Substrate/ligand concentration
    J_max : float
        Maximum response
    K_half : float
        Concentration at half-maximal response
    n : float
        Hill coefficient (cooperativity)

    Returns
    -------
    float
        Response magnitude

    Notes
    -----
    n > 1: Positive cooperativity (sigmoidal curve)
    n = 1: No cooperativity (hyperbolic, = Michaelis-Menten)
    n < 1: Negative cooperativity

    Hemoglobin O₂ binding: n ≈ 2.7, P₅₀ ≈ 26 mmHg
    """
    return J_max * (S**n) / (K_half**n + S**n)


# =============================================================================
# THERMODYNAMICS
# =============================================================================

def gibbs_free_energy(delta_G0: float, Q: float, T: float = BODY_TEMP) -> float:
    """
    Actual Gibbs free energy change.

    ΔG = ΔG° + RT × ln(Q)

    Parameters
    ----------
    delta_G0 : float
        Standard free energy change (J/mol)
    Q : float
        Reaction quotient ([products]/[reactants])
    T : float, optional
        Temperature (K), default 310 K

    Returns
    -------
    float
        Free energy change (J/mol)

    Notes
    -----
    ΔG < 0: Spontaneous (exergonic)
    ΔG > 0: Non-spontaneous (endergonic)
    ΔG = 0: Equilibrium

    ATP hydrolysis: ΔG° ≈ -30.5 kJ/mol, ΔG_cellular ≈ -54 kJ/mol
    """
    return delta_G0 + R * T * np.log(Q)


def equilibrium_constant(delta_G0: float, T: float = BODY_TEMP) -> float:
    """
    Calculate equilibrium constant from standard free energy.

    K_eq = exp(-ΔG°/RT)

    Parameters
    ----------
    delta_G0 : float
        Standard free energy change (J/mol)
    T : float, optional
        Temperature (K), default 310 K

    Returns
    -------
    float
        Equilibrium constant
    """
    return np.exp(-delta_G0 / (R * T))


def arrhenius_rate(A: float, E_a: float, T: float) -> float:
    """
    Arrhenius equation for temperature-dependent rate constant.

    k = A × exp(-E_a/RT)

    Parameters
    ----------
    A : float
        Pre-exponential factor (frequency factor)
    E_a : float
        Activation energy (J/mol)
    T : float
        Temperature (K)

    Returns
    -------
    float
        Rate constant
    """
    return A * np.exp(-E_a / (R * T))


# =============================================================================
# FIRST-ORDER KINETICS
# =============================================================================

def first_order_decay(t: float, A0: float, k: float) -> float:
    """
    First-order decay kinetics.

    A(t) = A₀ × e^(-kt)

    Parameters
    ----------
    t : float
        Time
    A0 : float
        Initial amount
    k : float
        Rate constant (1/time)

    Returns
    -------
    float
        Amount remaining at time t
    """
    return A0 * np.exp(-k * t)


def half_life(k: float) -> float:
    """
    Calculate half-life from rate constant.

    t₁/₂ = ln(2)/k ≈ 0.693/k

    Parameters
    ----------
    k : float
        Rate constant (1/time)

    Returns
    -------
    float
        Half-life (same units as 1/k)
    """
    return np.log(2) / k


# =============================================================================
# CARDIOVASCULAR EQUATIONS
# =============================================================================

def cardiac_output(heart_rate: float, stroke_volume: float) -> float:
    """
    Cardiac output calculation.

    CO = HR × SV

    Parameters
    ----------
    heart_rate : float
        Heart rate (beats/min)
    stroke_volume : float
        Stroke volume (mL)

    Returns
    -------
    float
        Cardiac output (mL/min)

    Notes
    -----
    Normal resting: CO ≈ 5000 mL/min (70 bpm × 70 mL)
    """
    return heart_rate * stroke_volume


def ejection_fraction(edv: float, esv: float) -> float:
    """
    Ventricular ejection fraction.

    EF = (EDV - ESV) / EDV × 100

    Parameters
    ----------
    edv : float
        End-diastolic volume (mL)
    esv : float
        End-systolic volume (mL)

    Returns
    -------
    float
        Ejection fraction (%)

    Notes
    -----
    Normal: 55-70%
    Heart failure with reduced EF: <40%
    """
    return ((edv - esv) / edv) * 100


def mean_arterial_pressure(sbp: float, dbp: float) -> float:
    """
    Mean arterial pressure estimation.

    MAP = DBP + (1/3) × PP = DBP + (1/3) × (SBP - DBP)

    Parameters
    ----------
    sbp : float
        Systolic blood pressure (mmHg)
    dbp : float
        Diastolic blood pressure (mmHg)

    Returns
    -------
    float
        Mean arterial pressure (mmHg)

    Notes
    -----
    Normal MAP: 70-100 mmHg
    Formula assumes 1/3 systole, 2/3 diastole in cardiac cycle.
    """
    return dbp + (sbp - dbp) / 3


def total_peripheral_resistance(map_pressure: float, cvp: float, co: float) -> float:
    """
    Total peripheral resistance.

    TPR = (MAP - CVP) / CO

    Parameters
    ----------
    map_pressure : float
        Mean arterial pressure (mmHg)
    cvp : float
        Central venous pressure (mmHg)
    co : float
        Cardiac output (L/min)

    Returns
    -------
    float
        TPR in Wood units (mmHg/(L/min))

    Notes
    -----
    Normal: 900-1200 dyn·s/cm⁵ or 10-15 Wood units
    To convert: 1 Wood unit = 80 dyn·s/cm⁵
    """
    return (map_pressure - cvp) / co


def pulse_wave_velocity(E: float, h: float, rho: float, d: float) -> float:
    """
    Moens-Korteweg equation for pulse wave velocity.

    PWV = √(E × h / (ρ × d))

    Parameters
    ----------
    E : float
        Elastic modulus of vessel wall (Pa)
    h : float
        Wall thickness (m)
    rho : float
        Blood density (kg/m³), typically ~1060
    d : float
        Vessel diameter (m)

    Returns
    -------
    float
        Pulse wave velocity (m/s)

    Notes
    -----
    Normal aortic PWV: 4-6 m/s (young), 8-12 m/s (elderly)
    Higher PWV indicates stiffer arteries.
    """
    return np.sqrt((E * h) / (rho * d))


# =============================================================================
# RESPIRATORY EQUATIONS
# =============================================================================

def alveolar_gas_equation(
    P_i_O2: float,
    P_a_CO2: float,
    R: float = 0.8
) -> float:
    """
    Alveolar gas equation for alveolar O₂ partial pressure.

    P_A_O2 = P_i_O2 - P_a_CO2/R

    Parameters
    ----------
    P_i_O2 : float
        Inspired O₂ partial pressure (mmHg)
    P_a_CO2 : float
        Arterial CO₂ partial pressure (mmHg)
    R : float, optional
        Respiratory quotient (default 0.8)

    Returns
    -------
    float
        Alveolar O₂ partial pressure (mmHg)

    Notes
    -----
    At sea level breathing room air:
    P_i_O2 = 0.21 × (760 - 47) ≈ 150 mmHg
    Normal P_A_O2 ≈ 100 mmHg
    """
    return P_i_O2 - P_a_CO2 / R


def oxygen_content(Hb: float, S_O2: float, P_O2: float) -> float:
    """
    Blood oxygen content.

    C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)

    Parameters
    ----------
    Hb : float
        Hemoglobin concentration (g/dL)
    S_O2 : float
        Oxygen saturation (fraction, 0-1)
    P_O2 : float
        Oxygen partial pressure (mmHg)

    Returns
    -------
    float
        Oxygen content (mL O₂/dL blood)

    Notes
    -----
    1.34 mL O₂ per gram Hb (Hüfner's constant)
    0.003 mL O₂ per dL per mmHg (dissolved O₂)
    Normal arterial: ~20 mL O₂/dL
    """
    return (1.34 * Hb * S_O2) + (0.003 * P_O2)


def henderson_hasselbalch(HCO3: float, P_CO2: float) -> float:
    """
    Henderson-Hasselbalch equation for blood pH.

    pH = 6.1 + log([HCO₃⁻] / (0.03 × P_CO2))

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)
    P_CO2 : float
        CO₂ partial pressure (mmHg)

    Returns
    -------
    float
        Blood pH

    Notes
    -----
    Normal values: pH 7.40, [HCO₃⁻] 24 mEq/L, P_CO2 40 mmHg
    pK_a of carbonic acid = 6.1
    0.03 = solubility coefficient of CO₂ in blood
    """
    return 6.1 + np.log10(HCO3 / (0.03 * P_CO2))


# =============================================================================
# RENAL EQUATIONS
# =============================================================================

def clearance(U_x: float, V_dot: float, P_x: float) -> float:
    """
    Renal clearance calculation.

    C_x = (U_x × V̇) / P_x

    Parameters
    ----------
    U_x : float
        Urine concentration of substance x
    V_dot : float
        Urine flow rate (mL/min)
    P_x : float
        Plasma concentration of substance x

    Returns
    -------
    float
        Clearance (mL/min)

    Notes
    -----
    Inulin clearance = GFR (gold standard)
    Creatinine clearance ≈ GFR (clinical approximation)
    PAH clearance ≈ RPF (at low concentrations)
    """
    return (U_x * V_dot) / P_x


def gfr_estimate(
    age: float,
    weight: float,
    serum_creatinine: float,
    female: bool = False
) -> float:
    """
    Cockcroft-Gault equation for creatinine clearance.

    C_Cr = [(140 - age) × weight] / (72 × S_Cr) × [0.85 if female]

    Parameters
    ----------
    age : float
        Patient age (years)
    weight : float
        Body weight (kg)
    serum_creatinine : float
        Serum creatinine (mg/dL)
    female : bool, optional
        True if female patient (default False)

    Returns
    -------
    float
        Estimated creatinine clearance (mL/min)

    Notes
    -----
    Normal GFR: ~125 mL/min = 180 L/day
    CKD staging based on GFR categories.
    """
    c_cr = ((140 - age) * weight) / (72 * serum_creatinine)
    if female:
        c_cr *= 0.85
    return c_cr


def filtered_load(gfr: float, P_x: float) -> float:
    """
    Calculate filtered load of a substance.

    Filtered Load = GFR × P_x

    Parameters
    ----------
    gfr : float
        Glomerular filtration rate (mL/min)
    P_x : float
        Plasma concentration

    Returns
    -------
    float
        Filtered load (amount/min)

    Notes
    -----
    Example: Glucose filtered load = 125 mL/min × 100 mg/dL = 180 g/day
    """
    return gfr * P_x


def free_water_clearance(V_dot: float, C_osm: float) -> float:
    """
    Free water clearance.

    C_H2O = V̇ - C_osm

    Parameters
    ----------
    V_dot : float
        Urine flow rate (mL/min)
    C_osm : float
        Osmolar clearance (mL/min)

    Returns
    -------
    float
        Free water clearance (mL/min)

    Notes
    -----
    C_H2O > 0: Dilute urine (water excretion)
    C_H2O < 0: Concentrated urine (water retention)
    C_H2O = 0: Iso-osmotic urine
    """
    return V_dot - C_osm


if __name__ == "__main__":
    # Example calculations
    print("=== Quantitative Physiology Core Examples ===\n")

    # Nernst potentials
    print("Nernst Equilibrium Potentials (37°C):")
    E_K = nernst_potential(1, 4, 140) * 1000  # mV
    E_Na = nernst_potential(1, 145, 10) * 1000
    E_Cl = nernst_potential(-1, 110, 10) * 1000
    print(f"  E_K  = {E_K:.1f} mV")
    print(f"  E_Na = {E_Na:.1f} mV")
    print(f"  E_Cl = {E_Cl:.1f} mV")

    # GHK equation
    V_m = goldman_hodgkin_katz(
        P_K=1, P_Na=0.04, P_Cl=0.45,
        K_o=4, K_i=140,
        Na_o=145, Na_i=10,
        Cl_o=110, Cl_i=10
    ) * 1000
    print(f"\nResting membrane potential (GHK): {V_m:.1f} mV")

    # Diffusion time
    print("\nDiffusion times (D = 10⁻⁹ m²/s):")
    D = 1e-9
    for x, label in [(1e-6, "1 μm"), (1e-3, "1 mm"), (1e-2, "1 cm")]:
        t = diffusion_time(x, D)
        print(f"  {label}: {t:.2g} seconds")

    # Henderson-Hasselbalch
    pH = henderson_hasselbalch(24, 40)
    print(f"\nBlood pH (normal): {pH:.2f}")
