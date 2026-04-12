# Suno V5 Features & Capabilities Reference

**Model**: Suno V5 (chirp-crow)
**Release**: September 2025
**Availability**: Pro & Premier tier subscribers
**Last Updated**: November 4, 2025

---

## CHARACTER LIMITS (V5)

```yaml
v5_limits:
  lyrics_prompt:
    maximum: 5000 characters
    recommended: 2000-3500 characters (brevity still helps)
    minimum: 50 characters

  style:
    maximum: 1000 characters
    recommended: 100-300 characters (concise is better)
    minimum: 10 characters

  title:
    maximum: 100 characters
    recommended: 30-60 characters
    minimum: 5 characters
```

**Key Principle**: While limits are generous, **brevity produces better results**. Short, clear prompts yield cleaner audio quality.

---

## CORE V5 IMPROVEMENTS

### 1. Audio Quality
- **Higher fidelity** with clearer instrument separation
- **Stronger out-of-the-box polish** (less post-processing needed)
- **Fuller, cleaner mixes** on first generation
- **10x faster processing** vs. previous versions

### 2. Vocal Enhancements
- **Natural pronunciation** and phrasing
- **Authentic vocal tone** (eliminated AI sound issues)
- **Better breaths and harmonies** (especially in acoustic, pop, hip-hop)
- **Tighter mix integration** (vocals sit better in mix)

### 3. Prompt Understanding
- **90% adherence rate** for well-structured prompts
- **More nuanced interpretation** of detailed prompts
- **Better emotion parsing** (tags like "haunting", "joyful", "somber" work well)
- **Reliable callback phrasing** ("continue with same vibe")

### 4. Structural Coherence
- **Flawless structural coherence** from 30-second hooks to 8-minute epics
- **Better metatag following**: [Verse] [Chorus] [Bridge] more consistent
- **Intelligent automatic arrangement** (can handle unconventional structures)
- **Professional transitions** automatically

### 5. Genre Fusion
- **Steadier fusion** for 2-genre combinations
- **Proven pairs**: Pop+EDM, Gospel+Trap, Jazz+Hip Hop
- **Avoid stacking 3-4 genres** (reduces quality)
- **Best practice**: 1-2 genres + 1 mood + optional instruments

---

## SUNO STUDIO FEATURES (V5)

### Timeline Interface
- **Section-based editing**: Visual timeline showing intro, verse, chorus, bridge, outro
- **Drag-and-drop arrangement**: Reorder sections
- **Multi-track view**: See all elements at once

### Replace Section
```yaml
feature: Replace Section
availability: Pro & Premier
function: Regenerate any song section with smooth crossfades

usage:
  1. Select clip or highlight region
  2. Choose "Replace" from left panel or Quick Replace button
  3. Optional: Add prompt ("Make this section dreamier")
  4. Fine-tune transition by dragging boundary line

use_cases:
  - Fix problematic section without regenerating whole song
  - Change lyrics in one verse
  - Add instrumental break in specific spot
  - Adjust mood/energy of particular section
```

### Extend Feature
```yaml
feature: Extend
improvement: "Far less drift than V4.5"
function: Continue tracks while preserving consistency

usage:
  - Appends bars at tail
  - Existing audio remains unchanged
  - Better style/voice consistency than previous versions

use_cases:
  - Song ends too early
  - Add outro to abrupt ending
  - Extend instrumental section
```

### Stem Export
```yaml
pro_tier: 2 stems
  - Vocals
  - Instrumental

premier_tier: 12 stems (individual tracks)
  - Vocals
  - Drums
  - Bass
  - Guitar
  - Piano
  - Synths
  - etc. (varies by song)

format: WAV
use_case: DAW integration, remixing, professional production
```

### MIDI Export
```yaml
feature: MIDI Export
availability: Pro & Premier
cost: Requires credits
use_case: Extract melody/chords for further production
```

