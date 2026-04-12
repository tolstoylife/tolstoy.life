#!/usr/bin/env python3
"""
RCT Effect Size Calculator
Calculates NNT, NNH, ARR, RRR, OR→RR conversions, and other effect metrics

Usage:
    python effect_size_calculator.py --intervention-events 42 --intervention-total 150 \
                                      --control-events 68 --control-total 150 \
                                      --output effect_sizes.json
"""

import argparse
import json
import sys
from typing import Dict, Optional, Tuple
import math


__version__ = "1.0.0"


class EffectSizeCalculator:
    """Calculate various effect size metrics from 2x2 contingency table data"""

    def __init__(self, intervention_events: int, intervention_total: int,
                 control_events: int, control_total: int):
        """
        Initialize calculator with RCT data

        Args:
            intervention_events: Number of events in intervention group
            intervention_total: Total participants in intervention group
            control_events: Number of events in control group
            control_total: Total participants in control group
        """
        self.ie = intervention_events
        self.it = intervention_total
        self.ce = control_events
        self.ct = control_total

        # Validate inputs
        if self.ie < 0 or self.ce < 0:
            raise ValueError("Number of events cannot be negative")
        if self.it <= 0 or self.ct <= 0:
            raise ValueError("Total participants must be positive")
        if self.ie > self.it or self.ce > self.ct:
            raise ValueError("Events cannot exceed total participants")

    @property
    def intervention_rate(self) -> float:
        """Event rate in intervention group (CER)"""
        return self.ie / self.it

    @property
    def control_rate(self) -> float:
        """Event rate in control group (CER)"""
        return self.ce / self.ct

    def absolute_risk_reduction(self) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate Absolute Risk Reduction (ARR) with 95% CI
        ARR = CER - IER
        Positive ARR indicates intervention reduces risk

        Returns:
            Tuple of (ARR, (CI_lower, CI_upper))
        """
        arr = self.control_rate - self.intervention_rate

        # 95% CI using Newcombe method
        se = math.sqrt(
            (self.ie * (self.it - self.ie)) / (self.it ** 3) +
            (self.ce * (self.ct - self.ce)) / (self.ct ** 3)
        )
        ci_lower = arr - 1.96 * se
        ci_upper = arr + 1.96 * se

        return arr, (ci_lower, ci_upper)

    def relative_risk(self) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate Relative Risk (RR) with 95% CI
        RR = IER / CER
        RR < 1 indicates intervention reduces risk

        Returns:
            Tuple of (RR, (CI_lower, CI_upper))
        """
        if self.ce == 0:
            return None, (None, None)  # Undefined if no control events

        rr = self.intervention_rate / self.control_rate

        # 95% CI using log transformation
        if self.ie == 0 or self.ce == 0:
            return rr, (None, None)

        log_rr = math.log(rr)
        se_log_rr = math.sqrt(
            (1 / self.ie) - (1 / self.it) +
            (1 / self.ce) - (1 / self.ct)
        )
        ci_lower = math.exp(log_rr - 1.96 * se_log_rr)
        ci_upper = math.exp(log_rr + 1.96 * se_log_rr)

        return rr, (ci_lower, ci_upper)

    def relative_risk_reduction(self) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate Relative Risk Reduction (RRR) with 95% CI
        RRR = (CER - IER) / CER = 1 - RR
        Positive RRR indicates intervention reduces risk

        Returns:
            Tuple of (RRR, (CI_lower, CI_upper))
        """
        if self.ce == 0:
            return None, (None, None)

        rr, (rr_ci_lower, rr_ci_upper) = self.relative_risk()
        if rr is None:
            return None, (None, None)

        rrr = 1 - rr
        ci_lower = 1 - rr_ci_upper
        ci_upper = 1 - rr_ci_lower

        return rrr, (ci_lower, ci_upper)

    def odds_ratio(self) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate Odds Ratio (OR) with 95% CI
        OR = (IE * CN) / (IN * CE) where N = non-events
        OR < 1 indicates intervention reduces odds

        Returns:
            Tuple of (OR, (CI_lower, CI_upper))
        """
        ie_n = self.it - self.ie  # Intervention non-events
        ce_n = self.ct - self.ce  # Control non-events

        if ie_n == 0 or ce_n == 0:
            return None, (None, None)

        odds_ratio = (self.ie * ce_n) / (ie_n * self.ce) if self.ce > 0 else None

        if odds_ratio is None:
            return None, (None, None)

        # 95% CI using log transformation
        if self.ie == 0 or self.ce == 0:
            return odds_ratio, (None, None)

        log_or = math.log(odds_ratio)
        se_log_or = math.sqrt(
            (1 / self.ie) + (1 / ie_n) +
            (1 / self.ce) + (1 / ce_n)
        )
        ci_lower = math.exp(log_or - 1.96 * se_log_or)
        ci_upper = math.exp(log_or + 1.96 * se_log_or)

        return odds_ratio, (ci_lower, ci_upper)

    def or_to_rr_conversion(self, or_value: float, control_risk: float) -> float:
        """
        Convert Odds Ratio to Relative Risk (Zhang and Yu method)
        RR = OR / (1 - CER + (CER * OR))

        Args:
            or_value: Odds ratio to convert
            control_risk: Control event rate (CER)

        Returns:
            Converted relative risk
        """
        if control_risk is None or or_value is None:
            return None
        return or_value / (1 - control_risk + (control_risk * or_value))

    def number_needed_to_treat(self) -> Tuple[Optional[float], Tuple[Optional[float], Optional[float]]]:
        """
        Calculate Number Needed to Treat (NNT) with 95% CI
        NNT = 1 / ARR
        Positive NNT: intervention beneficial
        Negative NNT: intervention harmful (report as NNH)

        Returns:
            Tuple of (NNT, (CI_lower, CI_upper))
        """
        arr, (arr_ci_lower, arr_ci_upper) = self.absolute_risk_reduction()

        if arr == 0:
            return None, (None, None)  # Infinite NNT

        nnt = 1 / arr

        # CI for NNT (reciprocal of ARR CI, bounds reversed)
        if arr_ci_lower == 0 or arr_ci_upper == 0:
            ci_lower, ci_upper = None, None
        else:
            ci_lower = 1 / arr_ci_upper
            ci_upper = 1 / arr_ci_lower

        return nnt, (ci_lower, ci_upper)

    def number_needed_to_harm(self) -> Tuple[Optional[float], Tuple[Optional[float], Optional[float]]]:
        """
        Calculate Number Needed to Harm (NNH) with 95% CI
        NNH = 1 / ARI where ARI = IER - CER (opposite of ARR)

        Returns:
            Tuple of (NNH, (CI_lower, CI_upper))
        """
        ari = self.intervention_rate - self.control_rate  # Absolute Risk Increase

        if ari == 0:
            return None, (None, None)

        nnh = 1 / ari

        # CI for NNH
        se = math.sqrt(
            (self.ie * (self.it - self.ie)) / (self.it ** 3) +
            (self.ce * (self.ct - self.ce)) / (self.ct ** 3)
        )
        ari_ci_lower = ari - 1.96 * se
        ari_ci_upper = ari + 1.96 * se

        if ari_ci_lower == 0 or ari_ci_upper == 0:
            ci_lower, ci_upper = None, None
        else:
            ci_lower = 1 / ari_ci_upper
            ci_upper = 1 / ari_ci_lower

        return nnh, (ci_lower, ci_upper)

    def calculate_all(self) -> Dict:
        """Calculate all effect size metrics"""
        arr, arr_ci = self.absolute_risk_reduction()
        rr, rr_ci = self.relative_risk()
        rrr, rrr_ci = self.relative_risk_reduction()
        odds_ratio, or_ci = self.odds_ratio()
        nnt, nnt_ci = self.number_needed_to_treat()
        nnh, nnh_ci = self.number_needed_to_harm()

        # Convert OR to RR if both available
        rr_from_or = self.or_to_rr_conversion(odds_ratio, self.control_rate) if odds_ratio else None

        return {
            "input_data": {
                "intervention_events": self.ie,
                "intervention_total": self.it,
                "control_events": self.ce,
                "control_total": self.ct
            },
            "event_rates": {
                "intervention_rate": round(self.intervention_rate, 4),
                "control_rate": round(self.control_rate, 4)
            },
            "absolute_measures": {
                "absolute_risk_reduction": {
                    "value": round(arr, 4) if arr else None,
                    "ci_95": [round(arr_ci[0], 4) if arr_ci[0] else None,
                             round(arr_ci[1], 4) if arr_ci[1] else None],
                    "interpretation": "Positive = Intervention reduces risk"
                }
            },
            "relative_measures": {
                "relative_risk": {
                    "value": round(rr, 4) if rr else None,
                    "ci_95": [round(rr_ci[0], 4) if rr_ci[0] else None,
                             round(rr_ci[1], 4) if rr_ci[1] else None],
                    "interpretation": "<1 = Intervention reduces risk"
                },
                "relative_risk_reduction": {
                    "value": round(rrr, 4) if rrr else None,
                    "ci_95": [round(rrr_ci[0], 4) if rrr_ci[0] else None,
                             round(rrr_ci[1], 4) if rrr_ci[1] else None],
                    "interpretation": "Positive = Intervention reduces risk"
                },
                "odds_ratio": {
                    "value": round(odds_ratio, 4) if odds_ratio else None,
                    "ci_95": [round(or_ci[0], 4) if or_ci[0] else None,
                             round(or_ci[1], 4) if or_ci[1] else None],
                    "interpretation": "<1 = Intervention reduces odds"
                },
                "rr_converted_from_or": {
                    "value": round(rr_from_or, 4) if rr_from_or else None,
                    "note": "Zhang and Yu conversion method"
                }
            },
            "clinical_significance": {
                "number_needed_to_treat": {
                    "value": round(nnt, 2) if nnt else None,
                    "ci_95": [round(nnt_ci[0], 2) if nnt_ci[0] else None,
                             round(nnt_ci[1], 2) if nnt_ci[1] else None],
                    "interpretation": "Number needed to treat to prevent one event",
                    "clinical_meaning": self._interpret_nnt(nnt)
                },
                "number_needed_to_harm": {
                    "value": round(nnh, 2) if nnh else None,
                    "ci_95": [round(nnh_ci[0], 2) if nnh_ci[0] else None,
                             round(nnh_ci[1], 2) if nnh_ci[1] else None],
                    "interpretation": "Number needed to treat to cause one additional harm",
                    "clinical_meaning": self._interpret_nnh(nnh)
                }
            },
            "benefit_harm_ratio": self._calculate_benefit_harm_ratio(nnt, nnh)
        }

    def _interpret_nnt(self, nnt: Optional[float]) -> str:
        """Provide clinical interpretation of NNT"""
        if nnt is None:
            return "Cannot calculate - no difference in event rates"

        nnt_abs = abs(nnt)
        if nnt > 0:
            if nnt_abs < 5:
                return "Excellent benefit - Large effect size"
            elif nnt_abs < 10:
                return "Substantial benefit - Moderate to large effect"
            elif nnt_abs < 20:
                return "Moderate benefit - Clinically meaningful"
            elif nnt_abs < 50:
                return "Small benefit - Consider patient values"
            else:
                return "Very small benefit - Limited clinical significance"
        else:
            return f"Intervention increases harm (NNH = {abs(nnt):.1f})"

    def _interpret_nnh(self, nnh: Optional[float]) -> str:
        """Provide clinical interpretation of NNH"""
        if nnh is None:
            return "Cannot calculate - no difference in harm rates"

        nnh_abs = abs(nnh)
        if nnh > 0:
            if nnh_abs < 10:
                return "Frequent harm - Major safety concern"
            elif nnh_abs < 20:
                return "Moderate harm frequency - Significant concern"
            elif nnh_abs < 50:
                return "Uncommon harm - Acceptable for serious conditions"
            elif nnh_abs < 100:
                return "Rare harm - Generally acceptable"
            else:
                return "Very rare harm - Minimal safety concern"
        else:
            return "Intervention reduces harm (protective effect)"

    def _calculate_benefit_harm_ratio(self, nnt: Optional[float],
                                       nnh: Optional[float]) -> Dict:
        """Calculate benefit-harm ratio and interpret"""
        if nnt is None or nnh is None:
            return {
                "ratio": None,
                "interpretation": "Cannot calculate - missing NNT or NNH"
            }

        # Both should be positive for standard interpretation
        if nnt > 0 and nnh > 0:
            ratio = nnh / nnt
            if ratio > 5:
                interpretation = "Favorable - Benefits substantially outweigh harms"
            elif ratio > 2:
                interpretation = "Acceptable - Benefits outweigh harms"
            elif ratio > 1:
                interpretation = "Marginal - Benefits slightly outweigh harms"
            elif ratio > 0.5:
                interpretation = "Uncertain - Harms approach benefits"
            else:
                interpretation = "Unfavorable - Harms outweigh benefits"

            return {
                "ratio": round(ratio, 2),
                "interpretation": interpretation,
                "note": f"For every {abs(round(nnt))} patients treated to benefit 1, "
                       f"{abs(round(nnh))} need to be treated to harm 1"
            }
        else:
            return {
                "ratio": None,
                "interpretation": "Complex scenario - manual interpretation required",
                "note": "NNT or NNH is negative (unusual pattern)"
            }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate effect size metrics from RCT 2x2 data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate NNT and other metrics
  python effect_size_calculator.py --intervention-events 42 --intervention-total 150 \\
                                     --control-events 68 --control-total 150

  # Save to JSON file
  python effect_size_calculator.py --intervention-events 42 --intervention-total 150 \\
                                     --control-events 68 --control-total 150 \\
                                     --output effect_sizes.json

Clinical Interpretation:
  NNT < 10: Substantial benefit
  NNT 10-20: Moderate benefit
  NNT > 50: Small benefit

  NNH > 100: Rare harm
  NNH 20-100: Uncommon harm
  NNH < 20: Frequent harm

  NNH/NNT > 2: Benefits likely outweigh harms
        """
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--intervention-events', type=int, required=True,
                       help='Number of events in intervention group')
    parser.add_argument('--intervention-total', type=int, required=True,
                       help='Total participants in intervention group')
    parser.add_argument('--control-events', type=int, required=True,
                       help='Number of events in control group')
    parser.add_argument('--control-total', type=int, required=True,
                       help='Total participants in control group')
    parser.add_argument('--output', '-o', type=str,
                       help='Output JSON file path (default: stdout)')

    args = parser.parse_args()

    try:
        calculator = EffectSizeCalculator(
            intervention_events=args.intervention_events,
            intervention_total=args.intervention_total,
            control_events=args.control_events,
            control_total=args.control_total
        )

        results = calculator.calculate_all()

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2))

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
