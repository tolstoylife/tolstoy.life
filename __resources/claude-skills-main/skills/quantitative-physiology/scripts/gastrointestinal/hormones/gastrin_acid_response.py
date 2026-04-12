"""Gastrin-stimulated acid secretion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gastrin_acid_response(gastrin_pg_mL: float, Amax: float = 25.0, EC50: float = 40.0, n: float = 1.5) -> float:
    """
    Calculate acid secretion response to gastrin using Hill equation.

    Gastrin released by G cells (antrum) in response to peptides, distension, vagal stimulation.

    Parameters
    ----------
    gastrin_pg_mL : float
        Plasma gastrin concentration (pg/mL)
    Amax : float
        Maximum acid output (mEq/h), default 25
    EC50 : float
        Half-maximal gastrin concentration (pg/mL), default 40
    n : float
        Hill coefficient, default 1.5

    Returns
    -------
    float
        Acid output (mEq/h)
    """
    return Amax * (gastrin_pg_mL ** n) / (EC50 ** n + gastrin_pg_mL ** n)


gastrin_acid_response = create_equation(
    id="gastrointestinal.hormones.gastrin_acid_response",
    name="Gastrin-Acid Secretion Response",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"AO = \frac{A_{\max} \times [\text{Gastrin}]^n}{EC_{50}^n + [\text{Gastrin}]^n}",
    simplified="AO = A_max × [Gastrin]^n / (EC50^n + [Gastrin]^n)",
    description="Gastrin dose-response for acid secretion. EC50 ≈ 30-50 pg/mL. Released by G cells in response to peptides, distension",
    compute_func=compute_gastrin_acid_response,
    parameters=[
        Parameter(
            name="gastrin_pg_mL",
            description="Plasma gastrin concentration",
            units="pg/mL",
            symbol=r"[\text{Gastrin}]",
            physiological_range=(10.0, 200.0)
        ),
        Parameter(
            name="Amax",
            description="Maximum acid output",
            units="mEq/h",
            symbol=r"A_{\max}",
            default_value=25.0,
            physiological_range=(20.0, 30.0)
        ),
        Parameter(
            name="EC50",
            description="Half-maximal gastrin concentration",
            units="pg/mL",
            symbol=r"EC_{50}",
            default_value=40.0,
            physiological_range=(30.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(gastrin_acid_response)
