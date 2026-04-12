#!/usr/bin/env python3
"""
GRADE Certainty Calculator for RCT Evidence
Applies downgrading and upgrading logic to determine evidence certainty level

Usage:
    python grade_calculator.py appraisal_results.json --output grade_assessment.json
"""

import argparse
import json
import sys
from typing import Dict, List, Optional
from enum import Enum


__version__ = "1.0.0"


class CertaintyLevel(Enum):
    """GRADE certainty levels"""
    HIGH = 4
    MODERATE = 3
    LOW = 2
    VERY_LOW = 1


class DowngradeReason(Enum):
    """Reasons for downgrading evidence certainty"""
    RISK_OF_BIAS = "risk_of_bias"
    INCONSISTENCY = "inconsistency"
    INDIRECTNESS = "indirectness"
    IMPRECISION = "imprecision"
    PUBLICATION_BIAS = "publication_bias"


class UpgradeReason(Enum):
    """Reasons for upgrading evidence certainty (rare for single RCT)"""
    LARGE_EFFECT = "large_effect"
    DOSE_RESPONSE = "dose_response"
    RESIDUAL_CONFOUNDING = "residual_confounding"


class GRADECalculator:
    """Calculate GRADE certainty level for RCT evidence"""

    def __init__(self, starting_level: CertaintyLevel = CertaintyLevel.HIGH):
        """
        Initialize GRADE calculator

        Args:
            starting_level: Starting certainty (HIGH for RCTs)
        """
        self.starting_level = starting_level
        self.current_level = starting_level.value
        self.downgrades: List[Dict] = []
        self.upgrades: List[Dict] = []

    def downgrade(self, reason: DowngradeReason, levels: int = 1, justification: str = ""):
        """
        Downgrade evidence certainty

        Args:
            reason: Reason for downgrading
            levels: Number of levels to downgrade (1 or 2)
            justification: Explanation for downgrade
        """
        if levels not in [1, 2]:
            raise ValueError("Can only downgrade by 1 or 2 levels")

        self.current_level = max(1, self.current_level - levels)
        self.downgrades.append({
            "reason": reason.value,
            "levels": levels,
            "justification": justification
        })

    def upgrade(self, reason: UpgradeReason, levels: int = 1, justification: str = ""):
        """
        Upgrade evidence certainty (rare for single RCT)

        Args:
            reason: Reason for upgrading
            levels: Number of levels to upgrade (1 or 2)
            justification: Explanation for upgrade
        """
        if levels not in [1, 2]:
            raise ValueError("Can only upgrade by 1 or 2 levels")

        self.current_level = min(4, self.current_level + levels)
        self.upgrades.append({
            "reason": reason.value,
            "levels": levels,
            "justification": justification
        })

    def get_certainty_level(self) -> CertaintyLevel:
        """Get current certainty level"""
        return CertaintyLevel(self.current_level)

    def get_symbol(self) -> str:
        """Get GRADE symbol representation"""
        symbols = {
            4: "⊕⊕⊕⊕",
            3: "⊕⊕⊕⊙",
            2: "⊕⊕⊙⊙",
            1: "⊕⊙⊙⊙"
        }
        return symbols[self.current_level]

    def get_interpretation(self) -> str:
        """Get interpretation of certainty level"""
        interpretations = {
            4: "High certainty: Very confident that true effect lies close to estimate",
            3: "Moderate certainty: Moderately confident; true effect likely close but may differ substantially",
            2: "Low certainty: Limited confidence; true effect may differ substantially",
            1: "Very low certainty: Very little confidence; true effect likely substantially different"
        }
        return interpretations[self.current_level]

    def get_summary(self) -> Dict:
        """Get summary of GRADE assessment"""
        return {
            "starting_level": self.starting_level.name,
            "final_level": self.get_certainty_level().name,
            "final_symbol": self.get_symbol(),
            "interpretation": self.get_interpretation(),
            "total_downgrades": sum(d['levels'] for d in self.downgrades),
            "total_upgrades": sum(u['levels'] for u in self.upgrades),
            "downgrades": self.downgrades,
            "upgrades": self.upgrades
        }


def assess_risk_of_bias_downgrade(rob2_data: Dict) -> tuple[int, str]:
    """
    Assess downgrade for risk of bias based on RoB 2.0 assessment

    Args:
        rob2_data: RoB 2.0 assessment results

    Returns:
        Tuple of (downgrade_levels, justification)
    """
    if not rob2_data:
        return 0, "No RoB 2.0 data available"

    # Count domains by risk level
    high_risk_domains = []
    some_concerns_domains = []

    for domain in rob2_data.get('domains', []):
        risk = domain.get('risk_level', '').lower()
        domain_name = domain.get('name', '')

        if risk == 'high risk':
            high_risk_domains.append(domain_name)
        elif risk == 'some concerns':
            some_concerns_domains.append(domain_name)

    # Downgrading logic
    if len(high_risk_domains) >= 2 or any('randomization' in d.lower() or 'selective' in d.lower()
                                           for d in high_risk_domains):
        return 2, f"Very serious risk of bias: HIGH risk in critical domains {', '.join(high_risk_domains)}"
    elif len(high_risk_domains) == 1:
        return 1, f"Serious risk of bias: HIGH risk in {high_risk_domains[0]}"
    elif len(some_concerns_domains) >= 3:
        return 1, f"Serious risk of bias: Some concerns in multiple domains ({len(some_concerns_domains)})"
    elif len(some_concerns_domains) >= 1:
        return 1, f"Serious risk of bias: Some concerns in {', '.join(some_concerns_domains)}"
    else:
        return 0, "Low risk of bias in all domains"


