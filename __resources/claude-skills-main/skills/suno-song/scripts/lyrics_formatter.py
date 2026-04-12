#!/usr/bin/env python3
"""
Lyrics Formatter for Suno V5 Song Skill
Formats raw lyrics with appropriate metatags and validates structure
"""

import re
from typing import Dict, List, Tuple

class LyricsFormatter:
    """Format and validate lyrics for Suno V5 with metatags"""

    # V5 Character limits
    V5_LYRICS_LIMIT = 5000
    V5_OPTIMAL_MIN = 2000
    V5_OPTIMAL_MAX = 3500

    # Tier 1 reliable metatags (90-95% success in V5)
    TIER_1_TAGS = [
        'Verse', 'Chorus', 'Bridge',
        'Short Instrumental Intro', 'Catchy Hook',
        'melodic interlude', 'Big Finish'
    ]

    def __init__(self):
        self.metatag_pattern = re.compile(r'\[([^\]]+)\]')

    def detect_existing_structure(self, lyrics: str) -> Dict:
        """Detect existing metatags and structure"""
        lines = lyrics.strip().split('\n')
        structure = []
        has_metatags = False

        for i, line in enumerate(lines):
            tags = self.metatag_pattern.findall(line)
            if tags:
                has_metatags = True
                structure.append({
                    'line_number': i,
                    'tag': tags[0],
                    'content': line
                })

        return {
            'has_metatags': has_metatags,
            'structure': structure,
            'total_lines': len(lines)
        }

    def count_syllables_simple(self, text: str) -> int:
        """
        Simple syllable counter (approximation)
        Good enough for validation, not linguistically perfect
        """
        # Remove metatags
        text = self.metatag_pattern.sub('', text)

        # Simple vowel-group counting
        text = text.lower()
        vowels = 'aeiouy'

        syllable_count = 0
        previous_was_vowel = False

        for char in text:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if text.endswith('e'):
            syllable_count -= 1

        # Minimum 1 syllable per word
        return max(1, syllable_count)

    def analyze_syllables(self, lyrics: str) -> Dict:
        """Analyze syllable consistency across sections"""
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
        current_section = None
        section_syllables = {}

        for line in lines:
            # Check for metatag
            tags = self.metatag_pattern.findall(line)
            if tags:
                current_section = tags[0]
                continue

            # Count syllables in lyric lines
            if current_section and not self.metatag_pattern.search(line):
                if current_section not in section_syllables:
                    section_syllables[current_section] = []

                syllable_count = self.count_syllables_simple(line)
                section_syllables[current_section].append(syllable_count)

        return section_syllables

    def validate_v5_structure(self, lyrics: str) -> Dict:
        """Validate lyrics against V5 best practices"""
        issues = []
        warnings = []

        # Check character count
        char_count = len(lyrics)
        if char_count > self.V5_LYRICS_LIMIT:
            issues.append(f"CRITICAL: Exceeds V5 limit ({char_count}/{self.V5_LYRICS_LIMIT} chars)")
        elif char_count > self.V5_OPTIMAL_MAX:
            warnings.append(f"Over optimal range ({char_count} chars, recommend 2000-3500)")
        elif char_count < self.V5_OPTIMAL_MIN:
            warnings.append(f"Below optimal range ({char_count} chars, might be too short for quality)")

        # Detect structure
        structure = self.detect_existing_structure(lyrics)

        if not structure['has_metatags']:
            warnings.append("No metatags detected - structure may be unpredictable")

        # Check syllable consistency (V5 best practice: 6-12 syllables/line)
        syllable_analysis = self.analyze_syllables(lyrics)

        for section, syllables in syllable_analysis.items():
            if not syllables:
                continue

            avg_syllables = sum(syllables) / len(syllables)

            if avg_syllables < 6:
                warnings.append(f"{section}: Average {avg_syllables:.1f} syllables/line (V5 optimal: 6-12)")
            elif avg_syllables > 12:
                warnings.append(f"{section}: Average {avg_syllables:.1f} syllables/line (V5 optimal: 6-12, may feel rushed)")

            # Check consistency within section
            if len(syllables) > 2:
                variance = max(syllables) - min(syllables)
                if variance > 5:
                    warnings.append(f"{section}: High syllable variance ({min(syllables)}-{max(syllables)}) - may affect flow")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'character_count': char_count,
            'structure_detected': structure['has_metatags'],
            'syllable_analysis': syllable_analysis
        }

    def format_simple_structure(self, lyrics: str, structure_type: str = "verse_chorus") -> str:
        """
        Add basic metatag structure to unformatted lyrics

        Args:
            lyrics: Raw lyrics without metatags
            structure_type: "verse_chorus" (simple) or "pop_standard" (with bridge)

        Returns:
            Formatted lyrics with metatags
        """
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]

        if structure_type == "verse_chorus":
            # Simple structure: Intro → Verse → Chorus → Verse → Chorus → Finish
            # Heuristic: Repeated sections likely chorus

            # Detect repeated sections (simple hash-based)
            line_hashes = {}
            for i, line in enumerate(lines):
                line_hash = line.lower().strip()
                if line_hash not in line_hashes:
                    line_hashes[line_hash] = []
                line_hashes[line_hash].append(i)

            # Lines that appear 2+ times are likely chorus
            chorus_indices = set()
            for line_hash, indices in line_hashes.items():
                if len(indices) >= 2:
                    chorus_indices.update(indices)

            # Build formatted output
            formatted = "[Short Instrumental Intro]\n\n"
            in_chorus = False

            for i, line in enumerate(lines):
                if i in chorus_indices:
                    if not in_chorus:
                        formatted += "[Chorus]\n"
                        in_chorus = True
                else:
                    if in_chorus:
                        formatted += "\n"
                        in_chorus = False
                    if i == 0 or (i > 0 and lines[i-1] in line_hashes and len(line_hashes[lines[i-1].lower().strip()]) < 2):
                        formatted += "[Verse]\n"

                formatted += line + "\n"

            formatted += "\n[Big Finish]"

            return formatted

        elif structure_type == "pop_standard":
            # More complex: Intro → V1 → PC → C → V2 → PC → C → Bridge → C → Finish
            # Simple approximation
            total_lines = len(lines)

            formatted = "[Short Instrumental Intro]\n\n[Verse]\n"
            section_line_count = 0

            for i, line in enumerate(lines):
                formatted += line + "\n"
                section_line_count += 1

                # Add section markers at rough boundaries
                progress = i / total_lines

                if section_line_count == 4 and progress < 0.2:
                    formatted += "\n[Pre-Chorus]\n"
                    section_line_count = 0
                elif section_line_count == 3 and 0.2 <= progress < 0.35:
                    formatted += "\n[Chorus]\n"
                    section_line_count = 0
                elif section_line_count == 4 and 0.35 <= progress < 0.55:
                    formatted += "\n[Verse]\n"
                    section_line_count = 0
                elif section_line_count == 3 and 0.55 <= progress < 0.7:
                    formatted += "\n[Chorus]\n"
                    section_line_count = 0
                elif section_line_count == 4 and 0.7 <= progress < 0.85:
                    formatted += "\n[Bridge]\n"
                    section_line_count = 0
                elif progress >= 0.85:
                    formatted += "\n[Chorus]\n\n[Big Finish]"
                    break

            return formatted

        return lyrics  # Return original if unknown type

    def compress_lyrics(self, lyrics: str, target_length: int = 3500) -> Tuple[str, Dict]:
        """
        Intelligent compression for V5 quality optimization

        Args:
            lyrics: Original lyrics
            target_length: Target character count (default 3500 = V5 optimal max)

        Returns:
            (compressed_lyrics, compression_report)
        """
        original_length = len(lyrics)

        if original_length <= target_length:
            return lyrics, {
                'compressed': False,
                'original_length': original_length,
                'final_length': original_length,
                'savings': 0,
                'changes': []
            }

        changes = []
        compressed = lyrics

        # Step 1: Simplify verbose metatags
        verbose_tags = [
            (r'\[Long Instrumental.*?\]', '[Instrumental]'),
            (r'\[Short Instrumental Intro.*?\]', '[Short Instrumental Intro]'),
            (r'\[Verse \d+\]', '[Verse]'),
            (r'\[Chorus \d+\]', '[Chorus]'),
        ]

        for pattern, replacement in verbose_tags:
            old_len = len(compressed)
            compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
            if len(compressed) < old_len:
                changes.append(f"Simplified verbose metatags (-{old_len - len(compressed)} chars)")

        # Step 2: Remove excessive newlines
        old_len = len(compressed)
        compressed = re.sub(r'\n\n\n+', '\n\n', compressed)
        if len(compressed) < old_len:
            changes.append(f"Removed excessive spacing (-{old_len - len(compressed)} chars)")

        # Step 3: If still over target, trim sections
        if len(compressed) > target_length:
            # This is a simple truncation - in practice, intelligent section removal would be better
            lines = compressed.split('\n')
            # Keep chorus sections, trim verses if needed
            # (More sophisticated logic would go here)
            changes.append(f"Trimmed content to reach target length")
            compressed = '\n'.join(lines[:int(len(lines) * 0.8)])  # Remove last 20%

        final_length = len(compressed)

        return compressed, {
            'compressed': True,
            'original_length': original_length,
            'final_length': final_length,
            'savings': original_length - final_length,
            'changes': changes,
            'target_achieved': final_length <= target_length
        }


