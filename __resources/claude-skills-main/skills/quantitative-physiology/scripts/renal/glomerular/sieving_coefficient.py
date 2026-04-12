"""
Sieving Coefficient - Glomerular Filtration Selectivity

The sieving coefficient (θ) quantifies the selectivity of glomerular filtration
for a given solute based on its size and charge relative to the filtration barrier.

θ = 1.0: Freely filtered (like water, small solutes)
θ = 0.0: Not filtered (large proteins, albumin normally)
0 < θ < 1: Partially filtered

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation A.119)
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_sieving_coefficient(C_f: float, C_p: float) -> float:
    """
    Calculate sieving coefficient from filtrate and plasma concentrations.

    Formula: θ = C_f / C_p

    The sieving coefficient indicates how easily a solute passes through
    the glomerular filtration barrier:
    - θ = 1: Freely filtered (inulin, creatinine, small ions)
    - θ ≈ 0: Not filtered (albumin, large proteins)
    - θ = 0.003 (albumin, minimal filtration)
    - θ = 0.75 (myoglobin, partial filtration)

    Parameters:
    -----------
    C_f : float - Concentration in filtrate (any concentration units)
    C_p : float - Concentration in plasma (same units as C_f)

    Returns:
    --------
    theta : float - Sieving coefficient (dimensionless, 0 to 1)

    Clinical relevance:
    - Proteinuria indicates increased albumin sieving (damaged barrier)
    - Sieving depends on molecular radius, charge, and shape
    - Glomerular basement membrane and podocyte slits determine selectivity
    """
    if C_p <= 0:
        raise ValueError("Plasma concentration must be positive")
    return C_f / C_p


def fractional_clearance(clearance_x: float, gfr: float) -> float:
    """
    Calculate fractional clearance (equivalent to sieving for freely filtered).

    For a substance that is only filtered (no secretion/reabsorption),
    fractional clearance equals sieving coefficient.

    Parameters:
    -----------
    clearance_x : float - Clearance of substance X (mL/min)
    gfr : float - Glomerular filtration rate (mL/min)

    Returns:
    --------
    theta : float - Fractional clearance (dimensionless)
    """
    if gfr <= 0:
        raise ValueError("GFR must be positive")
    return clearance_x / gfr


def sieving_from_radius(molecular_radius: float, pore_radius: float = 4.0) -> float:
    """
    Estimate sieving coefficient from molecular radius using hindered transport.

    Simplified model: θ ≈ (1 - r/R)² for r < R, else 0

    More accurate models include electrostatic effects and fiber matrix theory.

    Parameters:
    -----------
    molecular_radius : float - Molecular radius (nm)
    pore_radius : float - Effective pore radius (nm, default 4.0 nm for GBM)

    Returns:
    --------
    theta : float - Estimated sieving coefficient

    Reference values:
    - Water: r ≈ 0.14 nm, θ ≈ 1.0
    - Glucose: r ≈ 0.4 nm, θ ≈ 1.0
    - Inulin: r ≈ 1.4 nm, θ ≈ 1.0
    - Myoglobin: r ≈ 2.0 nm, θ ≈ 0.75
    - Hemoglobin: r ≈ 3.2 nm, θ ≈ 0.03
    - Albumin: r ≈ 3.6 nm, θ ≈ 0.003 (charge-restricted)
    """
    if molecular_radius >= pore_radius:
        return 0.0
    ratio = molecular_radius / pore_radius
    return (1 - ratio) ** 2


def albumin_sieving_pathological(normal_theta: float = 0.003,
                                  damage_factor: float = 1.0) -> float:
    """
    Calculate pathological albumin sieving coefficient.

    Normal albumin sieving is ~0.003 (very low).
    In nephrotic syndrome, damage increases sieving dramatically.

    Parameters:
    -----------
    normal_theta : float - Normal sieving coefficient (default 0.003)
    damage_factor : float - Damage multiplier (1.0 = normal, >1 = damaged)

    Returns:
    --------
    theta : float - Pathological sieving coefficient

    Clinical thresholds:
    - θ < 0.01: Normal
    - θ = 0.01-0.1: Microalbuminuria
    - θ > 0.1: Overt proteinuria (nephrotic if massive)
    """
    theta = normal_theta * damage_factor
    return min(theta, 1.0)  # Cannot exceed 1


# Create and register equation
sieving_coefficient_eq = create_equation(
    id="renal.glomerular.sieving_coefficient",
    name="Glomerular Sieving Coefficient",
    category=EquationCategory.RENAL,
    latex=r"\theta = \frac{C_f}{C_p}",
    simplified="θ = C_f / C_p",
    description="Ratio of filtrate to plasma concentration, quantifying glomerular permeability",
    compute_func=compute_sieving_coefficient,
    parameters=[
        Parameter(
            name="C_f",
            description="Concentration in glomerular filtrate",
            units="mM or mg/dL",
            symbol="C_f",
            physiological_range=(0.0, 200.0)  # Varies by solute
        ),
        Parameter(
            name="C_p",
            description="Concentration in plasma",
            units="mM or mg/dL",
            symbol="C_p",
            physiological_range=(0.001, 200.0)
        ),
    ],
    depends_on=["renal.glomerular.net_filtration_pressure"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2",
        textbook_equation_number="A.119"
    )
)
register_equation(sieving_coefficient_eq)

# Export convenience alias
sieving_coefficient = compute_sieving_coefficient
