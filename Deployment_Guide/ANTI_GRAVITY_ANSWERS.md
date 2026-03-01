# ANSWERS TO ANTI-GRAVITY'S QUESTIONS
## Complete Specifications for Implementation

---

## QUESTION 1: Complete procurement.py Model

**STATUS:** ✅ **PROVIDED ABOVE**

**File:** `procurement.py` (503 lines)

**Location in module:**
```
uploaded in the chat
```

**What's included:**
- 38 fields (all data types: Char, Float, Date, Selection, Many2one, etc.)
- 5 computed field methods (_compute_gsn, _compute_pricing, etc.)
- Commission calculation logic (6 source rates)
- GSN generation formula (TEMPORARY - marked with TODO)
- Auto-create approval on procurement create
- 2 constraint validators (unique IMEI, unique GSN)
- Complete docstrings

**Just copy the file contents EXACTLY as provided - no modifications needed.**

---

## QUESTION 2: GSN Format Specification

### Complete GSN Example:

```
GRGUNI6245SAUR31N
```

### Breakdown:

| Component | Value | Source | Description |
|-----------|-------|--------|-------------|
| Prefix | `GRG` | Fixed | Always "GRG" (GREST prefix) |
| Source | `UNI` | Source name | 3-char source abbreviation |
| IMEI | `6245` | IMEI last 5 | Last 5 digits of IMEI number |
| Tech | `SAUR` | Technician | First 4 chars of tech name |
| Serial | `31` | Serial number | Last 2 digits of serial |
| Month | `N` | Purchase month | First char of month (N=Nov) |

### Source Abbreviations:

```python
'cashify_b2b' → 'CAS'
'cashify_trading' → 'CAT'
'unicorn' → 'UNI'
'sangeeta' → 'SAN'
'trade_in' → 'TRA'
'other' → 'OTH'
```

### Examples with Different Sources:

**Unicorn purchase:**
```
Input:
- Source: unicorn
- IMEI: 356281920626245
- Technician: Saurabh
- Serial: 31
- Month: Nov_2025

Output: GRGUNI6245SAUR31N
```

**Cashify B2B purchase:**
```
Input:
- Source: cashify_b2b
- IMEI: 353080106921096
- Technician: Rahul
- Serial: 45
- Month: Dec_2025

Output: GRGCAS1096RAHU45D
```

**Sangeeta purchase:**
```
Input:
- Source: sangeeta
- IMEI: 123456789012345
- Technician: Amit
- Serial: 7
- Month: Jan_2026

Output: GRGSAN2345AMIT07J
```

### Important Notes:

1. **NO HYPHENS** - GSN is one continuous string
2. **ALWAYS UPPERCASE** - All letters capitalized
3. **ZERO-PADDED** - Serial number is 2 digits (07, not 7)
4. **TEMPORARY FORMULA** - Code has TODO comment for future update
5. **UNIQUE CONSTRAINT** - Database enforces uniqueness

### Where This Is Generated:

In `procurement.py`, the `_compute_gsn()` method (lines 264-321):

```python
@api.depends('source_name', 'imei', 'technician_id', 'serial_number', 'purchase_month')
def _compute_gsn(self):
    # ... code generates GSN automatically when record saved
```

### When Warehouse Provides Actual Formula:

**Update ONLY this one method** - rest of code unchanged.

---

## QUESTION 3: Payment Scenarios - Complete Specification

### The 3 Selection Options:

```python
payment_scenario = fields.Selection([
    ('paid', 'Fully Paid'),
    ('partial', 'Partially Paid'),
    ('credit', 'Credit Note'),
], string='Payment Scenario', required=True, default='paid')
```

### What Each Means:

#### **Scenario 1: FULLY PAID**

**When to use:**
- Immediate payment completed
- Supplier paid in full before device pickup
- Have payment UTR/reference

**Fields that apply:**
- ✅ `payment_utr` - Payment reference number
- ✅ `payment_date` - When payment made
- ✅ `payment_status` - Mark as "Paid"
- ❌ `credit_days` - NOT applicable
- ❌ `partial_amount` - NOT applicable
- ❌ `due_amount` - Should be 0

**Example workflow:**
```
1. Procurement creates entry
2. Selects: Payment Scenario = "Fully Paid"
3. Enters: Payment UTR = "ICICI1234567890"
4. Enters: Payment Date = 2025-11-14
5. Accounts approves immediately
```

---

#### **Scenario 2: PARTIALLY PAID**

**When to use:**
- Part payment now, rest later
- Supplier agreed to split payment
- Initial deposit made

