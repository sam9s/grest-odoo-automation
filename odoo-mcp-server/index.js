import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import xmlrpc from "xmlrpc";

// ─── Configuration (read from env) ───────────────────────────────────────────
const ODOO_URL = process.env.ODOO_URL || "https://godoo.sam9scloud.in";
const ODOO_DB = process.env.ODOO_DB || "grest_production";
const ODOO_USERNAME = process.env.ODOO_USERNAME || "admin";
const ODOO_API_KEY = process.env.ODOO_API_KEY || "";

if (!ODOO_API_KEY) {
    process.stderr.write("ERROR: ODOO_API_KEY environment variable is required\n");
    process.exit(1);
}

// ─── XML-RPC helpers ─────────────────────────────────────────────────────────
function makeClient(path) {
    const url = new URL(ODOO_URL);
    const opts = {
        host: url.hostname,
        port: url.port || (url.protocol === "https:" ? 443 : 80),
        path,
    };
    return url.protocol === "https:"
        ? xmlrpc.createSecureClient(opts)
        : xmlrpc.createClient(opts);
}

function call(client, method, params) {
    return new Promise((resolve, reject) => {
        client.methodCall(method, params, (err, val) => {
            if (err) reject(err);
            else resolve(val);
        });
    });
}

// Authenticate once and cache the uid
let _uid = null;
async function getUid() {
    if (_uid) return _uid;
    const common = makeClient("/xmlrpc/2/common");
    _uid = await call(common, "authenticate", [ODOO_DB, ODOO_USERNAME, ODOO_API_KEY, {}]);
    if (!_uid) throw new Error("Odoo authentication failed — check your API key and database name.");
    return _uid;
}

async function execute(model, method, args, kwargs = {}) {
    const uid = await getUid();
    const obj = makeClient("/xmlrpc/2/object");
    return call(obj, "execute_kw", [ODOO_DB, uid, ODOO_API_KEY, model, method, args, kwargs]);
}

// ─── MCP Server ──────────────────────────────────────────────────────────────
const server = new Server(
    { name: "odoo-mcp-server", version: "1.0.0" },
    { capabilities: { tools: {} } }
);

// ── List tools ────────────────────────────────────────────────────────────────
server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
        {
            name: "odoo_ping",
            description: "Test connectivity to the Odoo instance. Returns server version info.",
            inputSchema: { type: "object", properties: {} },
        },
        {
            name: "odoo_search_read",
            description: "Search and read records from any Odoo model.",
            inputSchema: {
                type: "object",
                properties: {
                    model: { type: "string", description: "Odoo model name, e.g. 'res.partner'" },
                    domain: { type: "array", description: "Odoo domain filter, e.g. [['is_company','=',true]]", default: [] },
                    fields: { type: "array", description: "Fields to return, e.g. ['name','email']", default: [] },
                    limit: { type: "number", description: "Max records to return", default: 10 },
                    offset: { type: "number", description: "Offset for pagination", default: 0 },
                },
                required: ["model"],
            },
        },
        {
            name: "odoo_create",
            description: "Create a new record in an Odoo model.",
            inputSchema: {
                type: "object",
                properties: {
                    model: { type: "string", description: "Odoo model name" },
                    values: { type: "object", description: "Field values for the new record" },
                },
                required: ["model", "values"],
            },
        },
        {
            name: "odoo_write",
            description: "Update an existing record in an Odoo model.",
            inputSchema: {
                type: "object",
                properties: {
                    model: { type: "string", description: "Odoo model name" },
                    ids: { type: "array", description: "List of record IDs to update" },
                    values: { type: "object", description: "Field values to write" },
                },
                required: ["model", "ids", "values"],
            },
        },
        {
            name: "odoo_unlink",
            description: "Delete records from an Odoo model.",
            inputSchema: {
                type: "object",
                properties: {
                    model: { type: "string", description: "Odoo model name" },
                    ids: { type: "array", description: "List of record IDs to delete" },
                },
                required: ["model", "ids"],
            },
        },
        {
            name: "odoo_get_fields",
            description: "Get field definitions for an Odoo model.",
            inputSchema: {
                type: "object",
                properties: {
                    model: { type: "string", description: "Odoo model name" },
                    attributes: { type: "array", description: "Attributes to return e.g. ['string','type']", default: ["string", "type", "required"] },
                },
                required: ["model"],
            },
        },
    ],
}));

// ── Call tools ────────────────────────────────────────────────────────────────
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
        switch (name) {
            case "odoo_ping": {
                const common = makeClient("/xmlrpc/2/common");
                const version = await call(common, "version", []);
                return { content: [{ type: "text", text: JSON.stringify(version, null, 2) }] };
            }

            case "odoo_search_read": {
                const { model, domain = [], fields = [], limit = 10, offset = 0 } = args;
                const records = await execute(model, "search_read", [domain], { fields, limit, offset });
                return { content: [{ type: "text", text: JSON.stringify(records, null, 2) }] };
            }

            case "odoo_create": {
                const { model, values } = args;
                const id = await execute(model, "create", [values]);
                return { content: [{ type: "text", text: `Created record with ID: ${id}` }] };
            }

            case "odoo_write": {
                const { model, ids, values } = args;
                const result = await execute(model, "write", [ids, values]);
                return { content: [{ type: "text", text: `Write result: ${result}` }] };
            }

            case "odoo_unlink": {
                const { model, ids } = args;
                const result = await execute(model, "unlink", [ids]);
                return { content: [{ type: "text", text: `Unlink result: ${result}` }] };
            }

            case "odoo_get_fields": {
                const { model, attributes = ["string", "type", "required"] } = args;
                const fields = await execute(model, "fields_get", [], { attributes });
                return { content: [{ type: "text", text: JSON.stringify(fields, null, 2) }] };
            }

            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    } catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});

// ─── Start ───────────────────────────────────────────────────────────────────
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    process.stderr.write("Odoo MCP stdio server started\n");
}

main().catch((err) => {
    process.stderr.write(`Fatal: ${err.message}\n`);
    process.exit(1);
});
