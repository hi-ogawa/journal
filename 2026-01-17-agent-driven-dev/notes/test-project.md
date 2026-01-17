# Test Project: LV2 to VST3 Plugin Porting

## Goal Recap

- DSP algorithm = pure math, copy verbatim, don't verify
- API integration = agent researches and ports
- Build system = agent can verify compilation passes
- Manual testing = human verifies audio at the end

## Key Insight: Faust Changes Everything

**Guitarix plugins use Faust DSP** - a high-level functional DSP language.

Faust compiles to multiple backends including **Rust**. This means:

```
Traditional porting:  C++ DSP code  →  manually translate  →  Rust
Faust porting:        Faust .dsp   →  faust-build crate   →  Rust (auto)
```

**Agent task simplifies to**:
1. Copy `.dsp` file from guitarix
2. Set up `build.rs` with faust-build
3. Write NIH-plug parameter mapping (boilerplate)
4. `cargo build` verifies everything

**No manual DSP translation** - Faust compiler does it.

Guitarix has **100+ Faust DSP files** ready to use:
- `tremolo.dsp` (48 lines)
- `distortion.dsp` (137 lines)
- `compressor.dsp`, `chorus.dsp`, `delay.dsp`, etc.

See `refs/guitarix/trunk/src/LV2/faust/` for full list.

## Framework: NIH-plug (Rust)

**Why NIH-plug:**

1. Already familiar (prior experience with nih-plug-examples)
2. Pure Rust - `cargo xtask bundle` builds VST3/CLAP
3. Minimal dependencies - just Rust toolchain
4. Docker-friendly - no system libs needed for headless build
5. Good examples in repo
6. ISC license

## Candidate Plugins to Port

**Recommended: Guitarix Faust plugins** (automatic Rust codegen)

### Tier 1: Simple (good first target)

| Plugin | Lines | Description |
| --- | --- | --- |
| `tremolo.dsp` | 48 | Vactrol tremolo model |
| `bassbooster.dsp` | ~30 | Simple bass boost |
| `echo.dsp` | ~50 | Basic delay |

### Tier 2: Medium

| Plugin | Lines | Description |
| --- | --- | --- |
| `distortion.dsp` | 137 | Multi-band distortion |
| `compressor.dsp` | ~100 | Compressor |
| `chorus.dsp` | ~80 | Chorus effect |
| `flanger.dsp` | ~80 | Flanger |

### Tier 3: Complex (stretch goal)

| Plugin | Description |
| --- | --- |
| `gxamp*.dsp` | Tube amp simulations |
| `freeverb.dsp` | Reverb algorithm |

### Alternative: Non-Faust plugins

If testing manual DSP translation:

| Plugin | Repo | Notes |
| --- | --- | --- |
| wolf-shaper | pdesaulniers/wolf-shaper | DPF, waveshaper, MIT |
| noise-repellent | lucianodato/noise-repellent | FFT-based, GPL |

## Build Verification Strategy

Agent verifies with Cargo:

```bash
cargo build --release 2>&1 | tee build.log
cargo xtask bundle plugin_name --release
test -d target/bundled/*.vst3 && echo "SUCCESS"
```

Human verifies:

- Load VST3 in DAW
- Play audio through it
- Does it sound correct?

## Docker Container Setup

For NIH-plug/Rust builds:

```dockerfile
# Just Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# That's it - no system audio libs needed for headless build
```

Simpler than C++ frameworks - no ALSA/Mesa headers needed.

## Sources

- [NIH-plug GitHub](https://github.com/robbert-vdh/nih-plug)
- [justOneOctaveUp.lv2](https://github.com/rominator1983/justOneOctaveUp.lv2)
- [Kapitonov Plugins Pack](https://github.com/olegkapitonov/Kapitonov-Plugins-Pack)
- [GxPlugins.lv2](https://github.com/brummer10/GxPlugins.lv2)
