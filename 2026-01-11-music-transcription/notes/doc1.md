# ML-assisted bass transcription: Current tools and realistic expectations

Bass guitar's monophonic nature makes it fundamentally easier to transcribe than piano or guitar—**90-95% pitch accuracy is achievable on clean recordings** with current tools. The technology has matured significantly, with several purpose-built bass solutions now available. However, fully automating your workflow from audio to fingered notation still requires piecing together multiple tools, and ghost notes, complex articulations, and low-frequency edge cases remain challenging.

## The practical bottom line for your workflow

Your current manual process (ear → MIDI in DAW → fingering in score app) can be substantially accelerated using a combination of stem separation, automatic pitch detection, and notation conversion. **The most effective current approach chains three tools**: Demucs for bass isolation, Basic Pitch or NeuralNote for audio-to-MIDI conversion, then MuseScore or Guitar Pro for notation with fingering.

For isolated bass recordings (DI or clean amp), expect **85-95% accuracy** requiring light cleanup. For bass extracted from full mixes, expect **70-85% accuracy** with more manual correction needed—the source separation step degrades transients and introduces artifacts. Complete automation of fingering suggestion remains an unsolved problem with no turnkey solution, though algorithmic approaches exist.

## Existing commercial tools worth considering

**Klangio Guitar2Tabs** and **BassConvert** are the only tools specifically designed for bass transcription. Klangio accepts audio (including YouTube links), outputs quantized/unquantized MIDI, MusicXML, and Guitar Pro tabs, and processes in seconds. It works best with isolated bass—the recommended workflow is to first run Demucs or Ultimate Vocal Remover to extract the bass stem. BassConvert (€29/month) claims to recognize fret positions, dynamics, and techniques including slap and walking bass.

**Melodyne 5** remains the professional standard for audio-to-MIDI in a DAW context. The Essential version ($99) handles monophonic bass well, with direct ARA2 integration into Logic, Cubase, Reaper, and Studio One. Users report it "works great except for very low/sub sounds"—the fundamental below ~50Hz can cause issues. For complex polyphonic passages, the Editor version ($449) includes DNA technology.

**NeuralNote** deserves special attention as it's a **free, open-source VST3/AU plugin** based on Spotify's Basic Pitch model. It works directly in your DAW, displays real-time transcription, supports pitch bend detection (critical for slides and vibrato), and exports MIDI via drag-and-drop. For bass covers, this is arguably the best value proposition available.

For stem separation specifically, **Moises** ($4-25/month) and **LALAL.AI** ($15-35/month) offer polished interfaces and excellent bass isolation, but neither produces MIDI—they're preprocessing steps for transcription tools.

## Open-source options that actually work

**Basic Pitch** from Spotify is the most practical open-source transcription solution. It's lightweight (<20MB, <17K parameters), runs in browser or via Python (`pip install basic-pitch`), and outputs MIDI with pitch bend data. The model is instrument-agnostic but handles monophonic bass well. Critical parameters for bass: set `minimum_freq=30` and `maximum_freq=500` to filter the relevant range.

**Demucs v4** (Meta) achieves state-of-the-art bass separation at **7.6 dB SDR**—the first model to surpass the theoretical ideal ratio mask. The `htdemucs_ft` variant includes fine-tuning that pushes separation quality even higher. Installation is straightforward (`pip install demucs`), and it processes a typical song in under a minute on GPU.

For pitch detection research or custom pipelines, **CREPE** achieves >90% raw pitch accuracy at 10-cent tolerance on monophonic sources, while **pYIN** (built into librosa) offers excellent robustness to the low-frequency noise characteristics of bass recordings.

## Why bass is both easier and harder for ML

Bass benefits significantly from being **predominantly monophonic**—this sidesteps the core difficulty of polyphonic transcription where models must determine which of multiple simultaneous pitches correspond to separate notes. State-of-the-art monophonic pitch detection (CREPE, SwiftF0) achieves over 90% accuracy, compared to 70-80% for polyphonic piano transcription.

However, bass presents unique **low-frequency challenges**. The standard 2048-sample FFT at 44.1kHz provides only ~21.5Hz resolution—meaning at low E (41Hz), you get roughly 2 frequency bins per semitone, far too coarse for accurate pitch detection. The Constant-Q Transform (CQT) addresses this with logarithmic frequency spacing that matches musical intervals, and most modern bass-capable models use CQT or harmonic stacking approaches.

The "missing fundamental" phenomenon creates additional complexity: bass guitar often produces harmonics louder than the fundamental frequency, especially in recordings with low-end roll-off. Human ears reconstruct the fundamental from the harmonic series, but naive pitch detectors can fail or report octave errors.

## Technique detection remains partially solved

Research has achieved **F-measure of 0.93 for bass string identification** (which string was plucked), and classification of plucking styles (fingerstyle, picked, muted, slap-thumb, slap-pluck) with reasonable accuracy. Expression detection (vibrato, bending, slides) also shows promise. The IDMT-SMT-Bass dataset provides labeled examples across these techniques.

Problematic cases include:
- **Ghost notes**: Very quiet, often masked, frequently missed by transcription systems
- **Hammer-ons/pull-offs**: Softer onsets create ambiguous note boundaries
- **Slides**: Continuous pitch change between notes requires contour tracking
- **Harmonics**: Different overtone structure can confuse models expecting fundamentals

