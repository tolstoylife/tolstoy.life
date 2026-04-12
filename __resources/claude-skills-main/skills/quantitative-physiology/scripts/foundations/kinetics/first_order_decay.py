"""
First-Order Decay and Half-Life

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 17-18)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def first_order_decay(C_0: float, k: float, t: float) -> float:
    """
    Calculate concentration after first-order decay.

    Formula: C(t) = C_0 × e^(-kt)

    First-order decay describes processes where the rate of decay is
    proportional to the current amount. Fundamental for drug elimination,
    radioactive decay, and protein turnover.

    Parameters:
    -----------
    C_0 : float - Initial concentration (arbitrary units)
    k : float - Rate constant (1/s or 1/min)
    t : float - Time elapsed (s or min, matching k units)

    Returns:
    --------
    C : float - Concentration at time t (same units as C_0)
    """
    return C_0 * np.exp(-k * t)


def half_life_from_rate_constant(k: float) -> float:
    """
    Calculate half-life from first-order rate constant.

    Formula: t_1/2 = ln(2) / k = 0.693 / k

    The half-life is the time required for a quantity to decrease to
    half its initial value. Critical for drug dosing, clearance
    calculations, and metabolic turnover.

    Parameters:
    -----------
    k : float - Rate constant (1/s or 1/min)

    Returns:
    --------
    t_half : float - Half-life (s or min, matching k units)
    """
    return np.log(2) / k


def rate_constant_from_half_life(t_half: float) -> float:
    """
    Calculate rate constant from half-life.

    Formula: k = ln(2) / t_1/2 = 0.693 / t_1/2

    Parameters:
    -----------
    t_half : float - Half-life (s or min)

    Returns:
    --------
    k : float - Rate constant (1/s or 1/min, matching t_half units)
    """
    return np.log(2) / t_half


# Create and register first-order decay equation
first_order_decay_eq = create_equation(
    id="foundations.kinetics.first_order_decay",
    name="First-Order Decay",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C(t) = C_0 e^{-kt}",
    simplified="C(t) = C₀ × e^(-kt)",
    description="Exponential decay with rate proportional to current amount",
    compute_func=first_order_decay,
    parameters=[
        Parameter(
            name="C_0",
            description="Initial concentration",
            units="variable",
            symbol="C_0",
            physiological_range=(0.0, 1e6)
        ),
        Parameter(
            name="k",
            description="Rate constant",
            units="1/time",
            symbol="k",
            physiological_range=(1e-6, 100.0)  # Very slow to fast reactions
        ),
        Parameter(
            name="t",
            description="Time elapsed",
            units="time",
            symbol="t",
            physiological_range=(0.0, 1e6)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.17"
    )
)
register_equation(first_order_decay_eq)


# Create and register half-life equation
half_life_eq = create_equation(
    id="foundations.kinetics.half_life",
    name="Half-Life from Rate Constant",
    category=EquationCategory.FOUNDATIONS,
    latex=r"t_{1/2} = \frac{\ln 2}{k} = \frac{0.693}{k}",
    simplified="t₁/₂ = 0.693 / k",
    description="Time for quantity to decrease to half its initial value",
    compute_func=half_life_from_rate_constant,
    parameters=[
        Parameter(
            name="k",
            description="Rate constant",
            units="1/time",
            symbol="k",
            physiological_range=(1e-6, 100.0)
        ),
    ],
    depends_on=["foundations.kinetics.first_order_decay"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.18"
    )
)
register_equation(half_life_eq)