### Remaster Function
```yaml
modes:
  subtle: "Smooth out small issues without changing vibe"
  normal: "Balanced polish for general use"
  high: "Adds variety but may shift tone (experimental)"

use_when:
  - Song has audio artifacts
  - Vocals need better clarity
  - Mix feels unbalanced
  - Want to try different dynamic range
```

---

## HOOOKS FEATURE (V5)

### What are Hoooks?
Shareable 20-30 second song highlights for community discovery and engagement.

### Capabilities
```yaml
function: "Create short clip of hook in your song, attach to video"

requirements:
  video_duration: 10 seconds - 2 minutes
  aspect_ratio: Specific ratio (varies)
  file_size: Within limits

engagement:
  - Like, share, remix snippets
  - Boosts visibility in recommendations
  - Community discovery tool

best_practices:
  - Pick memorable moments (chorus, drop)
  - 20-30 seconds optimal length
  - Pair with compelling visuals
  - Caption with context
  - Track engagement metrics
```

---

## V5-SPECIFIC PROMPTING IMPROVEMENTS

### Optimal Lyric Structure
```yaml
syllables_per_line: 6-12 (optimal for V5)
reasoning: Better rhythm and phrasing alignment

example:
  good: "Walking down the memory lane" (8 syllables)
  good: "Sunshine fades to rain" (6 syllables)
  avoid: "I am currently in the process of walking" (14 syllables - too long)
  avoid: "Lost love" (2 syllables - too short for full line)
```

### Metatag Consistency
V5 shows **improved metatag reliability**:

```yaml
v4_5_reliability:
  [Verse]: ~80%
  [Chorus]: ~85%
  [Bridge]: ~75%
  [Intro]: ~30% (problematic)

v5_reliability:
  [Verse]: ~90%
  [Chorus]: ~95%
  [Bridge]: ~85%
  [Intro]: ~40% (still problematic - use [Short Instrumental Intro])
```

**Key Improvement**: V5 "reliably respects callback phrasing and lyric markers"

### Emotion Tags (V5 Enhanced)
```yaml
clearer_emotion_parsing:
  improved_tags:
    - haunting
    - joyful
    - somber
    - ethereal
    - bittersweet
    - triumphant

  usage: "[Mood: haunting]" or incorporate in style field
  reliability: HIGH in V5 (vs. MEDIUM in V4.5)
```

### Prompt Enhancement Tool
```yaml
feature: Built-in Prompt Expander
function: Converts basic descriptors into detailed prompts

example:
  input: "emo"
  output: "Emo, Emotional, Guitar-driven, Male Vocals, Confessional Lyrics, Minor Key, 120 BPM"

user_control: Can further customize expanded prompt

benefit: Good starting point for beginners
```

---

## V5 ADVANCED PARAMETERS

### Weirdness Factor
```yaml
parameter: weirdness
range: 0.0 - 1.0
function: "Increases variance in song outputs"

recommendations:
  commercial: 0.2 - 0.4 (predictable, polished)
  creative: 0.5 - 0.7 (balanced experimentation)
  experimental: 0.8 - 1.0 (high variance, hit-or-miss)

v5_improvement: "More controlled weirdness (less chaos than V4)"
```

### Style Influence Weight
```yaml
parameter: style_weight (or styleWeight)
range: 0.0 - 1.0
function: "Adherence to style tags"

recommendations:
  loose_creative: 0.3 - 0.5 (AI has more freedom)
  balanced: 0.6 - 0.7 (recommended)
  strict: 0.8 - 0.9 (tight adherence to tags)

v5_behavior: Better balance - even low weights maintain coherence
```

### Persistent Voice & Instrument Memory
```yaml
feature: Voice/Instrument Consistency
function: "Characters and instrumental signatures remain consistent throughout project"

benefit: Multi-generation projects maintain same vocal character

use_case:
  - Creating album with same vocalist
  - Extending songs without voice change
  - Building consistent sonic brand
```

---

## V5 vs V4.5 COMPARISON

