# Linux Audio Plugin References

Curated from [Arch Linux pro-audio group](https://archlinux.org/groups/x86_64/pro-audio/).

## Plugin Collections (Effects)

| Package | GitHub | Description | Notes |
| --- | --- | --- | --- |
| **lsp-plugins** | [lsp-plugins/lsp-plugins](https://github.com/lsp-plugins/lsp-plugins) | 200+ plugins: EQ, comp, gate, reverb, delay | Huge, modular repo structure |
| **x42-plugins** | [x42/x42-plugins](https://github.com/x42/x42-plugins) | 80+ plugins: meters, EQ, tuner, delay | Submodules, Robin Gareus |
| **calf** | [calf-studio-gear/calf](https://github.com/calf-studio-gear/calf) | LV2 suite: comp, EQ, reverb, synths | Classic, feature-rich |
| **zam-plugins** | [zamaudio/zam-plugins](https://github.com/zamaudio/zam-plugins) | Compressors, EQ, saturation | Clean DSP, DPF-based |
| **dpf-plugins** | [DISTRHO/DPF-Plugins](https://github.com/DISTRHO/DPF-Plugins) | Collection of DPF-based plugins | Good DPF examples |
| **dragonfly-reverb** | [michaelwillis/dragonfly-reverb](https://github.com/michaelwillis/dragonfly-reverb) | Hall, room, plate reverbs | DPF-based, popular |

## Guitar/Bass Effects

| Package | GitHub | Description | Notes |
| --- | --- | --- | --- |
| **gxplugins.lv2** | [brummer10/GxPlugins.lv2](https://github.com/brummer10/GxPlugins.lv2) | Guitarix standalone LV2 plugins | Many pedal emulations |
| **guitarix** | [brummer10/guitarix](https://github.com/brummer10/guitarix) | Amp sim + effects suite | Faust DSP, large |

## Single-Purpose Plugins (Good Porting Candidates)

| Package | GitHub | Description | Complexity |
| --- | --- | --- | --- |
| **noise-repellent** | [lucianodato/noise-repellent](https://github.com/lucianodato/noise-repellent) | Broadband noise reduction | Medium |
| **wolf-shaper** | [pdesaulniers/wolf-shaper](https://github.com/pdesaulniers/wolf-shaper) | Waveshaper with graph editor | Low-Medium |

## Synths

| Package | GitHub | Description | Notes |
| --- | --- | --- | --- |
| **surge-xt** | [surge-synthesizer/surge](https://github.com/surge-synthesizer/surge) | Hybrid subtractive synth | Large, JUCE |
| **cardinal** | [DISTRHO/Cardinal](https://github.com/DISTRHO/Cardinal) | VCV Rack as plugin | Huge, modular |
| **dexed** | [asb2m10/dexed](https://github.com/asb2m10/dexed) | Yamaha DX7 emulation | JUCE-based |

## NIH-plug Ecosystem

### Official Examples (in nih-plug repo)

| Example | What to Learn |
| --- | --- |
| `plugins/examples/gain` | Minimal plugin, parameter smoothing |
| `plugins/examples/gain_gui_egui` | egui integration |
| `plugins/examples/gain_gui_vizia` | VIZIA integration |
| `plugins/examples/gain_gui_iced` | iced integration |
| `plugins/examples/stft` | FFT/spectral processing |
| `plugins/examples/poly_mod_synth` | Polyphonic synth, MIDI |
| `plugins/crisp` | Production plugin, saturation |
| `plugins/spectral_compressor` | Complex spectral DSP |

### Third-Party NIH-plug Plugins

| Project | GitHub | Description | GUI |
| --- | --- | --- | --- |
| **lamb-rs** | [magnetophon/lamb-rs](https://github.com/magnetophon/lamb-rs) | Lookahead compressor/limiter | VIZIA |
| **elysiera** | [azur1s/elysiera](https://github.com/azur1s/elysiera) | Shimmer reverb (Faust DSP) | None |
| **cyma** | [exa04/cyma](https://github.com/exa04/cyma) | Audio visualizer widgets | VIZIA |
| **nih-faust-jit** | [YPares/nih-faust-jit](https://github.com/YPares/nih-faust-jit) | JIT compile Faust DSP | Auto-gen |
| **crrshrr** | [erroreyes/crrshrr](https://github.com/erroreyes/crrshrr) | Bitcrusher | - |
| **FreqChain** | [Gluton-Official/FreqChain](https://github.com/Gluton-Official/FreqChain) | Frequency sidechain | - |
| **midiometry** | [dvub/midiometry](https://github.com/dvub/midiometry) | MIDI visualization | VIZIA |

### GUI Patterns

| Framework | Pros | Cons | Best For |
| --- | --- | --- | --- |
| **VIZIA** | Reactive, good widgets, cyma visualizers | Less docs | Production plugins |
| **egui** | Immediate mode, simple, fast iteration | Less pretty | Prototyping, simple UI |
| **iced** | Elm-like, clean architecture | Steeper learning | Complex state |
| **None** | Simplest, no deps | No UI | DSP-only, DAW controls |

### Faust + NIH-plug Pattern

Several plugins use Faust for DSP, Rust for plugin wrapper:

1. Write DSP in Faust (`.dsp` files)
2. Compile to Rust via `faust-build` crate in `build.rs`
3. Wrap generated `dsp.rs` with NIH-plug

**lamb-rs example** (`build.rs`):
```rust
faust_build::FaustBuilder::new("dsp/lamb-rs.dsp", "src/dsp.rs")
    .set_use_double(true)
    .build();
```

**Generated code** provides:
- `struct LambRs` with `init()`, `compute()`, `get_param()`, `set_param()`
- NIH-plug wrapper just calls `dsp.compute(count, inputs, outputs)`

Examples: lamb-rs, elysiera

### Implication for Porting Guitarix

Guitarix has **100+ Faust DSP files** at `trunk/src/LV2/faust/`:
- `tremolo.dsp` (48 lines, simple)
- `distortion.dsp` (137 lines, multi-band)
- `compressor.dsp`, `chorus.dsp`, `delay.dsp`, etc.

**Porting workflow**:
```
guitarix/*.dsp  →  faust-build  →  dsp.rs  →  NIH-plug wrapper
```

**No manual DSP translation needed** - Faust handles it.

Agent task becomes:
1. Copy `.dsp` file from guitarix
2. Set up `build.rs` with faust-build
3. Write NIH-plug parameter mapping
4. Optional: add GUI

## Frameworks (For Reference)

| Project | GitHub | Purpose |
| --- | --- | --- |
| **NIH-plug** | [robbert-vdh/nih-plug](https://github.com/robbert-vdh/nih-plug) | Rust plugin framework (target) |
| **DPF** | [DISTRHO/DPF](https://github.com/DISTRHO/DPF) | C++ plugin framework |
| **LV2** | [lv2/lv2](https://github.com/lv2/lv2) | LV2 spec + examples |
| **rust-faust** | [Frando/rust-faust](https://github.com/Frando/rust-faust) | Faust→Rust codegen |

## Local Reference Setup

Clone into `refs/` (gitignore it):

```bash
# NIH-plug framework + examples
git clone --depth 1 https://github.com/robbert-vdh/nih-plug refs/nih-plug

# NIH-plug third-party (patterns to follow)
git clone --depth 1 https://github.com/magnetophon/lamb-rs refs/lamb-rs
git clone --depth 1 https://github.com/azur1s/elysiera refs/elysiera
git clone --depth 1 https://github.com/exa04/cyma refs/cyma

# Source plugins to port (C/C++/Faust DSP)
git clone --depth 1 https://github.com/pdesaulniers/wolf-shaper refs/wolf-shaper
git clone --depth 1 https://github.com/lucianodato/noise-repellent refs/noise-repellent
git clone --depth 1 https://github.com/michaelwillis/dragonfly-reverb refs/dragonfly-reverb
git clone --depth 1 https://github.com/brummer10/GxPlugins.lv2 refs/gxplugins
git clone --depth 1 https://github.com/zamaudio/zam-plugins refs/zam-plugins
```

## What to Look At

| Ref | Focus |
| --- | --- |
| **nih-plug** | `plugins/examples/gain*`, parameter handling, `xtask bundle` |
| **lamb-rs** | Production VIZIA GUI, Faust DSP integration |
| **elysiera** | Faust reverb DSP, no-GUI pattern |
| **cyma** | VIZIA visualizer widgets |
| **wolf-shaper** | Simple DPF structure, waveshaper DSP to port |
| **noise-repellent** | FFT-based processing, spectral DSP |
| **dragonfly-reverb** | Reverb algorithms, DPF patterns |
| **gxplugins** | Guitarix DSP (Faust-generated C++) |
| **zam-plugins** | Clean compressor/EQ DSP |

## Recommended First Port

**wolf-shaper** → NIH-plug

Why:
- Single effect (waveshaper)
- Clear DSP (distortion curve)
- DPF structure is simple
- Has GUI (can skip initially)
- MIT license

## Sources

- [Arch pro-audio group](https://archlinux.org/groups/x86_64/pro-audio/)
- [awesome-linuxaudio](https://github.com/nodiscc/awesome-linuxaudio)
