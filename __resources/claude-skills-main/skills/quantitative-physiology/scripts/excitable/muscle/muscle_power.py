"""
Muscle Mechanical Power Output

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def muscle_power(F: float, v: float) -> float:
    """
    Mechanical power output of muscle.

    Formula: P = F × v

    Maximum power occurs at approximately:
    F_opt ≈ 0.3 × F_0
    v_opt ≈ 0.3 × v_max
    P_max ≈ 0.1 × F_0 × v_max

    Parameters:
    -----------
    F : float - Force (N)
    v : float - Velocity (m/s)

    Returns:
    --------
    P : float - Power (W)
    """
    return F * v

# Create and register atomic equation
muscle_power_eq = create_equation(
    id="excitable.muscle.muscle_power",
    name="Muscle Mechanical Power",
    category=EquationCategory.EXCITABLE,
    latex=r"P = F \cdot v",
    simplified="P = F × v",
    description="Mechanical power output as product of force and velocity",
    compute_func=muscle_power,
    parameters=[
        Parameter(
            name="F",
            description="Force",
            units="N",
            symbol="F",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="v",
            description="Velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(muscle_power_eq)
