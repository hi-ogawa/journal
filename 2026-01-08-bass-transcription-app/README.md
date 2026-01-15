# toy-midi

> **Status**: Planning complete. Project moved to dedicated repo:
> https://github.com/hi-ogawa/toy-midi

A minimal web-based MIDI piano roll for manual bass line transcription.

## Why

Ableton Live Lite works for transcription but has friction: overkill UI, no transcription-focused shortcuts, context-switching between note entry and playback. This project aims to build a focused, intuitive piano roll optimized for mouse-based note entry.

## Scope

- Audio playback (WAV/MP3 backing track)
- Piano roll with bass range (E1-G3)
- Click-drag to create/edit notes
- MIDI export (.mid)

## Stack

React + TypeScript + Vite, Tone.js for audio, Zustand for state, SVG for rendering.
