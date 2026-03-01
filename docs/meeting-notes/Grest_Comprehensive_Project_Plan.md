# GREST ODOO ERP - COMPREHENSIVE PROJECT PLAN
## Version 1.0 - Full Implementation

**Prepared by:** Samret Singh
**Date:** February 17, 2025
**Status:** APPROVED FOR EXECUTION

---

## PROJECT OVERVIEW

### What We're Building
A complete ERP system on Odoo Community Edition replacing 30+ Google Sheets for Grest's refurbished device business — tracking every device from procurement through quality check, repair, and multi-channel sales.

### Technology Stack
- **Platform:** Odoo 18 Community (installed ✅ at godoo.sam9scloud.in)
- **Database:** PostgreSQL (grest_production ✅)
- **Custom Modules:** Python + XML
- **Deployment:** VPS-2 (connected ✅)
- **Migration:** Python scripts via Odoo XML-RPC API

### Key Numbers
| Metric | Value |
|--------|-------|
| Total Users | ~100 |
| Devices in inventory | ~100,000 |
| Weekly intake | ~1,000 devices |
| Spare parts records | ~10,000+ |
| Repair records | 6,547 |
| Product models | 106+ |
| Brands | 24 |
| Vendors/Suppliers | 30 |
| Transaction types | 50 (21 IN + 29 OUT) |
| Warehouse locations | GRG (Gurgaon) + others |

---

## PHASE 1: FOUNDATION & CONFIGURATION
### Weeks 1-2 | Zero Custom Code | Odoo Admin Only

**Goal:** Set up Odoo so it mirrors Grest's business structure exactly.

---

### WEEK 1: Core Setup

#### Day 1-2: Warehouse & Location Structure

**Odoo Path:** Inventory → Configuration → Warehouses

**Create:**
```
Warehouse: "Grest Gurgaon" (Short: GRG)
  Locations:
  ├── GRG/Input          (Security gate receiving)
  ├── GRG/Purchase-IN    (Warehouse acceptance area)
  ├── GRG/TRC            (Technical Repair Center)
  ├── GRG/QC             (Quality Control)
  ├── GRG/Ready-Stock    (Post-QC, ready for sale)
  ├── GRG/B2B            (B2B allocated)
  ├── GRG/D2C            (D2C/E-com allocated)
  ├── GRG/B2R            (B2R allocated)
  ├── GRG/MG-Store       (MG Road retail)
  └── GRG/Spareparts     (Spare parts storage)
```

 
**Verification:** All locations visible in Inventory → Configuration → Locations

---

#### Day 2-3: Product Categories

**Odoo Path:** Inventory → Configuration → Product Categories

**Create hierarchy:**
```
All Products
├── Mobile Devices
│   ├── Apple (iPhone)
│   ├── Samsung
│   ├── OnePlus
│   ├── Xiaomi / Redmi
│   ├── Vivo
│   ├── Oppo / Realme
│   ├── Motorola
│   ├── Google Pixel
│   └── Others (Nokia, LG, Huawei, etc.)
├── Laptops
│   ├── MacBook
│   └── Windows Laptops
├── Tablets
│   ├── iPad
│   └── Android Tablets
├── Accessories
│   ├── AirPods
│   ├── Apple Watch
│   ├── Cables & Adapters
│   └── Others
└── Spare Parts
    ├── Display
    ├── Battery
    ├── Front Glass
    ├── Back Panel / Housing
    ├── Child Parts (cameras, ringers, flex)
    └── Consumables & Tools
```

 

---

#### Day 3: Grades as Product Attributes

**Odoo Path:** Inventory → Configuration → Attributes

**Create Attribute: "Device Grade"**
```
Values (in order):
A+, A, B+, B, B-, C+, C, D+, D, E
```

**Create Attribute: "Storage"**
```
Values: 32GB, 64GB, 128GB, 256GB, 512GB, 1TB
```

**Create Attribute: "RAM"**
```
Values: 2GB, 3GB, 4GB, 6GB, 8GB, 12GB, 16GB
```