**Fields that apply:**
- ✅ `partial_amount` - Amount paid now (in accounts approval module)
- ✅ `payment_utr` - Reference for partial payment
- ✅ `payment_date` - When partial payment made
- ✅ `due_amount` - Remaining amount owed
- ❌ `credit_days` - NOT applicable

**Example workflow:**
```
1. Procurement creates entry
   - Total Price: ₹100,000
2. Selects: Payment Scenario = "Partially Paid"
3. Accounts reviews:
   - Partial Amount: ₹50,000
   - Payment UTR: "HDFC9876543210"
   - Due Amount: ₹50,000
4. Accounts approves with note: "Balance due in 7 days"
```

---

#### **Scenario 3: CREDIT NOTE**

**When to use:**
- Supplier gives credit period (e.g., 15-20 days)
- No immediate payment needed
- Payment due after X days

**Fields that apply:**
- ✅ `credit_days` - Number of credit days (in accounts approval module)
- ✅ `payment_date` - FUTURE date (when payment due)
- ❌ `payment_utr` - Empty until payment made
- ❌ `partial_amount` - NOT applicable

**Example workflow:**
```
1. Procurement creates entry
   - Total Price: ₹200,000
2. Selects: Payment Scenario = "Credit Note"
3. Accounts reviews:
   - Credit Days: 15
   - Payment Due: 15 days from today
4. Accounts approves
5. Payment UTR entered later when actually paid
```

---

### Fields in Each Module:

**In grest_procurement (procurement.py):**
```python
payment_scenario = Selection (Paid/Partial/Credit)
payment_status = Char (free text)
payment_date = Date
payment_utr = Char
due_amount = Float
amount_balance = Float
```

**In grest_accounts_approval (accounts_approval.py):**
```python
payment_scenario = Related from procurement (readonly)
payment_utr = Char (accounts can edit)
credit_days = Integer (only for Credit scenario)
partial_amount = Float (only for Partial scenario)
```

### Form View Behavior:

**Using `attrs` to show/hide fields:**

```xml
<!-- In accounts approval form -->
<field name="credit_days" 
       attrs="{'invisible': [('payment_scenario', '!=', 'credit')]}"/>

<field name="partial_amount" 
       attrs="{'invisible': [('payment_scenario', '!=', 'partial')]}"/>
```

**This means:**
- If scenario = "Credit" → Show credit_days field
- If scenario = "Partial" → Show partial_amount field  
- If scenario = "Paid" → Show only payment_utr

---

## QUESTION 4: Staging DB - Should You Create It?

### ANSWER: **YES - CREATE BOTH DATABASES**

**Create TWO databases on Day 1:**

1. **grest_staging** (Development/Testing)
2. **grest_production** (Future Go-Live)

### Why Both?

**Staging (`grest_staging`):**
- ✅ Load demo data = YES
- ✅ Safe to experiment
- ✅ Can break and rebuild
- ✅ Test with sample entries
- ✅ Get team feedback
- ✅ Refine before production

**Production (`grest_production`):**
- ❌ Load demo data = NO
- ✅ Clean database
- ✅ Only deploy tested modules
- ✅ Real data only
- ✅ Actual go-live happens here

### Creation Process:

**Step 1: Access Odoo**
```
http://your-server:8069
```

**Step 2: Create Database 1**
```
Database name: grest_staging
Email: admin@grest.com
Password: [secure password]
Language: English
Country: India
Demo data: ☑ Load demonstration data
```

**Step 3: Create Database 2**
```
Database name: grest_production
Email: admin@grest.com
Password: [same password]
Language: English  
Country: India
Demo data: ☐ Do not load demonstration data
```

**Step 4: Switch to Staging**
```
In Odoo UI, select: grest_staging
```

### Your Development Flow:

```
Week 1-2: Build in grest_staging
  ↓
  Test, refine, get feedback
  ↓
Week 3: Export modules from staging
  ↓
  Import to grest_production
  ↓
  Final testing in production
  ↓
Week 4: Go-live
```

### How to Move from Staging → Production:

**When Phase 1 complete in staging:**

```bash
# Export module folders
cd /opt/odoo/custom_addons
tar -czf grest_modules.tar.gz grest_procurement/ grest_accounts_approval/

# They're already in custom_addons, just install in production DB
# Via Odoo UI:
# 1. Switch to grest_production database
# 2. Apps → Update Apps List
# 3. Search "GREST"
# 4. Install modules
```

**No need to copy files** - modules in `custom_addons` are available to all databases.

Just **install** them in production DB when ready.

---

