"""Diffusion Conductance Model equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_diffusion_conductance(D_M: float, theta: float, V_c: float) -> float:
    """
    Calculate total diffusing capacity from conductance model.

    1/D_L = 1/D_M + 1/(θ × V_c)

    Parameters
    ----------
    D_M : float
        Membrane diffusing capacity (mL/(min·mmHg))
    theta : float
        Reaction rate of gas with Hb (mL/(min·mmHg·mL))
    V_c : float
        Pulmonary capillary blood volume (mL)

    Returns
    -------
    float
        Total diffusing capacity (mL/(min·mmHg))
    """
    return 1.0 / (1.0/D_M + 1.0/(theta * V_c))


# Create equation
diffusion_conductance = create_equation(
    id="respiratory.gas_exchange.diffusion_conductance",
    name="Diffusion Conductance Model",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{1}{D_L} = \frac{1}{D_M} + \frac{1}{\theta \times V_c}",
    simplified="1/D_L = 1/D_M + 1/(θ × V_c)",
    description="Resistance model combining membrane diffusion and chemical reaction rates",
    compute_func=compute_diffusion_conductance,
    parameters=[
        Parameter(
            name="D_M",
            description="Membrane diffusing capacity",
            units="mL/(min·mmHg)",
            symbol="D_M",
            physiological_range=(20.0, 100.0)
        ),
        Parameter(
            name="theta",
            description="Reaction rate with Hb",
            units="mL/(min·mmHg·mL)",
            symbol=r"\theta",
            physiological_range=(0.001, 0.01)
        ),
        Parameter(
            name="V_c",
            description="Capillary blood volume",
            units="mL",
            symbol="V_c",
            default_value=70.0,
            physiological_range=(50.0, 150.0)
        )
    ],
    depends_on=["respiratory.gas_exchange.diffusing_capacity"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(diffusion_conductance)
