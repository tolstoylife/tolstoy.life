"""Gastric emptying equation for solids (lag phase + linear)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gastric_emptying_solid(t: float, V0: float, t_lag: float, r: float) -> float:
    """
    Calculate gastric volume remaining for solids (lag phase + linear emptying).

    Parameters
    ----------
    t : float
        Time (minutes)
    V0 : float
        Initial volume (g)
    t_lag : float
        Lag phase duration (minutes)
    r : float
        Emptying rate (kcal/min or g/min)

    Returns
    -------
    float
        Remaining volume (g)
    """
    if t < t_lag:
        return V0
    else:
        return max(0.0, V0 - r * (t - t_lag))


gastric_emptying_solid = create_equation(
    id="gastrointestinal.motility.gastric_emptying_solid",
    name="Gastric Emptying (Solids)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"V(t) = \begin{cases} V_0 & t < t_{\text{lag}} \\ V_0 - r(t - t_{\text{lag}}) & t \geq t_{\text{lag}} \end{cases}",
    simplified="V(t) = V₀ if t < t_lag, else V₀ - r×(t - t_lag)",
    description="Gastric emptying for solids with initial lag phase followed by linear emptying at ~1-2 kcal/min",
    compute_func=compute_gastric_emptying_solid,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 360.0)
        ),
        Parameter(
            name="V0",
            description="Initial volume",
            units="g",
            symbol="V_0",
            physiological_range=(50.0, 500.0)
        ),
        Parameter(
            name="t_lag",
            description="Lag phase duration",
            units="min",
            symbol=r"t_{\text{lag}}",
            default_value=30.0,
            physiological_range=(10.0, 60.0)
        ),
        Parameter(
            name="r",
            description="Emptying rate",
            units="g/min",
            symbol="r",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(gastric_emptying_solid)
