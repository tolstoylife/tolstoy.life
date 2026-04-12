#!/usr/bin/env python3
"""
Template Selector for Suno V5 Song Skill
Matches user input to appropriate genre templates using keyword analysis
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class TemplateSelector:
    """Match user input to appropriate Suno V5 genre templates"""

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            # Default to assets/templates relative to this script
            script_dir = Path(__file__).parent
            templates_dir = script_dir.parent / "assets" / "templates"

        self.templates_dir = Path(templates_dir)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load all YAML templates from directory"""
        templates = {}

        for template_file in self.templates_dir.glob("*_v5.yaml"):
            try:
                with open(template_file, 'r') as f:
                    # Skip markdown header if present
                    content = f.read()
                    if content.startswith('#'):
                        # Find first yaml content
                        yaml_start = content.find('meta:')
                        if yaml_start > 0:
                            content = content[yaml_start:]

                    template = yaml.safe_load(content)
                    templates[template['meta']['name']] = template
            except Exception as e:
                print(f"Warning: Could not load {template_file}: {e}")

        return templates

    def select_template(self, user_input: str, top_n: int = 3) -> List[Tuple[str, float, Dict]]:
        """
        Select best matching templates based on user input

        Args:
            user_input: User's description, lyrics, or request
            top_n: Number of top matches to return

        Returns:
            List of (template_name, confidence_score, template_data) tuples
        """
        user_lower = user_input.lower()
        scores = []

        # Keyword mappings for matching
        genre_keywords = {
            'indie_folk': ['indie', 'folk', 'acoustic', 'singer songwriter'],
            'pop': ['pop', 'catchy', 'radio', 'mainstream'],
            'hip_hop': ['hip hop', 'rap', 'storytelling', 'boom bap', 'beats'],
            'gospel_trap': ['gospel', 'trap', 'choir', '808', 'triumphant'],
            'edm': ['edm', 'electronic', 'dance', 'club', 'festival', 'drop', 'synth'],
            'piano_ballad': ['piano', 'ballad', 'emotional', 'intimate'],
            'jazz_hop': ['jazz hop', 'jazz hip hop', 'saxophone', 'smooth'],
        }

        mood_keywords = {
            'melancholic': ['sad', 'melancholic', 'melancholy', 'depressing', 'heartbreak'],
            'uplifting': ['happy', 'uplifting', 'joyful', 'positive', 'cheerful'],
            'energetic': ['energetic', 'high energy', 'intense', 'powerful'],
            'introspective': ['introspective', 'thoughtful', 'philosophical', 'reflective'],
            'emotional': ['emotional', 'moving', 'touching', 'bittersweet'],
        }

        for template_name, template in self.templates.items():
            score = 0.0
            meta = template['meta']

            # Genre matching (40% weight)
            for genre_key, keywords in genre_keywords.items():
                if genre_key in template_name or genre_key in meta.get('subcategory', ''):
                    for keyword in keywords:
                        if keyword in user_lower:
                            score += 0.4 / len(keywords)  # Normalize by keyword count

            # Mood matching (30% weight)
            template_mood = meta.get('mood', '')
            for mood_key, keywords in mood_keywords.items():
                if mood_key in template_mood:
                    for keyword in keywords:
                        if keyword in user_lower:
                            score += 0.3 / len(keywords)

            # Category matching (20% weight)
            template_category = meta.get('category', '')
            if template_category in user_lower:
                score += 0.2

            # Reliability bonus (10% weight)
            reliability = meta.get('reliability', '')
            if reliability == 'VERY HIGH':
                score += 0.1
            elif reliability == 'HIGH':
                score += 0.05

            scores.append((template_name, score, template))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_n]

    def get_template_summary(self, template: Dict) -> str:
        """Generate human-readable template summary"""
        meta = template['meta']
        style_vars = template.get('style_variations', {})

        summary = f"""
Template: {meta['name']}
Category: {meta['category']} → {meta['subcategory']}
Mood: {meta['mood']}
Reliability: {meta['reliability']} ({meta.get('tested_generations', 'N/A')} generations tested)
Average Quality: {meta.get('average_quality_score', 'N/A')}

Style Variations:
  Conservative: {style_vars.get('conservative', 'N/A')}
  Balanced: {style_vars.get('balanced', 'N/A')}
  Experimental: {style_vars.get('experimental', 'N/A')}

Best for: {template.get('usage_notes', 'See template for details')[:200]}...
"""
        return summary.strip()


def main():
    """CLI interface for template selection"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: template_selector.py '<user input>'")
        print("Example: template_selector.py 'create a sad piano song'")
        sys.exit(1)

    user_input = ' '.join(sys.argv[1:])

    selector = TemplateSelector()
    matches = selector.select_template(user_input, top_n=3)

    print(f"\n🎵 Template Matching Results for: '{user_input}'\n")
    print("=" * 70)

    for i, (name, score, template) in enumerate(matches, 1):
        print(f"\n{'='*70}")
        print(f"Match #{i} (Confidence: {score*100:.1f}%)")
        print(f"{'='*70}")
        print(selector.get_template_summary(template))

    if matches:
        print(f"\n{'='*70}")
        print(f"\n✅ Recommended: Match #1 ({matches[0][0]})")
        print(f"   Confidence: {matches[0][1]*100:.1f}%")
        print(f"   Reliability: {matches[0][2]['meta']['reliability']}")


if __name__ == "__main__":
    main()
