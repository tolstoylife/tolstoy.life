"""
Electrotonus Equations (Passive Spread of Potential)

Describes the spread of subthreshold potential changes along
excitable membranes, fundamental to understanding how signals
propagate and decay in neurons.

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 48-50)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def electrotonic_decay_distance(V_0: float, x: float, lambda_c: float) -> float:
    """
    Calculate voltage decay with distance (steady-state electrotonus).

    Formula: V(x) = V₀ × e^(-x/λ)

    Describes how a constant injected current creates a spatial
    gradient of membrane potential that decays exponentially
    with distance from the injection site.

    Parameters:
    -----------
    V_0 : float - Voltage at injection site (V)
    x : float - Distance from injection site (m)
    lambda_c : float - Space constant (m)

    Returns:
    --------
    V : float - Voltage at distance x (V)

    Notes:
    - At x = λ, voltage is 37% (1/e) of V₀
    - At x = 3λ, voltage is ~5% of V₀
    - Myelination dramatically increases λ (1-2 mm vs 50-200 μm unmyelinated)
    """
    return V_0 * np.exp(-x / lambda_c)


def electrotonic_decay_time(V_0: float, t: float, tau_m: float) -> float:
    """
    Calculate voltage decay with time at a point.

    Formula: V(t) = V₀ × e^(-t/τ_m)

    After removing a constant current, the membrane potential
    returns to rest exponentially with time constant τ_m.

    Parameters:
    -----------
    V_0 : float - Initial voltage deviation from rest (V)
    t : float - Time after stimulus removal (s)
    tau_m : float - Membrane time constant (s)

    Returns:
    --------
    V : float - Voltage at time t (V)
    """
    return V_0 * np.exp(-t / tau_m)


def electrotonic_spread_full(V_0: float, x: float, t: float,
                             lambda_c: float, tau_m: float) -> float:
    """
    Calculate voltage with both spatial and temporal dependence.

    Formula: V(x,t) = V₀ × e^(-x/λ) × (1 - e^(-t/τ_m))

    For a step current applied at t=0, this describes how the
    potential builds up at distance x over time.

    Parameters:
    -----------
    V_0 : float - Steady-state voltage at injection site (V)
    x : float - Distance from injection site (m)
    t : float - Time since stimulus onset (s)
    lambda_c : float - Space constant (m)
    tau_m : float - Membrane time constant (s)

    Returns:
    --------
    V : float - Voltage at position x and time t (V)
    """
    return V_0 * np.exp(-x / lambda_c) * (1 - np.exp(-t / tau_m))


def electrotonic_length(physical_length: float, lambda_c: float) -> float:
    """
    Calculate electrotonic length (dimensionless length in space constants).

    Formula: L = physical_length / λ

    Electrotonic length normalizes physical dimensions to electrical
    dimensions, allowing comparison of signal transmission efficiency
    across different neuron types.

    Parameters:
    -----------
    physical_length : float - Physical length of fiber segment (m)
    lambda_c : float - Space constant (m)

    Returns:
    --------
    L : float - Electrotonic length (dimensionless)

    Interpretation:
    - L < 1: Good signal propagation (myelinated axons)
    - L > 3: Significant attenuation (long unmyelinated fibers)
    - L = 1: Voltage attenuates to 37% over this length
    """
    return physical_length / lambda_c


def input_resistance_infinite_cable(r_m: float, r_i: float) -> float:
    """
    Calculate input resistance of an infinite cable.

    Formula: R_∞ = √(r_m × r_i)

    Where r_m is membrane resistance per unit length (Ω·m)
    and r_i is internal resistance per unit length (Ω/m).

    Parameters:
    -----------
    r_m : float - Membrane resistance per unit length (Ω·m)
    r_i : float - Internal (axoplasmic) resistance per unit length (Ω/m)

    Returns:
    --------
    R_inf : float - Input resistance (Ω)
    """
    return np.sqrt(r_m * r_i)


def velocity_factor(lambda_c: float, tau_m: float) -> float:
    """
    Calculate the electrotonus velocity factor.

    Formula: v_factor = λ / τ_m

    This is a characteristic velocity for passive spread of potential,
    though actual action potential velocity depends on active conductances.

    Parameters:
    -----------
    lambda_c : float - Space constant (m)
    tau_m : float - Membrane time constant (s)

    Returns:
    --------
    v : float - Velocity factor (m/s)
    """
    return lambda_c / tau_m


# Create and register electrotonic decay with distance equation
electrotonic_distance_eq = create_equation(
    id="excitable.action_potential.electrotonic_distance",
    name="Electrotonic Decay (Distance)",
    category=EquationCategory.EXCITABLE,
    latex=r"V(x) = V_0 e^{-x/\lambda}",
    simplified="V(x) = V₀ × e^(-x/λ)",
    description="Exponential decay of membrane potential with distance from current injection",
    compute_func=electrotonic_decay_distance,
    parameters=[
        Parameter(
            name="V_0",
            description="Voltage at injection site",
            units="V",
            symbol="V_0",
            physiological_range=(1e-4, 0.1)  # 0.1 mV to 100 mV from rest
        ),
        Parameter(
            name="x",
            description="Distance from injection site",
            units="m",
            symbol="x",
            physiological_range=(0, 0.01)  # 0 to 10 mm
        ),
        Parameter(
            name="lambda_c",
            description="Space constant (length constant)",
            units="m",
            symbol=r"\lambda",
            physiological_range=(5e-5, 5e-3)  # 50 μm to 5 mm
        ),
    ],
    depends_on=["excitable.action_potential.space_constant"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.2",
        textbook_equation_number="A.48"
    )
)
register_equation(electrotonic_distance_eq)


# Create and register electrotonic decay with time equation
electrotonic_time_eq = create_equation(
    id="excitable.action_potential.electrotonic_time",
    name="Electrotonic Decay (Time)",
    category=EquationCategory.EXCITABLE,
    latex=r"V(t) = V_0 e^{-t/\tau_m}",
    simplified="V(t) = V₀ × e^(-t/τ_m)",
    description="Exponential decay of membrane potential over time",
    compute_func=electrotonic_decay_time,
    parameters=[
        Parameter(
            name="V_0",
            description="Initial voltage deviation from rest",
            units="V",
            symbol="V_0",
            physiological_range=(1e-4, 0.1)
        ),
        Parameter(
            name="t",
            description="Time since stimulus removal",
            units="s",
            symbol="t",
            physiological_range=(0, 0.1)  # 0 to 100 ms
        ),
        Parameter(
            name="tau_m",
            description="Membrane time constant",
            units="s",
            symbol=r"\tau_m",
            physiological_range=(1e-4, 0.05)  # 0.1 to 50 ms
        ),
    ],
    depends_on=["respiratory.mechanics.time_constant"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.2",
        textbook_equation_number="A.49"
    )
)
register_equation(electrotonic_time_eq)


# Create and register input resistance of infinite cable
input_resistance_eq = create_equation(
    id="excitable.action_potential.input_resistance_cable",
    name="Input Resistance (Infinite Cable)",
    category=EquationCategory.EXCITABLE,
    latex=r"R_\infty = \sqrt{r_m \cdot r_i}",
    simplified="R_∞ = √(r_m × r_i)",
    description="Input resistance of an infinite unmyelinated cable",
    compute_func=input_resistance_infinite_cable,
    parameters=[
        Parameter(
            name="r_m",
            description="Membrane resistance per unit length",
            units="Ω·m",
            symbol="r_m",
            physiological_range=(1e5, 1e9)  # 100 kΩ·m to 1 GΩ·m
        ),
        Parameter(
            name="r_i",
            description="Internal (axoplasmic) resistance per unit length",
            units="Ω/m",
            symbol="r_i",
            physiological_range=(1e6, 1e10)  # 1 MΩ/m to 10 GΩ/m
        ),
    ],
    depends_on=["excitable.action_potential.space_constant", "excitable.action_potential.cable_equation"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.2",
        textbook_equation_number="A.50"
    )
)
register_equation(input_resistance_eq)