## IMMEDIATE ACTION PLAN FOR ANTI-GRAVITY

### Step 1: Download procurement.py
✅ File provided above - copy to your system

### Step 2: Create Databases (15 mins)
```
Access Odoo UI
Create: grest_staging (demo data = YES)
Create: grest_production (demo data = NO)
Switch to: grest_staging
```

### Step 3: Create Module Structure (10 mins)
```bash
cd /opt/odoo/custom_addons
mkdir -p grest_procurement/{models,views,security}
touch grest_procurement/__init__.py
touch grest_procurement/__manifest__.py
touch grest_procurement/models/__init__.py
```

### Step 4: Copy Files (20 mins)
```
Copy procurement.py → models/procurement.py
Copy __manifest__.py from deployment guide
Copy views XML from deployment guide
Copy security files from deployment guide
Copy __init__.py files from deployment guide
```

### Step 5: Install Module (10 mins)
```
Restart Odoo
Apps → Update Apps List
Search "GREST Procurement"
Install
```

### Step 6: Test (20 mins)
```
Create 1 test entry
Verify GSN generates
Verify commission calculates
```

**Total time: ~90 minutes to working procurement module**

---

## VERIFICATION CHECKLIST

Before proceeding to accounts module, verify:

**Database:**
- [ ] grest_staging created with demo data
- [ ] grest_production created without demo data
- [ ] Currently using grest_staging

**Module Files:**
- [ ] procurement.py is 503 lines
- [ ] All imports at top: models, fields, api, UserError, ValidationError
- [ ] GSN function has TODO comment
- [ ] Commission rates dictionary has 6 sources
- [ ] create() method auto-creates approval

**Module Install:**
- [ ] Module appears in Apps list
- [ ] Menu "Procurement" appears in top bar
- [ ] Can navigate to Device Purchases
- [ ] Form view loads without errors

**Test Entry:**
- [ ] Can create entry with all required fields
- [ ] GSN generates on save (format: GRG...)
- [ ] Commission calculates (Unicorn = 12%)
- [ ] Total price = (price * 1.12) + logistics
- [ ] Serial number auto-increments

**GSN Examples to Test:**

Test 1:
```
Source: unicorn
IMEI: 356281920626245
Technician: Saurabh
Serial: 1 (auto)
Month: Nov_2025 (auto)

Expected GSN: GRGUNI6245SAUR01N
```

Test 2:
```
Source: cashify_b2b
IMEI: 123456789012345
Technician: Admin
Serial: 2 (auto)
Month: Mar_2026 (auto)

Expected GSN: GRGCAS2345ADMI02M
```

---

## PAYMENT SCENARIO TESTING

**Test each scenario:**

**Test 1: Fully Paid**
```
Create procurement:
- Payment Scenario: Fully Paid
- Price: ₹5000
- Source: Unicorn

Accounts approval should show:
- Payment UTR field (editable)
- Credit days field (hidden)
- Partial amount field (hidden)
```

**Test 2: Credit Note**
```
Create procurement:
- Payment Scenario: Credit Note
- Price: ₹10000
- Source: Sangeeta

Accounts approval should show:
- Credit days field (visible)
- Payment UTR field (empty, will fill later)
- Partial amount field (hidden)
```

**Test 3: Partial Payment**
```
Create procurement:
- Payment Scenario: Partially Paid  
- Price: ₹20000
- Source: Cashify Trading

Accounts approval should show:
- Partial amount field (visible)
- Payment UTR field (editable)
- Credit days field (hidden)
```

---

## NEXT STEPS AFTER VERIFICATION

**Once procurement module working:**

1. ✅ Mark Day 3-4 complete
2. ✅ Move to Day 5: Build accounts approval module
3. ✅ Test integration (procurement → accounts)
4. ✅ Verify approval workflow
5. ✅ Complete Phase 1

**Estimated remaining time:** 
- Day 5 (Accounts module): 2-3 hours
- Day 6 (Testing): 1 hour
- Day 7 (User setup): 30 mins

**Total Phase 1 completion: Today + 4 hours of focused work**

---

## CONTACT FOR ISSUES

**If you encounter:**
- Python syntax errors → Check indentation (use spaces, not tabs)
- Import errors → Verify Odoo path in sys.path
- Field not found → Check exact field name spelling
- GSN not generating → Verify all 5 dependencies filled
- Module won't install → Check __manifest__.py syntax

**Share:**
- Error message (full traceback)
- Which step you're on
- What you tried

**We'll debug together.** 🚀

---

**YOU'RE UNBLOCKED, ANTI-GRAVITY!**

**Go build.** 💪
