"""
Cable Equation for Dendrites - Spatial and temporal voltage distribution

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_cable_equation_steady_state(x: float, V_0: float, lambda_const: float) -> float:
    """
    Calculate steady-state voltage distribution along dendrite (cable equation).

    Formula: V(x) = V_0 × e^(-x/λ)
    Full PDE: λ² × (∂²V/∂x²) = τ_m × (∂V/∂t) + V

    Parameters:
    -----------
    x : float
        Distance along dendrite (μm)
    V_0 : float
        Voltage at x=0 (mV)
    lambda_const : float
        Length constant λ = sqrt(R_m / R_i) (μm)

    Returns:
    --------
    V : float
        Voltage at position x (mV)

    Notes:
    ------
    Length constant λ determines how far voltage spreads electrotonically.
    Typical values: λ ≈ 100-1000 μm for dendrites
    At x = λ, voltage decays to 1/e ≈ 37% of original
    """
    return V_0 * np.exp(-x / lambda_const)


# Create and register atomic equation
cable_equation = create_equation(
    id="nervous.integration.cable_equation_dendrite",
    name="Cable Equation (Dendrite)",
    category=EquationCategory.NERVOUS,
    latex=r"\lambda^2 \times \frac{\partial^2 V}{\partial x^2} = \tau_m \times \frac{\partial V}{\partial t} + V",
    simplified="λ² × (∂²V/∂x²) = τ_m × (∂V/∂t) + V",
    description="Cable equation describing voltage distribution in dendrites. Governs electrotonic spread of synaptic potentials. Steady-state solution: V(x) = V_0 × e^(-x/λ)",
    compute_func=compute_cable_equation_steady_state,
    parameters=[
        Parameter(
            name="x",
            description="Distance along dendrite",
            units="μm",
            symbol="x",
            default_value=None,
            physiological_range=(0.0, 2000.0)
        ),
        Parameter(
            name="V_0",
            description="Voltage at origin",
            units="mV",
            symbol="V_0",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="lambda_const",
            description="Length constant",
            units="μm",
            symbol=r"\lambda",
            default_value=None,
            physiological_range=(10.0, 2000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(cable_equation)
