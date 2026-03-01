# Connecting Antigravity AI to Odoo 18 via Custom MCP Server

> **A complete guide** — what we were trying to do, every issue we hit, how we fixed it, and the final working setup. Written so anyone (or Antigravity itself in a future session) can reproduce this from scratch.

---

## 🎯 What We Were Trying to Do

[Antigravity](https://antigravity.dev) is a VS Code-based AI coding assistant that supports the **Model Context Protocol (MCP)** — a standard that lets AI assistants talk directly to external services (databases, APIs, ERPs).

**Goal:** Connect Antigravity to a live **Odoo 18 Community** instance so the AI can:
- Read and create Odoo records directly (customers, sales orders, products, etc.)
- Build and configure Odoo workflows without manual UI interaction
- Act as an intelligent automation layer on top of live business data

Our Odoo 18 instance was running at `https://godoo.sam9scloud.in` on a VPS via Docker Compose, with PostgreSQL 16 as the database.

---

## 🧱 How MCP Works (Quick Background)

MCP servers are small programs that Antigravity spawns as a **subprocess** and communicates with via **stdio** (standard input/output). The client (Antigravity) sends JSON-RPC messages; the server responds with tool results.

The MCP config file at:
```
C:\Users\<you>\.gemini\antigravity\mcp_config.json
```

Tells Antigravity which servers to launch at startup:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": { "MY_KEY": "value" }
    }
  }
}
```

---

## 🚧 Issues We Faced (and How We Fixed Each One)

### Issue 1 — No Official Odoo MCP Package

Odoo does not ship an official MCP server. We tried the community package `@mweinheimer/odoo-mcp-server` via `npx`.

**What happened:** Antigravity **crashed entirely** with:
```
[Error] Stopping server failed
Message: Cannot call write after a stream was destroyed
Code: -32099
```

**Root cause:** This package starts an **HTTP server on port 3001**, not a stdio server. Antigravity expects stdio — when the child process doesn't behave like a stdio MCP server, the IPC stream is destroyed, crashing Antigravity.

**Lesson:** Any npx-launched Odoo MCP package that prints `Starting Odoo MCP HTTP Server on port 3001...` is **incompatible** with Antigravity (and most stdio-based MCP clients).

---

### Issue 2 — Trying SSE/URL Mode

We attempted to run the HTTP server as a background process and configure Antigravity to connect via SSE URL:
```json
"odoo-mcp-server": {
  "url": "http://localhost:3001/sse"
}
```

**What happened:** Antigravity crashed again with the same error. SSE/URL mode does not work reliably in this version of Antigravity.

**Fix:** Removed the entry. Never use `url` mode with Antigravity for a child-process server.

---

### Issue 3 — Building a Custom stdio Server (SDK Version Mismatch)

We built a custom Node.js MCP server using `@modelcontextprotocol/sdk`. The server started cleanly, but tool calls returned:
```
Error: Not Found
```

**Root cause #1:** The SDK was at version `1.26.0` — newer than what Antigravity supports.  
**Fix:** Downgraded to `@modelcontextprotocol/sdk@1.0.4`.

**Root cause #2 (the real one):** The Odoo XML-RPC endpoint paths were wrong:
- ❌ We used: `/web/xmlrpc/2/common` and `/web/xmlrpc/2/object`
- ✅ Correct for Odoo 18: `/xmlrpc/2/common` and `/xmlrpc/2/object`

The `/web` prefix returns an HTML page (404 equivalent), not an XML-RPC response.

**Verification command** (run from the VPS):
```bash
curl -s -o /dev/null -w '%{http_code}' -X POST https://your-odoo-domain/xmlrpc/2/common \
  -H 'Content-Type: text/xml' \
  -d '<?xml version="1.0"?><methodCall><methodName>version</methodName><params></params></methodCall>'
# Should return 200
```

---

## ✅ The Working Solution

### Architecture

```
Antigravity (VS Code)
    │
    │  spawns via stdio
    ▼
odoo-mcp-server/index.js   (Node.js, @modelcontextprotocol/sdk@1.0.4)
    │
    │  HTTPS XML-RPC calls
    ▼
