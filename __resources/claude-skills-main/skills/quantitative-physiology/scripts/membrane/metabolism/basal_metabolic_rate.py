"""
Basal Metabolic Rate - Kleiber's law for metabolic scaling

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_basal_metabolic_rate(M: float) -> float:
    """
    Calculate basal metabolic rate using Kleiber's law.

    Formula: BMR ≈ 70 × M^0.75

    This is an allometric scaling law showing BMR scales with body mass
    to the 3/4 power across species.

    Parameters:
    -----------
    M : float
        Body mass (kg)

    Returns:
    --------
    BMR : float
        Basal metabolic rate (kcal/day)

    Examples:
        70 kg human: BMR ≈ 1680 kcal/day
        5 kg cat: BMR ≈ 260 kcal/day
        500 kg horse: BMR ≈ 7400 kcal/day

    Notes:
        The 3/4 power law is observed across 27 orders of magnitude
        in body size, from bacteria to whales.
    """
    return 70 * M**0.75


# Create and register atomic equation
basal_metabolic_rate = create_equation(
    id="membrane.metabolism.basal_metabolic_rate",
    name="Basal Metabolic Rate (Kleiber's Law)",
    category=EquationCategory.MEMBRANE,
    latex=r"BMR \approx 70 \cdot M^{0.75}",
    simplified="BMR = 70 * M^0.75",
    description="Allometric scaling of basal metabolic rate with body mass (Kleiber's law).",
    compute_func=compute_basal_metabolic_rate,
    parameters=[
        Parameter(
            name="M",
            description="Body mass",
            units="kg",
            symbol="M",
            default_value=None,
            physiological_range=(0.001, 100000.0)  # 1g to 100 tons
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(basal_metabolic_rate)