| Feature | V4.5 | V5 |
|---------|------|-----|
| **Lyrics Limit** | 5000 chars | 5000 chars (same) |
| **Style Limit** | 1000 chars | 1000 chars (same) |
| **Title Limit** | 100 chars | 100 chars (same) |
| **Max Duration** | 8 minutes | 8 minutes (same) |
| **Prompt Adherence** | ~75% | ~90% |
| **Metatag Reliability** | Medium | High |
| **Vocal Quality** | Good | Excellent (near-human) |
| **Processing Speed** | Standard | 10x faster |
| **Genre Fusion** | Good | Better (more stable) |
| **Emotion Tags** | Basic | Enhanced (haunting, somber, etc.) |
| **Studio Features** | Limited | Full timeline editing |
| **Stems** | Yes | Yes (cleaner separation) |
| **MIDI Export** | No | Yes |
| **Audio Quality** | Good | Studio-grade |

---

## V5 BEST PRACTICES

### 1. Leverage Extended Limits Wisely
```yaml
do:
  - Use full 5000 chars for complex storytelling songs
  - Expand style to 500-800 chars for detailed fusion descriptions
  - Include nuanced mood/instrumentation details

don't:
  - Fill space just because it exists
  - Over-specify (still causes artifacts)
  - Ignore "brevity is better" principle
```

### 2. Optimize for V5 Strengths
```yaml
v5_excels_at:
  - Complex genre fusions (Pop+EDM, Gospel+Trap)
  - Emotional nuance (haunting, bittersweet, triumphant)
  - Structural consistency (8-minute compositions)
  - Natural vocals (breaths, phrasing, harmonies)
  - Professional polish (less post-processing needed)

prompting_strategies:
  - Specify emotions explicitly (V5 parses better)
  - Use 2-genre fusion confidently
  - Provide detailed lyrics for better vocal delivery
  - Trust automatic transitions (V5 handles better)
```

### 3. Studio Workflow Integration
```yaml
recommended_workflow:
  step_1: Generate full song with detailed prompt
  step_2: Use Studio Timeline to view structure
  step_3: Replace Section for any problematic parts
  step_4: Extend if song ends early
  step_5: Remaster (Subtle or Normal) for final polish
  step_6: Export stems for DAW work (if needed)

benefit: Non-destructive editing without full regeneration
```

---

## V5 LIMITATIONS & KNOWN ISSUES

### Current Gaps
```yaml
reported_issues:
  early_cutoff:
    symptom: "Songs occasionally cut off slightly early"
    workaround: Use Extend feature to complete

  generic_auto_lyrics:
    symptom: "Auto-generated lyrics use cliché terms (echoes, algorithms)"
    solution: Always provide custom lyrics for better results

  reduced_shimmer:
    symptom: "Some users report less 'shimmer' vs V4.5"
    context: Trade-off for cleaner, more professional sound

  prompt_expansion_generic:
    symptom: "Prompt Enhancement tool can be too generic"
    solution: Customize expanded prompts before generating
```

### What Still Doesn't Work Perfectly
```yaml
moderate_reliability:
  - [Intro] tag (use [Short Instrumental Intro] instead)
  - [Fade Out] (accept natural endings)
  - 3+ genre fusion (stick to 2 genres)
  - Very long songs (6-8 min may have drift)
```

---

## TECHNICAL SPECIFICATIONS

### Model Details
```yaml
model_name: chirp-crow (V5)
release_date: September 2025
architecture: Proprietary (Suno)
training: Unknown (commercial product)

performance_benchmark:
  elo_score: ~1,293
  v4_5_plus_score: ~1,208
  improvement: +7% on internal benchmarks
```

### Generation Speed
```yaml
typical_generation_time:
  30_second_clip: ~5-10 seconds
  3_minute_song: ~30-40 seconds
  8_minute_song: ~60-90 seconds

improvement: "10x faster than previous versions"
```

---

## PROMPTING STRATEGIES FOR V5

### Short vs. Long Prompts

