"""
Slope Conductance and Membrane Resistance Equations

Describes the relationship between membrane current and voltage,
including slope conductance, input resistance, and membrane conductance.

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 51-53)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def slope_conductance(delta_I: float, delta_V: float) -> float:
    """
    Calculate slope conductance from current-voltage relationship.

    Formula: g = ΔI / ΔV

    Slope conductance measures how membrane current changes with
    voltage at a particular operating point. Unlike chord conductance,
    slope conductance characterizes small-signal behavior and can
    be negative in regions of negative resistance (e.g., N-type I-V curves).

    Parameters:
    -----------
    delta_I : float - Change in membrane current (A)
    delta_V : float - Change in membrane voltage (V)

    Returns:
    --------
    g : float - Slope conductance (S = A/V)

    Clinical relevance:
    - Negative slope conductance enables action potential generation
    - Determines membrane stability and oscillations
    - Key parameter in computational neuron models
    """
    return delta_I / delta_V


def membrane_conductance(I_m: float, V_m: float, E_rev: float) -> float:
    """
    Calculate membrane conductance from Ohm's law.

    Formula: g_m = I_m / (V_m - E_rev)

    This is the chord conductance for a specific reversal potential.
    For total membrane current, E_rev is typically E_leak.

    Parameters:
    -----------
    I_m : float - Membrane current (A)
    V_m : float - Membrane potential (V)
    E_rev : float - Reversal potential (V)

    Returns:
    --------
    g_m : float - Membrane conductance (S)
    """
    return I_m / (V_m - E_rev)


def specific_membrane_resistance(R_m: float, area: float) -> float:
    """
    Calculate specific membrane resistance (resistance × area).

    Formula: r_m = R_m × A

    Specific membrane resistance is an intrinsic property of the
    membrane independent of cell size. Typical values:
    - 1,000-100,000 Ω·cm² for most neurons
    - Myelinated segments: ~160,000 Ω·cm²
    - Nodes of Ranvier: ~50 Ω·cm²

    Parameters:
    -----------
    R_m : float - Membrane resistance (Ω)
    area : float - Membrane area (m²)

    Returns:
    --------
    r_m : float - Specific membrane resistance (Ω·m²)
    """
    return R_m * area


def axoplasmic_resistance(rho: float, L: float, area: float) -> float:
    """
    Calculate axoplasmic (internal) resistance.

    Formula: R_i = ρ × L / A

    Axoplasmic resistance limits current spread within the cytoplasm.
    Typical resistivity: 50-200 Ω·cm for axoplasm.

    Parameters:
    -----------
    rho : float - Axoplasm resistivity (Ω·m)
    L : float - Length of segment (m)
    area : float - Cross-sectional area (m²)

    Returns:
    --------
    R_i : float - Internal resistance (Ω)
    """
    return rho * L / area


def transmembrane_resistance(specific_r_m: float, circumference: float, length: float) -> float:
    """
    Calculate transmembrane resistance for a cylindrical segment.

    Formula: R_m = r_m / (circumference × length)

    For a cylinder of radius r: circumference = 2πr
    Membrane area = 2πr × L

    Parameters:
    -----------
    specific_r_m : float - Specific membrane resistance (Ω·m²)
    circumference : float - Circumference of cylinder (m)
    length : float - Length of segment (m)

    Returns:
    --------
    R_m : float - Transmembrane resistance (Ω)
    """
    return specific_r_m / (circumference * length)


def resistance_per_unit_length_membrane(specific_r_m: float, circumference: float) -> float:
    """
    Calculate membrane resistance per unit length.

    Formula: r_m = r_m_specific / circumference = r_m_specific / (2πr)

    This is the r_m used in cable equation, with units Ω·m.

    Parameters:
    -----------
    specific_r_m : float - Specific membrane resistance (Ω·m²)
    circumference : float - Circumference = 2πr (m)

    Returns:
    --------
    r_m : float - Membrane resistance per unit length (Ω·m)
    """
    return specific_r_m / circumference


def resistance_per_unit_length_axoplasm(rho: float, cross_area: float) -> float:
    """
    Calculate axoplasmic resistance per unit length.

    Formula: r_i = ρ / A = ρ / (πr²)

    This is the r_i used in cable equation, with units Ω/m.

    Parameters:
    -----------
    rho : float - Axoplasm resistivity (Ω·m)
    cross_area : float - Cross-sectional area = πr² (m²)

    Returns:
    --------
    r_i : float - Axoplasmic resistance per unit length (Ω/m)
    """
    return rho / cross_area


# Create and register slope conductance equation
slope_conductance_eq = create_equation(
    id="excitable.membrane_potential.slope_conductance",
    name="Slope Conductance",
    category=EquationCategory.EXCITABLE,
    latex=r"g_{slope} = \frac{\Delta I}{\Delta V}",
    simplified="g_slope = ΔI / ΔV",
    description="Slope of I-V curve at a point, can be negative for regenerative currents",
    compute_func=slope_conductance,
    parameters=[
        Parameter(
            name="delta_I",
            description="Change in membrane current",
            units="A",
            symbol=r"\Delta I",
            physiological_range=(-1e-6, 1e-6)  # ±1 μA range
        ),
        Parameter(
            name="delta_V",
            description="Change in membrane voltage",
            units="V",
            symbol=r"\Delta V",
            physiological_range=(-0.1, 0.1)  # ±100 mV range
        ),
    ],
    depends_on=["excitable.membrane_potential.chord_conductance"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.1",
        textbook_equation_number="A.51"
    )
)
register_equation(slope_conductance_eq)


# Create and register transmembrane resistance equation
transmembrane_resistance_eq = create_equation(
    id="excitable.membrane_potential.transmembrane_resistance",
    name="Transmembrane Resistance (Cylindrical)",
    category=EquationCategory.EXCITABLE,
    latex=r"R_m = \frac{r_m^{specific}}{2\pi r \cdot L}",
    simplified="R_m = r_m / (circumference × L)",
    description="Membrane resistance for a cylindrical segment of nerve or muscle",
    compute_func=transmembrane_resistance,
    parameters=[
        Parameter(
            name="specific_r_m",
            description="Specific membrane resistance",
            units="Ω·m²",
            symbol="r_m^{specific}",
            physiological_range=(0.01, 10.0)  # 100 to 100,000 Ω·cm²
        ),
        Parameter(
            name="circumference",
            description="Circumference of fiber (2πr)",
            units="m",
            symbol="C",
            physiological_range=(1e-6, 1e-3)  # 1 μm to 1 mm
        ),
        Parameter(
            name="length",
            description="Length of segment",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 0.01)  # 1 μm to 10 mm
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.2",
        textbook_equation_number="A.52"
    )
)
register_equation(transmembrane_resistance_eq)


# Create and register axoplasmic resistance equation
axoplasmic_resistance_eq = create_equation(
    id="excitable.membrane_potential.axoplasmic_resistance",
    name="Axoplasmic (Internal) Resistance",
    category=EquationCategory.EXCITABLE,
    latex=r"R_i = \frac{\rho \cdot L}{A}",
    simplified="R_i = ρ × L / A",
    description="Internal resistance of axoplasm in a cylindrical segment",
    compute_func=axoplasmic_resistance,
    parameters=[
        Parameter(
            name="rho",
            description="Axoplasm resistivity",
            units="Ω·m",
            symbol=r"\rho",
            physiological_range=(0.5, 3.0)  # 50-300 Ω·cm typical
        ),
        Parameter(
            name="L",
            description="Segment length",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 0.01)  # 1 μm to 10 mm
        ),
        Parameter(
            name="area",
            description="Cross-sectional area (πr²)",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-8)  # μm² to mm² range
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.2",
        textbook_equation_number="A.53"
    )
)
register_equation(axoplasmic_resistance_eq)
