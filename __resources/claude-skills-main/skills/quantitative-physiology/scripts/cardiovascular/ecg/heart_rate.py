"""Heart rate modulation by autonomic tone."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_heart_rate(f_intrinsic: float, df_symp: float, df_para: float) -> float:
    """
    Calculate heart rate with autonomic modulation.

    Parameters
    ----------
    f_intrinsic : float
        Intrinsic SA node firing rate (bpm)
    df_symp : float
        Sympathetic contribution (increase, bpm)
    df_para : float
        Parasympathetic contribution (decrease, bpm)

    Returns
    -------
    float
        Resulting heart rate (bpm)
    """
    return f_intrinsic + df_symp - df_para


heart_rate = create_equation(
    id="cardiovascular.ecg.heart_rate_autonomic",
    name="Heart Rate with Autonomic Tone",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"f_{\text{heart}} = f_{\text{intrinsic}} + \Delta f_{\text{sympathetic}} - \Delta f_{\text{parasympathetic}}",
    simplified="f_heart = f_intrinsic + Δf_symp - Δf_para",
    description="Heart rate modulation by sympathetic and parasympathetic nervous systems",
    compute_func=compute_heart_rate,
    parameters=[
        Parameter(
            name="f_intrinsic",
            description="Intrinsic SA node rate",
            units="bpm",
            symbol="f_{intrinsic}",
            default_value=100.0,
            physiological_range=(60.0, 100.0)
        ),
        Parameter(
            name="df_symp",
            description="Sympathetic increase",
            units="bpm",
            symbol=r"\Delta f_{symp}",
            physiological_range=(0.0, 80.0)
        ),
        Parameter(
            name="df_para",
            description="Parasympathetic decrease",
            units="bpm",
            symbol=r"\Delta f_{para}",
            physiological_range=(0.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(heart_rate)