**Short Prompts** (100-500 chars):
```yaml
when_to_use: Simple, clear concepts
quality: Often produces cleanest audio
example: "Uplifting pop song, female vocals, catchy chorus about summer love"
success_rate: 90%+
```

**Medium Prompts** (500-2000 chars):
```yaml
when_to_use: Structured songs with clear sections
quality: Balanced control and clarity
example: Full lyrics with metatags, clear structure
success_rate: 85%+
```

**Long Prompts** (2000-5000 chars):
```yaml
when_to_use: Complex storytelling, progressive compositions
quality: Can work but risk increases
caution: May introduce artifacts if over-specified
success_rate: 70-80%
```

### Style Field Strategy (1000 char limit)

**Concise (50-150 chars)**: RECOMMENDED
```
"Pop, Uplifting, Female Vocals, Synth, Guitar, 120 BPM"
```
**Quality**: Excellent, clean output

**Moderate (150-400 chars)**:
```
"Indie Pop with Electronic elements, Uplifting and Energetic mood, Female Vocals with harmonies, Synth Bass and Pads, Acoustic Guitar strums, Driving beat at 120 BPM, Clear production"
```
**Quality**: Good, may be slightly over-specified

**Detailed (400-1000 chars)**:
```
[Very detailed description with multiple instruments, moods, specific production notes, tempo changes, arrangement details, etc.]
```
**Quality**: Risky - often introduces conflicts or artifacts

**V5 Recommendation**: Keep style 100-300 chars for optimal results

---

## V5-SPECIFIC METATAG BEHAVIORS

### Improved Reliability

V5 shows **better structural consistency**:

```yaml
highly_reliable_in_v5:
  - [Verse] (90% reliability, up from 80%)
  - [Chorus] (95% reliability, up from 85%)
  - [Bridge] (85% reliability, up from 75%)
  - [melodic interlude] (85% reliability)
  - [Catchy Hook] (90% reliability)

moderately_improved:
  - [Pre-Chorus] (70% reliability, up from 60%)
  - [Instrumental] (75% reliability, up from 70%)

still_problematic:
  - [Intro] (~40% reliability, slight improvement from 30%)
  - [Fade Out] (~40% reliability)
  - [Outro] (~45% reliability)

  better_alternatives:
    - Use [Short Instrumental Intro] instead of [Intro]
    - Use [Big Finish] instead of [Outro]
```

### New Emotion Tags Work Better

```yaml
v5_enhanced_tags:
  emotion_descriptors:
    - haunting (HIGH reliability)
    - joyful (HIGH reliability)
    - somber (HIGH reliability)
    - ethereal (HIGH reliability)
    - bittersweet (MEDIUM-HIGH reliability)
    - triumphant (HIGH reliability)

  usage: "[Mood: haunting]" or in style field: "haunting, ethereal vocals"

  improvement: V4.5 parsed these generically; V5 interprets specifically
```

---

## STUDIO TIMELINE WORKFLOW

### Professional Production Flow

```yaml
stage_1_generation:
  - Create song with detailed V5 prompt
  - Use generous character limits for full vision
  - Generate 2 variations initially

stage_2_review:
  - Open in Studio Timeline
  - View section breakdown visually
  - Identify any problematic sections

stage_3_editing:
  - Replace Section: Fix individual parts
    - "Make this chorus more energetic"
    - "Change lyrics in verse 2"
    - "Add guitar solo here"

  - Extend: If song ends early
    - Maintains voice/style consistency
    - Less drift than V4.5 extend

stage_4_polish:
  - Remaster: Subtle/Normal/High
    - Subtle: Minor cleanup only
    - Normal: Balanced polish (recommended)
    - High: Adds variety (experimental)

stage_5_export:
  - Stems: For DAW production
  - MIDI: For melody/chord extraction
  - Final WAV/MP3: For distribution
```

**Advantage**: Non-destructive workflow - original always preserved

---

