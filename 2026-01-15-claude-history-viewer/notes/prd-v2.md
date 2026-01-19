# PRD v2: Terminal Integration (xterm.js + WebSocket)

## Overview

Add integrated terminal emulation directly in the browser UI, powered by **xterm.js** + **WebSocket** connection to local pseudo-terminal (pty.js).

**Goal**: Browse Claude Code history on the left, run CLI commands in terminal on the right—all without leaving browser.

## Current Architecture (v1)

```
Node.js HTTP Server
├── /api/projects, /api/sessions, /api/search → JSON responses
├── / → HTML layout
└── Static CSS/JS
```

## New Architecture (v2)

```
Node.js HTTP + WebSocket Server
├── HTTP Routes (existing)
│   ├── / → Split-view HTML (history + terminal)
│   └── /static/* → CSS, bundled JS
│
└── WebSocket Endpoint: /ws
    └── TerminalManager
        ├── Spawn shell process (pty.js)
        ├── Manage I/O streams
        └── Handle resize events
```

## Key Features

### 1. Split-View Layout

- **Left Panel (50%)**: History browser (projects → sessions → conversation)
- **Right Panel (50%)**: xterm.js terminal emulation
- Resizable divider (optional phase 2)

### 2. Terminal Capabilities

- Full terminal emulation (ANSI colors, cursor, escape codes)
- Keyboard input → server → shell → output → browser
- Resize handling (terminal reflows on window resize)
- Full shell features (pipes, redirects, aliases, etc.)
- Compatible with `claude-code` CLI

### 3. Ephemeral Sessions

- Each browser page/tab = fresh terminal
- Page refresh = new shell process
- No persistent state across sessions
- WebSocket close = terminal kill

### 4. History ↔ Terminal Integration

- **"Open in Terminal"** button on session view
  - Suggests: `cd /path/to/project`
  - Or: `claude-code --resume <session-id>`
- Click project name → auto-cd in terminal
- Display current history context in sidebar
- Keyboard shortcut: `Ctrl+`` to focus terminal

### 5. Safety & Simplicity

- Single Node process (no external managers)
- No authentication (personal tool, localhost)
- No persistent sessions (ephemeral = no cleanup)
- Secure by default (server controls spawning)

## Technical Stack

### Backend

- **Language**: Node.js + TypeScript
- **Server**: Native `http` module with WebSocket upgrade
- **WebSocket**: `ws` package (lightweight)
- **Terminal**: `pty.js` (pseudo-terminal spawning)
- **No external dependencies** for routing/framework

### Frontend

- **Terminal UI**: `xterm.js` + `xterm-addon-fit`
- **Bundle**: esbuild (simple bundling)
- **No framework** (vanilla JS, minimal dependencies)

## Data Flow

### Terminal I/O

```
User types in browser
    ↓
xterm.js captures input
    ↓
WebSocket sends { type: 'input', data: 'ls\n' }
    ↓
Server receives, writes to PTY stdin
    ↓
Shell process executes
    ↓
Output captured from PTY stdout/stderr
    ↓
WebSocket sends { type: 'output', data: '...' }
    ↓
Browser receives, renders in xterm.js
```

### Resize

```
Browser window resized
    ↓
xterm.js detects cols/rows change
    ↓
WebSocket sends { type: 'resize', cols: 120, rows: 30 }
    ↓
Server updates PTY dimensions
    ↓
Shell gets SIGWINCH signal
    ↓
Terminal reflows
```

## WebSocket Message Format

```typescript
// Client → Server
interface ClientMessage {
  type: "input" | "resize" | "kill";
  data?: string; // for 'input'
  cols?: number;
  rows?: number; // for 'resize'
}

