"""Body surface area (Du Bois formula)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_body_surface_area(W: float, H: float) -> float:
    """
    Calculate body surface area using Du Bois formula.

    Parameters
    ----------
    W : float
        Weight (kg)
    H : float
        Height (cm)

    Returns
    -------
    float
        Body surface area (m²)
    """
    return 0.007184 * (W ** 0.425) * (H ** 0.725)


body_surface_area = create_equation(
    id="cardiovascular.cardiac.body_surface_area_dubois",
    name="Body Surface Area (Du Bois)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{BSA} = 0.007184 \times W^{0.425} \times H^{0.725}",
    simplified="BSA = 0.007184 × W^0.425 × H^0.725",
    description="Body surface area from weight and height (Du Bois formula)",
    compute_func=compute_body_surface_area,
    parameters=[
        Parameter(
            name="W",
            description="Body weight",
            units="kg",
            symbol="W",
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="H",
            description="Height",
            units="cm",
            symbol="H",
            physiological_range=(150.0, 200.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(body_surface_area)
