"""GLP-1 potentiation of insulin secretion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_glp1_insulin_response(GLP1_pM: float, glucose_mM: float, EC50_GLP1: float = 10.0, glucose_threshold: float = 5.0) -> float:
    """
    Calculate GLP-1 potentiation of insulin secretion.

    GLP-1 only effective above glucose threshold (~5 mM).
    Released by L cells (ileum) in response to nutrients.

    Parameters
    ----------
    GLP1_pM : float
        GLP-1 concentration (pM)
    glucose_mM : float
        Plasma glucose concentration (mM)
    EC50_GLP1 : float
        Half-maximal GLP-1 concentration (pM), default 10
    glucose_threshold : float
        Glucose threshold for GLP-1 effect (mM), default 5.0

    Returns
    -------
    float
        Insulin potentiation signal (0-1)
    """
    glucose_factor = max(0.0, (glucose_mM - glucose_threshold) / glucose_threshold)
    GLP1_effect = GLP1_pM / (EC50_GLP1 + GLP1_pM)
    return glucose_factor * GLP1_effect


glp1_insulin_response = create_equation(
    id="gastrointestinal.hormones.glp1_insulin_response",
    name="GLP-1 Insulin Potentiation",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Potentiation} = \frac{\max(0, \text{Glc} - 5)}{5} \times \frac{[\text{GLP-1}]}{EC_{50} + [\text{GLP-1}]}",
    simplified="Potentiation = max(0, Glc-5)/5 × [GLP-1]/(EC50 + [GLP-1])",
    description="GLP-1 potentiates insulin secretion only above glucose threshold (~5 mM). Released by L cells in ileum",
    compute_func=compute_glp1_insulin_response,
    parameters=[
        Parameter(
            name="GLP1_pM",
            description="GLP-1 concentration",
            units="pM",
            symbol=r"[\text{GLP-1}]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="glucose_mM",
            description="Plasma glucose concentration",
            units="mM",
            symbol=r"\text{Glc}",
            physiological_range=(3.0, 15.0)
        ),
        Parameter(
            name="EC50_GLP1",
            description="Half-maximal GLP-1 concentration",
            units="pM",
            symbol=r"EC_{50}",
            default_value=10.0,
            physiological_range=(5.0, 15.0)
        ),
        Parameter(
            name="glucose_threshold",
            description="Glucose threshold for GLP-1 effect",
            units="mM",
            symbol=r"\text{Glc}_{\text{threshold}}",
            default_value=5.0,
            physiological_range=(4.0, 6.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(glp1_insulin_response)
