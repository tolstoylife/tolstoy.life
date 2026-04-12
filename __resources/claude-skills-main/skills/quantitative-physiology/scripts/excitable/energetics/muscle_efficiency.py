"""
Muscle Mechanical Efficiency

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def muscle_efficiency(P: float, heat_rate: float) -> float:
    """
    Mechanical efficiency of muscle contraction.

    Formula: η = Mechanical work / Total energy = P / (P + Heat rate)

    Maximum efficiency is approximately 25-40% in skeletal muscle.

    Parameters:
    -----------
    P : float - Mechanical power output (W)
    heat_rate : float - Heat production rate (W)

    Returns:
    --------
    eta : float - Efficiency (dimensionless, 0-1)
    """
    total_energy = P + heat_rate
    if total_energy > 0:
        return P / total_energy
    else:
        return 0.0

# Create and register atomic equation
muscle_efficiency_eq = create_equation(
    id="excitable.energetics.muscle_efficiency",
    name="Muscle Mechanical Efficiency",
    category=EquationCategory.EXCITABLE,
    latex=r"\eta = \frac{P}{P + \dot{Q}}",
    simplified="η = P / (P + Heat rate)",
    description="Ratio of mechanical work to total energy expenditure",
    compute_func=muscle_efficiency,
    parameters=[
        Parameter(
            name="P",
            description="Mechanical power output",
            units="W",
            symbol="P",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="heat_rate",
            description="Heat production rate",
            units="W",
            symbol=r"\dot{Q}",
            physiological_range=(0.0, 2000.0)
        ),
    ],
    depends_on=["excitable.muscle.muscle_power"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(muscle_efficiency_eq)
