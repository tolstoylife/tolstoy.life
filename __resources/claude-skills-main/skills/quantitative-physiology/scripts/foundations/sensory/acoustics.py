"""
Acoustics Equations (Decibel Scale, Sound Intensity)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 29-30)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def sound_intensity_level(I: float, I_0: float = 1e-12) -> float:
    """
    Calculate sound intensity level in decibels (dB SPL).

    Formula: L = 10 × log₁₀(I/I₀)

    The decibel scale compresses the enormous range of audible
    intensities (10^12 range) into a manageable 0-120 dB scale.

    Parameters:
    -----------
    I : float - Sound intensity (W/m²)
    I_0 : float - Reference intensity (W/m²), default 10⁻¹² (hearing threshold)

    Returns:
    --------
    L : float - Sound intensity level (dB SPL)

    Reference points:
    - 0 dB: Threshold of hearing (I₀ = 10⁻¹² W/m²)
    - 60 dB: Normal conversation
    - 90 dB: Power tools (OSHA limit for 8-hour exposure)
    - 120 dB: Threshold of pain
    - 140 dB: Jet engine (risk of instant damage)
    """
    return 10 * np.log10(I / I_0)


def intensity_from_decibels(L: float, I_0: float = 1e-12) -> float:
    """
    Calculate sound intensity from decibel level.

    Formula: I = I₀ × 10^(L/10)

    Parameters:
    -----------
    L : float - Sound intensity level (dB SPL)
    I_0 : float - Reference intensity (W/m²), default 10⁻¹²

    Returns:
    --------
    I : float - Sound intensity (W/m²)
    """
    return I_0 * 10**(L / 10)


def sound_pressure_level(P: float, P_0: float = 20e-6) -> float:
    """
    Calculate sound pressure level in decibels.

    Formula: SPL = 20 × log₁₀(P/P₀)

    Since intensity ∝ pressure², SPL uses factor of 20 instead of 10.

    Parameters:
    -----------
    P : float - Sound pressure (Pa)
    P_0 : float - Reference pressure (Pa), default 20 μPa (hearing threshold)

    Returns:
    --------
    SPL : float - Sound pressure level (dB SPL)
    """
    return 20 * np.log10(P / P_0)


def pressure_from_spl(SPL: float, P_0: float = 20e-6) -> float:
    """
    Calculate sound pressure from SPL.

    Formula: P = P₀ × 10^(SPL/20)

    Parameters:
    -----------
    SPL : float - Sound pressure level (dB)
    P_0 : float - Reference pressure (Pa), default 20 μPa

    Returns:
    --------
    P : float - Sound pressure (Pa)
    """
    return P_0 * 10**(SPL / 20)


def combine_sound_levels(L1: float, L2: float) -> float:
    """
    Calculate combined sound level from two sources.

    Formula: L_total = 10 × log₁₀(10^(L₁/10) + 10^(L₂/10))

    Sound intensities add linearly, not decibel values.

    Parameters:
    -----------
    L1 : float - First sound level (dB)
    L2 : float - Second sound level (dB)

    Returns:
    --------
    L_total : float - Combined sound level (dB)

    Note: Two equal sources add 3 dB (e.g., 60 + 60 = 63 dB)
    """
    return 10 * np.log10(10**(L1/10) + 10**(L2/10))


def hearing_threshold_shift(exposure_dB: float, duration_hours: float) -> float:
    """
    Estimate temporary threshold shift (TTS) from noise exposure.

    Simplified model based on OSHA permissible exposure limits.
    85 dB for 8 hours is reference level.

    Formula: TTS ∝ (L - 85) × log(t)  (simplified approximation)

    Parameters:
    -----------
    exposure_dB : float - Exposure level (dB SPL)
    duration_hours : float - Exposure duration (hours)

    Returns:
    --------
    TTS : float - Estimated temporary threshold shift (dB)
    """
    if exposure_dB < 85:
        return 0.0
    # Simplified model - actual TTS depends on many factors
    return (exposure_dB - 85) * np.log10(duration_hours + 1) * 2


def intensity_distance_ratio(I1: float, r1: float, r2: float) -> float:
    """
    Calculate intensity at different distance (inverse square law).

    Formula: I₂ = I₁ × (r₁/r₂)²

    Sound intensity decreases with square of distance from source
    (in free field, without reflections).

    Parameters:
    -----------
    I1 : float - Intensity at distance r1 (W/m²)
    r1 : float - Reference distance (m)
    r2 : float - New distance (m)

    Returns:
    --------
    I2 : float - Intensity at distance r2 (W/m²)
    """
    return I1 * (r1 / r2)**2


# Create and register sound intensity level equation
sound_intensity_level_eq = create_equation(
    id="foundations.sensory.sound_intensity_level",
    name="Sound Intensity Level (Decibels)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"L = 10 \log_{10}\left(\frac{I}{I_0}\right)",
    simplified="L = 10 × log₁₀(I/I₀)",
    description="Sound intensity expressed in decibels relative to hearing threshold",
    compute_func=sound_intensity_level,
    parameters=[
        Parameter(
            name="I",
            description="Sound intensity",
            units="W/m²",
            symbol="I",
            physiological_range=(1e-12, 10.0)  # Threshold to painful
        ),
        Parameter(
            name="I_0",
            description="Reference intensity (hearing threshold)",
            units="W/m²",
            symbol="I_0",
            default_value=1e-12,
            physiological_range=(1e-13, 1e-11)
        ),
    ],
    depends_on=["foundations.sensory.fechner_law"],  # Decibel scale is logarithmic like Fechner's law
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.8",
        textbook_equation_number="A.29"
    )
)
register_equation(sound_intensity_level_eq)


# Create and register sound pressure level equation
sound_pressure_level_eq = create_equation(
    id="foundations.sensory.sound_pressure_level",
    name="Sound Pressure Level (SPL)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"SPL = 20 \log_{10}\left(\frac{P}{P_0}\right)",
    simplified="SPL = 20 × log₁₀(P/P₀)",
    description="Sound pressure expressed in decibels (factor of 20 due to I ∝ P²)",
    compute_func=sound_pressure_level,
    parameters=[
        Parameter(
            name="P",
            description="Sound pressure",
            units="Pa",
            symbol="P",
            physiological_range=(2e-5, 200.0)  # 0 to 140 dB SPL
        ),
        Parameter(
            name="P_0",
            description="Reference pressure (hearing threshold)",
            units="Pa",
            symbol="P_0",
            default_value=20e-6,  # 20 μPa
            physiological_range=(1e-5, 5e-5)
        ),
    ],
    depends_on=["foundations.sensory.sound_intensity_level"],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="1.8",
        textbook_equation_number="A.30"
    )
)
register_equation(sound_pressure_level_eq)
