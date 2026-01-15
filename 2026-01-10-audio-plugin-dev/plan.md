# Audio Plugin Development - Research & Learning Plan

## Prior Experience

Previously experimented with nih-plug in December 2022: https://github.com/hi-ogawa/nih-plug-examples

Built two plugins:
- `midi_keyboard` - MIDI input device
- `soundfont_player` - Soundfont playback with JACK MIDI

Used nih-plug + egui for GUI. Already familiar with `cargo xtask bundle` workflow.

## Overview

This document covers the current landscape of open source audio plugin development, with a focus on Rust-based options and alternatives to traditional C++/JUCE workflows.

## Plugin Formats

### VST3 (Now Open Source!)
- **Developer**: Steinberg
- **License**: **MIT** (as of October 2025, VST 3.8)
- **Status**: Industry standard, supported by virtually all DAWs
- **Pros**:
  - Universal DAW support
  - **Now MIT licensed** - no more proprietary agreements needed
  - Can freely use in closed-source/commercial projects
  - Sample-accurate automation
  - Stable, future-proof legal footing
- **Cons**: MIDI handling still awkward (CCs mapped to parameters), Steinberg still controls the spec

**What changed (October 2025)**:
- VST3 SDK moved from dual proprietary/GPLv3 to pure MIT license
- No need to sign Steinberg license agreements anymore
- Logo/trademark usage now optional
- ASIO SDK also relicensed to GPLv3 (dual with proprietary)

### CLAP (CLever Audio Plug-in)
- **Developer**: Open standard (u-he, Bitwig, and others)
- **License**: MIT - fully open source
- **Status**: Growing adoption, supported by FL Studio, Bitwig, Reaper, and more
- **Pros**:
  - MIT licensed (commercial-friendly, no royalties)
  - Full native MIDI support
  - Advanced threading model with "thread-pool" for DAW/plugin collaboration
  - Polyphonic parameter modulation as first-class feature
  - Non-destructive automation
- **Cons**: Slower DAW adoption compared to VST3, not yet universal

### AU (Audio Units)
- **Developer**: Apple
- **Platform**: macOS/iOS only
- **Status**: Required for Apple ecosystem

### LV2
- **Developer**: Open standard
- **Platform**: Primarily Linux
- **Status**: Standard for Linux audio

---

## Rust Frameworks

### NIH-plug (Recommended for Rust)
**Repository**: https://github.com/robbert-vdh/nih-plug

The most mature and feature-rich Rust framework for audio plugin development.

**Supported Formats**: VST3, CLAP

**Key Features**:
- Simple macro-based export: `nih_export_vst3!(Plugin)` or `nih_export_clap!(Plugin)`
- Efficient buffer iteration (per-sample, per-block, SIMD-ready)
- Built-in FFT adapters for spectral processing
- Sample-accurate automation support
- Zstandard-compressed state files
- Parameter types: float, int, bool, enum

**GUI Support**:
- egui (immediate mode, easy to use)
- iced (Elm-inspired)
- VIZIA (reactive)

**Licensing**:
- Framework: ISC license (permissive)
- VST3: Now MIT (as of Oct 2025) - **no more GPL concerns for VST3 plugins!**
- Both VST3 and CLAP plugins can now be fully proprietary

**Getting Started**:
```bash
# Clone and build an example
git clone https://github.com/robbert-vdh/nih-plug
cd nih-plug
cargo xtask bundle gain --release
```

**Why NIH-plug**: Lowest barrier to entry for Rust, can get a basic VST running in ~20 minutes, actively maintained, real production plugins built with it.

### Clack (Low-Level CLAP)
**Repository**: https://github.com/prokopyl/clack

Low-level, safe Rust bindings for CLAP. Use this if you need full control over the CLAP API or want to build a plugin host.

**Use Case**: Building hosts, advanced plugin architectures, or when NIH-plug is too high-level.

### clap-wrapper
**Repository**: https://crates.io/crates/clap-wrapper

Wraps CLAP plugins to export as VST3 and AUv2. Write once in CLAP, deploy everywhere.

### vst-rs (Legacy)
**Repository**: https://github.com/RustAudio/vst-rs

VST 2.4 implementation. Note: VST2 is deprecated by Steinberg, new licenses unavailable. Consider NIH-plug instead.

---

## Rust Audio Ecosystem (Supporting Crates)

### FunDSP
**Repository**: https://github.com/SamiPerttu/fundsp
**Downloads**: Popular in the Rust audio community

A DSP library with an elegant inline graph notation:

```rust
// Example: Simple oscillator with filter
let sound = sine_hz(440.0) >> lowpass_hz(1000.0, 0.5);
```

**Features**:
- Compile-time connectivity checking
- Static (AudioNode) and dynamic (AudioUnit) systems
- Bandlimited wavetable/granular synthesizers
- Moog ladder filter, SVF filters
- Reverb, oversampling, panning
- 32-bit (speed) and 64-bit (quality) variants

