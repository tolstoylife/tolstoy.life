"""
Electric Dipole Moment

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equation 15)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def dipole_moment(q: float, d: float) -> float:
    """
    Calculate electric dipole moment from charge and separation distance.

    Formula: p = q × d

    A dipole consists of two equal and opposite charges separated by a
    distance. The dipole moment is fundamental in understanding
    electrocardiography (heart as a dipole source) and molecular polarity.

    Parameters:
    -----------
    q : float - Charge magnitude (C)
    d : float - Separation distance between charges (m)

    Returns:
    --------
    p : float - Dipole moment (C·m)
    """
    return q * d


# Create and register atomic equation
dipole_moment_eq = create_equation(
    id="foundations.electrical.dipole_moment",
    name="Electric Dipole Moment",
    category=EquationCategory.FOUNDATIONS,
    latex=r"p = qd",
    simplified="p = q × d",
    description="Electric dipole moment from charge and separation distance",
    compute_func=dipole_moment,
    parameters=[
        Parameter(
            name="q",
            description="Charge magnitude",
            units="C",
            symbol="q",
            physiological_range=(1e-20, 1e-10)  # Molecular to cellular scale
        ),
        Parameter(
            name="d",
            description="Separation distance",
            units="m",
            symbol="d",
            physiological_range=(1e-10, 1e-1)  # Atomic to organ scale
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.4",
        textbook_equation_number="A.15"
    )
)
register_equation(dipole_moment_eq)