Odoo 18  (https://your-odoo-domain/xmlrpc/2/...)
```

### Step-by-Step Setup

#### 1. Create the MCP server project

```bash
mkdir odoo-mcp-server
cd odoo-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk@1.0.4 xmlrpc
```

Set `"type": "module"` in `package.json`.

#### 2. Create `index.js`

```js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import xmlrpc from "xmlrpc";

const ODOO_URL     = process.env.ODOO_URL;
const ODOO_DB      = process.env.ODOO_DB;
const ODOO_API_KEY = process.env.ODOO_API_KEY;

function makeClient(path) {
  const url = new URL(ODOO_URL);
  const opts = { host: url.hostname, port: url.port || (url.protocol === "https:" ? 443 : 80), path };
  return url.protocol === "https:" ? xmlrpc.createSecureClient(opts) : xmlrpc.createClient(opts);
}

function call(client, method, params) {
  return new Promise((resolve, reject) =>
    client.methodCall(method, params, (err, val) => err ? reject(err) : resolve(val))
  );
}

let _uid = null;
async function getUid() {
  if (_uid) return _uid;
  const common = makeClient("/xmlrpc/2/common");          // ✅ No /web prefix!
  _uid = await call(common, "authenticate", [ODOO_DB, "admin", ODOO_API_KEY, {}]);
  if (!_uid) throw new Error("Odoo auth failed — check API key and DB name");
  return _uid;
}

async function execute(model, method, args, kwargs = {}) {
  const uid = await getUid();
  const obj = makeClient("/xmlrpc/2/object");             // ✅ No /web prefix!
  return call(obj, "execute_kw", [ODOO_DB, uid, ODOO_API_KEY, model, method, args, kwargs]);
}

const server = new Server(
  { name: "odoo-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: "odoo_ping",        description: "Test connectivity. Returns Odoo version.", inputSchema: { type: "object", properties: {} } },
    { name: "odoo_search_read", description: "Query any Odoo model.",
      inputSchema: { type: "object", required: ["model"], properties: {
        model:  { type: "string" }, domain: { type: "array", default: [] },
        fields: { type: "array", default: [] }, limit: { type: "number", default: 10 }, offset: { type: "number", default: 0 }
      }}},
    { name: "odoo_create",  description: "Create a record.", inputSchema: { type: "object", required: ["model","values"],  properties: { model: { type: "string" }, values: { type: "object" } }}},
    { name: "odoo_write",   description: "Update records.",  inputSchema: { type: "object", required: ["model","ids","values"], properties: { model: { type: "string" }, ids: { type: "array" }, values: { type: "object" } }}},
    { name: "odoo_unlink",  description: "Delete records.",  inputSchema: { type: "object", required: ["model","ids"],  properties: { model: { type: "string" }, ids: { type: "array" } }}},
    { name: "odoo_get_fields", description: "Get model field definitions.", inputSchema: { type: "object", required: ["model"], properties: { model: { type: "string" }, attributes: { type: "array", default: ["string","type","required"] } }}},
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;
  try {
    switch (name) {
      case "odoo_ping": {
        const v = await call(makeClient("/xmlrpc/2/common"), "version", []);
        return { content: [{ type: "text", text: JSON.stringify(v, null, 2) }] };
      }
      case "odoo_search_read": {
        const { model, domain=[], fields=[], limit=10, offset=0 } = args;
        const r = await execute(model, "search_read", [domain], { fields, limit, offset });
        return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
      }
      case "odoo_create": {
        const id = await execute(args.model, "create", [args.values]);
        return { content: [{ type: "text", text: `Created ID: ${id}` }] };
      }
      case "odoo_write": {
        const ok = await execute(args.model, "write", [args.ids, args.values]);
        return { content: [{ type: "text", text: `Write: ${ok}` }] };
      }
      case "odoo_unlink": {
        const ok = await execute(args.model, "unlink", [args.ids]);
        return { content: [{ type: "text", text: `Unlink: ${ok}` }] };
      }
      case "odoo_get_fields": {
        const f = await execute(args.model, "fields_get", [], { attributes: args.attributes || ["string","type","required"] });
        return { content: [{ type: "text", text: JSON.stringify(f, null, 2) }] };
      }
      default: throw new Error(`Unknown tool: ${name}`);
    }
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
process.stderr.write("Odoo MCP stdio server started\n");
```

#### 3. Create a `.env` file for credentials

```env
ODOO_URL=https://your-odoo-domain
ODOO_DB=your_database_name
ODOO_USERNAME=your_admin_login_email
ODOO_API_KEY=your_odoo_api_key_here
```

> Generate an API key in Odoo at: **Settings → My Profile → Account Security → API Keys → New**

> ⚠️ **`ODOO_USERNAME` is the login email** shown in Odoo under Settings → Users — not necessarily the string `admin`. If unsure, see the tip at the bottom of this guide.

#### 4. Register the server in `mcp_config.json`

File location: `C:\Users\<you>\.gemini\antigravity\mcp_config.json`

```json
{
  "mcpServers": {
    "odoo-mcp-server": {
      "command": "node",
      "args": ["C:\\full\\path\\to\\odoo-mcp-server\\index.js"],
      "env": {
        "ODOO_URL": "https://your-odoo-domain",
        "ODOO_DB": "your_database_name",
        "ODOO_USERNAME": "your_admin_login_email",
        "ODOO_API_KEY": "your_odoo_api_key_here"
      }
    }
  }
}
```

#### 5. Reload Antigravity

`Ctrl+Shift+P` → **Developer: Reload Window**

#### 6. Test the connection

Ask Antigravity: *"Can you ping my Odoo instance?"*

Expected response:
```json
{
  "server_version": "18.0-...",
  "server_serie": "18.0",
  "protocol_version": 1
}
```

---

## 🔑 Key Gotchas (Summary)

| Gotcha | Detail |
|---|---|
| **Don't use HTTP/SSE packages** | `@mweinheimer/odoo-mcp-server` and similar crash Antigravity — they're HTTP servers, not stdio |
| **Don't use `url` mode** | `"url": "http://localhost:3001/sse"` also causes crashes |
| **XML-RPC path** | Use `/xmlrpc/2/common` — NOT `/web/xmlrpc/2/common` |
| **SDK version** | Use `@modelcontextprotocol/sdk@1.0.4` — newer versions may have protocol mismatches |
| **API key auth** | Odoo API key replaces the password in XML-RPC `authenticate` calls |
| **`ODOO_USERNAME` is an email** | The admin login in Odoo is almost always an email address (e.g. `admin@company.com`), not the string `admin` |
| **package.json type** | Must be `"type": "module"` for ESM imports |

---

## 🛠️ How to Find Your Odoo Database Name

If you've forgotten it, SSH into your VPS and run:

```bash
docker exec <postgres-container-name> psql -U odoo -d postgres -t -A \
  -c 'SELECT datname FROM pg_database WHERE datistemplate = false;'
```

---

*Built during the GREST Odoo Automation project — February 2026*  
*Team: Sammy (PM) • Astra/Claude Desktop (Architect) • Antigravity (Developer)*
