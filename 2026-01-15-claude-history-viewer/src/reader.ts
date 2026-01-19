import { homedir } from "node:os";
import { join } from "node:path";
import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";

export const CLAUDE_DIR = join(homedir(), ".claude");
export const PROJECTS_DIR = join(CLAUDE_DIR, "projects");

export interface Project {
  encoded: string;
  decoded: string;
  sessionCount: number;
}

export interface Session {
  id: string;
  projectEncoded: string;
  mtime: Date;
  sizeKB: number;
  preview: string;
}

export interface Message {
  type: "user" | "assistant" | "summary";
  message?: {
    content: string | ContentBlock[];
  };
  timestamp?: number;
  uuid?: string;
}

export interface ContentBlock {
  type: "text" | "thinking" | "tool_use" | "tool_result";
  text?: string;
  thinking?: string;
  name?: string;
  input?: unknown;
  content?: string;
}

export interface HistoryEntry {
  timestamp: number;
  sessionId: string;
  display: string;
  projectPath?: string;
}

/**
 * Decode an encoded project path back to the original filesystem path.
 *
 * Claude encodes paths like /home/user/my-project as -home-user-my-project.
 * We can't naively replace all hyphens with slashes because hyphens may be
 * part of actual directory names. Instead, we try all possible interpretations
 * and pick the one that matches the most path components on the filesystem.
 */
export function decodePath(encoded: string): string {
  // Remove leading hyphen if present
  const normalized = encoded.startsWith("-") ? encoded.slice(1) : encoded;
  const parts = normalized.split("-");

  if (parts.length === 0) return "/";

  type Result = { validated: number; total: number; parts: string[] };

  function findBestPath(idx: number, currentPath: string): Result {
    if (idx >= parts.length) {
      return { validated: 0, total: 0, parts: [] };
    }

    let best: Result | null = null;

    // Try joining parts[idx:end+1] as a single path component
    let component = "";
    for (let end = idx; end < parts.length; end++) {
      component = component ? component + "-" + parts[end] : parts[end];

      const testPath = join(currentPath, component);
      const isValid = existsSync(testPath) && statSync(testPath).isDirectory();

      // Recurse to find remaining path
      const sub = findBestPath(end + 1, isValid ? testPath : currentPath);

      const validated = (isValid ? 1 : 0) + sub.validated;
      const total = 1 + sub.total;
      const result: Result = {
        validated,
        total,
        parts: [component, ...sub.parts],
      };

      // Prefer: more validated, then fewer total parts
      if (
        !best ||
        validated > best.validated ||
        (validated === best.validated && total < best.total)
      ) {
        best = result;
      }
    }

    return best || { validated: 0, total: 0, parts: [] };
  }

  const { parts: pathParts } = findBestPath(0, "/");
  return "/" + pathParts.join("/");
}

export function listProjects(): Project[] {
  if (!existsSync(PROJECTS_DIR)) return [];

  return readdirSync(PROJECTS_DIR)
    .filter((name) => statSync(join(PROJECTS_DIR, name)).isDirectory())
    .map((encoded) => {
      const dir = join(PROJECTS_DIR, encoded);
      const sessions = readdirSync(dir).filter((f) => f.endsWith(".jsonl"));
      return {
        encoded,
        decoded: decodePath(encoded),
        sessionCount: sessions.length,
      };
    })
    .sort((a, b) => a.decoded.localeCompare(b.decoded));
}

export function listSessions(projectEncoded: string): Session[] {
  const projectDir = join(PROJECTS_DIR, projectEncoded);
  if (!existsSync(projectDir)) return [];

  return readdirSync(projectDir)
    .filter((f) => f.endsWith(".jsonl"))
    .map((filename) => {
      const filepath = join(projectDir, filename);
      const stat = statSync(filepath);
      const id = filename.replace(".jsonl", "");

      // Get first user message as preview
      let preview = "";
      try {
        const content = readFileSync(filepath, "utf-8");
        for (const line of content.split("\n")) {
          if (!line.trim()) continue;
          const msg: Message = JSON.parse(line);
          if (msg.type === "user" && typeof msg.message?.content === "string") {
            preview = msg.message.content.slice(0, 80).replace(/\n/g, " ");
            break;
          }
        }
      } catch {
        // ignore parse errors
      }

      return {
        id,
        projectEncoded,
        mtime: stat.mtime,
        sizeKB: Math.round(stat.size / 1024),
        preview,
      };
    })
    .sort((a, b) => b.mtime.getTime() - a.mtime.getTime());
}

export function findSession(sessionId: string): string | null {
  if (!existsSync(PROJECTS_DIR)) return null;

  for (const projectDir of readdirSync(PROJECTS_DIR)) {
    const dir = join(PROJECTS_DIR, projectDir);
    if (!statSync(dir).isDirectory()) continue;

    // Exact match
    const exact = join(dir, `${sessionId}.jsonl`);
    if (existsSync(exact)) return exact;

    // Partial match
    for (const file of readdirSync(dir)) {
      if (file.startsWith(sessionId) && file.endsWith(".jsonl")) {
        return join(dir, file);
      }
    }
  }
  return null;
}

export function readSession(filepath: string): Message[] {
  const content = readFileSync(filepath, "utf-8");
  const messages: Message[] = [];

  for (const line of content.split("\n")) {
    if (!line.trim()) continue;
    try {
      messages.push(JSON.parse(line));
    } catch {
      // skip malformed lines
    }
  }

  return messages;
}

export function searchHistory(query: string, limit = 50): HistoryEntry[] {
  const historyFile = join(CLAUDE_DIR, "history.jsonl");
  if (!existsSync(historyFile)) return [];

  const content = readFileSync(historyFile, "utf-8");
  const matches: HistoryEntry[] = [];
  const lowerQuery = query.toLowerCase();

  for (const line of content.split("\n")) {
    if (!line.trim()) continue;
    try {
      const entry: HistoryEntry = JSON.parse(line);
      if (entry.display?.toLowerCase().includes(lowerQuery)) {
        matches.push(entry);
      }
    } catch {
      // skip
    }
  }

  // Return most recent matches
  return matches.slice(-limit).reverse();
}
