import type { IncomingMessage, ServerResponse } from "node:http";
import { URL } from "node:url";
import {
  listProjects,
  listSessions,
  findSession,
  readSession,
  searchHistory,
  decodePath,
} from "./reader.ts";
import type { Message, ContentBlock } from "./reader.ts";

type Handler = (
  req: IncomingMessage,
  res: ServerResponse,
  params: Record<string, string>
) => void;

const routes: Array<{ pattern: RegExp; handler: Handler }> = [];

function route(pattern: string, handler: Handler) {
  // Convert /project/:id to regex with named groups
  const regexStr = pattern.replace(/:(\w+)/g, "(?<$1>[^/]+)");
  routes.push({ pattern: new RegExp(`^${regexStr}$`), handler });
}

export function router(req: IncomingMessage, res: ServerResponse) {
  const url = new URL(req.url || "/", `http://${req.headers.host}`);
  const path = url.pathname;

  for (const { pattern, handler } of routes) {
    const match = path.match(pattern);
    if (match) {
      handler(req, res, match.groups || {});
      return;
    }
  }

  res.writeHead(404, { "Content-Type": "text/html" });
  res.end(layout("Not Found", "<h1>404 - Not Found</h1>"));
}

// --- Templates ---

function layout(title: string, content: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} - Claude History</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem;
      background: #fafafa;
      color: #333;
    }
    a { color: #0066cc; text-decoration: none; }
    a:hover { text-decoration: underline; }
    nav {
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid #ddd;
      display: flex;
      gap: 1rem;
      align-items: center;
    }
    nav .title { font-weight: 600; margin-right: auto; }
    .search-form { display: flex; gap: 0.5rem; }
    .search-form input {
      padding: 0.4rem 0.6rem;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    .search-form button {
      padding: 0.4rem 0.8rem;
      background: #0066cc;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .project-list, .session-list {
      list-style: none;
      padding: 0;
    }
    .project-list li, .session-list li {
      padding: 0.75rem;
      background: white;
      margin-bottom: 0.5rem;
      border-radius: 6px;
      border: 1px solid #e0e0e0;
    }
    .session-meta {
      color: #666;
      font-size: 0.85rem;
      margin-left: 0.5rem;
    }
    .preview {
      color: #888;
      font-size: 0.9rem;
      margin-top: 0.25rem;
    }
    .message {
      margin-bottom: 1.5rem;
      padding: 1rem;
      border-radius: 8px;
    }
    .message.user {
      background: #e3f2fd;
      border-left: 4px solid #2196f3;
    }
    .message.assistant {
      background: white;
      border-left: 4px solid #4caf50;
    }
    .message.summary {
      background: #fff3e0;
      border-left: 4px solid #ff9800;
    }
    .message-label {
      font-weight: 600;
      font-size: 0.8rem;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
      color: #666;
    }
    .message-content {
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    details {
      margin-top: 0.5rem;
      padding: 0.5rem;
      background: #f5f5f5;
      border-radius: 4px;
    }
    details summary {
      cursor: pointer;
      font-size: 0.85rem;
      color: #666;
    }
    details pre {
      margin: 0.5rem 0 0;
      font-size: 0.8rem;
      overflow-x: auto;
    }
    .breadcrumb {
      font-size: 0.9rem;
      color: #666;
      margin-bottom: 1rem;
    }
    .breadcrumb a { color: #666; }
    code {
      background: #f0f0f0;
      padding: 0.1rem 0.3rem;
      border-radius: 3px;
      font-size: 0.9em;
    }
    pre {
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 6px;
      overflow-x: auto;
    }
    pre code {
      background: none;
      padding: 0;
    }
    .controls {
      margin-bottom: 1rem;
      padding: 0.75rem;
      background: white;
      border-radius: 6px;
      border: 1px solid #e0e0e0;
      display: flex;
      gap: 1.5rem;
    }
    .controls label {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .thinking-block, .tool-block { display: none; }
    .show-thinking .thinking-block { display: block; }
    .show-tools .tool-block { display: block; }
  </style>
</head>
<body>
  <nav>
    <span class="title"><a href="/">Claude History</a></span>
    <form class="search-form" action="/search" method="get">
      <input type="text" name="q" placeholder="Search history...">
      <button type="submit">Search</button>
    </form>
  </nav>
  ${content}
</body>
</html>`;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// --- Routes ---

route("/", (_req, res) => {
  const projects = listProjects();
  const html = `
    <h1>Projects</h1>
    <ul class="project-list">
      ${projects
        .map(
          (p) => `
        <li>
          <a href="/project/${encodeURIComponent(p.encoded)}">${escapeHtml(p.decoded)}</a>
          <span class="session-meta">(${p.sessionCount} sessions)</span>
        </li>
      `
        )
        .join("")}
    </ul>
  `;
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(layout("Projects", html));
});

route("/project/:encoded", (_req, res, params) => {
  const encoded = decodeURIComponent(params.encoded);
  const sessions = listSessions(encoded);
  const decoded = decodePath(encoded);

  const html = `
    <div class="breadcrumb"><a href="/">Projects</a> / ${escapeHtml(decoded)}</div>
    <h1>Sessions</h1>
    <ul class="session-list">
      ${sessions
        .map(
          (s) => `
        <li>
          <a href="/session/${s.id}">${s.id.slice(0, 8)}</a>
          <span class="session-meta">${s.mtime.toISOString().slice(0, 16).replace("T", " ")} · ${s.sizeKB} KB</span>
          <div class="preview">${escapeHtml(s.preview)}${s.preview.length >= 80 ? "..." : ""}</div>
        </li>
      `
        )
        .join("")}
    </ul>
  `;
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(layout(decoded, html));
});

route("/session/:id", (_req, res, params) => {
  const filepath = findSession(params.id);
  if (!filepath) {
    res.writeHead(404, { "Content-Type": "text/html" });
    res.end(layout("Not Found", "<h1>Session not found</h1>"));
    return;
  }

  const messages = readSession(filepath);
  const html = `
    <div class="breadcrumb"><a href="/">Projects</a> / Session ${params.id.slice(0, 8)}</div>
    <h1>Conversation</h1>
    <div class="controls">
      <label><input type="checkbox" id="toggle-thinking"> Show thinking</label>
      <label><input type="checkbox" id="toggle-tools"> Show tool calls</label>
    </div>
    <div id="messages">
      ${messages.map((m) => renderMessage(m)).join("")}
    </div>
    <script>
      const container = document.getElementById('messages');
      document.getElementById('toggle-thinking').addEventListener('change', (e) => {
        container.classList.toggle('show-thinking', e.target.checked);
      });
      document.getElementById('toggle-tools').addEventListener('change', (e) => {
        container.classList.toggle('show-tools', e.target.checked);
      });
    </script>
  `;
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(layout(`Session ${params.id.slice(0, 8)}`, html));
});

route("/search", (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host}`);
  const query = url.searchParams.get("q") || "";

  if (!query) {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(layout("Search", "<h1>Search</h1><p>Enter a search term.</p>"));
    return;
  }

  const results = searchHistory(query);
  const html = `
    <h1>Search: "${escapeHtml(query)}"</h1>
    <p>${results.length} results</p>
    <ul class="session-list">
      ${results
        .map(
          (r) => `
        <li>
          <a href="/session/${r.sessionId}">${r.sessionId.slice(0, 8)}</a>
          <span class="session-meta">${new Date(r.timestamp).toISOString().slice(0, 16).replace("T", " ")}</span>
          <div class="preview">${escapeHtml(r.display.slice(0, 100))}${r.display.length > 100 ? "..." : ""}</div>
        </li>
      `
        )
        .join("")}
    </ul>
  `;
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(layout(`Search: ${query}`, html));
});

function renderMessage(msg: Message): string {
  if (msg.type === "summary") {
    const content =
      typeof msg.message?.content === "string" ? msg.message.content : "";
    return `
      <div class="message summary">
        <div class="message-label">Summary</div>
        <div class="message-content">${escapeHtml(content)}</div>
      </div>
    `;
  }

  if (msg.type === "user") {
    const content = msg.message?.content;
    if (typeof content === "string") {
      return `
        <div class="message user">
          <div class="message-label">User</div>
          <div class="message-content">${escapeHtml(content)}</div>
        </div>
      `;
    }
    // Tool results in user message
    if (Array.isArray(content)) {
      const toolResults = content
        .filter((b): b is ContentBlock => b.type === "tool_result")
        .map(
          (b) => `
          <details class="tool-block">
            <summary>Tool Result</summary>
            <pre><code>${escapeHtml(String(b.content || "").slice(0, 500))}</code></pre>
          </details>
        `
        )
        .join("");
      if (toolResults) {
        return `<div class="message user tool-block">${toolResults}</div>`;
      }
    }
    return "";
  }

  if (msg.type === "assistant") {
    const content = msg.message?.content;
    if (!Array.isArray(content)) return "";

    const blocks = content
      .map((block: ContentBlock) => {
        if (block.type === "text") {
          return `<div class="message-content">${escapeHtml(block.text || "")}</div>`;
        }
        if (block.type === "thinking") {
          return `
            <details class="thinking-block">
              <summary>Thinking</summary>
              <pre><code>${escapeHtml(block.thinking || "")}</code></pre>
            </details>
          `;
        }
        if (block.type === "tool_use") {
          return `
            <details class="tool-block">
              <summary>Tool: ${escapeHtml(block.name || "unknown")}</summary>
              <pre><code>${escapeHtml(JSON.stringify(block.input, null, 2).slice(0, 1000))}</code></pre>
            </details>
          `;
        }
        return "";
      })
      .join("");

    return `
      <div class="message assistant">
        <div class="message-label">Assistant</div>
        ${blocks}
      </div>
    `;
  }

  return "";
}