**Integrations**: bevy_fundsp (game engine), midi_fundsp (live synths)

### CPAL (Cross-Platform Audio Library)
**Repository**: https://github.com/RustAudio/cpal
**Downloads**: 8.7M total

Low-level cross-platform audio I/O:
- WASAPI, CoreAudio, ALSA, JACK, ASIO
- WebAssembly support
- Foundation for most Rust audio projects

### Rodio
**Repository**: https://github.com/RustAudio/rodio
**Downloads**: 5.3M total

High-level audio playback built on CPAL:
- Format decoding (FLAC, MP3, Vorbis, WAV via Symphonia)
- Simple playback API
- Good for games, apps, prototyping

---

## C++ Frameworks

### JUCE
**Website**: https://juce.com
**License**: GPLv3 (free for open source) or commercial ($40/month or $800)

The industry standard for audio plugin development.

**Pros**: Comprehensive, well-documented, huge community, handles all plugin formats
**Cons**: Commercial license for closed-source, heavy framework

### iPlug2
**Repository**: https://github.com/iPlug2/iPlug2
**License**: Fully open source

The main open-source alternative to JUCE.

**Supported Formats**: VST2, VST3, AU, AAX, standalone
**Pros**: Completely free, same GUI across all formats
**Cons**: Smaller community than JUCE

### FAUST
**Website**: https://faust.grame.fr
**License**: GPLv2

Functional programming language for DSP:
```faust
// Simple gain
process = *(0.5);
```

**Pros**: Concise DSP syntax, generates optimized C++, web playground
**Cons**: Domain-specific, steeper learning curve for complex UIs

### HISE
**Website**: https://hise.audio
**License**: GPLv3

Visual/scripting environment for building instruments:
- JavaScript-like scripting
- Node-based DSP wiring
- FAUST integration
- Great for samplers, romplers, simple synths

---

## Learning Resources

