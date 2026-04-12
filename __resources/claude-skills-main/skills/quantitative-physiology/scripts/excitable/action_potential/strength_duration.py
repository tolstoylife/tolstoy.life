"""
Strength-Duration Curve (Weiss Equation)

Describes the relationship between stimulus strength and duration
required to elicit an action potential in excitable tissues.

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 45-47)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def threshold_current(rheobase: float, chronaxie: float, t: float) -> float:
    """
    Calculate threshold stimulus current using Weiss strength-duration equation.

    Formula: I_th = I_rh × (1 + τ_c/t)

    The strength-duration curve shows that:
    - Short pulses require higher currents
    - Long pulses asymptote to rheobase
    - Chronaxie is the pulse width at 2× rheobase

    Parameters:
    -----------
    rheobase : float - Rheobase current (minimum current at infinite duration, A)
    chronaxie : float - Chronaxie (time constant of excitability, s)
    t : float - Stimulus pulse duration (s)

    Returns:
    --------
    I_th : float - Threshold stimulus current (A)

    Clinical relevance:
    - Pacemaker pulse programming (typically 0.4-1.0 ms)
    - Neurostimulator parameter optimization
    - Assessment of nerve excitability
    """
    return rheobase * (1 + chronaxie / t)


def threshold_charge(rheobase: float, chronaxie: float, t: float) -> float:
    """
    Calculate threshold charge using Weiss equation.

    Formula: Q_th = I_rh × (t + τ_c)

    Charge is the integral of current over time. The minimum charge
    needed for excitation increases with pulse duration but never
    equals zero (requires at least I_rh × τ_c at short durations).

    Parameters:
    -----------
    rheobase : float - Rheobase current (A)
    chronaxie : float - Chronaxie (s)
    t : float - Stimulus pulse duration (s)

    Returns:
    --------
    Q_th : float - Threshold charge (C = A·s)
    """
    return rheobase * (t + chronaxie)


def rheobase_from_curve(I_th1: float, t1: float, I_th2: float, t2: float) -> float:
    """
    Estimate rheobase from two points on strength-duration curve.

    Formula: I_rh = (I_th1 × t1 - I_th2 × t2) / (t1 - t2)

    Parameters:
    -----------
    I_th1 : float - First threshold current (A)
    t1 : float - First pulse duration (s)
    I_th2 : float - Second threshold current (A)
    t2 : float - Second pulse duration (s)

    Returns:
    --------
    I_rh : float - Estimated rheobase (A)
    """
    return (I_th1 * t1 - I_th2 * t2) / (t1 - t2)


def chronaxie_from_curve(I_th1: float, t1: float, I_th2: float, t2: float) -> float:
    """
    Estimate chronaxie from two points on strength-duration curve.

    Formula: τ_c = (I_th1 - I_rh) × t1 / I_rh

    Parameters:
    -----------
    I_th1 : float - First threshold current (A)
    t1 : float - First pulse duration (s)
    I_th2 : float - Second threshold current (A)
    t2 : float - Second pulse duration (s)

    Returns:
    --------
    τ_c : float - Estimated chronaxie (s)
    """
    rheobase = rheobase_from_curve(I_th1, t1, I_th2, t2)
    return (I_th1 - rheobase) * t1 / rheobase


def lapicque_equation(rheobase: float, tau_m: float, t: float) -> float:
    """
    Calculate threshold using Lapicque's exponential model.

    Formula: I_th = I_rh / (1 - e^(-t/τ_m))

    Alternative to Weiss equation based on membrane time constant.
    More accurate for very short pulses but more complex.

    Parameters:
    -----------
    rheobase : float - Rheobase current (A)
    tau_m : float - Membrane time constant (s)
    t : float - Stimulus pulse duration (s)

    Returns:
    --------
    I_th : float - Threshold stimulus current (A)
    """
    return rheobase / (1 - np.exp(-t / tau_m))


# Create and register strength-duration (Weiss) equation
strength_duration_eq = create_equation(
    id="excitable.action_potential.strength_duration",
    name="Strength-Duration Curve (Weiss Equation)",
    category=EquationCategory.EXCITABLE,
    latex=r"I_{th} = I_{rh} \left(1 + \frac{\tau_c}{t}\right)",
    simplified="I_th = I_rh × (1 + τ_c/t)",
    description="Threshold stimulus current as function of pulse duration (Weiss equation)",
    compute_func=threshold_current,
    parameters=[
        Parameter(
            name="rheobase",
            description="Rheobase (minimum threshold current at infinite duration)",
            units="A",
            symbol="I_{rh}",
            physiological_range=(1e-9, 1e-3)  # nA to mA for neural stimulation
        ),
        Parameter(
            name="chronaxie",
            description="Chronaxie (pulse duration at 2× rheobase)",
            units="s",
            symbol=r"\tau_c",
            physiological_range=(1e-5, 1e-2)  # 10 μs to 10 ms typical range
        ),
        Parameter(
            name="t",
            description="Stimulus pulse duration",
            units="s",
            symbol="t",
            physiological_range=(1e-6, 1.0)  # 1 μs to 1 s
        ),
    ],
    depends_on=["respiratory.mechanics.time_constant"],  # Related to membrane time constant
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.3",
        textbook_equation_number="A.45"
    )
)
register_equation(strength_duration_eq)


# Create and register threshold charge equation
threshold_charge_eq = create_equation(
    id="excitable.action_potential.threshold_charge",
    name="Threshold Charge (Weiss)",
    category=EquationCategory.EXCITABLE,
    latex=r"Q_{th} = I_{rh}(t + \tau_c)",
    simplified="Q_th = I_rh × (t + τ_c)",
    description="Minimum charge required for excitation as function of pulse duration",
    compute_func=threshold_charge,
    parameters=[
        Parameter(
            name="rheobase",
            description="Rheobase current",
            units="A",
            symbol="I_{rh}",
            physiological_range=(1e-9, 1e-3)
        ),
        Parameter(
            name="chronaxie",
            description="Chronaxie time constant",
            units="s",
            symbol=r"\tau_c",
            physiological_range=(1e-5, 1e-2)
        ),
        Parameter(
            name="t",
            description="Stimulus pulse duration",
            units="s",
            symbol="t",
            physiological_range=(1e-6, 1.0)
        ),
    ],
    depends_on=["excitable.action_potential.strength_duration"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.3",
        textbook_equation_number="A.46"
    )
)
register_equation(threshold_charge_eq)


# Create and register Lapicque equation
lapicque_eq = create_equation(
    id="excitable.action_potential.lapicque_equation",
    name="Lapicque Strength-Duration Equation",
    category=EquationCategory.EXCITABLE,
    latex=r"I_{th} = \frac{I_{rh}}{1 - e^{-t/\tau_m}}",
    simplified="I_th = I_rh / (1 - e^(-t/τ_m))",
    description="Exponential strength-duration model based on membrane time constant",
    compute_func=lapicque_equation,
    parameters=[
        Parameter(
            name="rheobase",
            description="Rheobase current",
            units="A",
            symbol="I_{rh}",
            physiological_range=(1e-9, 1e-3)
        ),
        Parameter(
            name="tau_m",
            description="Membrane time constant",
            units="s",
            symbol=r"\tau_m",
            physiological_range=(1e-4, 0.1)  # 0.1 ms to 100 ms
        ),
        Parameter(
            name="t",
            description="Stimulus pulse duration",
            units="s",
            symbol="t",
            physiological_range=(1e-6, 1.0)
        ),
    ],
    depends_on=["respiratory.mechanics.time_constant", "excitable.action_potential.strength_duration"],
    metadata=EquationMetadata(
        source_unit=3,
        source_chapter="3.3",
        textbook_equation_number="A.47"
    )
)
register_equation(lapicque_eq)