Basic Pitch's pitch bend detection helps capture slides and vibrato as continuous gestures rather than discrete notes, which is valuable for expressive bass parts.

## Building a custom bass transcription system

The **minimum viable approach** (achievable in a day) chains existing tools:

```python
# 1. Separate bass from mix
from demucs.api import Separator
separator = Separator(model="htdemucs_ft")
origin, separated = separator.separate_audio_file("song.mp3")

# 2. Transcribe to MIDI
from basic_pitch.inference import predict
_, midi_data, _ = predict("bass.wav", minimum_freq=30, maximum_freq=500)
midi_data.write("bass.mid")
```

For **better results with custom fine-tuning** (1-2 weeks of work), the recommended base model is the High-Resolution Piano Transcription architecture (Kong et al., 2021), which has been successfully adapted for guitar and tolerates label misalignment well. Fine-tune on the **IDMT-SMT-Bass dataset** (3.6 hours of isolated bass notes across techniques, freely available on Zenodo) combined with synthetic bass lines rendered from MIDI using various virtual instruments.

**YourMT3+** represents the current research frontier—a Transformer-based multi-instrument transcription model that already includes IDMT-SMT-Bass in its training data. It achieves 14.7% F-score improvement over technique-unaware baselines through joint technique-and-note prediction.

Training requires meaningful GPU resources (RTX 3080+ with 10GB+ VRAM for fine-tuning, multi-GPU for training from scratch), but inference runs comfortably on consumer hardware.

## Automating the complete workflow

Your ideal pipeline—audio to fingered notation—can be largely automated with current tools:

| Stage | Recommended Tool | Alternative |
|-------|-----------------|-------------|
| Stem separation | Demucs htdemucs_ft | UVR (GUI wrapper) |
| Audio → MIDI | Basic Pitch / NeuralNote | Melodyne (commercial) |
| Beat tracking | madmom DBNBeatTracker | librosa (less accurate) |
| MIDI → Notation | MuseScore CLI | Dorico, Sibelius |
| Tablature | Guitar Pro import | Direct tab entry |

**Fingering optimization** is the least automated component. MuseScore (yes, the free one) has automatic tablature generation when you link a tab staff to notation, but it uses a naive algorithm that defaults to the lowest possible fret position for each note—essentially keeping everything near the nut regardless of playability. You can manually adjust positions afterward using `Ctrl+Up/Down` to move notes between strings, but there's no intelligent position-aware generation.

Guitar Pro provides better auto-tablature with some understanding of position playing, though still requires manual refinement. For true optimization, the algorithmic approach is well-established: build a graph where nodes represent (note, fret_position, finger) combinations, assign edge weights based on biomechanical costs (finger stretch, position shifts, string crossings), then find the minimum-cost path using dynamic programming or Dijkstra's algorithm. The AutoBassTab implementation documents this approach in detail, and PyGuitarPro allows programmatic manipulation of GP files for custom logic.

## Realistic accuracy expectations by scenario

| Source Material | Expected Pitch Accuracy | Cleanup Required |
|----------------|------------------------|------------------|
| DI recording, clean | 90-95% | Light (ghost notes, articulations) |
| Amped recording, isolated | 85-92% | Moderate |
| Separated from mix (Demucs) | 75-85% | Significant (transients affected) |
| Full mix, no separation | 60-75% | Heavy (masking issues) |

Onset detection typically achieves **85-92% F1-score** on clean material, dropping with source separation. Offset (note-off) detection runs 10-15% lower than onset detection—sustain and overlapping notes remain challenging.

Rhythm quantization works well for straightforward parts but can mangle syncopated bass lines. Set quantization strength to 50-75% rather than 100% to preserve groove, or use intelligent quantization in your DAW that analyzes the input pattern.

## Key technical libraries and resources

For Python-based automation:
```
pip install basic-pitch demucs music21 librosa madmom pretty_midi
```

Essential GitHub repositories:
- **Basic Pitch**: github.com/spotify/basic-pitch (transcription)
- **NeuralNote**: github.com/DamRsn/NeuralNote (VST plugin)
- **Demucs**: github.com/facebookresearch/demucs (separation)
- **CREPE**: github.com/marl/crepe (pitch detection)
- **YourMT3+**: github.com/mimbres/yourmt3 (state-of-the-art AMT)

The **IDMT-SMT-Bass dataset** (zenodo.org/records/7188892) provides the only substantial labeled bass-specific training data—essential for any custom model development.

## What remains unsolved

Complete automation of bass transcription to publication-ready notation with fingering is not yet achievable. The gaps:

- **Articulation notation**: Slap/pop, harmonics, and ghost notes require manual annotation
- **Enharmonic spelling**: MIDI-to-score conversion often chooses wrong sharp/flat
- **Complex rhythms**: Odd meters and quintuplets are poorly handled
- **Fingering intelligence**: No ML system suggests fingerings based on musical context
- **Human nuance**: Micro-timing that defines groove is typically quantized away

For bass covers specifically, expect to spend 20-40% of your previous manual time on cleanup rather than zero—but the tedious pitch-by-pitch work of initial transcription can be largely eliminated. The technology has reached the point where it's genuinely faster to correct ML output than to start from scratch by ear.
