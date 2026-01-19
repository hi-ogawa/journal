#!/usr/bin/env node
import { createServer } from "node:http";
import { homedir } from "node:os";
import { join } from "node:path";
import { existsSync } from "node:fs";
import { exec } from "node:child_process";
import { router } from "./server.ts";

const PORT = parseInt(process.env.PORT || "3000", 10);
const CLAUDE_DIR = join(homedir(), ".claude");

if (!existsSync(CLAUDE_DIR)) {
  console.error(`Claude directory not found: ${CLAUDE_DIR}`);
  process.exit(1);
}

const server = createServer(router);

server.listen(PORT, () => {
  const url = `http://localhost:${PORT}`;
  console.log(`Claude History Viewer running at ${url}`);

  // Try to open browser
  const cmd =
    process.platform === "darwin"
      ? "open"
      : process.platform === "win32"
        ? "start"
        : "xdg-open";
  exec(`${cmd} ${url}`);
});
