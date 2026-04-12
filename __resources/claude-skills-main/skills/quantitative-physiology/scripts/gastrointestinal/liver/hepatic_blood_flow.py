"""Total hepatic blood flow."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hepatic_blood_flow(portal: float = 1.1, arterial: float = 0.4) -> float:
    """
    Calculate total hepatic blood flow.

    Dual blood supply: ~75% portal vein, ~25% hepatic artery.
    Total ~1.5 L/min (~25% of cardiac output).

    Parameters
    ----------
    portal : float
        Portal venous flow (L/min), default 1.1 L/min
    arterial : float
        Hepatic arterial flow (L/min), default 0.4 L/min

    Returns
    -------
    float
        Total hepatic blood flow (L/min)
    """
    return portal + arterial


hepatic_blood_flow = create_equation(
    id="gastrointestinal.liver.hepatic_blood_flow",
    name="Total Hepatic Blood Flow",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"Q_H = Q_{\text{portal}} + Q_{\text{arterial}}",
    simplified="Q_H = Q_portal + Q_arterial",
    description="Total hepatic blood flow ~1.5 L/min (~25% CO). Portal vein ~75%, hepatic artery ~25%",
    compute_func=compute_hepatic_blood_flow,
    parameters=[
        Parameter(
            name="portal",
            description="Portal venous flow",
            units="L/min",
            symbol=r"Q_{\text{portal}}",
            default_value=1.1,
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="arterial",
            description="Hepatic arterial flow",
            units="L/min",
            symbol=r"Q_{\text{arterial}}",
            default_value=0.4,
            physiological_range=(0.3, 0.6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(hepatic_blood_flow)
