"""Transit time calculation for GI segments."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_transit_time(length: float, velocity: float) -> float:
    """
    Calculate transit time through a GI segment.

    Parameters
    ----------
    length : float
        Length of GI segment (cm)
    velocity : float
        Propagation velocity (cm/s)

    Returns
    -------
    float
        Transit time (seconds)
    """
    return length / velocity


transit_time = create_equation(
    id="gastrointestinal.motility.transit_time",
    name="GI Segment Transit Time",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"t_{\text{transit}} = \frac{L}{v}",
    simplified="t_transit = L / v",
    description="Transit time through GI segment based on length and propagation velocity",
    compute_func=compute_transit_time,
    parameters=[
        Parameter(
            name="length",
            description="Length of GI segment",
            units="cm",
            symbol="L",
            physiological_range=(10.0, 600.0)
        ),
        Parameter(
            name="velocity",
            description="Propagation velocity",
            units="cm/s",
            symbol="v",
            physiological_range=(0.5, 10.0)
        )
    ],
    depends_on=["gastrointestinal.motility.peristalsis_velocity"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(transit_time)
