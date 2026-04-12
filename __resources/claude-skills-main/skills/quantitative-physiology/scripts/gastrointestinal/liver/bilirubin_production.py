"""Daily bilirubin production."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bilirubin_production(Hb_turnover_g: float = 6.0, conversion_factor: float = 35.0) -> float:
    """
    Calculate daily bilirubin production from hemoglobin turnover.

    Heme → Biliverdin → Bilirubin (unconjugated)
    ~35 mg bilirubin per gram Hb

    Parameters
    ----------
    Hb_turnover_g : float
        Daily hemoglobin turnover (g/day), default 6 g/day
    conversion_factor : float
        mg bilirubin per g Hb, default 35 mg/g

    Returns
    -------
    float
        Daily bilirubin production (mg/day)
    """
    return Hb_turnover_g * conversion_factor


bilirubin_production = create_equation(
    id="gastrointestinal.liver.bilirubin_production",
    name="Daily Bilirubin Production",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Bilirubin} = \text{Hb}_{\text{turnover}} \times 35 \, \text{mg/g}",
    simplified="Bilirubin = Hb_turnover × 35 mg/g",
    description="Daily bilirubin production ~250-300 mg/day from Hb turnover. ~35 mg bilirubin per g Hb. Jaundice if >2-2.5 mg/dL",
    compute_func=compute_bilirubin_production,
    parameters=[
        Parameter(
            name="Hb_turnover_g",
            description="Daily hemoglobin turnover",
            units="g/day",
            symbol=r"\text{Hb}_{\text{turnover}}",
            default_value=6.0,
            physiological_range=(5.0, 8.0)
        ),
        Parameter(
            name="conversion_factor",
            description="mg bilirubin per g Hb",
            units="mg/g",
            symbol=r"f_{\text{conv}}",
            default_value=35.0,
            physiological_range=(30.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(bilirubin_production)
