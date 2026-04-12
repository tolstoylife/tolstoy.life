"""
Dendrite Input Resistance - Input resistance at dendritic branch point

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_dendrite_input_resistance(R_m: float, R_i: float, a: float) -> float:
    """
    Calculate input resistance at infinite dendrite.

    Formula: R_∞ = √(R_m × R_i) / (2πa^(3/2))

    Parameters:
    -----------
    R_m : float
        Specific membrane resistance (Ω·cm²)
    R_i : float
        Specific internal (axial) resistance (Ω·cm)
    a : float
        Dendrite radius (μm)

    Returns:
    --------
    R_inf : float
        Input resistance (MΩ)

    Notes:
    ------
    This is the input resistance for semi-infinite cylindrical dendrite.
    Lower for large dendrites, higher for thin dendrites.
    Determines amplitude of synaptic potentials.
    """
    # Convert radius from μm to cm
    a_cm = a * 1e-4
    # Calculate in Ω, then convert to MΩ
    R_inf = np.sqrt(R_m * R_i) / (2 * np.pi * a_cm**1.5)
    return R_inf * 1e-6  # Convert to MΩ


# Create and register atomic equation
dendrite_input_resistance = create_equation(
    id="nervous.integration.dendrite_input_resistance",
    name="Dendrite Input Resistance",
    category=EquationCategory.NERVOUS,
    latex=r"R_\infty = \frac{\sqrt{R_m \times R_i}}{2\pi a^{3/2}}",
    simplified="R_∞ = √(R_m × R_i) / (2πa^(3/2))",
    description="Input resistance at a dendritic location, assuming semi-infinite cable. Determines how current injection affects local voltage.",
    compute_func=compute_dendrite_input_resistance,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=None,
            physiological_range=(100.0, 100000.0)
        ),
        Parameter(
            name="R_i",
            description="Specific internal resistance",
            units="Ω·cm",
            symbol="R_i",
            default_value=None,
            physiological_range=(10.0, 500.0)
        ),
        Parameter(
            name="a",
            description="Dendrite radius",
            units="μm",
            symbol="a",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(dendrite_input_resistance)