// Server → Client
interface ServerMessage {
  type: "output" | "error" | "exit" | "init";
  data?: string; // for 'output'
  code?: number; // for 'exit'
  sessionId?: string; // for 'init'
}
```

## File Structure

### New Files

```
src/terminal.ts                 # TerminalManager, session handling
public/terminal-client.ts       # xterm.js + WebSocket client
public/terminal.css            # Dark terminal styling
```

### Modified Files

```
src/cli.ts                      # WebSocket upgrade handler
src/server.ts                   # Split-view HTML layout
package.json                    # Add deps, update build script
tsconfig.json                   # Add DOM lib for xterm.js
```

### Build Output

```
dist/
├── cli.js
├── server.js
├── terminal.js
└── terminal-client.js         # Bundled via esbuild
public/
└── terminal.js               # Client bundle
```

## Implementation Phases

### Phase 1: Core Terminal (Required)

- [ ] Add dependencies (xterm, ws, pty.js)
- [ ] Create TerminalManager class
- [ ] Implement WebSocket server
- [ ] Create xterm.js client
- [ ] Wire up HTML layout
- [ ] Test basic I/O

### Phase 2: Integration (Nice-to-have)

- [ ] "Open in Terminal" buttons
- [ ] Auto-cd from history clicks
- [ ] Keyboard shortcuts (Ctrl+`)
- [ ] Status display in sidebar

### Phase 3: Polish (Deferred)

- [ ] Resizable divider
- [ ] Theme customization
- [ ] Terminal scrollback buffer
- [ ] Session history/recording

## Success Criteria

- [ ] Terminal renders in browser alongside history
- [ ] Can type commands and see output
- [ ] `claude-code` CLI works in terminal
- [ ] Resize handling works smoothly
- [ ] Single Node.js process (no background workers)
- [ ] Ephemeral terminals (fresh on page load)
- [ ] Zero frictions—just works

## Known Limitations

| Limitation           | Reason                        | Workaround                                           |
| -------------------- | ----------------------------- | ---------------------------------------------------- |
| Ephemeral sessions   | Simpler state management      | Open multiple browser tabs for independent terminals |
| Single shell per tab | Matches browser context model | Can't have multiple shells in one tab                |
| No SSH/remote        | pty.js is local-only          | Use SSH client or deploy app to remote               |
| No persistence       | Intentional—personal tool     | Terminal history lost on refresh (OK)                |

## Dependencies to Add

```
xterm@^5.x                      # Terminal emulator
xterm-addon-fit@^0.x            # Auto-fit addon
ws@^8.x                         # WebSocket server
pty.js@^0.x                     # Pseudo-terminal
esbuild@^0.x                    # Bundler for client code
```

Total new size: ~5MB node_modules (acceptable)

## Environment Variables

```
PORT=3000                       # Server port (existing)
TERMINAL_SHELL=/bin/bash        # Shell to spawn (optional)
TERMINAL_CWD=$HOME              # Initial directory (optional)
```

## Testing Strategy

### Manual Testing

1. Start server: `pnpm dev`
2. Open browser: `http://localhost:3000`
3. Terminal appears on right side
4. Type `ls` → see output
5. Type `pwd` → confirm working directory
6. Click history item → terminal `cd`s to project
7. Run `claude-code show <session-id>` → works
8. Refresh page → new terminal

### No Unit Tests for Phase 1

- Focus on integration/E2E
- Terminal logic is straightforward (spawn, I/O, resize)

## Security Considerations

- **Server controls spawning**: User can't inject arbitrary commands via URL
- **Shell sandboxing**: Standard shell security (user's permissions, filesystem)
- **No auth needed**: Personal tool on localhost
- **No data exfiltration**: Terminal output never leaves machine (no logging)

## Performance Notes

- **Memory**: One PTY per WebSocket connection (~10-20MB each)
- **CPU**: Minimal (just pipe I/O)
- **Latency**: WebSocket < 1ms (localhost), imperceptible
- **Scaling**: Not intended for multi-user (personal tool)

## Future Enhancements (Not v2)

- [ ] Session recording/playback
- [ ] Resizable split pane
- [ ] Multiple terminals in tabs
- [ ] Terminal themes
- [ ] Shell history across sessions (store in localStorage)
- [ ] Ability to "attach" to running `claude-code` session
- [ ] Export terminal session as markdown

## Acceptance Criteria

### Functional

- Terminal renders without errors
- User can type and see output
- Claude Code CLI runs successfully
- Resize events handled gracefully
- WebSocket reconnect on disconnect (optional)

### Non-Functional

- Single Node.js process
- < 5s startup time
- Minimal memory per terminal
- No external process managers

### Quality

- No console errors
- Handles edge cases (long lines, special chars, colors)
- Works with existing history browser (no regressions)
