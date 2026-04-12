"""
Permeability Coefficient - Rate of passive diffusion across membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_permeability_coefficient(D: float, K: float, delta: float) -> float:
    """
    Calculate membrane permeability coefficient.

    Formula: P = D × K / δ

    Parameters:
    -----------
    D : float
        Diffusion coefficient in membrane (m²/s)
    K : float
        Partition coefficient (membrane/water concentration ratio)
    delta : float
        Membrane thickness (m)

    Returns:
    --------
    P : float
        Permeability coefficient (m/s)

    Typical values:
        H₂O: 10⁻⁴ m/s (10⁻² cm/s)
        Urea: 10⁻⁸ m/s (10⁻⁶ cm/s)
        Glucose: 10⁻⁹ m/s (10⁻⁷ cm/s)
        Na⁺: 10⁻¹⁴ m/s (10⁻¹² cm/s)
        Cl⁻: 10⁻¹³ m/s (10⁻¹¹ cm/s)
    """
    return D * K / delta


# Create and register atomic equation
permeability_coefficient = create_equation(
    id="membrane.structure.permeability_coefficient",
    name="Permeability Coefficient",
    category=EquationCategory.MEMBRANE,
    latex=r"P = \frac{D \cdot K}{\delta}",
    simplified="P = (D * K) / delta",
    description="Permeability coefficient determining the rate of passive diffusion across a membrane, combining diffusion within the membrane and partitioning into the membrane.",
    compute_func=compute_permeability_coefficient,
    parameters=[
        Parameter(
            name="D",
            description="Diffusion coefficient in membrane",
            units="m²/s",
            symbol="D",
            default_value=None
        ),
        Parameter(
            name="K",
            description="Partition coefficient (membrane/water)",
            units="dimensionless",
            symbol="K",
            default_value=None
        ),
        Parameter(
            name="delta",
            description="Membrane thickness",
            units="m",
            symbol=r"\delta",
            default_value=4e-9
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.1")
)

register_equation(permeability_coefficient)