---

#### Day 4: Custom Fields (CRITICAL)

**Odoo Path:** Settings → Technical → Custom Fields

**On stock.lot (Serial Numbers):**
```
Field Name          | Type      | Label
imei_number         | Char      | IMEI Number
device_grade        | Selection | Device Grade (A+,A,B+,B,B-,C+,C,D+,D,E)
store_grade         | Selection | Store Grade (same values)
els_grade           | Selection | ELS Grade (same values)
fqc_grade           | Selection | FQC Grade (same values)
source_channel      | Selection | Source (C2B, Supplier, Walk-in, Amazon)
supplier_code       | Char      | Supplier Code
purchase_price      | Float     | Purchase Price
spare_consumption   | Float     | Spare Cost
pp_for_sales        | Float     | PP for Sales (auto = purchase + spare)
barcode_printed     | Boolean   | Barcode Printed?
warranty_status     | Selection | Warranty (With/Without)
color               | Char      | Color
```

---

#### Day 5: Operation Types

**Odoo Path:** Inventory → Configuration → Operations Types

**Create custom operation types for OUT:**
```
Sold                    | Out for Sales
Out for Repair (In)     | Out for Repair (Outsource)
Return to Supplier      | Return to Vendor
Out for MG Store        | Out for B2R
Amazon Out              | Out for E-commerce
Lost Device             | Out for Liquidation
Out for Cannibalization | Out for Swapping
Out for Office Use      | Out for Refurb
```

**Create custom operation types for IN:**
```
Fresh Inventory              | Received after Repair (In)
Received after Repair (Out)  | Retailer Return
Customer Return              | Return from Amazon
Received After Swapping      | Received After Cannibalization
```
 
---

### WEEK 2: Data Foundation

#### Day 6-7: Import Vendors (30 vendors)

**Script: 02_import_vendors.py**

This is the first script  Code will write.

**Vendors to import:**
Diva, MNC, Purohit, Namdev, Lohia, Laxmi Telecom, AR Trading, Ahuja, All IN One, Baba Tools, Bharat, Bolta, Britco, Friends Telecom, Itech, LR Spare, Maa Vaishno, Mahaveer, Mobatree, Namdev, Newgen Technologies, PR King, Refurbix, SKI, Satguru, Shree Accessories, Spare City, Sun Display, TN, The Housing Club

**Data format:**
```json
{
  "name": "Diva",
  "supplier_rank": 1,
  "ref": "VEN001",
  "phone": "",
  "category": "Spare Parts Vendor"
}
```

---

#### Day 7-8: Import Product Catalog (106 iPhone models)

**Script: 03_import_products.py**

**Source:** TRC sheet SALE PRICE tab (106 models with prices)

**For each model, create:**
- Product with brand, model, storage, RAM as attributes
- Pricelists for each grade (A+ through E)
- Internal reference code (e.g., APGRGA001)

---

#### Day 8-9: Import Spare Parts Catalog

**Script: 05_import_spare_parts.py**

**Sources:** All Spares tabs (Display, Battery, Front Glass, Back Panel, Child Parts)

**For each spare:**
```
Brand + Series + Model + Part Name + Quality
→ Odoo Product (type=consumable)
→ Category: Spare Parts → [subcategory]
→ Vendor: from vendor code
```

**~8,000 spare parts to import**

---

#### Day 9-10: User Accounts & Permissions

**Odoo Path:** Settings → Users & Companies → Users

**Create user groups:**
```
Group: Warehouse TL/Manager
  - Full inventory access
  - Can approve/reject
  - Can see purchase prices
  - Can override decisions

Group: Warehouse Member  
  - See only assigned devices
  - Can generate barcodes
  - Can transfer to TRC

Group: TRC Manager
  - QC workflow full access
  - Can approve repairs
  - Can see profitability

Group: QC Technician
  - Assigned devices only
  - Enter ELS/QC grades
  - Cannot approve repairs

Group: Repair Technician
  - Repair queue only
  - Mark repair complete
  - Log parts used

Group: Spare Department
  - Spare parts module only
  - Cannot see inventory

Group: Sales Team
  - View allocated inventory
  - Create sales orders
  - Cannot see purchase prices

Group: Admin
  - Full system access
```

