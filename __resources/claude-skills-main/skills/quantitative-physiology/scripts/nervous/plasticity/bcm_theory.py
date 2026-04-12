"""
BCM Theory - Bienenstock-Cooper-Munro sliding threshold plasticity

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_bcm_weight_change(r: float, theta_m: float, learning_rate: float = 0.01) -> float:
    """
    Calculate weight change according to BCM theory.

    Formula: Δw ∝ r × (r - θ_m)

    Parameters:
    -----------
    r : float
        Postsynaptic firing rate (Hz)
    theta_m : float
        Modification threshold (Hz)
    learning_rate : float
        Learning rate constant, default 0.01

    Returns:
    --------
    delta_w : float
        Weight change

    Notes:
    ------
    BCM theory implements sliding threshold for LTP/LTD:
    - If r < θ_m: LTD (weight decreases)
    - If r > θ_m: LTP (weight increases)
    - θ_m adjusts with average activity: θ_m ∝ ⟨r⟩²

    Stabilizes learning and prevents runaway potentiation.
    Accounts for metaplasticity (plasticity of plasticity).
    """
    return learning_rate * r * (r - theta_m)


# Create and register atomic equation
bcm_theory = create_equation(
    id="nervous.plasticity.bcm_theory",
    name="BCM Theory",
    category=EquationCategory.NERVOUS,
    latex=r"\Delta w \propto r \times (r - \theta_m)",
    simplified="Δw ∝ r × (r - θ_m)",
    description="Bienenstock-Cooper-Munro theory of synaptic plasticity with sliding threshold. LTD when r<θ_m, LTP when r>θ_m. Threshold θ_m adjusts with activity to stabilize learning.",
    compute_func=compute_bcm_weight_change,
    parameters=[
        Parameter(
            name="r",
            description="Postsynaptic firing rate",
            units="Hz",
            symbol="r",
            default_value=None,
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="theta_m",
            description="Modification threshold",
            units="Hz",
            symbol=r"\theta_m",
            default_value=None,
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="learning_rate",
            description="Learning rate constant",
            units="dimensionless",
            symbol=r"\eta",
            default_value=0.01,
            physiological_range=(0.0001, 0.1)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(bcm_theory)
