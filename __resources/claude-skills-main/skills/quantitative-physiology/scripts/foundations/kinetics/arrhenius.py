"""
Arrhenius Equation for Temperature Dependence of Reaction Rates

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation 19)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def arrhenius_rate(A: float, E_a: float, T: float,
                   R: float = 8.314) -> float:
    """
    Calculate reaction rate constant using Arrhenius equation.

    Formula: k = A × e^(-E_a / RT)

    The Arrhenius equation describes how reaction rate depends on
    temperature. Important for understanding enzyme kinetics,
    metabolic rate changes with fever, and Q10 temperature coefficients.

    Parameters:
    -----------
    A : float - Pre-exponential (frequency) factor (1/s or appropriate units)
    E_a : float - Activation energy (J/mol)
    T : float - Absolute temperature (K)
    R : float - Gas constant (J/(mol·K)), default 8.314

    Returns:
    --------
    k : float - Rate constant (same units as A)
    """
    return A * np.exp(-E_a / (R * T))


def q10_from_arrhenius(E_a: float, T: float = 310.0,
                        R: float = 8.314) -> float:
    """
    Calculate Q10 temperature coefficient from activation energy.

    Q10 is the factor by which reaction rate increases for a 10°C rise.

    Formula: Q10 = e^(10 × E_a / (R × T × (T+10)))

    Parameters:
    -----------
    E_a : float - Activation energy (J/mol)
    T : float - Reference temperature (K), default 310 (37°C)
    R : float - Gas constant (J/(mol·K)), default 8.314

    Returns:
    --------
    Q10 : float - Temperature coefficient (dimensionless)
    """
    return np.exp(10 * E_a / (R * T * (T + 10)))


# Create and register Arrhenius equation
arrhenius_eq = create_equation(
    id="foundations.kinetics.arrhenius",
    name="Arrhenius Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"k = A e^{-E_a/RT}",
    simplified="k = A × e^(-Eₐ / RT)",
    description="Temperature dependence of reaction rate constants",
    compute_func=arrhenius_rate,
    parameters=[
        Parameter(
            name="A",
            description="Pre-exponential (frequency) factor",
            units="1/s",
            symbol="A",
            physiological_range=(1e6, 1e15)  # Typical enzyme range
        ),
        Parameter(
            name="E_a",
            description="Activation energy",
            units="J/mol",
            symbol="E_a",
            physiological_range=(20000.0, 100000.0)  # 20-100 kJ/mol typical
        ),
        Parameter(
            name="T",
            description="Absolute temperature",
            units="K",
            symbol="T",
            default_value=310.0,  # Body temperature
            physiological_range=(273.0, 323.0)  # 0°C to 50°C
        ),
        PHYSICAL_CONSTANTS['R'],
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.19"
    )
)
register_equation(arrhenius_eq)