---

## PHASE 2: DATA MIGRATION
### Weeks 3-4 | Python Scripts |  Code Writes, You Run

**Goal:** Move all historical data from Google Sheets into Odoo.

---

### Migration Script Sequence

**Run in this EXACT order:**

```
Step 1: 01_setup_categories.py      → Creates all categories/attributes
Step 2: 02_import_vendors.py        → 30 vendors
Step 3: 03_import_products.py       → 106 device models + pricing
Step 4: 04_import_purchase_in.py    → 14,000 purchase records
Step 5: 05_import_spare_parts.py    → 8,000+ spare parts
Step 6: 06_import_trc_records.py    → 2,336 ELS/QC records
Step 7: 07_import_repair_data.py    → 6,547 repair records
```

**Each script:**
- Reads from Excel file
- Validates data
- Connects to Odoo via XML-RPC
- Creates/updates records
- Logs successes and failures
- Generates report at end

---

### Week 3: Purchase IN + Spares Migration

#### Script: 04_import_purchase_in.py

**Source:** Sheet22 in TRC-2025.xlsx (14,000 records)

**Mapping:**
```
Sheet Column          → Odoo Field
Sr. No                → Reference (lot name)
Inventory Location    → Location (GRG)
Purchase In Date      → Date
Category              → Product Category
IMEI                  → Serial Number (lot.imei_number)
COLOR                 → lot.color
Sub Category          → Product Sub-category
Grest Part Name       → Product Internal Reference
Model Details         → Product Name
Supplier Code         → Vendor (lot.supplier_code)
Amount with Tax       → lot.purchase_price
Spare Consumption     → lot.spare_consumption
P.P for Sales         → lot.pp_for_sales (auto-calculated)
```

**Barcode generation during import:**
```
Format: [BrandCode][Location][Category][Sequence]
Example: APGRGA001

BrandCode:
  AP = Apple
  SA = Samsung  
  ON = OnePlus
  XI = Xiaomi
  VI = Vivo
  OP = Oppo
  MO = Motorola
  GO = Google
  RE = Realme
```

---

#### Script: 05_import_spare_parts.py

**Source:** Spares_Purchase_-_IN__2025.xlsx

**For each tab (Display, Battery, etc.):**
```
Purchased Date    → Date
Brand + Series + Model + Part → Product (match or create)
Part Quality      → OG/A-Grade/B-Grade/GX/DD/Copy
Quantity          → Stock quantity
Price Per Pcs     → Cost price
Vendor Name       → Vendor
Total Cost        → Total cost
```

---

### Week 4: TRC + Repair Migration

#### Script: 06_import_trc_records.py

**Source:** ELSFQC tab in TRC-2025.xlsx (2,336 records)

**Mapping:**
```
IMEI No         → Find matching lot by IMEI
Bar Code        → lot.barcode (verify match)
Model           → Product (verify)
Store Grade     → lot.store_grade
Els-Grade       → lot.els_grade
FQC Grade       → lot.fqc_grade (= lot.device_grade for sales)
Status          → lot.grade_change_status (Upgrade/Same/Downgrade)
```

---

#### Script: 07_import_repair_data.py

**Source:** Grest Repair tab in TRC-2025.xlsx (6,547 records)

**Mapping:**
```
Date            → Repair Order date
Barcode         → Find device by barcode
IMEI            → Verify match
Model           → Verify product
Supplier Code   → Vendor reference
ELS-Grade       → lot.els_grade
QC-Grade        → lot.fqc_grade
Status          → Repair status
Spare Cost      → repair.parts_cost
Labour Cost     → repair.labour_cost
Total Cost      → repair.total_cost
Purchase Price  → lot.purchase_price (VLOOKUP replaced by Odoo relation)
Total Cost P/R  → Computed field (purchase + repair)
```

---

