"""Secretin-stimulated bicarbonate secretion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_secretin_bicarbonate(pH_duodenum: float, threshold: float = 4.5, max_response: float = 140.0) -> float:
    """
    Calculate secretin release and bicarbonate secretion based on duodenal pH.

    Secretin released by S cells when duodenal pH < 4.5.

    Parameters
    ----------
    pH_duodenum : float
        Duodenal pH
    threshold : float
        pH threshold for secretin release, default 4.5
    max_response : float
        Maximum HCO3- response (mM), default 140

    Returns
    -------
    float
        HCO3- secretion response (mM)
    """
    if pH_duodenum > threshold:
        return 0.0
    else:
        return max_response * (threshold - pH_duodenum) / threshold


secretin_bicarbonate = create_equation(
    id="gastrointestinal.hormones.secretin_bicarbonate",
    name="Secretin-Bicarbonate Secretion",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{HCO}_3^-] = \begin{cases} 0 & \text{pH} > 4.5 \\ 140 \times \frac{4.5 - \text{pH}}{4.5} & \text{pH} \leq 4.5 \end{cases}",
    simplified="[HCO3-] = 0 if pH > 4.5, else 140 × (4.5 - pH) / 4.5",
    description="Secretin release triggered by duodenal pH < 4.5. Stimulates pancreatic HCO3- secretion",
    compute_func=compute_secretin_bicarbonate,
    parameters=[
        Parameter(
            name="pH_duodenum",
            description="Duodenal pH",
            units="dimensionless",
            symbol=r"\text{pH}",
            physiological_range=(1.0, 7.0)
        ),
        Parameter(
            name="threshold",
            description="pH threshold for secretin release",
            units="dimensionless",
            symbol=r"\text{pH}_{\text{threshold}}",
            default_value=4.5,
            physiological_range=(4.0, 5.0)
        ),
        Parameter(
            name="max_response",
            description="Maximum HCO3- response",
            units="mM",
            symbol=r"[\text{HCO}_3^-]_{\max}",
            default_value=140.0,
            physiological_range=(120.0, 150.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(secretin_bicarbonate)
