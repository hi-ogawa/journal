# ML-Assisted Bass Transcription

Research on ML-assisted (not fully automated) bass transcription workflow.

## Why

Current bass cover workflow is entirely manual: transcribe by ear, MIDI in DAW, fingering in score app. Exploring ML tools to accelerate this process while maintaining quality control.

## Target Workflow

1. **Demucs** - Bass isolation from full mix (~90 sec)
2. **Basic Pitch / NeuralNote** - Audio to MIDI (70-85% accuracy)
3. **LLM Pattern Completion** - Extend repetitive sections via ABC notation
4. **LLM Fret Positioning** - Fine-tuned on personal transcription history
5. **Manual Review** - Final verification in MuseScore

## Key Insight

Fret positioning is ideal for LLM fine-tuning: purely text-based, context-dependent, personal training data available, bounded problem.

## Time Savings

- Manual: 55-75 min per track
- ML-assisted: 17-25 min per track