## PHASE 3: CUSTOM MODULES
### Weeks 5-8 | Python + XML |  Code Builds, Anti- Deploys

**Goal:** Build the smart business logic that Odoo doesn't have natively.

---

### Module 1: grest_warehouse (Week 5)

**What it does:**
- Adds IMEI, Grade, Source fields to stock records
- Custom barcode generation (GRG-IMEI-SEQ format)
- Status-driven workflow (PENDING → ACCEPTED → BARCODE → SENT_TO_QC)
- Role-based visibility rules

**Files  Code will write:**
```python
# models/grest_device.py
class GrestDevice(models.Model):
    _inherit = 'stock.lot'
    
    imei_number = fields.Char('IMEI', size=15)
    device_grade = fields.Selection([
        ('A+','A+'),('A','A'),('B+','B+'),('B','B'),
        ('B-','B-'),('C+','C+'),('C','C'),
        ('D+','D+'),('D','D'),('E','E')
    ])
    els_grade = fields.Selection(...)
    fqc_grade = fields.Selection(...)
    purchase_price = fields.Float('Purchase Price')
    spare_cost = fields.Float('Spare Cost')
    pp_for_sales = fields.Float(
        compute='_compute_pp_for_sales', store=True
    )
    
    @api.depends('purchase_price', 'spare_cost')
    def _compute_pp_for_sales(self):
        for rec in self:
            rec.pp_for_sales = rec.purchase_price + rec.spare_cost
```

**Deployment:**
- Anti- copies module to /opt/odoo/custom-modules/
- Restart Odoo service
- Activate module in Settings → Apps

---

### Module 2: grest_trc (Week 6)

**What it does:**
- TRC Order model (separate from Odoo repair module)
- ELS → routing decision (Grade ≤ B → warehouse, Grade > B → full QC)
- Profitability engine (purchase + repair cost vs. sale price)
- Repair blocking when loss (with override)

**Key logic - Profitability Engine:**
```python
def compute_profitability(self):
    purchase_price = self.lot_id.purchase_price
    spare_cost = self.spare_cost
    labour_cost = self.labour_cost
    total_investment = purchase_price + spare_cost + labour_cost
    
    # Get sale price from pricelists
    after_repair_value = self._get_sale_price(
        self.lot_id.product_id, 
        self.fqc_grade
    )
    
    profit_loss = after_repair_value - total_investment
    
    if profit_loss < 0:
        # Block repair - show warning
        self.repair_blocked = True
        self.block_reason = f"Loss of ₹{abs(profit_loss):.0f}"
    else:
        self.repair_blocked = False
```

**ELS Routing Logic:**
```python
DIRECT_TO_WAREHOUSE_GRADES = ['B', 'B-', 'C', 'C+', 'D', 'D+', 'E']

def route_after_els(self):
    if self.els_grade in DIRECT_TO_WAREHOUSE_GRADES:
        # Skip full QC, return to warehouse
        self.state = 'ready_for_stock'
    else:
        # Needs full QC evaluation
        self.state = 'repair_evaluation'
```

---

### Module 3: grest_dashboard (Week 7-8)

**What it does:**
Replicates the OPS DASHBOARD from Google Sheets in real-time:

```
Left Panel:               Middle Panel:          Right Panel:
Purchase In Pending       B2B Aging:             Category Stock:
QC Pending               0-30 days              iPhone: 1,247
B2B Ready                30-45 days             Samsung: 834
B2B VRP                  45-60 days             OnePlus: 312
B2R                      60-90 days             MacBook: 89
E-COM                    90-180 days            ...
Out for Repair           Above 180 days
In Transit
Out for MG Store
```

**All numbers clickable → drill down to device list**

---

## PHASE 4: INTEGRATIONS
### Weeks 9-10 | API Connections

**Goal:** Connect Odoo to external systems.

---

### Shopify Integration (D2C Channel)

**You already have admin access ✅**

