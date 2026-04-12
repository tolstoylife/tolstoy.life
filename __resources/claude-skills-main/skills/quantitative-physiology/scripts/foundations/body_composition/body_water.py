"""
Body Water Compartment Equations

Equations for calculating body fluid compartments including intracellular
fluid (ICF), interstitial fluid (ISF), plasma volume, and lean body mass.

Source: Quantitative Human Physiology 3rd Edition, Appendix I (Equations 108-110)
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def intracellular_fluid_volume(TBW: float, ECF: float) -> float:
    """
    Calculate intracellular fluid (ICF) volume.

    Formula: ICF = TBW - ECF

    Intracellular fluid is the largest body fluid compartment (~2/3 of TBW),
    containing the fluid within all cells. Typical values:
    - Males: ~25 L (42% of body weight)
    - Females: ~20 L (35% of body weight)

    Parameters:
    -----------
    TBW : float - Total body water (L)
    ECF : float - Extracellular fluid volume (L)

    Returns:
    --------
    ICF : float - Intracellular fluid volume (L)

    Clinical relevance:
    - Hyponatremia causes cell swelling (water moves into ICF)
    - Hypernatremia causes cell shrinkage (water moves out of ICF)
    - Brain ICF changes cause neurological symptoms
    """
    return TBW - ECF


def interstitial_fluid_volume(ECF: float, PV: float) -> float:
    """
    Calculate interstitial fluid (ISF) volume.

    Formula: ISF = ECF - PV

    Interstitial fluid is the fluid between cells, outside blood vessels.
    Comprises ~75% of ECF (~3/4 of ECF). Typical values:
    - Males: ~10.5 L (17.5% of body weight)
    - Females: ~7.5 L (15% of body weight)

    Parameters:
    -----------
    ECF : float - Extracellular fluid volume (L)
    PV : float - Plasma volume (L)

    Returns:
    --------
    ISF : float - Interstitial fluid volume (L)

    Clinical relevance:
    - Edema represents expanded ISF
    - Starling forces govern ISF-plasma exchange
    - Lymphatic system returns ISF to circulation
    """
    return ECF - PV


def plasma_volume(TBW: float, hematocrit: float = 0.45) -> float:
    """
    Estimate plasma volume from total body water.

    Formula: PV ≈ TBW × 0.07 (approximate)

    More accurately: PV = BV × (1 - Hct)
    where BV ≈ TBW × 0.12 for typical body composition.

    Typical plasma volume: 3-3.5 L (4-5% of body weight)

    Parameters:
    -----------
    TBW : float - Total body water (L)
    hematocrit : float - Hematocrit fraction (default 0.45)

    Returns:
    --------
    PV : float - Plasma volume (L)
    """
    # Blood volume is approximately 12% of TBW
    blood_volume = TBW * 0.12
    return blood_volume * (1 - hematocrit)


def extracellular_fluid_volume(TBW: float) -> float:
    """
    Estimate extracellular fluid (ECF) volume from total body water.

    Formula: ECF ≈ TBW / 3

    ECF is approximately 1/3 of TBW, comprising:
    - Plasma volume (~3 L)
    - Interstitial fluid (~10-11 L)
    - Transcellular fluid (~1 L)

    Typical values:
    - Males: ~14 L (23% of body weight)
    - Females: ~10 L (20% of body weight)

    Parameters:
    -----------
    TBW : float - Total body water (L)

    Returns:
    --------
    ECF : float - Extracellular fluid volume (L)
    """
    return TBW / 3


def total_body_water(body_weight: float, fraction: float = 0.60) -> float:
    """
    Calculate total body water from body weight.

    Formula: TBW = body_weight × fraction

    Fraction varies by:
    - Sex: Males ~60%, Females ~50% (more adipose tissue)
    - Age: Decreases with age (infants ~75%, elderly ~50%)
    - Body composition: Lean individuals higher, obese lower

    Parameters:
    -----------
    body_weight : float - Body weight (kg)
    fraction : float - TBW fraction of body weight (default 0.60)

    Returns:
    --------
    TBW : float - Total body water (L or kg, since 1 L water ≈ 1 kg)
    """
    return body_weight * fraction


def lean_body_mass_from_tbw(TBW: float) -> float:
    """
    Calculate lean body mass from total body water.

    Formula: LBM = TBW / 0.732

    Lean tissue is approximately 73.2% water (constant across individuals),
    so LBM can be estimated from TBW measurement (dilution method).

    Parameters:
    -----------
    TBW : float - Total body water (L or kg)

    Returns:
    --------
    LBM : float - Lean body mass (kg)

    Clinical applications:
    - Drug dosing (many drugs distribute in lean mass)
    - Nutritional assessment
    - Metabolic rate estimation (correlates with LBM)
    """
    return TBW / 0.732


def body_fat_percentage(body_weight: float, LBM: float) -> float:
    """
    Calculate body fat percentage from body weight and lean body mass.

    Formula: Fat% = (body_weight - LBM) / body_weight × 100

    Parameters:
    -----------
    body_weight : float - Total body weight (kg)
    LBM : float - Lean body mass (kg)

    Returns:
    --------
    fat_percentage : float - Body fat as percentage of total weight

    Reference ranges:
    - Essential fat: 2-5% (men), 10-13% (women)
    - Athletes: 6-13% (men), 14-20% (women)
    - Fitness: 14-17% (men), 21-24% (women)
    - Average: 18-24% (men), 25-31% (women)
    """
    return ((body_weight - LBM) / body_weight) * 100


# Create and register ICF volume equation
icf_volume_eq = create_equation(
    id="foundations.body_composition.icf_volume",
    name="Intracellular Fluid Volume",
    category=EquationCategory.FOUNDATIONS,
    latex=r"V_{ICF} = V_{TBW} - V_{ECF}",
    simplified="ICF = TBW - ECF",
    description="Volume of fluid within all cells, approximately 2/3 of total body water",
    compute_func=intracellular_fluid_volume,
    parameters=[
        Parameter(
            name="TBW",
            description="Total body water",
            units="L",
            symbol="V_{TBW}",
            physiological_range=(25.0, 50.0)  # Adult range
        ),
        Parameter(
            name="ECF",
            description="Extracellular fluid volume",
            units="L",
            symbol="V_{ECF}",
            physiological_range=(10.0, 20.0)  # Adult range
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1",
        textbook_equation_number="A.108"
    )
)
register_equation(icf_volume_eq)


# Create and register ISF volume equation
isf_volume_eq = create_equation(
    id="foundations.body_composition.isf_volume",
    name="Interstitial Fluid Volume",
    category=EquationCategory.FOUNDATIONS,
    latex=r"V_{ISF} = V_{ECF} - V_{plasma}",
    simplified="ISF = ECF - PV",
    description="Volume of fluid between cells, outside blood vessels (~75% of ECF)",
    compute_func=interstitial_fluid_volume,
    parameters=[
        Parameter(
            name="ECF",
            description="Extracellular fluid volume",
            units="L",
            symbol="V_{ECF}",
            physiological_range=(10.0, 20.0)
        ),
        Parameter(
            name="PV",
            description="Plasma volume",
            units="L",
            symbol="V_{plasma}",
            physiological_range=(2.5, 4.5)  # Normal plasma volume range
        ),
    ],
    depends_on=["foundations.body_composition.icf_volume"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1",
        textbook_equation_number="A.109"
    )
)
register_equation(isf_volume_eq)


# Create and register lean body mass equation
lean_body_mass_eq = create_equation(
    id="foundations.body_composition.lean_body_mass",
    name="Lean Body Mass from Total Body Water",
    category=EquationCategory.FOUNDATIONS,
    latex=r"LBM = \frac{TBW}{0.732}",
    simplified="LBM = TBW / 0.732",
    description="Lean tissue is 73.2% water, allowing LBM estimation from TBW",
    compute_func=lean_body_mass_from_tbw,
    parameters=[
        Parameter(
            name="TBW",
            description="Total body water",
            units="L",
            symbol="TBW",
            physiological_range=(25.0, 50.0)  # Adult range
        ),
    ],
    depends_on=["foundations.body_composition.icf_volume", "foundations.body_composition.isf_volume"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1",
        textbook_equation_number="A.110"
    )
)
register_equation(lean_body_mass_eq)
