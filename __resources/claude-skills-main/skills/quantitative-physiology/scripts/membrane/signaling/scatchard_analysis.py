"""
Scatchard Analysis - Linear form of receptor binding for parameter determination

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_scatchard_bound_over_free(B: float, B_max: float, K_d: float) -> float:
    """
    Calculate B/F ratio for Scatchard analysis.

    Formula: B/F = (B_max - B) / K_d

    This linearizes binding data:
    Plot B/F vs B gives slope = -1/K_d, intercept = B_max/K_d

    Parameters:
    -----------
    B : float
        Bound ligand concentration
    B_max : float
        Maximum binding capacity (total receptor sites)
    K_d : float
        Dissociation constant

    Returns:
    --------
    B_over_F : float
        Ratio of bound to free ligand

    Notes:
        Used experimentally to determine K_d and B_max from binding data
        Linearizes the hyperbolic binding isotherm
    """
    return (B_max - B) / K_d


# Create and register atomic equation
scatchard_analysis = create_equation(
    id="membrane.signaling.scatchard_analysis",
    name="Scatchard Analysis",
    category=EquationCategory.MEMBRANE,
    latex=r"\frac{B}{F} = \frac{B_{max} - B}{K_d}",
    simplified="B/F = (B_max - B) / K_d",
    description="Linear transformation of receptor binding data for determining K_d and B_max experimentally.",
    compute_func=compute_scatchard_bound_over_free,
    parameters=[
        Parameter(
            name="B",
            description="Bound ligand concentration",
            units="mol/m³",
            symbol="B",
            default_value=None
        ),
        Parameter(
            name="B_max",
            description="Maximum binding capacity",
            units="mol/m³",
            symbol="B_{max}",
            default_value=None
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant",
            units="mol/m³",
            symbol="K_d",
            default_value=None
        ),
    ],
    depends_on=["membrane.signaling.receptor_occupancy"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.6")
)

register_equation(scatchard_analysis)
