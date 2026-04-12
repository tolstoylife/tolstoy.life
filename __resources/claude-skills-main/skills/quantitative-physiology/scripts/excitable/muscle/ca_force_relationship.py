"""
Force-Calcium Relationship (Hill Equation)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def ca_force_relationship(Ca: float, F_max: float, K_d: float = 1.0, n: float = 3.0) -> float:
    """
    Force-calcium relationship using Hill equation.

    Formula: F/F_max = [Ca²⁺]^n / (K_d^n + [Ca²⁺]^n)

    This describes the cooperative binding of calcium to troponin
    and the resulting force generation.

    Parameters:
    -----------
    Ca : float - Calcium concentration (μM)
    F_max : float - Maximum force (N)
    K_d : float - Dissociation constant (μM), default: 1.0
    n : float - Hill coefficient (cooperative binding), default: 3.0

    Returns:
    --------
    F : float - Force (N)
    """
    return F_max * (Ca**n) / (K_d**n + Ca**n)

# Create and register atomic equation
ca_force_relationship_eq = create_equation(
    id="excitable.muscle.ca_force_relationship",
    name="Force-Calcium Relationship",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{F}{F_{max}} = \frac{[\text{Ca}^{2+}]^n}{K_d^n + [\text{Ca}^{2+}]^n}",
    simplified="F/F_max = [Ca²⁺]^n / (K_d^n + [Ca²⁺]^n)",
    description="Hill equation relating calcium concentration to muscle force",
    compute_func=ca_force_relationship,
    parameters=[
        Parameter(
            name="Ca",
            description="Calcium concentration",
            units="μM",
            symbol=r"[\text{Ca}^{2+}]",
            physiological_range=(0.05, 10.0)  # 50 nM to 10 μM
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant",
            units="μM",
            symbol="K_d",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (cooperativity)",
            units="dimensionless",
            symbol="n",
            default_value=3.0,
            physiological_range=(2.0, 4.0)
        ),
        Parameter(
            name="F_max",
            description="Maximum force",
            units="N",
            symbol="F_{max}",
            physiological_range=(0.0, 10000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.6")
)
register_equation(ca_force_relationship_eq)
