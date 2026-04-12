"""
Enthalpy Definition

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation 14)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def enthalpy(U: float, P: float, V: float) -> float:
    """
    Calculate enthalpy from internal energy, pressure, and volume.

    Formula: H = U + PV

    Enthalpy is the total heat content of a system. It represents the
    internal energy plus the work required to make room for the system
    at constant pressure.

    Parameters:
    -----------
    U : float - Internal energy (J)
    P : float - Pressure (Pa)
    V : float - Volume (m³)

    Returns:
    --------
    H : float - Enthalpy (J)
    """
    return U + P * V


# Create and register atomic equation
enthalpy_eq = create_equation(
    id="foundations.thermodynamics.enthalpy",
    name="Enthalpy Definition",
    category=EquationCategory.FOUNDATIONS,
    latex=r"H = U + PV",
    simplified="H = U + PV",
    description="Total heat content of a thermodynamic system",
    compute_func=enthalpy,
    parameters=[
        Parameter(
            name="U",
            description="Internal energy",
            units="J",
            symbol="U",
            physiological_range=(0.0, 1e6)
        ),
        Parameter(
            name="P",
            description="Pressure",
            units="Pa",
            symbol="P",
            default_value=101325.0,  # 1 atm
            physiological_range=(50000.0, 200000.0)
        ),
        Parameter(
            name="V",
            description="Volume",
            units="m³",
            symbol="V",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.2",
        textbook_equation_number="A.14"
    )
)
register_equation(enthalpy_eq)
