"""
Hill Force-Velocity Relationship

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def hill_force_velocity(F_0: float, a: float, b: float,
                        F: float = None, v: float = None) -> float:
    """
    Hill force-velocity relationship for muscle contraction.

    Formula: (F + a)(v + b) = (F_0 + a) × b
    Or equivalently: v = b × (F_0 - F) / (F + a)

    This hyperbolic relationship describes how force and velocity
    are inversely related during muscle shortening.

    Parameters:
    -----------
    F_0 : float - Isometric force (maximum force at v=0) (N)
    a : float - Hill constant (N)
    b : float - Hill constant (m/s)
    F : float - Force (N) - optional if computing v, default: None
    v : float - Velocity (m/s) - optional if computing F, default: None

    Returns:
    --------
    v or F : float - Velocity (m/s) or Force (N) depending on input
    """
    if F is not None:
        # Calculate velocity from force
        return b * (F_0 - F) / (F + a)
    elif v is not None:
        # Calculate force from velocity
        return (F_0 * b - a * v) / (v + b)
    else:
        raise ValueError("Must provide either F or v")

# Create and register atomic equation
hill_force_velocity_eq = create_equation(
    id="excitable.muscle.hill_force_velocity",
    name="Hill Force-Velocity Relationship",
    category=EquationCategory.EXCITABLE,
    latex=r"(F + a)(v + b) = (F_0 + a)b",
    simplified="(F + a)(v + b) = (F_0 + a) × b",
    description="Hyperbolic relationship between muscle force and shortening velocity",
    compute_func=hill_force_velocity,
    parameters=[
        Parameter(
            name="F_0",
            description="Isometric force (maximum force)",
            units="N",
            symbol="F_0",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="a",
            description="Hill constant (force parameter)",
            units="N",
            symbol="a",
            physiological_range=(0.0, 5000.0)
        ),
        Parameter(
            name="b",
            description="Hill constant (velocity parameter)",
            units="m/s",
            symbol="b",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="F",
            description="Force (for computing velocity)",
            units="N",
            symbol="F",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="v",
            description="Velocity (for computing force)",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(hill_force_velocity_eq)