## PERSISTENT VOICE & INSTRUMENT MEMORY

### What This Means

```yaml
feature: Voice/Instrument Consistency
behavior: "Same vocal character and instrument tones across multiple generations"

use_cases:
  album_creation:
    - Generate 5 songs for an EP
    - Same vocalist throughout
    - Consistent instrument timbres

  song_extension:
    - Extend existing song
    - Voice remains identical
    - Instrument signatures match

  iterative_refinement:
    - Regenerate sections
    - Maintains character consistency
```

**How to Leverage**:
- Reference previous generations: "Use same vocal style as [song ID]"
- Build cohesive bodies of work
- Create recognizable sonic brand

---

## WEIRDNESS & STYLE INFLUENCE (V5 TUNING)

### Weirdness Factor Improvements

```yaml
v4_5_behavior:
  low: Predictable but sometimes boring
  high: Creative but often chaotic/artifacts

v5_behavior:
  low: Predictable and polished
  high: Creative but more controlled

improvement: "More controlled weirdness - less chaos"

recommendations:
  safe_commercial:
    weirdness: 0.2 - 0.3
    outcome: "Radio-friendly, predictable, clean"

  creative_exploration:
    weirdness: 0.5 - 0.7
    outcome: "Interesting, unique, still coherent"

  experimental_avant_garde:
    weirdness: 0.8 - 1.0
    outcome: "Very unique, hit-or-miss, exciting risks"
```

### Style Influence Weight

```yaml
v5_improvements:
  - Better balance at all weight levels
  - Low weights (0.3-0.5) still maintain coherence
  - High weights (0.8-0.9) less rigid/mechanical

recommendations:
  exploratory: 0.4 - 0.6 (let AI contribute creativity)
  balanced: 0.65 - 0.75 (recommended default)
  precise: 0.80 - 0.90 (tight adherence to tags)
```

---

## GENRE FUSION BEST PRACTICES (V5)

### What Works Well

```yaml
proven_2_genre_fusions:
  pop_electronic:
    - "Pop, Electronic" or "Pop EDM"
    - Reliability: 95%
    - Result: Clean fusion, commercial sound

  gospel_trap:
    - "Gospel, Trap" or "Gospel Trap"
    - Reliability: 90%
    - Result: Choir vocals with 808s, unique blend

  jazz_hip_hop:
    - "Jazz, Hip Hop" or "Jazz Hop"
    - Reliability: 90%
    - Result: Smooth jazz instruments with rap/beats

  rock_orchestral:
    - "Rock, Orchestral" or "Symphonic Rock"
    - Reliability: 85%
    - Result: Epic, cinematic rock

  classical_electronic:
    - "Classical, Electronic" or "Electro-Classical"
    - Reliability: 85%
    - Result: Orchestra meets synths
```

### What to Avoid

```yaml
problematic_fusions:
  three_plus_genres:
    example: "Jazz, Rock, Electronic, Classical"
    issue: "Diluted identity, inconsistent results"
    success_rate: 50-60%

  conflicting_moods:
    example: "Aggressive, Calm, Uplifting, Melancholic"
    issue: "AI gets confused, picks one randomly"

  incompatible_tempos:
    example: "Very Slow Ballad, Upbeat Dance Energy"
    issue: "Contradictory directives"
```

---

## OPTIMAL PROMPT STRUCTURE FOR V5

### Recommended Template

