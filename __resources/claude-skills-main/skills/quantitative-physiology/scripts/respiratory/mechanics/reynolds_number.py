"""Reynolds Number equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_reynolds_number(rho: float, v: float, d: float, eta: float) -> float:
    """
    Calculate Reynolds number to determine flow pattern.

    Re = ρvd/η

    Parameters
    ----------
    rho : float
        Fluid density (kg/m³)
    v : float
        Velocity (m/s)
    d : float
        Characteristic diameter (m)
    eta : float
        Viscosity (Pa·s)

    Returns
    -------
    float
        Reynolds number (dimensionless)
    """
    return (rho * v * d) / eta


# Create equation
reynolds_number = create_equation(
    id="respiratory.mechanics.reynolds_number_airway",
    name="Reynolds Number (Airway Flow)",
    category=EquationCategory.RESPIRATORY,
    latex=r"Re = \frac{\rho v d}{\eta}",
    simplified="Re = ρvd/η",
    description="Dimensionless number determining laminar (Re<2000) vs turbulent (Re>2000) flow",
    compute_func=compute_reynolds_number,
    parameters=[
        Parameter(
            name="rho",
            description="Air density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1.2,
            physiological_range=(1.0, 1.3)
        ),
        Parameter(
            name="v",
            description="Flow velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="d",
            description="Airway diameter",
            units="m",
            symbol="d",
            physiological_range=(0.0002, 0.02)
        ),
        Parameter(
            name="eta",
            description="Air viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=1.8e-5,
            physiological_range=(1.5e-5, 2.0e-5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(reynolds_number)
