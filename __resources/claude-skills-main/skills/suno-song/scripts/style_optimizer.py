#!/usr/bin/env python3
"""
Style Optimizer for Suno V5 Song Skill
Optimizes style field for V5's 1000 char limit with quality focus
"""

import re
from typing import List, Dict, Tuple

class StyleOptimizer:
    """Optimize style field for Suno V5"""

    V5_STYLE_LIMIT = 1000
    V5_OPTIMAL_MIN = 100
    V5_OPTIMAL_MAX = 300

    # Tag conflicts to detect
    CONFLICTS = [
        ('Very Slow', 'High Energy'),
        ('Slow', 'Upbeat'),
        ('Minimal', 'Orchestral'),
        ('Minimal', 'Heavy'),
        ('Acoustic', 'Heavy Electronic'),
        ('Calm', 'Aggressive'),
        ('Peaceful', 'Intense'),
        ('Lo-fi', 'Crystal Clear'),
        ('Lo-fi', 'Studio Polish'),
        ('Intimate', 'Heavy Drums'),
        ('Melancholic', 'Joyful'),
        ('Sad', 'Uplifting'),
    ]

    # V5 enhanced emotion tags (85% reliability)
    V5_EMOTION_TAGS = [
        'haunting', 'joyful', 'somber', 'ethereal', 'bittersweet', 'triumphant'
    ]

    def __init__(self):
        pass

    def parse_style_tags(self, style_field: str) -> List[str]:
        """Parse comma-separated style tags"""
        # Split by comma, strip whitespace
        tags = [tag.strip() for tag in style_field.split(',')]
        return [tag for tag in tags if tag]  # Remove empty

    def detect_conflicts(self, style_field: str) -> List[str]:
        """Detect conflicting style tags"""
        conflicts_found = []
        style_lower = style_field.lower()

        for tag1, tag2 in self.CONFLICTS:
            if tag1.lower() in style_lower and tag2.lower() in style_lower:
                conflicts_found.append(f"Conflict: '{tag1}' and '{tag2}' may produce inconsistent results")

        return conflicts_found

    def count_instruments(self, style_field: str) -> int:
        """Count instrument tags"""
        instrument_keywords = [
            'guitar', 'piano', 'synth', 'bass', 'drums', 'percussion',
            'strings', 'violin', 'cello', 'saxophone', 'sax', 'trumpet',
            'organ', 'rhodes', 'harmonica', 'flute'
        ]

        style_lower = style_field.lower()
        count = sum(1 for inst in instrument_keywords if inst in style_lower)

        return count

    def optimize_style_field(self, style_field: str, mode: str = "balanced") -> Tuple[str, Dict]:
        """
        Optimize style field for V5

        Args:
            style_field: Original style field
            mode: "conservative" (minimal), "balanced" (optimal), "experimental" (detailed)

        Returns:
            (optimized_style, optimization_report)
        """
        original = style_field
        optimized = style_field
        changes = []

        # Remove filler words
        filler_words = [
            ' and ', ' with ', ' featuring ', ' includes ',
            ' along with ', ' combined with ', ' plus '
        ]

        for filler in filler_words:
            if filler in optimized.lower():
                old_len = len(optimized)
                # Replace with comma
                optimized = re.sub(filler, ', ', optimized, flags=re.IGNORECASE)
                # Clean up double commas
                optimized = re.sub(r',\s*,', ',', optimized)
                if len(optimized) < old_len:
                    changes.append(f"Removed filler words (-{old_len - len(optimized)} chars)")

        # Remove redundant spaces
        old_len = len(optimized)
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        optimized = re.sub(r',\s+', ', ', optimized)
        if len(optimized) < old_len:
            changes.append(f"Cleaned spacing (-{old_len - len(optimized)} chars)")

        # Mode-specific optimization
        if mode == "conservative" and len(optimized) > 80:
            # Reduce to core 3-4 tags
            tags = self.parse_style_tags(optimized)
            if len(tags) > 4:
                optimized = ', '.join(tags[:4])
                changes.append(f"Reduced to core 4 tags (conservative mode)")

        elif mode == "balanced" and len(optimized) > 200:
            # Reduce to 5-6 tags
            tags = self.parse_style_tags(optimized)
            if len(tags) > 6:
                optimized = ', '.join(tags[:6])
                changes.append(f"Reduced to 6 tags (balanced mode)")

        # Final length check
        final_length = len(optimized)

        # Detect issues
        conflicts = self.detect_conflicts(optimized)
        instrument_count = self.count_instruments(optimized)

        warnings = []
        if final_length > self.V5_OPTIMAL_MAX:
            warnings.append(f"Over optimal range ({final_length} chars, recommend 100-300)")
        if conflicts:
            warnings.extend(conflicts)
        if instrument_count > 4:
            warnings.append(f"Many instruments specified ({instrument_count}) - may dilute sonic focus")

        return optimized, {
            'original_length': len(original),
            'optimized_length': final_length,
            'savings': len(original) - final_length,
            'changes': changes,
            'warnings': warnings,
            'within_limit': final_length <= self.V5_STYLE_LIMIT,
            'within_optimal': self.V5_OPTIMAL_MIN <= final_length <= self.V5_OPTIMAL_MAX,
            'instrument_count': instrument_count,
            'tag_count': len(self.parse_style_tags(optimized))
        }

    def generate_variations(self, base_style: str) -> Dict[str, str]:
        """Generate 3 variations (conservative, balanced, experimental) from base style"""
        tags = self.parse_style_tags(base_style)

        # Conservative: Core 3-4 tags
        conservative = ', '.join(tags[:4])

        # Balanced: 4-6 tags (original or enhanced)
        balanced = base_style if len(tags) <= 6 else ', '.join(tags[:6])

        # Experimental: Add complexity or V5 emotion tags
        experimental_tags = tags[:7]  # Can go up to 7
        # Check if V5 emotion tag present, add if missing
        has_v5_emotion = any(emotion in base_style.lower() for emotion in self.V5_EMOTION_TAGS)
        if not has_v5_emotion and len(experimental_tags) < 7:
            # Add appropriate V5 emotion based on existing tags
            if 'sad' in base_style.lower() or 'melancholic' in base_style.lower():
                experimental_tags.append('Bittersweet')
            elif 'happy' in base_style.lower() or 'uplifting' in base_style.lower():
                experimental_tags.append('Joyful')
            elif 'energetic' in base_style.lower():
                experimental_tags.append('Triumphant')

        experimental = ', '.join(experimental_tags)

        return {
            'conservative': conservative,
            'balanced': balanced,
            'experimental': experimental
        }


