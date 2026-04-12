"""Reynolds number for flow characterization."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_reynolds_number(rho: float, v: float, d: float, eta: float) -> float:
    """
    Calculate Reynolds number to predict turbulent vs laminar flow.

    Parameters
    ----------
    rho : float
        Blood density (kg/m³)
    v : float
        Flow velocity (m/s)
    d : float
        Vessel diameter (m)
    eta : float
        Dynamic viscosity (Pa·s)

    Returns
    -------
    float
        Reynolds number (dimensionless)
    """
    return (rho * v * d) / eta


reynolds_number = create_equation(
    id="cardiovascular.hemodynamics.reynolds_number_blood",
    name="Reynolds Number (Blood Flow)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{Re} = \frac{\rho v d}{\eta}",
    simplified="Re = ρvd / η",
    description="Dimensionless number predicting flow regime (laminar vs turbulent)",
    compute_func=compute_reynolds_number,
    parameters=[
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            physiological_range=(1050.0, 1070.0)
        ),
        Parameter(
            name="v",
            description="Flow velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.01, 2.0)
        ),
        Parameter(
            name="d",
            description="Vessel diameter",
            units="m",
            symbol="d",
            physiological_range=(0.001, 0.03)
        ),
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        )
    ],
    depends_on=["cardiovascular.blood.blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(reynolds_number)
