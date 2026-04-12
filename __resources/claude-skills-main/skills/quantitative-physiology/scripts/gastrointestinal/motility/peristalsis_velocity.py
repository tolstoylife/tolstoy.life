"""Peristalsis propagation velocity equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_peristalsis_velocity(wavelength: float, frequency: float) -> float:
    """
    Calculate peristaltic wave propagation velocity.

    Parameters
    ----------
    wavelength : float
        Wavelength of peristaltic contraction (cm)
    frequency : float
        Contraction frequency (Hz)

    Returns
    -------
    float
        Propagation velocity (cm/s)
    """
    return wavelength * frequency


peristalsis_velocity = create_equation(
    id="gastrointestinal.motility.peristalsis_velocity",
    name="Peristalsis Propagation Velocity",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"v = \lambda \times f",
    simplified="v = λ × f",
    description="Velocity of peristaltic wave propagation along GI tract",
    compute_func=compute_peristalsis_velocity,
    parameters=[
        Parameter(
            name="wavelength",
            description="Wavelength of peristaltic contraction",
            units="cm",
            symbol=r"\lambda",
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="frequency",
            description="Contraction frequency",
            units="Hz",
            symbol="f",
            physiological_range=(0.01, 0.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(peristalsis_velocity)
