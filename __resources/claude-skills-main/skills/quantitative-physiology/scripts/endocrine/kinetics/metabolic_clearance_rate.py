"""
Metabolic clearance rate for hormones.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_mcr(production_rate: float, plasma_concentration: float) -> float:
    """
    Calculate metabolic clearance rate.

    Parameters
    ----------
    production_rate : float
        Hormone production rate (mass/time)
    plasma_concentration : float
        Steady-state plasma concentration (mass/volume)

    Returns
    -------
    float
        Metabolic clearance rate (volume/time)
    """
    return production_rate / plasma_concentration


# Create equation
mcr_equation = create_equation(
    id="endocrine.kinetics.metabolic_clearance_rate",
    name="Metabolic Clearance Rate",
    category=EquationCategory.ENDOCRINE,
    latex=r"MCR = \frac{\text{Production rate}}{\text{Plasma concentration}}",
    simplified="MCR = Production_rate / Plasma_conc",
    description="Metabolic clearance rate: volume of plasma completely cleared of hormone per unit time. "
                "Reflects the efficiency of hormone removal from circulation.",
    compute_func=compute_mcr,
    parameters=[
        Parameter(
            name="production_rate",
            description="Hormone production rate",
            units="μg/day or mg/day",
            symbol="P",
            physiological_range=(1e-3, 1e3)
        ),
        Parameter(
            name="plasma_concentration",
            description="Steady-state plasma concentration",
            units="μg/L or mg/L",
            symbol="C",
            physiological_range=(1e-6, 1e3)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(mcr_equation)