def assess_imprecision_downgrade(effect_data: Dict, sample_size: int) -> tuple[int, str]:
    """
    Assess downgrade for imprecision

    Args:
        effect_data: Effect size data with confidence intervals
        sample_size: Total sample size

    Returns:
        Tuple of (downgrade_levels, justification)
    """
    if not effect_data:
        return 0, "No effect size data available"

    # Check if CI crosses null
    ci_lower = effect_data.get('ci_95', [None, None])[0]
    ci_upper = effect_data.get('ci_95', [None, None])[1]

    if ci_lower is None or ci_upper is None:
        return 1, "Serious imprecision: Confidence intervals not available"

    # For RR/OR, null is 1.0; for differences, null is 0
    is_ratio = effect_data.get('type', 'ratio') == 'ratio'
    null_value = 1.0 if is_ratio else 0.0

    ci_crosses_null = (ci_lower < null_value < ci_upper)

    # Check optimal information size (OIS)
    # Rule of thumb: <400 participants for continuous, <300 events for dichotomous
    ois_not_met = sample_size < 400

    # Very wide CI
    ci_width = abs(ci_upper - ci_lower)
    point_estimate = effect_data.get('value', null_value)
    relative_width = ci_width / abs(point_estimate) if point_estimate != null_value else float('inf')

    very_wide_ci = relative_width > 1.0  # CI width > 100% of point estimate

    # Downgrading logic
    if very_wide_ci and ci_crosses_null:
        return 2, f"Very serious imprecision: Very wide CI ({ci_lower:.2f} to {ci_upper:.2f}) crossing null"
    elif ci_crosses_null or (ois_not_met and very_wide_ci):
        return 1, f"Serious imprecision: CI crosses null ({ci_lower:.2f} to {ci_upper:.2f}) or OIS not met"
    elif ois_not_met:
        return 1, f"Serious imprecision: Optimal information size not met (N={sample_size})"
    else:
        return 0, f"No serious imprecision: Narrow CI excluding null"


def assess_indirectness_downgrade(pico_data: Dict) -> tuple[int, str]:
    """
    Assess downgrade for indirectness (PICO mismatch)

    Args:
        pico_data: PICO assessment data

    Returns:
        Tuple of (downgrade_levels, justification)
    """
    if not pico_data:
        return 0, "No PICO data available"

    issues = []

    if pico_data.get('population_indirect'):
        issues.append("Population differs from target (narrow inclusion criteria)")
    if pico_data.get('intervention_indirect'):
        issues.append("Intervention differs (dose, duration, or delivery)")
    if pico_data.get('comparator_indirect'):
        issues.append("Comparator not optimal (placebo when active comparator relevant)")
    if pico_data.get('outcome_indirect'):
        issues.append("Surrogate outcome instead of patient-important outcome")

    if len(issues) >= 3:
        return 2, f"Very serious indirectness: {'; '.join(issues)}"
    elif len(issues) >= 1:
        return 1, f"Serious indirectness: {'; '.join(issues)}"
    else:
        return 0, "No serious indirectness"


def assess_publication_bias_downgrade(registration_data: Dict, coi_data: Dict) -> tuple[int, str]:
    """
    Assess downgrade for publication bias / selective reporting

    Args:
        registration_data: Trial registration data
        coi_data: Conflicts of interest data

    Returns:
        Tuple of (downgrade_levels, justification)
    """
    issues = []

    if registration_data:
        if not registration_data.get('registered'):
            issues.append("Trial not registered")
        if registration_data.get('retrospective_registration'):
            issues.append("Retrospectively registered")
        if registration_data.get('outcome_switching'):
            issues.append("Reported outcomes differ from registered")

    if coi_data:
        if coi_data.get('high_coi_impact'):
            issues.append("High COI impact with sponsor control")

    if len(issues) >= 2:
        return 1, f"Serious concern for publication bias: {'; '.join(issues)}"
    elif len(issues) >= 1:
        return 1, f"Some concern for publication bias: {issues[0]}"
    else:
        return 0, "No serious concern for publication bias"


