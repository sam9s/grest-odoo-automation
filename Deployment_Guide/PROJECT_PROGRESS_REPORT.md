# GREST ERP — Project Progress Report
**Author:** Antigravity (Developer)  
**Date:** 2 March 2026  
**For:** Sammy (PM), Nikhil (Technical Lead), Astra (Solution Architect)

---

## 1. Project Overview

GREST is a mobile device refurbishment business currently operating on 50+ Google Sheets and WhatsApp coordination. This project replaces that with a **centralized Odoo 18 ERP**, built and deployed in phases.

**Tech Stack:**
- Odoo 18 (Community) on Docker, VPS at `72.61.240.154`
- Domain: `https://godoo.sam9scloud.in`
- Dev DB: `grest_staging` | Prod DB: `grest_production`
- Custom modules in Python/XML at `D:\RAVENs\Grest-odoo-automation\custom_addons\`
- GitHub: `https://github.com/sam9s/grest-odoo-automation`
- AI tooling: Antigravity (dev) + Astra (architect) both have live MCP access to `grest_staging`

---

## 2. Full Phased Roadmap

| Phase | Scope | Timeline | Status |
|---|---|---|---|
| **Phase 1** | Procurement + Accounts Approval | 1 week | ✅ **Complete** |
| **Phase 2** | Warehouse Operations (TRC, grading, stock) | ~4 weeks | ⬜ Not started |
| **Phase 3** | P&L Calculation, TRC module | ~4 weeks | ⬜ Not started |
| **Phase 4** | Sales, full integration, reporting | ~4 weeks | ⬜ Not started |

---

## 3. Phase 1 — What Was Built (COMPLETE ✅)

### Module 1: `grest_procurement`
> Replaces the procurement Google Sheet. Captures every device purchase end-to-end.

**File:** `custom_addons/grest_procurement/models/procurement.py` (467 lines)

| Section | Fields | Notes |
|---|---|---|
| Identity | `name`, `serial_number`, `gsn`, `grest_unique_code` | All auto-generated |
| Device | `category`, `imei`, `model_id`, `brand`, `ram`, `rom` | brand/ram/rom auto from product |
| Source | `source_name`, `store_name` | 6 sources: Cashify B2B/Trading, Unicorn, Sangeeta, Trade-In, Other |
| Timing | `purchase_date`, `purchase_month` | Month auto-derived |
| Pricing | `price_offered`, `ave_price`, `logistic_charge`, `extra_amount`, `credit_used`, `commission_amount`, `purchase_price_no_commission`, `total_price` | Commission/total auto-calculated |
| Payment | `payment_scenario`, `payment_status`, `payment_date`, `payment_month`, `payment_utr` | 3 scenarios: Paid, Partial, Credit |
| Receiving | `grest_received`, `receiving_date`, `receiving_month` | |
| Handover | `handover_date`, `handover_month` | |
| Grading | `grade`, `els_grade` | Filled by warehouse (Phase 2) |
| Status | `status`, `approval_status` | Pending → Received → Handed Over |
| Financials | `due_amount`, `amount_balance` | |
| Commission | `commission_payment_status`, `commission_utr`, `commission_paid_date` | |
| Invoice | `invoice_file`, `invoice_filename` | Binary attachment |
| Phase 3 (stub) | `price_with_spare`, `final_price`, `sales_price`, `p_and_l` | Reserved for P&L phase |

**Key Auto-Logic:**
- **GSN Generation**: `GRG + Source(3) + IMEI(last4) + Tech(4) + Serial(2) + Month(1)` → e.g. `GRGUNI6245MITC01M`
  > ⚠️ **Temporary formula** — Nikhil to confirm final GSN spec in upcoming meeting
- **Commission Rates**: Unicorn/Sangeeta/Other = 12%, Trade-In = 10%, Cashify = 0%
- **Auto-approval record**: On every save, a linked `grest.accounts.approval` record is created automatically
- **IMEI uniqueness**: Enforced at DB level via `@api.constrains`

---

