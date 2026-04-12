"""Law of Laplace for Alveolar Pressure."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_laplace_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure in a sphere (Law of Laplace).

    ΔP = 2T/r

    Parameters
    ----------
    T : float
        Surface tension (mN/m)
    r : float
        Radius (m)

    Returns
    -------
    float
        Transmural pressure (Pa)
    """
    return 2.0 * T / r


# Create equation
laplace_pressure = create_equation(
    id="respiratory.mechanics.laplace_pressure",
    name="Law of Laplace (Sphere)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta P = \frac{2T}{r}",
    simplified="ΔP = 2T/r",
    description="Pressure difference across a spherical surface due to surface tension",
    compute_func=compute_laplace_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Surface tension",
            units="mN/m",
            symbol="T",
            default_value=25.0,
            physiological_range=(10.0, 70.0)
        ),
        Parameter(
            name="r",
            description="Radius of sphere",
            units="m",
            symbol="r",
            physiological_range=(0.00005, 0.0005)  # 50-500 μm
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(laplace_pressure)
