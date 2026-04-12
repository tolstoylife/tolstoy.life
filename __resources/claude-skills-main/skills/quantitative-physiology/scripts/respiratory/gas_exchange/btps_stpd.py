"""
Gas Volume Correction Factors: BTPS, STPD, ATPS

Standard conditions for reporting gas volumes:
- BTPS: Body Temperature (37°C), Pressure (ambient), Saturated with water vapor
- STPD: Standard Temperature (0°C), Pressure (760 mmHg), Dry
- ATPS: Ambient Temperature, Pressure, Saturated (spirometer conditions)

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations A.52-54)
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


# Water vapor pressure at common temperatures (mmHg)
WATER_VAPOR_PRESSURE = {
    20: 17.5,   # Room temperature
    22: 19.8,
    24: 22.4,
    25: 23.8,
    37: 47.0,   # Body temperature
    0: 0.0      # STP (ice point, negligible)
}


def water_vapor_pressure(T: float) -> float:
    """
    Calculate saturated water vapor pressure at given temperature.

    Uses simplified Antoine equation approximation.

    Parameters:
    -----------
    T : float - Temperature (°C)

    Returns:
    --------
    P_H2O : float - Saturated water vapor pressure (mmHg)

    Reference values:
    - 20°C: 17.5 mmHg
    - 25°C: 23.8 mmHg
    - 37°C: 47.0 mmHg (body temperature)
    """
    if T in WATER_VAPOR_PRESSURE:
        return WATER_VAPOR_PRESSURE[T]

    # Antoine equation approximation for water (simplified)
    # P_H2O ≈ exp(20.386 - 5132/(T + 273)) mmHg
    import math
    return math.exp(20.386 - 5132 / (T + 273.15)) * 0.75  # Convert to mmHg


def atps_to_btps(V_atps: float, T_ambient: float, P_ambient: float) -> float:
    """
    Convert volume from ATPS to BTPS conditions.

    ATPS: Ambient Temperature, Pressure, Saturated (spirometer)
    BTPS: Body Temperature (37°C), Pressure, Saturated

    Formula: V_BTPS = V_ATPS × (310/(T_ambient + 273)) × ((P_ambient - P_H2O_ambient)/(P_ambient - 47))

    Parameters:
    -----------
    V_atps : float - Volume at ATPS (L or mL)
    T_ambient : float - Ambient temperature (°C)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    V_btps : float - Volume at BTPS (same units as input)

    Clinical note:
    Lung volumes measured by spirometry are typically at ATPS
    and must be converted to BTPS for physiological calculations.
    """
    T_body = 310.0  # K (37°C)
    T_amb_K = T_ambient + 273.15
    P_H2O_ambient = water_vapor_pressure(T_ambient)
    P_H2O_body = 47.0  # mmHg at 37°C

    correction_factor = (T_body / T_amb_K) * (
        (P_ambient - P_H2O_ambient) / (P_ambient - P_H2O_body)
    )
    return V_atps * correction_factor


def atps_to_stpd(V_atps: float, T_ambient: float, P_ambient: float) -> float:
    """
    Convert volume from ATPS to STPD conditions.

    ATPS: Ambient Temperature, Pressure, Saturated
    STPD: Standard Temperature (0°C), Pressure (760 mmHg), Dry

    Formula: V_STPD = V_ATPS × (273/(T_ambient + 273)) × ((P_ambient - P_H2O_ambient)/760)

    Parameters:
    -----------
    V_atps : float - Volume at ATPS (L or mL)
    T_ambient : float - Ambient temperature (°C)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    V_stpd : float - Volume at STPD (same units as input)

    Clinical note:
    STPD is used for reporting gas consumption (VO₂, VCO₂)
    to allow comparison across different conditions.
    """
    T_standard = 273.15  # K (0°C)
    P_standard = 760.0  # mmHg
    T_amb_K = T_ambient + 273.15
    P_H2O_ambient = water_vapor_pressure(T_ambient)

    correction_factor = (T_standard / T_amb_K) * (
        (P_ambient - P_H2O_ambient) / P_standard
    )
    return V_atps * correction_factor


def btps_to_stpd(V_btps: float, P_ambient: float) -> float:
    """
    Convert volume from BTPS to STPD conditions.

    Formula: V_STPD = V_BTPS × (273/310) × ((P_ambient - 47)/760)

    Parameters:
    -----------
    V_btps : float - Volume at BTPS (L or mL)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    V_stpd : float - Volume at STPD (same units as input)

    Note: Body temperature assumed to be 37°C (P_H2O = 47 mmHg)
    """
    T_body = 310.0  # K
    T_standard = 273.15  # K
    P_standard = 760.0  # mmHg
    P_H2O_body = 47.0  # mmHg at 37°C

    correction_factor = (T_standard / T_body) * (
        (P_ambient - P_H2O_body) / P_standard
    )
    return V_btps * correction_factor


def stpd_to_btps(V_stpd: float, P_ambient: float) -> float:
    """
    Convert volume from STPD to BTPS conditions.

    Formula: V_BTPS = V_STPD × (310/273) × (760/(P_ambient - 47))

    Parameters:
    -----------
    V_stpd : float - Volume at STPD (L or mL)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    V_btps : float - Volume at BTPS (same units as input)
    """
    T_body = 310.0  # K
    T_standard = 273.15  # K
    P_standard = 760.0  # mmHg
    P_H2O_body = 47.0  # mmHg at 37°C

    correction_factor = (T_body / T_standard) * (
        P_standard / (P_ambient - P_H2O_body)
    )
    return V_stpd * correction_factor


def btps_correction_factor(T_ambient: float, P_ambient: float) -> float:
    """
    Calculate the ATPS to BTPS correction factor.

    Parameters:
    -----------
    T_ambient : float - Ambient temperature (°C)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    factor : float - Multiply ATPS volume by this to get BTPS

    Typical values:
    - 22°C, 760 mmHg → factor ≈ 1.10
    - 25°C, 760 mmHg → factor ≈ 1.08
    """
    return atps_to_btps(1.0, T_ambient, P_ambient)


def stpd_correction_factor(T_ambient: float, P_ambient: float) -> float:
    """
    Calculate the ATPS to STPD correction factor.

    Parameters:
    -----------
    T_ambient : float - Ambient temperature (°C)
    P_ambient : float - Ambient barometric pressure (mmHg)

    Returns:
    --------
    factor : float - Multiply ATPS volume by this to get STPD

    Typical values:
    - 22°C, 760 mmHg → factor ≈ 0.89
    - 25°C, 760 mmHg → factor ≈ 0.88
    """
    return atps_to_stpd(1.0, T_ambient, P_ambient)


# Create and register BTPS conversion equation
btps_conversion_eq = create_equation(
    id="respiratory.gas_exchange.btps_conversion",
    name="ATPS to BTPS Gas Volume Conversion",
    category=EquationCategory.RESPIRATORY,
    latex=r"V_{BTPS} = V_{ATPS} \times \frac{310}{T_{amb} + 273} \times \frac{P_{amb} - P_{H_2O}^{amb}}{P_{amb} - 47}",
    simplified="V_BTPS = V_ATPS × (310/(T+273)) × ((P-P_H2O)/(P-47))",
    description="Convert gas volumes from ambient spirometer to body conditions",
    compute_func=atps_to_btps,
    parameters=[
        Parameter(
            name="V_atps",
            description="Volume at ambient temperature, pressure, saturated",
            units="L",
            symbol="V_{ATPS}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="T_ambient",
            description="Ambient temperature",
            units="°C",
            symbol="T_{amb}",
            default_value=22.0,
            physiological_range=(15.0, 35.0)
        ),
        Parameter(
            name="P_ambient",
            description="Ambient barometric pressure",
            units="mmHg",
            symbol="P_{amb}",
            default_value=760.0,
            physiological_range=(600.0, 800.0)
        ),
    ],
    depends_on=["foundations.thermodynamics.ideal_gas_law"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2",
        textbook_equation_number="A.52"
    )
)
register_equation(btps_conversion_eq)


# Create and register STPD conversion equation
stpd_conversion_eq = create_equation(
    id="respiratory.gas_exchange.stpd_conversion",
    name="ATPS to STPD Gas Volume Conversion",
    category=EquationCategory.RESPIRATORY,
    latex=r"V_{STPD} = V_{ATPS} \times \frac{273}{T_{amb} + 273} \times \frac{P_{amb} - P_{H_2O}^{amb}}{760}",
    simplified="V_STPD = V_ATPS × (273/(T+273)) × ((P-P_H2O)/760)",
    description="Convert gas volumes from ambient to standard temperature/pressure dry",
    compute_func=atps_to_stpd,
    parameters=[
        Parameter(
            name="V_atps",
            description="Volume at ambient temperature, pressure, saturated",
            units="L",
            symbol="V_{ATPS}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="T_ambient",
            description="Ambient temperature",
            units="°C",
            symbol="T_{amb}",
            default_value=22.0,
            physiological_range=(15.0, 35.0)
        ),
        Parameter(
            name="P_ambient",
            description="Ambient barometric pressure",
            units="mmHg",
            symbol="P_{amb}",
            default_value=760.0,
            physiological_range=(600.0, 800.0)
        ),
    ],
    depends_on=["foundations.thermodynamics.ideal_gas_law"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2",
        textbook_equation_number="A.53"
    )
)
register_equation(stpd_conversion_eq)