### Curated Lists
- [awesome-audio-dsp](https://github.com/BillyDM/awesome-audio-dsp) - Comprehensive DSP resource list
- [awesome-musicdsp](https://github.com/olilarkin/awesome-musicdsp) - Music DSP and audio programming
- [Audio-Plugin-Development-Resources](https://github.com/jareddrayton/Audio-Plugin-Development-Resources)

### Books
- **"The Complete Beginner's Guide to Audio Plug-in Development"** by Matthijs Hollemans
  - From zero knowledge to working plugin
  - Covers C++, IDE setup, JUCE, DSP basics

- **"Designing Audio Effect Plug-Ins in C++"** by Will Pirkle
  - Deep dive into effect algorithms
  - Virtual analog techniques

- **"Designing Software Synthesizer Plug-Ins in C++"** by Will Pirkle
  - Synth architecture and algorithms

### Online Courses
- [Kadenze: Intro to Audio Plugin Development](https://www.kadenze.com/courses/intro-to-audio-plugin-development/info) - Free, covers VST/AU
- [Official JUCE Course](https://juce.com/learn/tutorials) - Free, comprehensive JUCE tutorials

### Video
- [The Audio Programmer YouTube](https://www.youtube.com/c/TheAudioProgrammer) - JUCE tutorials, industry interviews
- [The Audio Programmer Discord](https://discord.gg/theaudioprogrammer) - Active community, beginner-friendly

### DSP Theory
- [musicdsp.org](https://www.musicdsp.org) - Algorithm archive
- [DSPRelated.com](https://www.dsprelated.com) - Articles and tutorials

---

## Testing & Debugging Tools

### Pluginval
**Repository**: https://github.com/Tracktion/pluginval
**License**: GPLv3

Automated plugin validation:
- CLI and GUI modes
- Strictness levels 1-10 (5+ recommended for host compatibility)
- CI/CD integration support
- Catches crashes, memory issues, parameter bugs

```bash
# Example usage
pluginval --validate /path/to/plugin.vst3 --strictness-level 5
```

### Carla
**Repository**: https://github.com/falkTX/Carla
**License**: GPLv2

Full-featured plugin host:
- Supports LADSPA, DSSI, LV2, VST2, VST3, AU
- Patchbay mode for complex routing
- Dummy driver for leak detection
- Available on Linux, macOS, Windows

### DAW Testing
- **REAPER**: Affordable, excellent for testing (supports CLAP, VST3, LV2)
- **Ardour**: Open source DAW, good for Linux testing
- **Bitwig**: Strong CLAP support, good for modulation testing

---

## Recommended Learning Path

### If you prefer Rust:

1. **Start with NIH-plug examples**
   ```bash
   git clone https://github.com/robbert-vdh/nih-plug
   cd nih-plug
   # Study the gain example
   cargo xtask bundle gain --release
   ```

2. **Learn FunDSP for DSP prototyping**
   - Experiment with the graph notation
   - Build filters, oscillators, effects

3. **Build progressively**:
   - Gain plugin (parameter smoothing)
   - Simple filter (biquad, state variable)
   - Delay effect (circular buffer)
   - Synthesizer (oscillators, envelopes, voices)

4. **Add GUI with egui**
   - Start with nih-plug's egui examples
   - Build custom widgets as needed

### If you prefer C++:

1. **Start with JUCE tutorials** (free if open source)
2. **Or use iPlug2** for fully open source approach
3. **Study Will Pirkle's books** for DSP depth
4. **Join The Audio Programmer Discord** for community support

### DSP Fundamentals to Learn:

1. Sample rate, bit depth, buffer size
2. Filters (lowpass, highpass, bandpass, biquad)
3. Oscillators (sine, saw, square, wavetable)
4. Envelopes (ADSR)
5. Delay lines, feedback
6. Modulation (LFO, envelope followers)
7. FFT/spectral processing
8. Oversampling, aliasing

---

## Quick Reference: When to Use What

| Goal | Recommended Tool |
|------|------------------|
| Rust + VST3/CLAP | NIH-plug |
| Rust + CLAP only (no GPL) | NIH-plug (CLAP export only) |
| Rust + Custom host | Clack |
| Rust + DSP prototyping | FunDSP |
| Rust + Game audio | CPAL + Rodio |
| C++ + Commercial | JUCE (paid license) |
| C++ + Open source | iPlug2 or JUCE (GPL) |
| Visual/Scripting | HISE |
| DSP algorithm design | FAUST |

---

## LLM-Friendly Workflow

### The Challenge

**LLMs are good at**: Reading/writing code, text configs, CLI tools, analyzing logs/data
**LLMs are bad at**: GUIs, listening to audio, real-time interaction, subjective tuning

Traditional audio plugin development has pain points for LLM collaboration:
- "Does it sound right?" requires human ears
- GUI-heavy tools (node wiring, knob tweaking)
- DAW reload cycle (build → restart DAW → load plugin → test)
- Subjective feedback ("too muddy", "needs more presence")

### LLM-Friendly Approaches

#### 1. Offline Audio Processing
```bash
# Render test audio to file, no DAW needed
cargo run --bin my_effect -- input.wav output.wav --param gain=0.5
```
Process files, diff outputs, iterate in code.

#### 2. Numerical DSP Testing
- Test impulse responses, frequency responses as data
- Assert filter cutoff is -3dB at target frequency
- Compare output samples against expected values
- No listening required for correctness

#### 3. FunDSP for Prototyping
```rust
// DSP as code, not visual wiring
let chain = sine_hz(440.0) >> lowpass_hz(1000.0, 0.7) >> pan(0.0);
```
LLM can read, write, and reason about DSP directly.

#### 4. CLI Spectral Analysis
```bash
sox output.wav -n spectrogram -o spec.png
ffmpeg -i output.wav -af "showfreqs" -f null -
```
Analyze audio properties without listening.

#### 5. Text-Based Presets
NIH-plug uses JSON for state - LLM can read/write presets directly.

#### 6. Standalone Mode
Build as standalone app, test without DAW loading cycle.

#### 7. MIDI as Text Input
```
note_on 60 127 0.0
note_off 60 0 0.5
```
Script test sequences, no manual playing.

### Ideal Stack for LLM Collaboration

```
FunDSP (prototype DSP as code)
    ↓
NIH-plug (wrap as plugin)
    ↓
Offline CLI renderer (test without DAW)
    ↓
Numerical assertions (verify correctness)
    ↓
pluginval (validate plugin compliance)
```

**Division of labor**:
- LLM handles: Code structure, DSP algorithms, correctness testing, iteration
- Human handles: "Does it sound good?" tuning, subjective quality

---

## Industry Context

The audio industry remains approximately 99% C++. However, Rust is gaining traction:
- NIH-plug has production plugins (Diopser, Spectral Compressor)
- Safety guarantees help with real-time audio constraints
- Growing ecosystem and community

For hobbyist/indie development, Rust is a viable choice. For professional employment, C++ proficiency is still expected.

---

## Sources

- [NIH-plug GitHub](https://github.com/robbert-vdh/nih-plug)
- [FunDSP GitHub](https://github.com/SamiPerttu/fundsp)
- [CLAP Developer Guide](https://cleveraudio.org/developers-getting-started/)
- [awesome-audio-dsp](https://github.com/BillyDM/awesome-audio-dsp)
- [Kadenze Plugin Course](https://www.kadenze.com/courses/intro-to-audio-plugin-development/info)
- [The Audio Programmer](https://www.theaudioprogrammer.com/)
- [Pluginval](https://github.com/Tracktion/pluginval)
- [Carla Plugin Host](https://github.com/falkTX/Carla)
- [KVR Audio Forums](https://www.kvraudio.com/forum/)
- [JUCE vs CLAP Discussion](https://www.martinic.com/en/blog/clap-audio-plugin-format)