### Module 2: `grest_accounts_approval`
> Accounts team sees a Kanban dashboard of all pending procurements. They approve or reject.

**File:** `custom_addons/grest_accounts_approval/models/accounts_approval.py`

| Field | Description |
|---|---|
| `procurement_id` | Link back to the procurement record |
| `gsn`, `imei`, `model_id`, `source_name`, `price_offered`, `total_price` | Mirrored (read-only) from procurement |
| `payment_scenario`, `payment_status`, `payment_utr` | Payment tracking |
| `credit_days`, `partial_amount` | Conditional fields (shown based on scenario) |
| `state` | `pending` → `approved` / `rejected` |
| `approved_by_id`, `approval_date`, `rejection_reason` | Audit trail |
| `notes` | Free-text notes |
| `invoice_file` | Invoice view |

**Workflow:**  
`Procurement saves record` → `Approval auto-created (state: pending)` → `Accounts opens Kanban` → `Approve or Reject` → `Audit trail recorded`

---

### Infrastructure Deployed

| Component | Detail |
|---|---|
| VPS | `72.61.240.154` (root SSH access) |
| Docker | `odoo-setup-web-1` (Odoo), `odoo-setup-db-1` (PostgreSQL) |
| Addons path (container) | `/mnt/extra-addons` → mounted from `/root/odoo-setup/addons/` |
| **odoo.conf location** | `/root/odoo-setup/config/odoo.conf` ← Docker mounts `./config:/etc/odoo` |
| `db_name` in conf | `grest_staging` |
| Module install command | `odoo --addons-path='...' -d grest_staging -u grest_procurement,grest_accounts_approval` |
| Backups | `/root/backups/grest_staging_2026-03-01.sql` (16 MB dump) |

---

### MCP Server (AI Tooling)

Both Antigravity and Astra have direct Odoo access:

```json
{
  "ODOO_URL": "https://godoo.sam9scloud.in",
  "ODOO_DB": "grest_staging",
  "ODOO_USERNAME": "samret.singh@grest.in",
  "ODOO_API_KEY": "956ee96c2db9252cf2c608aef0fb41c914333357"
}
```

**Bug fixed in MCP server (`index.js`):** Removed UID caching — now authenticates fresh per call. This prevents stale sessions when switching databases.

---

## 4. Bugs Fixed During Phase 1 Deployment

| # | Bug | Root Cause | Fix |
|---|---|---|---|
| 1 | Circular dependency | `grest_procurement` had `One2many` → `grest.accounts.approval` at class-definition time | Removed `approval_id` field; approval linked via `procurement_id` on the approval model |
| 2 | `tree` view invalid | Odoo 17/18 renamed `tree` → `list` | Replaced all `<tree>` with `<list>` in all 4 view XML files |
| 3 | Invalid `category_id` refs | `base.module_category_operations_inventory` doesn't exist without `stock` module | Removed `category_id` from both security XMLs |
| 4 | `odoo.conf` ignored | Docker mounts `./config:/etc/odoo` but conf was at `./odoo.conf` | Copied to `./config/odoo.conf` |
| 5 | Custom models not in XML-RPC | `db_name` + `addons_path` missing from `odoo.conf` | Added both; Odoo now loads correct registry on boot |
| 6 | MCP stale UID | `index.js` cached auth UID from first login; stale after DB switch | Removed `_uid` cache; fresh auth per call |
| 7 | Admin can't access models | Security groups restrict access; admin not in any group | Added admin to `Procurement Manager` + `Accounts Manager` via MCP |

---

## 5. Verified Working ✅

Tested via MCP on 1 March 2026:

```
Created: grest.procurement ID=2
  GSN:             GRGUNI6245MITC01M  ✅ auto-generated
  Commission:      ₹600               ✅ 12% of ₹5,000 (Unicorn rate)
  Total Price:     ₹5,600             ✅ correct
  Approval Status: pending            ✅ correct default
  Purchase Month:  Mar_2026           ✅ auto-derived

Auto-created: grest.accounts.approval ID=1
  Name:  APPR-PROC-1                  ✅ linked
  GSN:   GRGUNI6245MITC01M            ✅ mirrored
  Total: ₹5,600                       ✅ mirrored
  State: pending                      ✅
```