def main():
    """CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: lyrics_formatter.py <command> [args]")
        print("\nCommands:")
        print("  validate <lyrics_file>  - Validate lyrics against V5 best practices")
        print("  format <lyrics_file>    - Add metatags to unformatted lyrics")
        print("  compress <lyrics_file>  - Compress for V5 quality optimization")
        sys.exit(1)

    command = sys.argv[1]
    formatter = LyricsFormatter()

    if command == "validate" and len(sys.argv) == 3:
        with open(sys.argv[2], 'r') as f:
            lyrics = f.read()

        result = formatter.validate_v5_structure(lyrics)

        print("\n🎵 Suno V5 Lyrics Validation Report\n")
        print("=" * 70)
        print(f"Character Count: {result['character_count']}/5000 (V5 limit)")

        if result['character_count'] <= formatter.V5_OPTIMAL_MAX:
            print(f"✓ Within optimal range (2000-3500 recommended)")
        else:
            print(f"⚠️  Over optimal range (recommend compression for quality)")

        print(f"\nStructure Detected: {'✓ Yes' if result['structure_detected'] else '✗ No metatags found'}")

        if result['issues']:
            print("\n❌ ISSUES:")
            for issue in result['issues']:
                print(f"  - {issue}")

        if result['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in result['warnings']:
                print(f"  - {warning}")

        if result['syllable_analysis']:
            print("\n📊 Syllable Analysis (V5 optimal: 6-12/line):")
            for section, syllables in result['syllable_analysis'].items():
                avg = sum(syllables) / len(syllables)
                print(f"  {section}: {avg:.1f} avg ({min(syllables)}-{max(syllables)} range)")

        print("\n" + "=" * 70)
        if result['valid'] and not result['warnings']:
            print("✅ READY FOR V5 - No issues detected!")
        elif result['valid']:
            print("✓ Valid but could be optimized (see warnings)")
        else:
            print("❌ ISSUES MUST BE FIXED before using in Suno")

    elif command == "format" and len(sys.argv) == 3:
        with open(sys.argv[2], 'r') as f:
            lyrics = f.read()

        formatted = formatter.format_simple_structure(lyrics, "verse_chorus")
        print(formatted)

    elif command == "compress" and len(sys.argv) == 3:
        with open(sys.argv[2], 'r') as f:
            lyrics = f.read()

        compressed, report = formatter.compress_lyrics(lyrics, target_length=3500)

        print(f"\n🎵 Suno V5 Lyrics Compression Report\n")
        print("=" * 70)
        print(f"Original Length: {report['original_length']} chars")
        print(f"Final Length: {report['final_length']} chars")
        print(f"Savings: {report['savings']} chars ({report['savings']/report['original_length']*100:.1f}%)")
        print(f"Target Achieved: {'✓ Yes' if report['target_achieved'] else '✗ No'}")

        if report['changes']:
            print("\nChanges Made:")
            for change in report['changes']:
                print(f"  - {change}")

        print("\n" + "=" * 70)
        print("\nCompressed Lyrics:\n")
        print(compressed)

    else:
        print(f"Unknown command: {command}")
        print("Use: validate, format, or compress")
        sys.exit(1)


if __name__ == "__main__":
    main()