def main():
    """CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: style_optimizer.py <command> [args]")
        print("\nCommands:")
        print("  optimize '<style_field>' [mode]  - Optimize style (modes: conservative, balanced, experimental)")
        print("  validate '<style_field>'         - Validate and check for conflicts")
        print("  variations '<style_field>'       - Generate 3 variations")
        sys.exit(1)

    command = sys.argv[1]
    optimizer = StyleOptimizer()

    if command == "optimize":
        if len(sys.argv) < 3:
            print("Error: Provide style field to optimize")
            sys.exit(1)

        style = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "balanced"

        optimized, report = optimizer.optimize_style_field(style, mode)

        print(f"\n🎵 Suno V5 Style Optimization Report ({mode} mode)\n")
        print("=" * 70)
        print(f"Original: {style}")
        print(f"  Length: {report['original_length']} chars")
        print(f"\nOptimized: {optimized}")
        print(f"  Length: {report['optimized_length']} chars")
        print(f"  Savings: {report['savings']} chars")

        print(f"\nTag Count: {report['tag_count']}")
        print(f"Instrument Count: {report['instrument_count']}")

        status = "✓ Optimal" if report['within_optimal'] else ("✓ Valid" if report['within_limit'] else "❌ Over limit")
        print(f"Status: {status}")

        if report['warnings']:
            print("\n⚠️  Warnings:")
            for warning in report['warnings']:
                print(f"  - {warning}")

        if report['changes']:
            print("\nChanges Made:")
            for change in report['changes']:
                print(f"  - {change}")

    elif command == "validate":
        style = sys.argv[2]

        conflicts = optimizer.detect_conflicts(style)
        instrument_count = optimizer.count_instruments(style)
        tag_count = len(optimizer.parse_style_tags(style))
        char_count = len(style)

        print(f"\n🎵 Suno V5 Style Validation\n")
        print("=" * 70)
        print(f"Style: {style}")
        print(f"Length: {char_count}/1000 chars")
        print(f"Tags: {tag_count}")
        print(f"Instruments: {instrument_count}")

        if char_count <= optimizer.V5_OPTIMAL_MAX:
            print(f"✓ Optimal length (100-300 recommended)")
        elif char_count <= optimizer.V5_STYLE_LIMIT:
            print(f"⚠️  Over optimal but within limit")
        else:
            print(f"❌ EXCEEDS V5 LIMIT")

        if conflicts:
            print("\n❌ Conflicts Detected:")
            for conflict in conflicts:
                print(f"  - {conflict}")
        else:
            print("\n✓ No conflicts detected")

        if instrument_count > 4:
            print(f"\n⚠️  Warning: {instrument_count} instruments may dilute focus (recommend 3-4 max)")

    elif command == "variations":
        style = sys.argv[2]
        variations = optimizer.generate_variations(style)

        print(f"\n🎵 Suno V5 Style Variations\n")
        print("=" * 70)
        print(f"Base Style: {style}\n")

        for var_name, var_style in variations.items():
            print(f"{var_name.title()}:")
            print(f"  {var_style}")
            print(f"  ({len(var_style)} chars)\n")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
