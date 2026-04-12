"""
Henry's Law - Gas Solubility Equation

Henry's law describes the solubility of gases in liquids at equilibrium.
Critical for understanding blood gas content and diffusion across
biological membranes.

C = k_H × P

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation A.51)
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_henrys_law(k_H: float, P: float) -> float:
    """
    Calculate dissolved gas concentration using Henry's law.

    Formula: C = k_H × P

    The concentration of dissolved gas is proportional to the
    partial pressure of the gas above the liquid.

    Parameters:
    -----------
    k_H : float - Henry's constant (mL gas / dL liquid / mmHg)
    P : float - Partial pressure of gas (mmHg)

    Returns:
    --------
    C : float - Concentration of dissolved gas (mL gas / dL liquid)

    Common Henry's constants at 37°C (mL/dL/mmHg):
    - Oxygen (O₂): 0.003
    - Carbon dioxide (CO₂): 0.067 (much more soluble)
    - Nitrogen (N₂): 0.0012
    - Carbon monoxide (CO): 0.0024
    """
    if P < 0:
        raise ValueError("Partial pressure cannot be negative")
    return k_H * P


def dissolved_oxygen(P_O2: float) -> float:
    """
    Calculate dissolved oxygen content in blood.

    Formula: [O₂]_dissolved = 0.003 × P_O2

    Parameters:
    -----------
    P_O2 : float - Partial pressure of oxygen (mmHg)

    Returns:
    --------
    C_O2 : float - Dissolved oxygen (mL O₂ / dL blood)

    Reference values:
    - Arterial P_O2 = 100 mmHg → 0.3 mL/dL dissolved
    - Venous P_O2 = 40 mmHg → 0.12 mL/dL dissolved
    - Total arterial O₂ ≈ 20 mL/dL (mostly hemoglobin-bound)
    """
    k_H_O2 = 0.003  # mL O₂/dL/mmHg at 37°C
    return compute_henrys_law(k_H_O2, P_O2)


def dissolved_co2(P_CO2: float) -> float:
    """
    Calculate dissolved CO₂ content in blood.

    Formula: [CO₂]_dissolved = 0.067 × P_CO2

    Parameters:
    -----------
    P_CO2 : float - Partial pressure of CO₂ (mmHg)

    Returns:
    --------
    C_CO2 : float - Dissolved CO₂ (mL CO₂ / dL blood)

    Note: CO₂ is ~22× more soluble than O₂
    At P_CO2 = 40 mmHg: [CO₂]_dissolved ≈ 2.7 mL/dL
    """
    k_H_CO2 = 0.067  # mL CO₂/dL/mmHg at 37°C
    return compute_henrys_law(k_H_CO2, P_CO2)


def dissolved_co2_mmol(P_CO2: float) -> float:
    """
    Calculate dissolved CO₂ in mmol/L (clinical units).

    Formula: [CO₂] = 0.03 × P_CO2 (mmol/L)

    Parameters:
    -----------
    P_CO2 : float - Partial pressure of CO₂ (mmHg)

    Returns:
    --------
    C_CO2 : float - Dissolved CO₂ (mmol/L)

    At P_CO2 = 40 mmHg: [CO₂] = 1.2 mmol/L
    Used in Henderson-Hasselbalch equation
    """
    solubility_coefficient = 0.03  # mmol/L/mmHg at 37°C
    return solubility_coefficient * P_CO2


def bunsen_coefficient(T: float, gas: str = 'O2') -> float:
    """
    Approximate Bunsen solubility coefficient at given temperature.

    Bunsen coefficient = mL gas (STP) dissolved per mL liquid per atm

    Parameters:
    -----------
    T : float - Temperature (°C)
    gas : str - Gas type ('O2', 'CO2', 'N2')

    Returns:
    --------
    alpha : float - Bunsen coefficient (mL gas/mL liquid/atm)

    Note: Solubility generally decreases with increasing temperature
    """
    # Approximate values at 37°C (simplified model)
    coefficients = {
        'O2': 0.024,   # mL/mL/atm at 37°C
        'CO2': 0.57,   # mL/mL/atm at 37°C (much higher)
        'N2': 0.012    # mL/mL/atm at 37°C
    }

    if gas not in coefficients:
        raise ValueError(f"Unknown gas: {gas}. Use 'O2', 'CO2', or 'N2'")

    # Temperature correction (solubility decreases ~2.5% per °C rise)
    alpha_37 = coefficients[gas]
    temp_factor = 1 - 0.025 * (T - 37)
    return alpha_37 * temp_factor


# Create and register equation
henrys_law_eq = create_equation(
    id="foundations.thermodynamics.henrys_law",
    name="Henry's Law - Gas Solubility",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C = k_H \times P",
    simplified="C = k_H × P",
    description="Dissolved gas concentration proportional to partial pressure",
    compute_func=compute_henrys_law,
    parameters=[
        Parameter(
            name="k_H",
            description="Henry's constant (solubility coefficient)",
            units="mL gas/dL/mmHg",
            symbol="k_H",
            physiological_range=(0.001, 0.1)  # Covers O₂ to CO₂ range
        ),
        Parameter(
            name="P",
            description="Partial pressure of gas",
            units="mmHg",
            symbol="P",
            physiological_range=(0.0, 760.0)
        ),
    ],
    depends_on=["respiratory.gas_exchange.partial_pressure"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.51"
    )
)
register_equation(henrys_law_eq)

# Export convenience alias
henrys_law = compute_henrys_law