```yaml
lyrics_section (2000-3500 chars recommended):
  - Use metatags for structure: [Verse], [Chorus], [Bridge]
  - 6-12 syllables per line
  - Clear section breaks
  - Specific emotional cues within sections

  example:
    [Short Instrumental Intro]

    [Verse] [intimate, minimal]
    Walking down the memory lane (8 syllables)
    Sunshine fades to gentle rain (8 syllables)
    Every moment feels so far away (10 syllables)
    Lost in thoughts of yesterday (8 syllables)

    [Chorus] [uplifting, full arrangement]
    But I'll rise again (5 syllables)
    Through the joy and pain (6 syllables)
    Finding light within the rain (8 syllables)

style_section (100-300 chars recommended):
  - Primary genre (most important first)
  - Secondary genre (if fusion)
  - Mood/emotion (1-2 descriptors)
  - Key instruments (2-3 max)
  - Vocal style
  - Tempo/BPM (optional)

  example:
    "Indie Pop, Electronic, Uplifting, Bittersweet, Female Vocals, Synth Pads, Acoustic Guitar, 115 BPM"
    (100 characters - clear, effective, within limits)

title (30-60 chars recommended):
  - Evocative but concise
  - Captures song essence
  - Avoid generic titles

  examples:
    good: "Echoes of Summer Light"
    good: "Midnight Revelations"
    avoid: "My Song" (too generic)
    avoid: "A Beautiful Melancholic Indie Pop Song About Lost Love and Finding Yourself Again" (too long)
```

---

## V5 PERSONA SYSTEM

### Built-In Personas

```yaml
personas:
  whisper_soul:
    style: "Intimate, breathy vocals"
    genres: R&B, Neo-Soul, Indie

  power_praise:
    style: "Strong, gospel-influenced"
    genres: Gospel, Soul, Pop

  retro_diva:
    style: "Classic, powerful vocals"
    genres: Pop, Disco, Soul

  conversational_flow:
    style: "Natural, spoken-word influenced"
    genres: Hip Hop, R&B, Indie

usage:
  - Reference in prompt: "Use [Persona Name] vocal style"
  - Or describe characteristics: "Whisper Soul style vocals"
  - Maintains consistency across generations
```

---

## MIGRATION FROM V4.5 TO V5

### What Changes

```yaml
prompts_from_v4_5:
  mostly_compatible: "95% of V4.5 prompts work in V5"

  improvements_noticed:
    - Better structure following
    - Cleaner vocal delivery
    - More professional mix
    - Faster generation

  adjustments_recommended:
    - Can add more detail (better parsing)
    - Emotion tags more effective
    - Genre fusion more stable
```

### What Stays the Same

```yaml
unchanged:
  - Character limits (5000/1000/100)
  - Metatag syntax ([Tag] format)
  - Basic prompt structure
  - Style field comma-separation
```

---

## CREDITS & COSTS (V5)

### Generation Costs

```yaml
standard_generation:
  cost: 10 credits per song
  includes: 2 variations

extend:
  cost: 10 credits per extension

replace_section:
  cost: 10 credits per replacement

remaster:
  cost: 10 credits per remaster

midi_export:
  cost: Credits required (amount varies)

stems:
  pro: Included (2 stems)
  premier: Included (12 stems)
```

**Note**: Credit costs may vary; check current pricing at suno.com

---

## SUMMARY: V5 FOR PROMPT ENGINEERING

### Key Takeaways

1. **Character Limits**: 5000/1000/100 but **brevity still wins** (100-300 chars style recommended)

2. **Metatag Reliability**: Significantly improved but **not perfect** (still use Tier 1 tags primarily)

3. **Prompt Adherence**: ~90% success rate with **well-structured prompts**

4. **Best Strength**: **Natural vocals** and **genre fusion** (2-genre combinations)

5. **Studio Integration**: **Non-destructive editing** workflow is game-changer

6. **Professional Output**: **Studio-grade quality** with minimal post-processing

### Golden Rules for V5

✅ Use generous limits for complex ideas, but stay concise when possible
✅ Leverage 2-genre fusion confidently
✅ Specify emotions explicitly (haunting, triumphant, bittersweet)
✅ Trust V5's automatic transitions and arrangements
✅ Use Studio Timeline for iterative refinement
✅ Provide custom lyrics (auto-gen still generic)
✅ Keep style field 100-300 chars for best results

---

**End of V5 Features Reference**

**Next**: See `suno_best_practices.md` for detailed prompting strategies and `template_library.md` for V5-optimized genre templates.
