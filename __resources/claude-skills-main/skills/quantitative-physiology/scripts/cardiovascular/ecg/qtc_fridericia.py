"""Fridericia's formula for QTc correction."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_qtc_fridericia(QT: float, RR: float) -> float:
    """
    Calculate rate-corrected QT interval using Fridericia's formula.

    More accurate at extreme heart rates than Bazett's formula.

    Parameters
    ----------
    QT : float
        Measured QT interval (ms)
    RR : float
        RR interval (seconds)

    Returns
    -------
    float
        Corrected QT interval (ms)
    """
    return QT / np.cbrt(RR)


qtc_fridericia = create_equation(
    id="cardiovascular.ecg.qtc_fridericia",
    name="Fridericia's QTc Correction",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{QTc} = \frac{\text{QT}}{\sqrt[3]{\text{RR}}}",
    simplified="QTc = QT / ∛(RR)",
    description="Rate-corrected QT interval using Fridericia's formula (more accurate at extreme rates)",
    compute_func=compute_qtc_fridericia,
    parameters=[
        Parameter(
            name="QT",
            description="Measured QT interval",
            units="ms",
            symbol="QT",
            physiological_range=(350.0, 440.0)
        ),
        Parameter(
            name="RR",
            description="RR interval",
            units="s",
            symbol="RR",
            physiological_range=(0.6, 1.2)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(qtc_fridericia)
