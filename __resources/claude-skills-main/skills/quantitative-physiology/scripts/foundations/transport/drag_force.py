"""
Drag Force (Stokes Drag)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation 12)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def drag_force(eta: float, r: float, v: float) -> float:
    """
    Calculate Stokes drag force on a spherical particle in viscous flow.

    Formula: F_d = 6πηrv

    Stokes drag describes the force on a sphere moving through viscous fluid
    at low Reynolds numbers. Important for understanding sedimentation,
    cell motility, and molecular diffusion in physiological fluids.

    Parameters:
    -----------
    eta : float - Dynamic viscosity (Pa·s)
    r : float - Sphere radius (m)
    v : float - Velocity (m/s)

    Returns:
    --------
    F_d : float - Drag force (N)
    """
    return 6 * np.pi * eta * r * v


def friction_coefficient(eta: float, r: float) -> float:
    """
    Calculate Einstein friction coefficient for a sphere.

    Formula: f = 6πηr

    The friction coefficient relates force to velocity: F = f × v.
    Fundamental for understanding molecular mobility and diffusion.

    Parameters:
    -----------
    eta : float - Dynamic viscosity (Pa·s)
    r : float - Sphere radius (m)

    Returns:
    --------
    f : float - Friction coefficient (N·s/m = kg/s)
    """
    return 6 * np.pi * eta * r


# Create and register drag force equation
drag_force_eq = create_equation(
    id="foundations.transport.drag_force",
    name="Stokes Drag Force",
    category=EquationCategory.FOUNDATIONS,
    latex=r"F_d = 6\pi\eta r v",
    simplified="F_d = 6πηrv",
    description="Drag force on a spherical particle in viscous flow",
    compute_func=drag_force,
    parameters=[
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=0.001,  # Water at 20°C
            physiological_range=(0.0007, 0.005)  # Water to blood plasma
        ),
        Parameter(
            name="r",
            description="Sphere radius",
            units="m",
            symbol="r",
            physiological_range=(1e-10, 1e-3)  # Molecule to cell
        ),
        Parameter(
            name="v",
            description="Velocity",
            units="m/s",
            symbol="v",
            physiological_range=(1e-9, 1.0)  # Diffusion to flow
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.12"
    )
)
register_equation(drag_force_eq)


# Create and register friction coefficient equation
friction_coefficient_eq = create_equation(
    id="foundations.transport.friction_coefficient",
    name="Einstein Friction Coefficient",
    category=EquationCategory.FOUNDATIONS,
    latex=r"f = 6\pi\eta r",
    simplified="f = 6πηr",
    description="Friction coefficient for a sphere in viscous medium",
    compute_func=friction_coefficient,
    parameters=[
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=0.001,
            physiological_range=(0.0007, 0.005)
        ),
        Parameter(
            name="r",
            description="Sphere radius",
            units="m",
            symbol="r",
            physiological_range=(1e-10, 1e-3)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.3",
        textbook_equation_number="A.12b"
    )
)
register_equation(friction_coefficient_eq)