Visual verification by Sammy confirmed:
- **Procurement → Device Purchases** visible in UI ✅
- **Accounts → Dashboard** (Kanban with Approve/Reject buttons) visible ✅

---

## 6. Known Issues / Pending Items (Before Phase 2)

| # | Item | Priority | Owner |
|---|---|---|---|
| 1 | **GSN formula needs Nikhil's confirmation** | 🔴 High | Nikhil / upcoming meeting |
| 2 | **Product catalog needs importing** (`sample_products.csv` ready) | 🟡 Medium | Sammy / Antigravity |
| 3 | **Real-time data entry test** | 🟡 Medium | Sammy |
| 4 | **User accounts for procurement team** (real users, not admin) | 🟡 Medium | Sammy |
| 5 | **Kanban card template deprecation warning** (`kanban-box` → `card`) | 🟢 Low | Antigravity (cosmetic) |
| 6 | **DeprecationWarning on `create()` method** (not batch) | 🟢 Low | Antigravity (cosmetic) |
| 7 | **Production deployment** (when staging is stable) | 🟢 Low | After Nikhil meeting |

---

## 7. Phase 2 — What's Next (Warehouse)

Based on Astra's design and Nikhil's domain, Phase 2 will likely include:

- **`grest_warehouse` module** — receives devices from Procurement, assigns technicians, tracks repair status
- **TRC (Technical Report Card)** — condition assessment, grading
- **Grade-based pricing** — feeds back into P&L
- **Stock integration** — Odoo's built-in `stock` module may be used, or custom

> ⚠️ **Requires Nikhil's input at the March 2 afternoon meeting** before any Phase 2 development begins.

---

## 8. Repo Structure (as of 2 March 2026)

```
Grest-odoo-automation/
├── custom_addons/
│   ├── grest_procurement/          ← Phase 1, LIVE
│   │   ├── models/
│   │   │   ├── procurement.py      ← 467 lines, 38 fields
│   │   │   └── product_template.py ← brand/ram/rom fields on product
│   │   ├── views/
│   │   │   ├── procurement_views.xml
│   │   │   └── procurement_menu.xml
│   │   └── security/
│   │       ├── procurement_security.xml
│   │       └── ir.model.access.csv
│   └── grest_accounts_approval/    ← Phase 1, LIVE
│       ├── models/accounts_approval.py
│       ├── views/
│       │   ├── accounts_approval_views.xml
│       │   └── accounts_approval_menu.xml
│       └── security/
│           ├── accounts_security.xml
│           └── ir.model.access.csv
├── odoo-mcp-server/
│   └── index.js                    ← MCP server (fixed: no UID caching)
├── odoo-setup/
│   └── config/
│       └── odoo.conf               ← db_name + addons_path set correctly
├── Deployment_Guide/
│   ├── GREST_ERP_COMPLETE_DEPLOYMENT_GUIDE.md  ← Astra's full spec
│   ├── ANTI_GRAVITY_ANSWERS.md
│   └── ANTI_GRAVITY_EXECUTION_PROMPT.md
├── docs/                           ← Meeting notes, transcripts, requirements
├── README.md
└── .gitignore                      ← .env, node_modules, temp, odoo-setup excluded
```

---

## 9. Ground Rules for Future Development

1. **MCP first** — always use `odoo_create`, `odoo_write`, `odoo_search_read` before falling back to SSH/psql
2. **Test on `grest_staging`** — never deploy untested code directly to `grest_production`
3. **Git commit every change** — `git add -A && git commit -m "..."` → `git push origin main`
4. **Deploy to VPS** — SCP files → restart container (or run `-u` flag with server stopped)
5. **`odoo.conf` is at `/root/odoo-setup/config/odoo.conf`** — NOT at `./odoo.conf`
6. **Security groups** — New modules need admin added to their groups before MCP can access them
