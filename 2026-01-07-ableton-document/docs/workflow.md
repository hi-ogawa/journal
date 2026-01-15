# Ableton Live Lite - My Workflow

Personal workflow for bass cover audio production and MIDI transcription.

**Scope**: This document contains a mix of:
- Ableton-specific workflows and shortcuts
- General audio production knowledge (compression, EQ, limiting concepts)
- Personal setup and preferences (hardware, latency settings, practice routine)

## Verification Status (Updated 2026-01-04)

✅ **VERIFIED AGAINST OFFICIAL DOCS**: All keyboard shortcuts and core workflows verified against Ableton Live 12 official documentation.

**Key corrections made:**
- `F` is "Fold to Notes", not "Fold view"
- `A` is NOT "Select mode" in MIDI editor (it's Automation Mode toggle in Arrangement)
- No default `A` key for select mode - just use `Esc` to exit Draw Mode
- `Ctrl+L` is "Loop Selection" (sets loop AND enables it), not just "set loop brace"
- Locator shortcuts (`/`, `,`, `.`, `1-9`) are **PerforModule template only**, NOT default Ableton
- Default Ableton uses "Set Locator" button and "Previous/Next Locator" buttons (no keyboard shortcuts)
- No backtick or `p` shortcuts for playback in default Ableton
- `Alt+Space` does NOT play from clip position - that's `Ctrl+Space` (Win) / `Option+Space` (Mac) for "Stop at end of selection"

## Context

- **Background**: Linux audio production (Ardour, JACK, PipeWire)
- **Current setup**: Windows 11 + Ableton Live Lite + Focusrite Scarlett
- **Goal**: Bass recording, mixing, and manual MIDI transcription
- **Philosophy**: Manual transcription as ear training, not automation

## Audio Production

✅ **Verified**: Basic backtrack + bass DI mixing workflow confirmed working.

#### Initial Setup

**Audio preferences (first time):**
- Audio Device: Focusrite USB ASIO
- Sample Rate: 44100 Hz
- Buffer Size: 128 samples (adjust for latency vs stability)

**Import backing track:**
- Drag WAV file onto track
- Enable Warp on clip
- Set/verify project tempo

#### Recording

1. Create audio track (Ctrl+T)
2. Input: Scarlett channel 1
3. Monitor: Off (use Scarlett direct monitoring)
4. Arm track
5. Record bass performance

#### Mixing Chain

**Backing track:**
- MEqualizer: Low shelf boost ~150Hz, kick boost ~60Hz if needed

**Bass track:**
1. MEqualizer (initial trim)
2. MEqualizer (fine-tuning)
3. MCompressor:
   - Ratio: 3:1 to 4:1
   - Attack: 5-10ms
   - Release: 100-200ms
4. Reverb (minimal, built-in is fine)

**Master track:**
- Limiter (safety, -0.3 dB ceiling)

**Export:**
- File → Export Audio/Video
- Format: WAV, 44100 Hz, 16-bit
- Save as `final-mix.wav`

## Daily Practice Setup

🔄 **In Progress**: Exploring software-based practice setup to replace external pedal.

### Current Approach

**Goal**: Replace external multi-effects pedal with Live Lite for daily practice (non-recording).

**Previous setup**: Bass → Pedal (compressor + amp sim + reverb) → Direct monitor + PC audio blend

**New software setup**: Bass → Scarlett → Live Lite (plugins) → Blend with browser audio → Headphones

### Latency Configuration

**Current settings**:
- Sample Rate: 44100 Hz
- Buffer Size: 128 samples
- Round-trip latency: ~15ms (acceptable for practice)

**Optimization option**:
- Buffer Size: 64 samples → ~7-8ms (more responsive, test if system handles it)
- Adjust in: Preferences → Audio → Buffer Size

### Practice Signal Chain

**Basic chain** (being tested):
1. Tuner (built-in or plugin)
2. Amp/Cabinet (Live Lite built-in, exploring better options)
3. Reverb (built-in presets work well)

**Notes**:
- Live Lite's built-in Amp device is basic but functional
- Live Lite's built-in Cabinet device for speaker simulation
- Built-in Reverb presets confirmed working well

### Blending with Backing Tracks

**Method 1: Driver-level blend** (current practice workflow)
- YouTube/browser audio plays through Windows audio
- Live Lite runs through ASIO
- Focusrite driver blends both automatically
- Works fine for practice, but check sample rate alignment:
  - Windows Sound Settings → Scarlett → Properties → Advanced
  - Set to: "2 channel, 24 bit, 44100 Hz" (match ASIO settings)
  - Mismatched rates (e.g., Windows at 48000 Hz) cause resampling artifacts

**Method 2: DAW-internal blend** (better for recording)
- Import backing track WAV into Live Lite
- Everything runs through ASIO cleanly
- More reliable, no sample rate issues

### Bass Amp Sim Exploration

⚠️ **UNVERIFIED**: Amp sim recommendations from LLM conversations, not yet tested.

**Current**: Using Live Lite built-in Amp + Cabinet devices

**Exploring free alternatives**:
- **Amplitube 5 Free** - Includes bass amp models
- **STL Tones Ignite Emissary/NadIR** - Metal-focused but good bass tone
- **LePou amp sims** - Free, decent quality
- **TSE BOD** - Bass overdrive plugin

**Next steps**:
- Test built-in Amp device settings thoroughly
- Compare with free amp sims listed above
- Document preferred settings for practice tone

### Plugin Management

**Plugin Format Guide**:

Most plugin installers offer multiple formats - you can select which to install:
- **VST3** (.vst3) - Modern standard, best performance, use this for Ableton ✅
- **VST2** (.dll) - Older format, skip if VST3 available ❌
- **AAX** - Pro Tools only, skip if you don't have Pro Tools ❌
- **AU** (Mac only) - Audio Units for Logic/GarageBand
- **Standalone** - Runs without DAW, useful for testing/practice ✅

**For Ableton Live Lite**, install only:
- ✅ VST3 (best option)
- ✅ Standalone (optional, convenient for testing)
- ❌ Skip VST2, AAX (save disk space, avoid duplicate entries)

**VST Folder Conventions (Windows)**:
- **VST2** (.dll): `C:\Program Files\VstPlugins\[Vendor Name]\` (custom location, use vendor subfolders)
- **VST3** (.vst3): `C:\Program Files\Common Files\VST3\` (fixed by specification, cannot change)

**Installed plugins**:
- MeldaProduction: VST3 (also has VST2 but disabled in Ableton)
- IK Multimedia AmpliTube: VST3 + Standalone
- MPluginManager prompts for admin access: Can ignore, only needed for updates

**Plugin configuration** (current setup):
1. Preferences → Plug-Ins → Plug-In Sources
2. Turn OFF "Use VST Plug-In Custom Folder" (disables VST2, using VST3 only)
3. Turn ON "Use VST3 Plug-in System Folder" (scans `C:\Program Files\Common Files\VST3\`)
4. Click "Rescan"
5. Plugins appear in Browser → Plug-ins tab (VST3 versions only)

## MIDI Transcription

✅ **VERIFIED**: Core shortcuts verified against official Ableton Live 12 documentation.
⚠️ **NOTE**: Locator shortcuts (`/`, `,`, `.`, `1-9`) are from PerforModule template, NOT default Ableton.

**My approach from Ardour:**
1. Align DAW tempo with backing track
2. Create locators to mark song parts (verse, chorus, bridge)
3. Loop small sections and transcribe by ear

**Setup:**
1. Create MIDI track (Ctrl+T → MIDI)
2. Enable metronome (top-left icon, uncheck "Enable Only While Recording")
3. Adjust global tempo if needed (can slow down for transcribing)

### Slowing Down for Transcription

✅ **VERIFIED**: Warping allows slowing down while maintaining pitch.

**Steps to slow down audio:**
1. **Enable Warp** on audio clip (double-click clip → turn on Warp switch in Clip View)
2. **Choose Warp Mode** (in Clip View's Audio panel):
   - **Complex or Complex Pro**: Best for full songs/polyphonic material
   - **Tones**: Good for bass/monophonic instruments with distinct pitch
   - **Beats**: For percussive/rhythmic material
3. **Lower global tempo** in Control Bar's tempo field (top of screen)
   - Click and drag to adjust, or hold Shift while dragging for fine adjustments
   - Example: 120 BPM → 80 BPM for easier transcription
4. **Enable metronome** (click metronome icon in Control Bar) for tempo reference

**Result**: Audio slows down while maintaining original pitch - perfect for transcription!

**Note**: Don't use Re-Pitch mode for transcription - it changes pitch like old tape/vinyl.

**Locators:**
- **Default Ableton**: Use "Set Locator" button in Control Bar, or Create menu → Add Locator
- **Default Ableton**: Click "Previous/Next Locator" buttons to navigate (no keyboard shortcuts by default)
- **PerforModule template only**: `/` set locator, `,` previous, `.` next, `1-9` jump to numbered locator
- Double-click locator to rename (e.g., "Verse 1", "Chorus")

### Navigation & Playhead Movement

✅ **VERIFIED**: Insert marker and scrub area behavior confirmed.

**Playhead (Insert Marker)**: The flashing blue line that shows where playback starts.

**Moving playhead without playing:**
1. **Click in track area** (not scrub area) - moves insert marker without starting playback
2. **Type position** in Control Bar's Arrangement Position fields (bars-beats-sixteenths)
3. **Keyboard shortcuts:**
   - `Home` (Win) / `Fn+Left Arrow` (Mac) - Return to start
   - `Left/Right arrows` - Move insert marker in time
   - `Ctrl+Left/Right` (Win) / `Option+Left/Right` (Mac) - Snap to locators/clip edges

**Scrubbing (moving + playing):**
- **Scrub area** = bar above tracks (between beat ruler and tracks)
- **Click scrub area** - Starts playback from that point
- **Hold mouse down** in scrub area - Loops that section
- `Shift+Click` beat-time ruler - Scrub without quantization

**Clip View scrubbing:**
- Click lower half of waveform OR scrub area below time ruler - Jumps to that point in clip

**Piano roll shortcuts:**
- `F` - Fold to Notes (show only key tracks containing notes)
- `B` - Draw mode (click to place notes)
- `Esc` - Exit draw mode, return to select mode (no dedicated "A" shortcut)
- Ctrl+L (Cmd+L) - Loop Selection (sets loop brace to selection AND enables loop)
- Ctrl+D (Cmd+D) - Duplicate selected notes
- `0` (zero) - Deactivate (mute) selected notes
- Ctrl+Space (Option+Space Mac) - Stop playback at end of selection
- Shift+Left/Right Arrow - Shorten/extend selected note(s) duration by grid increment

**Transcription process:**
1. Set loop to 2-4 bar section
2. Fold view to bass range (E1-G3)
3. Enable note preview (headphone icon in piano roll)
4. Draw notes in rhythm first, adjust pitch second
   - In Draw Mode (B), click creates note at current grid length (e.g., 16th note)
   - To extend note: Select note, then Shift+Right Arrow to extend by grid increments
   - Alternative: Click right edge of note and drag to desired length
5. Edit velocity for dynamics
6. Verify by playing along with bass
7. Move to next section

**Grid settings:**
- Ctrl+1 - Narrow grid (more precision)
- Ctrl+2 - Widen grid
- Ctrl+4 - Toggle snap on/off
- Hold Alt while dragging - Temporary disable snap

**Export MIDI:**
- Right-click MIDI clip → Export MIDI Clip
- Save as `bass-transcription.mid` (for use in MuseScore or other notation software)

## Project File Organization

```
D:\Projects\song-name\
├── backtrack.wav           # Backing track audio
├── song-name.als           # Ableton project file
├── Samples\                # Ableton auto-creates (recorded audio)
├── final-mix.wav           # Exported audio mix
└── bass-transcription.mid  # Exported MIDI (optional)
```

**Benefits:**
- All Ableton assets in one folder
- Easy to archive entire project folder
- Relative paths work when moved to external drive

## Key Shortcuts

✅ **VERIFIED**: Default Ableton Live 12 shortcuts verified against official documentation.
⚠️ **NOTE**: PerforModule-specific shortcuts marked clearly.

### Locators & Navigation (PerforModule Template Only)
⚠️ These are NOT default Ableton shortcuts - they require PerforModule template:
- `/` - Set locator (Default: Use "Set Locator" button or Create menu)
- `,` - Previous locator (Default: Click "Previous Locator" button)
- `.` - Next locator (Default: Click "Next Locator" button)
- `1`, `2`, `3`... - Jump to locator 1, 2, 3... (Default: Click on locator)

### Playback (Default Ableton)
- Space - Play from start marker / Stop
- Shift+Space - Continue play from stop point
- (PerforModule may add backtick/`p` shortcuts, not in default Ableton)

### Loop (Default Ableton)
- Ctrl+L (Cmd+L) - Loop Selection (enables loop AND sets brace to selection)
- Ctrl+L (Cmd+L) again - Toggle loop off when clip/time is selected

### MIDI Editor (Default Ableton)
- `B` - Toggle Draw Mode (click to add notes, click existing notes to delete)
- `Esc` - Exit draw mode (no dedicated "A" for select mode)
- `F` - Fold to Notes (show only key tracks with notes)
- `K` - Highlight Scale (when scale mode is enabled)
- `0` - Deactivate (mute) selected notes
- Ctrl+D (Cmd+D) - Duplicate
- Ctrl+1/2 (Cmd+1/2) - Narrow/widen grid
- Ctrl+3 (Cmd+3) - Toggle triplet grid
- Ctrl+4 (Cmd+4) - Toggle snap to grid
- Alt (Cmd on Mac) while dragging - Bypass snap temporarily

### Track Management (Default Ableton)
- Ctrl+T (Cmd+T) - Insert audio track
- Ctrl+Shift+T (Cmd+Shift+T) - Insert MIDI track
- Ctrl+E (Cmd+E) - Split clip at selection
- Ctrl+R (Cmd+R) - Rename selected track/clip/locator

## Ardour → Ableton Mappings

✅ **VERIFIED**: Core terminology and workflow differences confirmed.

| Ardour | Ableton | Notes |
|--------|---------|-------|
| Markers | Locators | Default: Button/menu (no shortcuts); PerforModule adds `/`,`,`,`.` |
| Regions | Clips | Same concept, different terminology |
| JACK routing | Internal routing | Less flexible in Ableton Lite |
| Timeline ruler click | Scrub area click | Starts playback from that point |

## Common Issues & Solutions

✅ **VERIFIED**: Solutions confirmed against official documentation.

**Delay when clicking scrub area during playback:**
- **Issue**: Odd delay when clicking scrub area to jump to a different position while already playing
- **Cause**: **Quantization** - jumps are quantized to the next bar/beat boundary (musical timing feature)
- **Solution 1**: Press `Ctrl+0` (Win) / `Cmd+0` (Mac) to **disable quantization** (instant jumps)
- **Solution 2**: Use smaller quantization for shorter delays:
  - `Ctrl+6` / `Cmd+6` - Sixteenth-note (very short delay)
  - `Ctrl+7` / `Cmd+7` - Eighth-note
  - `Ctrl+8` / `Cmd+8` - Quarter-note
  - `Ctrl+9` / `Cmd+9` - 1-bar (longest delay)
- **Note**: Quantization Chooser is in Control Bar (top of screen, near transport controls)
- **Tip**: Disable quantization (`Ctrl+0`) while transcribing for instant navigation

**Locators:**
- **Issue**: No default keyboard shortcuts for locators in Ableton Live 12
- **Solution**: Use "Set Locator" button or Create menu → Add Locator
- **Alternative**: Install PerforModule template for `/`, `,`, `.` shortcuts
- **Alternative**: Create custom MIDI/key mapping (Ctrl+K / Cmd+K to enter Key Map Mode)

**Timeline navigation:**
- **Issue**: Clicking in scrub area starts playback (by default with Permanent Scrub Areas enabled)
- **Solution**: To set play position without starting playback, click directly in track area to set insert marker
- **Note**: Arrangement Position fields in Control Bar can be typed into for precise positioning

**Arrangement View not visible:**
- **Issue**: Can't see arrangement timeline or tracks
- **Solution**: Press Tab to toggle between Session/Arrangement View
- **Solution**: Drag window split between Session/Arrangement and Clip View to resize

**Audio interface latency:**
- **Issue**: Delayed monitoring when playing
- **Solution**: Lower buffer size (Preferences → Audio → 128 or 64 samples)
- **Solution**: Use Scarlett hardware direct monitoring (set track Monitor to "Off")

## Plugin & Mixing Concepts

ℹ️ **NOTE**: These are general audio production concepts, not Ableton-specific. The principles apply across all DAWs.

### Compressor (for finger/slap dynamics)

**Purpose**: Even out volume differences between finger style and slap technique

**Key parameters**:
- **Ratio**: How much compression is applied
  - 2:1 = gentle (slap still noticeably louder)
  - 4:1 = moderate (evens them out well)
  - 8:1 = aggressive (almost same volume)
- **Attack**: How fast compressor reacts
  - 5-10ms = catches slap peaks immediately
- **Release**: How long compression holds
  - 100-200ms = keeps sustained notes even
- **Threshold**: Set so slap triggers compression, finger technique mostly doesn't

### Limiter/Maximizer (master track)

**Purpose**: Prevent clipping (going over 0dB) and increase overall loudness

**How threshold works**:
- Lower threshold = more peaks get limited = louder overall output
- Higher threshold = only tallest peaks limited = more dynamic, less loud

**Two approaches**:
1. **Safety/minimal** (0-2 dB gain reduction): Just catching peaks, preserves dynamics
2. **Louder** (3-6 dB gain reduction): More consistent loudness for YouTube/streaming

**Common settings**:
- Ceiling: -0.3 dB (safe headroom)
- Threshold: Adjust until desired gain reduction achieved

## Resources

- **PerforModule template**: https://performodule.com - Opinionated keyboard mappings for Ableton Live 12
- **MeldaProduction Free Bundle**: https://meldaproduction.com/MFreeFXBundle - Free VST plugins (MEqualizer, MCompressor)
- **Ableton Manual**: Help → Help View (built-in documentation)

## Learning Approach

**Manual transcription benefits:**
- Ear training
- Understanding bass lines deeply
- Rhythm recognition (place notes in rhythm first, pitch second)
- Interval recognition (more important than perfect pitch)

**Practice structure:**
- Transcribe 4 bars completely before moving on
- Play back MIDI vs original - verify feel and groove
- If stuck on a note >2 minutes, mark it and move forward
- 90% accuracy is fine initially - process over perfection