**What we'll build:**
```python
# automation/src/api/shopify_sync.py

class ShopifySync:
    """
    Bidirectional sync between Shopify and Odoo
    
    Odoo → Shopify:
    - When device allocated to D2C → Create/update Shopify product
    - When device sold elsewhere → Remove from Shopify
    - Real-time inventory count sync
    
    Shopify → Odoo:
    - New order → Create Odoo sales order
    - Order fulfilled → Update inventory out
    - Return → Create return receipt
    """
```

**Trigger:** Inventory allocated to D2C location → auto-sync to Shopify

---

### Grest Partners Integration (B2B)

**Pending:** API availability check (ask Kavita)

**If API available:**
- Similar to Shopify integration
- Inventory sync when allocated to B2B

**If no API:**
- Export report from Odoo
- Manual update remains (temporary)

 3-5 days

---

## PHASE 5: GO-LIVE
### Weeks 11-12 | Training + Cutover


### Week 11: Training

**Training plan:**

**Day 1-2: Warehouse Team (Balpreet + 10 members)**
- How to receive devices
- Generate barcodes
- Transfer to TRC
- View inventory

**Day 3-4: TRC Team (Rajesh, Dinesh + technicians)**
- ELS submission
- QC grading
- Repair orders
- Spare parts

**Day 5: Sales Teams (Aniket, Ishani, Suyash)**
- View allocated inventory
- Create sales orders
- Channel allocation requests

**Day 6: Management (Kavita + Sanjeev)**
- Dashboard overview
- Reports and exports
- User management

---

### Week 12: Parallel Run + Cutover

**Days 1-7: Parallel Run**
- ALL operations in BOTH Google Sheets AND Odoo
- Compare outputs daily
- Fix discrepancies

**Day 8: Final Data Sync**
- One last import of any gaps
- Verify all records match

**Day 9: Cutover**
- Google Sheets go READ-ONLY
- Odoo becomes system of record
- Support hotline active

**Day 10+: Hypercare**
- Daily check-ins with Balpreet
- Fix any issues within 24 hours
- Sheets remain as backup for 2 weeks

---

## COMPLETE FIELD MAPPING REFERENCE

### Warehouse Sheet → Odoo

| Sheet Field | Odoo Model | Odoo Field | Notes |
|------------|-----------|-----------|-------|
| Sr. No | stock.lot | name | Lot reference |
| Inventory Location | stock.location | location_id | GRG |
| Purchase In Date | stock.picking | date | Receipt date |
| Category | product.category | categ_id | Mobile/Laptop etc |
| IMEI | stock.lot | imei_number | Custom field |
| COLOR | stock.lot | color | Custom field |
| Sub Category | product.template | sub_category | Custom field |
| Grest Part Name | product.template | default_code | Internal ref |
| Model Details | product.template | name | Product name |
| Market Model | product.template | market_model | Custom field |
| Supplier Code | res.partner | ref | Vendor ref |
| Amount with Tax | stock.lot | purchase_price | Custom field |
| Code1 | product.template | brand_code1 | Custom field |
| Code2 | product.template | brand_code2 | Custom field |
| Spare Consumption | stock.lot | spare_cost | Custom field |
| P.P for Sales | stock.lot | pp_for_sales | Computed |
| PI Date | stock.picking | date | Same as Purchase In Date |
| Month | - | - | Computed from date |

---

### Spares Sheet → Odoo

| Sheet Field | Odoo Model | Odoo Field | Notes |
|------------|-----------|-----------|-------|
| Purchased Date | stock.picking | date | |
| Brand | product.template | brand | Category |
| Series | product.template | series | Custom field |
| Model | product.template | model | Custom field |
| Colour | product.template | color | Attribute |
| Parts Details | product.template | name | Part name |
| Parts Quality | product.template | quality | OG/A-Grade etc |
| Purchase Quantity | stock.move | product_qty | |
| Price Per Pcs | product.template | standard_price | Cost |
| Total Cost | - | - | Computed |
| Vendor Name | res.partner | name | Supplier |
| Vendor Code | res.partner | ref | |

---

### TRC Sheet → Odoo

