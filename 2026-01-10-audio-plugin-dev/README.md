# Audio Plugin Development Research

Research and learning plan for open source audio plugin development, focusing on Rust-based options.

## Why

Exploring the current landscape of audio plugin development for hobbyist/indie use. Prior experience with nih-plug (December 2022) - built MIDI keyboard and soundfont player plugins.

## Key Topics

- **Plugin Formats**: VST3 (now MIT licensed!), CLAP, AU, LV2
- **Rust Frameworks**: NIH-plug (recommended), Clack, FunDSP
- **C++ Frameworks**: JUCE, iPlug2, FAUST, HISE
- **Testing**: Pluginval, Carla, DAW testing

## LLM-Friendly Workflow

Identified approaches for LLM collaboration in audio dev:
- Offline audio processing (no DAW reload cycle)
- Numerical DSP testing (assertions, not listening)
- FunDSP for DSP-as-code prototyping
- Text-based presets (JSON)