def assess_large_effect_upgrade(effect_data: Dict) -> tuple[int, str]:
    """
    Assess upgrade for large magnitude of effect (rare for RCTs)

    Args:
        effect_data: Effect size data

    Returns:
        Tuple of (upgrade_levels, justification)
    """
    if not effect_data:
        return 0, "No effect data"

    rr = effect_data.get('relative_risk', {}).get('value')
    if rr is None:
        return 0, "No relative risk available"

    # Large effect: RR > 2 or < 0.5
    # Very large effect: RR > 5 or < 0.2
    if rr > 5 or rr < 0.2:
        return 2, f"Very large effect (RR = {rr:.2f})"
    elif rr > 2 or rr < 0.5:
        return 1, f"Large effect (RR = {rr:.2f})"
    else:
        return 0, "Effect size does not warrant upgrade"


def apply_grade_from_appraisal(appraisal_data: Dict) -> Dict:
    """
    Apply GRADE assessment based on comprehensive appraisal data

    Args:
        appraisal_data: Complete RCT appraisal results

    Returns:
        GRADE assessment summary
    """
    calculator = GRADECalculator(starting_level=CertaintyLevel.HIGH)

    # Extract relevant data
    rob2_data = appraisal_data.get('rob2_assessment', {})
    effect_data = appraisal_data.get('effect_sizes', {})
    pico_data = appraisal_data.get('pico_assessment', {})
    registration_data = appraisal_data.get('registration', {})
    coi_data = appraisal_data.get('coi_assessment', {})
    sample_size = appraisal_data.get('study_metadata', {}).get('total_participants', 0)

    # Apply downgrades sequentially
    rob_downgrade, rob_justification = assess_risk_of_bias_downgrade(rob2_data)
    if rob_downgrade > 0:
        calculator.downgrade(DowngradeReason.RISK_OF_BIAS, rob_downgrade, rob_justification)

    imprecision_downgrade, imprecision_justification = assess_imprecision_downgrade(effect_data, sample_size)
    if imprecision_downgrade > 0:
        calculator.downgrade(DowngradeReason.IMPRECISION, imprecision_downgrade, imprecision_justification)

    indirectness_downgrade, indirectness_justification = assess_indirectness_downgrade(pico_data)
    if indirectness_downgrade > 0:
        calculator.downgrade(DowngradeReason.INDIRECTNESS, indirectness_downgrade, indirectness_justification)

    pub_bias_downgrade, pub_bias_justification = assess_publication_bias_downgrade(registration_data, coi_data)
    if pub_bias_downgrade > 0:
        calculator.downgrade(DowngradeReason.PUBLICATION_BIAS, pub_bias_downgrade, pub_bias_justification)

    # Consider upgrades (rare for single RCT)
    large_effect_upgrade, large_effect_justification = assess_large_effect_upgrade(effect_data)
    if large_effect_upgrade > 0:
        calculator.upgrade(UpgradeReason.LARGE_EFFECT, large_effect_upgrade, large_effect_justification)

    return calculator.get_summary()


def main():
    parser = argparse.ArgumentParser(
        description="Calculate GRADE certainty level from RCT appraisal data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate GRADE from appraisal results
  python grade_calculator.py appraisal_results.json

  # Save to JSON file
  python grade_calculator.py appraisal_results.json --output grade_assessment.json

GRADE Certainty Levels:
  High (⊕⊕⊕⊕): Very confident in effect estimate
  Moderate (⊕⊕⊕⊙): Moderately confident; may differ substantially
  Low (⊕⊕⊙⊙): Limited confidence; likely differs substantially
  Very Low (⊕⊙⊙⊙): Very little confidence

Downgrading Criteria:
  - Risk of bias (RoB 2.0 assessment)
  - Inconsistency (usually for meta-analysis)
  - Indirectness (PICO mismatch)
  - Imprecision (wide CI, small sample)
  - Publication bias (selective reporting)
        """
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('appraisal_file', type=str,
                       help='JSON file with appraisal results')
    parser.add_argument('--output', '-o', type=str,
                       help='Output JSON file path (default: stdout)')

    args = parser.parse_args()

    try:
        # Load appraisal data
        with open(args.appraisal_file, 'r') as f:
            appraisal_data = json.load(f)

        # Apply GRADE
        grade_assessment = apply_grade_from_appraisal(appraisal_data)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(grade_assessment, f, indent=2)
            print(f"GRADE assessment saved to {args.output}")
        else:
            print(json.dumps(grade_assessment, indent=2))

        # Print summary
        print(f"\nGRADE Assessment Summary:", file=sys.stderr)
        print(f"Final Certainty: {grade_assessment['final_level']} {grade_assessment['final_symbol']}", file=sys.stderr)
        print(f"Interpretation: {grade_assessment['interpretation']}", file=sys.stderr)

        return 0

    except FileNotFoundError:
        print(f"Error: File '{args.appraisal_file}' not found", file=sys.stderr)
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{args.appraisal_file}'", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
