"""
Ideal Gas Law Equation

The ideal gas law relates pressure, volume, temperature, and amount of gas.
Fundamental to understanding gas behavior in physiology, including
respiratory gas volumes and blood gas analysis.

PV = nRT

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation A.50)
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation


def compute_ideal_gas_pressure(n: float, V: float, T: float = 310.0) -> float:
    """
    Calculate pressure using ideal gas law.

    Formula: P = nRT/V

    Parameters:
    -----------
    n : float - Amount of substance (mol)
    V : float - Volume (L)
    T : float - Absolute temperature (K, default 310 K = 37°C)

    Returns:
    --------
    P : float - Pressure (atm)

    Note: Uses R = 0.08206 L·atm/(mol·K) for pressure in atm
    """
    R_atm = 0.08206  # L·atm/(mol·K)
    if V <= 0:
        raise ValueError("Volume must be positive")
    return (n * R_atm * T) / V


def compute_ideal_gas_volume(n: float, P: float, T: float = 310.0) -> float:
    """
    Calculate volume using ideal gas law.

    Formula: V = nRT/P

    Parameters:
    -----------
    n : float - Amount of substance (mol)
    P : float - Pressure (atm)
    T : float - Absolute temperature (K, default 310 K = 37°C)

    Returns:
    --------
    V : float - Volume (L)
    """
    R_atm = 0.08206  # L·atm/(mol·K)
    if P <= 0:
        raise ValueError("Pressure must be positive")
    return (n * R_atm * T) / P


def compute_ideal_gas_moles(P: float, V: float, T: float = 310.0) -> float:
    """
    Calculate amount of substance using ideal gas law.

    Formula: n = PV/RT

    Parameters:
    -----------
    P : float - Pressure (atm)
    V : float - Volume (L)
    T : float - Absolute temperature (K, default 310 K = 37°C)

    Returns:
    --------
    n : float - Amount of substance (mol)
    """
    R_atm = 0.08206  # L·atm/(mol·K)
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return (P * V) / (R_atm * T)


def molar_volume_stp() -> float:
    """
    Return molar volume of ideal gas at STP (0°C, 1 atm).

    At STP: V_m = 22.414 L/mol

    Returns:
    --------
    V_m : float - Molar volume at STP (L/mol)
    """
    return 22.414


def molar_volume_btps() -> float:
    """
    Return molar volume of ideal gas at BTPS (37°C, 1 atm, saturated).

    At BTPS: V_m ≈ 25.44 L/mol

    Body Temperature (310 K), Pressure (1 atm), Saturated with water vapor

    Returns:
    --------
    V_m : float - Molar volume at BTPS (L/mol)
    """
    R_atm = 0.08206  # L·atm/(mol·K)
    T_body = 310.0  # K
    P_atm = 1.0  # atm
    return R_atm * T_body / P_atm


# Create and register equation
ideal_gas_law_eq = create_equation(
    id="foundations.thermodynamics.ideal_gas_law",
    name="Ideal Gas Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"PV = nRT",
    simplified="P = nRT/V",
    description="Relates pressure, volume, temperature, and moles of an ideal gas",
    compute_func=compute_ideal_gas_pressure,
    parameters=[
        Parameter(
            name="n",
            description="Amount of substance",
            units="mol",
            symbol="n",
            physiological_range=(0.0001, 100.0)  # mmol to large volumes
        ),
        Parameter(
            name="V",
            description="Volume",
            units="L",
            symbol="V",
            physiological_range=(0.001, 10.0)  # mL to TLC range
        ),
        Parameter(
            name="T",
            description="Absolute temperature",
            units="K",
            symbol="T",
            default_value=310.0,  # Body temperature
            physiological_range=(273.0, 330.0)  # 0°C to ~57°C
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.50"
    )
)
register_equation(ideal_gas_law_eq)

# Export convenience aliases
ideal_gas_pressure = compute_ideal_gas_pressure
ideal_gas_volume = compute_ideal_gas_volume
ideal_gas_moles = compute_ideal_gas_moles
