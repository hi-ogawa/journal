# ML-Assisted Bass Transcription Workflow

## Problem Statement

Current bass cover workflow is entirely manual: transcribe by ear → MIDI in DAW → fingering in score app. Explore ML-assisted (not fully automated) approaches to accelerate this process while maintaining quality control.

## Current Workflow

```
Audio (full mix or isolated bass)
       │
       ▼
┌──────────────────┐
│  Transcribe      │  ← Manual, by ear (bottleneck)
│  to MIDI in DAW  │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Export to       │  ← MuseScore for notation
│  Score App       │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Manual Fret     │  ← Second bottleneck
│  Positioning     │
└──────────────────┘
       │
       ▼
    Fingered Tab / Score
```

## ML-Assisted Approach

Key insight: Not seeking full automation, but **interactive assistance** where ML handles tedious pattern work while human maintains creative/verification control.

### Three Opportunities

1. **Audio → MIDI**: ML pitch detection (70-85% accuracy) as starting point
2. **Pattern Completion**: LLM extends repetitive sections given partial transcription
3. **Note → Fret Positioning**: LLM inference (text-only, trainable on personal data)

## Target Workflow

```
Audio (full mix)
       │
       ▼
┌──────────────────┐
│  Demucs          │  ← Stem separation (~90 sec)
│  Bass Isolation  │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Basic Pitch /   │  ← 70-85% pitch accuracy
│  NeuralNote      │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Manual Cleanup  │  ← Fix obvious errors, unique sections
│  + LLM Pattern   │  ← Extend repetitive parts via ABC notation
│  Completion      │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  LLM Fret        │  ← Fine-tuned on personal transcription history
│  Positioning     │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Manual Review   │  ← Final verification in MuseScore
└──────────────────┘
       │
       ▼
    Fingered Tab / Score
```

## Research Summary

### Audio → MIDI Tools

| Tool | Type | Accuracy | Notes |
|------|------|----------|-------|
| Basic Pitch | Python/Web | 85-95% (isolated) | Spotify open-source, pitch bend support |
| NeuralNote | VST Plugin | Similar | Free, DAW integration |
| Melodyne | Commercial | Professional | $99-449, ARA2 integration |
| Klangio | Cloud | Good | Accepts YouTube links |

### Stem Separation

| Tool | Quality | Notes |
|------|---------|-------|
| Demucs v4 | 7.6 dB SDR | State-of-art, htdemucs_ft variant |
| Moises | Excellent | $4-25/month, polished UI |
| UVR | Good | Free GUI wrapper |

### LLM Pattern Completion

- **ABC notation** is the sweet spot for text-based LLMs
- ChatMusician (open-source) outperforms GPT-4 on music generation
- MIDI-LLM supports native infilling
- 70-85% success rate for pattern extension tasks

### Note-to-Fret Positioning (Best LLM Application)

This is ideal for LLM fine-tuning because:
- Purely text-based (no audio ambiguity)
- Context-dependent (position N depends on N-1)
- Personal training data available (past transcriptions)
- Bounded problem (4 strings, limited frets)

Expected accuracy with fine-tuning:
- Few-shot (GPT-4/Claude): 60-75%
- Fine-tuned GPT-2: 75-85%
- Fine-tuned LLaMA 7B: 85-92%

## Implementation Steps

### Phase 1: Audio Pipeline
- [ ] Set up Demucs for bass isolation
- [ ] Set up Basic Pitch for audio→MIDI
- [ ] Test pipeline on sample tracks
- [ ] Benchmark accuracy on known transcriptions

### Phase 2: LLM Pattern Completion
- [ ] Establish MIDI ↔ ABC notation conversion
- [ ] Test pattern extension with GPT-4/Claude
- [ ] Evaluate ChatMusician for better music understanding
- [ ] Build prompt templates for bass-specific generation

### Phase 3: Fret Positioning Model
- [ ] Export past transcriptions from MuseScore (MusicXML)
- [ ] Extract MIDI→fingering pairs programmatically
- [ ] Test few-shot prompting with consumer LLMs
- [ ] Fine-tune small model (GPT-2 or similar)
- [ ] Integrate into workflow

### Phase 4: End-to-End Pipeline
- [ ] Build unified Python workflow
- [ ] Create CLI tool for batch processing
- [ ] Measure time savings vs manual workflow

## Key Tools & Libraries

```bash
pip install basic-pitch demucs music21 librosa pretty_midi
```

- **basic-pitch**: Spotify's pitch detection
- **demucs**: Meta's stem separation
- **music21**: MusicXML/ABC parsing
- **pretty_midi**: MIDI manipulation

## Accuracy Expectations

| Source Material | Pitch Accuracy | Cleanup Required |
|-----------------|----------------|------------------|
| DI recording | 90-95% | Light |
| Separated from mix | 75-85% | Significant |
| Full mix (no separation) | 60-75% | Heavy |

## Time Savings Estimate

| Task | Manual | ML-Assisted |
|------|--------|-------------|
| Full transcription | 45-60 min | 15-20 min |
| Fret positioning | 10-15 min | 2-5 min |
| **Total** | **55-75 min** | **17-25 min** |

## What Remains Manual

- Ghost notes (too subtle for ML)
- Unique one-time fills (no pattern to extend)
- Micro-timing/groove nuances
- Technique annotations (slap, harmonics)
- Final verification against audio

## Notes

See `notes/` directory for detailed research:
- `doc1.md`: Current tools and accuracy benchmarks
- `doc2.md`: LLM pattern completion workflows
- `doc3.md`: Note-to-fret positioning fine-tuning

---

## Progress Log

### 2026-01-11

- Created plan based on prior research
- Focus: ML-assisted (not automated) bass transcription
- Key insight: Fret positioning is ideal LLM application (text-only, trainable)
