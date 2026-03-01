# GREST ODOO PROJECT - FINAL DIRECTORY STRUCTURE
## Merged: Original Structure + Astra's Enhancements

---

grest-odoo-automation/
│
├── README.md
├── .gitignore
├── requirements.txt                        # Python dependencies
├── package.json                            # Node dependencies (if needed)
│
├── odoo-setup/                             # Odoo installation (DONE ✅)
│   ├── docker-compose.yml
│   ├── odoo.conf
│   ├── .env
│   └── setup-instructions.md
│
├── custom-modules/                         # ⭐ NEW - Odoo custom Python modules
│   │                                       # Built by Claude Code, deployed by Anti-Gravity
│   ├── grest_warehouse/                    # Core device tracking module
│   │   ├── __init__.py
│   │   ├── __manifest__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── grest_device.py             # IMEI, Grade, Barcode fields
│   │   │   └── stock_picking_ext.py        # Extended warehouse workflow
│   │   ├── views/
│   │   │   └── grest_device_views.xml      # UI views
│   │   └── security/
│   │       └── ir.model.access.csv         # RBAC rules
│   │
│   ├── grest_trc/                          # TRC/QC workflow module
│   │   ├── __init__.py
│   │   ├── __manifest__.py
│   │   ├── models/
│   │   │   ├── trc_order.py                # TRC processing
│   │   │   ├── qc_grade.py                 # Grading logic (A+ to E)
│   │   │   └── profitability.py            # Repair P&L engine ⭐
│   │   └── views/
│   │       └── trc_views.xml
│   │
│   └── grest_dashboard/                    # Operations dashboard
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── controllers/
│       │   └── dashboard.py
│       └── views/
│           └── dashboard_views.xml
│
├── automation/                             # AI Automation layer (EXISTING)
│   ├── src/
│   │   ├── api/                            # Odoo API integrations
│   │   │   ├── odoo_client.py              # Odoo XML-RPC wrapper
│   │   │   ├── auth.py                     # Authentication
│   │   │   └── endpoints/
│   │   │       ├── products.py
│   │   │       ├── inventory.py
│   │   │       ├── contacts.py
│   │   │       ├── sales.py
│   │   │       └── trc.py                  # ⭐ NEW - TRC operations
│   │   │
│   │   ├── ai/                             # AI/LLM components (EXISTING)
│   │   │   ├── agent.py
│   │   │   ├── prompts.py
│   │   │   └── parsers.py
│   │   │
│   │   ├── data/                           # Data processing
│   │   │   ├── excel_reader.py             # Read Grest's Excel files
│   │   │   ├── data_mapper.py              # Map to Odoo fields
│   │   │   ├── validator.py                # Validate data quality
│   │   │   └── transformer.py              # Transform data formats
│   │   │
│   │   ├── workflows/                      # Business logic
│   │   │   ├── inventory_allocation.py
│   │   │   ├── channel_distribution.py
│   │   │   ├── buyback_processing.py
│   │   │   ├── trc_processing.py           # ⭐ NEW
│   │   │   └── profitability_check.py      # ⭐ NEW - Repair P&L
│   │   │
│   │   └── utils/
│   │       ├── logger.py
│   │       └── config.py
│   │
│   ├── scripts/
│   │   ├── migrate/                        # ⭐ NEW - Numbered migration sequence
│   │   │   ├── 01_setup_categories.py      # Run FIRST
│   │   │   ├── 02_import_vendors.py        # 30 vendors
│   │   │   ├── 03_import_products.py       # 106 device models + pricing
│   │   │   ├── 04_import_purchase_in.py    # 14,000 purchase records
│   │   │   ├── 05_import_spare_parts.py    # 8,000+ spare parts
│   │   │   ├── 06_import_trc_records.py    # 2,336 ELS/QC records
│   │   │   └── 07_import_repair_data.py    # 6,547 repair records
│   │   │
│   │   ├── initial_import.py               # (EXISTING - will be replaced by above)
│   │   ├── configure_odoo.py               # Auto-configure Odoo settings
│   │   └── sync_excel_to_odoo.py           # One-time Google Sheets sync
│   │
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_data_mapping.py
│   │   └── test_workflows.py
│   │
│   └── config/
│       ├── odoo_modules.json
│       ├── data_mappings.json              # ⭐ CRITICAL - all field mappings
│       └── business_rules.json             # Grest-specific rules
│
├── data-mappings/                          # ⭐ NEW - Human-readable mapping docs
│   ├── warehouse_sheet_mapping.md          # Warehouse → Odoo (DONE ✅)
│   ├── spares_sheet_mapping.md             # Spares → Odoo (DONE ✅)
│   ├── trc_sheet_mapping.md                # TRC → Odoo (DONE ✅)
│   └── master_field_reference.json         # Machine-readable for scripts
│
├── docs/
│   ├── requirements/
│   │   ├── business_process.md
│   │   ├── data_structure.md
│   │   └── odoo_modules.md
│   ├── architecture/
│   │   ├── system_design.md
│   │   ├── data_flow.md
│   │   └── api_design.md
│   ├── meeting-notes/
│   │   ├── 2025-02-12-aditya.md
│   │   └── 2025-02-17-analysis-complete.md
│   └── guides/
│       ├── odoo_setup.md
│       ├── module_deployment.md            # ⭐ NEW - Anti-Gravity deploy guide
│       └── user_training.md                # ⭐ NEW - 100 user training guide
│
├── sample-data/
│   ├── excel-templates/
│   │   ├── Warehouse_sheet_FORMATs.xlsx    # ✅ Analyzed
│   │   ├── Spares_Purchase_IN_2025.xlsx    # ✅ Analyzed
│   │   └── TRC-2025.xlsx                   # ✅ Analyzed
│   └── test-data/
│
└── migration-plan/                         # ⭐ ENHANCED
    ├── phase1-foundation.md                # Weeks 1-2: Odoo config
    ├── phase2-migration.md                 # Weeks 3-4: Data import
    ├── phase3-custom-modules.md            # Weeks 5-8: Claude Code builds
    ├── phase4-integrations.md              # Weeks 9-10: Shopify etc.
    └── phase5-golive.md                    # Weeks 11-12: Training + cutover

---

## KEY ADDITIONS vs ORIGINAL STRUCTURE:

1. custom-modules/     → Where Claude Code builds Odoo Python modules
2. data-mappings/      → Field mapping docs (already complete from analysis)
3. scripts/migrate/    → Numbered migration scripts (run in sequence)
4. workflows/trc_processing.py     → TRC-specific business logic
5. workflows/profitability_check.py → Repair P&L engine
6. docs/guides/module_deployment.md → How Anti-Gravity deploys to VPS

## ANTI-GRAVITY DEPLOYMENT PATH ON VPS:
/opt/odoo/custom-addons/grest_warehouse/
/opt/odoo/custom-addons/grest_trc/
/opt/odoo/custom-addons/grest_dashboard/

## ODOO CONFIG (odoo.conf) ADDITION NEEDED:
addons_path = /opt/odoo/addons,/opt/odoo/custom-addons
