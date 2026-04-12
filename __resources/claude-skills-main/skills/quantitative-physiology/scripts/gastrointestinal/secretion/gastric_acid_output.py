"""Gastric acid output equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gastric_acid_output(stim_fraction: float, MAO: float = 25.0) -> float:
    """
    Calculate gastric acid output based on stimulation level.

    Parameters
    ----------
    stim_fraction : float
        Stimulation fraction (0 = basal, 1 = maximal)
    MAO : float
        Maximal acid output (mEq/h), default 25 mEq/h

    Returns
    -------
    float
        Acid output (mEq/h)
    """
    BAO = 0.15 * MAO  # Basal is ~15% of maximal
    return BAO + (MAO - BAO) * stim_fraction


gastric_acid_output = create_equation(
    id="gastrointestinal.secretion.gastric_acid_output",
    name="Gastric Acid Output",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{AO} = \text{BAO} + (\text{MAO} - \text{BAO}) \times f",
    simplified="AO = BAO + (MAO - BAO) × f",
    description="Gastric acid output as function of stimulation (BAO ~2-5 mEq/h, MAO ~20-25 mEq/h)",
    compute_func=compute_gastric_acid_output,
    parameters=[
        Parameter(
            name="stim_fraction",
            description="Stimulation fraction (0 = basal, 1 = maximal)",
            units="dimensionless",
            symbol="f",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="MAO",
            description="Maximal acid output",
            units="mEq/h",
            symbol=r"\text{MAO}",
            default_value=25.0,
            physiological_range=(20.0, 30.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(gastric_acid_output)
