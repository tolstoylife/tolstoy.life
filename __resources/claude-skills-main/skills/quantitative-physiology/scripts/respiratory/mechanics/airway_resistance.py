"""Airway Resistance (Poiseuille's Law) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import math


def compute_airway_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate airway resistance using Poiseuille's law.

    R = 8ηL/(πr⁴)

    Parameters
    ----------
    eta : float
        Viscosity (Pa·s)
    L : float
        Length (m)
    r : float
        Radius (m)

    Returns
    -------
    float
        Resistance (Pa·s/m³)
    """
    return (8.0 * eta * L) / (math.pi * r**4)


# Create equation
airway_resistance = create_equation(
    id="respiratory.mechanics.airway_resistance",
    name="Airway Resistance (Poiseuille)",
    category=EquationCategory.RESPIRATORY,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = 8ηL/(πr⁴)",
    description="Resistance to airflow in cylindrical airways - highly sensitive to radius",
    compute_func=compute_airway_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Air viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=1.8e-5,
            physiological_range=(1.5e-5, 2.0e-5)
        ),
        Parameter(
            name="L",
            description="Airway length",
            units="m",
            symbol="L",
            physiological_range=(0.001, 0.1)
        ),
        Parameter(
            name="r",
            description="Airway radius",
            units="m",
            symbol="r",
            physiological_range=(0.0001, 0.01)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(airway_resistance)