| Sheet Field | Odoo Model | Odoo Field | Notes |
|------------|-----------|-----------|-------|
| IMEI No | stock.lot | imei_number | Find by IMEI |
| Bar Code | stock.lot | name | Verify match |
| Model | product.template | name | Verify |
| Store Grade | stock.lot | store_grade | Custom field |
| ELS Grade | stock.lot | els_grade | Custom field |
| FQC Grade | stock.lot | fqc_grade | = device_grade |
| Status | stock.lot | grade_change | Upgrade/Same/Down |
| Spare Cost | repair.order | parts_cost | |
| Labour Cost | repair.order | labour_cost | |
| Total Cost | repair.order | total_cost | Computed |

---

## RISK REGISTER

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Data quality issues in sheets | Medium | High | Validate before import, fix errors |
| Odoo module deployment issues | Low | Medium | Test on dev first |
| User adoption resistance | Medium | High | Training + champion users |
| Shopify API changes | Low | Medium | Use official Shopify API |
| Sanjeev requests scope changes | Medium | Medium | Phase approach allows flexibility |
| Server performance with 100K records | Low | High | Optimize queries, proper indexing |

---

## SUCCESS METRICS

### Technical
- [ ] All 14,000 purchase records migrated
- [ ] All 8,000 spare parts imported
- [ ] All 6,547 repair records imported
- [ ] Real-time updates working (< 1 second)
- [ ] All 100 users can login
- [ ] Barcode generation working
- [ ] Shopify sync working

### Business
- [ ] Any device findable by IMEI in < 3 seconds
- [ ] Profitability calculated automatically
- [ ] Google Sheets officially retired
- [ ] Zero inventory discrepancy between Odoo and physical count
- [ ] Dashboard showing correct live numbers

---

## TIMELINE SUMMARY

| Phase | Duration | What Happens | Who Does What |
|-------|----------|-------------|--------------|
| Phase 1 | Weeks 1-2 | Odoo configuration | Sammy clicks, Astra guides |
| Phase 2 | Weeks 3-4 | Data migration | Astra writes scripts, Sammy runs |
| Phase 3 | Weeks 5-8 | Custom modules |  Code builds, Anti- deploys |
| Phase 4 | Weeks 9-10 | Integrations |  Code builds, Sammy tests |
| Phase 5 | Weeks 11-12 | Training + Go-live | Sammy leads, Astra supports |

**Total: 12 weeks from start to full go-live**
**Start date: Feb, 2025**
**Target go-live: May, 2025**

---

## IMMEDIATE NEXT ACTIONS

### This Week (Week of Feb 17):

**Day 1 (TODAY):**
- [ ] Sammy reviews and approves this project plan
- [ ] Sammy opens Odoo admin panel
- [ ] Create Grest Gurgaon warehouse
- [ ] Create first 3 locations (Input, Purchase-IN, TRC)

**Day 2:**
- [ ] Create remaining locations
- [ ] Create product category hierarchy
- [ ] Create Device Grade attribute

**Day 3:**
- [ ] Create custom fields on stock.lot
- [ ] Verify fields appear in Odoo UI

**Day 4:**
- [ ] Create Operation Types (IN and OUT)
- [ ] Create User Groups

**Day 5:**
- [ ] Create first 10 test users
- [ ] Test role-based visibility
- [ ] Report progress to Kavita/Sanjeev

**End of Week 1/2 Deliverable:**
Odoo structured and ready for data import.

---

## NOTES FOR SAMMY as CODER

When we reach Phase 3, the custom modules need to be built following Odoo 18 Community standards:

1. Each module in `/opt/odoo/custom-addons/` on the VPS
2. Module structure: `__manifest__.py`, `__init__.py`, `models/`, `views/`, `security/`
3. Inherit existing Odoo models (don't replace)
4. Use `_inherit` not `_name` for extensions
5. All custom fields prefixed with `grest_` to avoid conflicts
6. Security rules via `ir.model.access.csv`
7. Test on staging before production

---

*Document Version: 1.0*
*Next Review: After Phase 1 complete (Week 2)*
*Maintained by: Samret Singh
