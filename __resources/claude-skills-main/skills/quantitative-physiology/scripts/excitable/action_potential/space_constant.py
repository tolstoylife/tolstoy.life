"""
Cable Space Constant (Length Constant)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def space_constant(a: float, R_m: float = 1000.0, R_i: float = 100.0) -> float:
    """
    Cable space constant (length constant).

    Formula: λ = √(r_m / r_i) = √(R_m × a / 2R_i)

    The space constant determines how far voltage spreads passively
    along the axon before decaying to 1/e of its original value.

    Parameters:
    -----------
    a : float - Axon radius (cm)
    R_m : float - Specific membrane resistance (Ω·cm²), default 1000.0
    R_i : float - Axoplasm resistivity (Ω·cm), default 100.0

    Returns:
    --------
    lambda : float - Space constant (cm)
    """
    return np.sqrt(R_m * a / (2 * R_i))

# Create and register atomic equation
space_constant_eq = create_equation(
    id="excitable.action_potential.space_constant",
    name="Cable Space Constant",
    category=EquationCategory.EXCITABLE,
    latex=r"\lambda = \sqrt{\frac{r_m}{r_i}} = \sqrt{\frac{R_m a}{2R_i}}",
    simplified="λ = √(R_m × a / 2R_i)",
    description="Characteristic length for passive voltage spread along an axon",
    compute_func=space_constant,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=1000.0,
            physiological_range=(500.0, 10000.0)
        ),
        Parameter(
            name="R_i",
            description="Axoplasm resistivity",
            units="Ω·cm",
            symbol="R_i",
            default_value=100.0,
            physiological_range=(50.0, 200.0)
        ),
        Parameter(
            name="a",
            description="Axon radius",
            units="cm",
            symbol="a",
            physiological_range=(0.0001, 0.1)  # 1 μm to 1 mm
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(space_constant_eq)
