# ANTI-GRAVITY EXECUTION PROMPT
## GREST Odoo ERP - Phase 1 Deployment

**READ THIS FIRST, THEN EXECUTE THE DEPLOYMENT GUIDE**

---

## YOUR MISSION

You are tasked with deploying Phase 1 of the GREST Odoo ERP system.

**Timeline:** 7 days  
**Deliverable:** Working Procurement + Accounts Approval modules  
**Reference Document:** `GREST_ERP_COMPLETE_DEPLOYMENT_GUIDE.md`

---

## WHAT YOU'RE BUILDING

A procurement and approval workflow system for a mobile device refurbishment company.

**Module 1: grest_procurement**
- Tracks device purchases
- Auto-generates GSN barcodes
- Calculates commission
- Uploads invoices

**Module 2: grest_accounts_approval**
- Approval workflow
- 3 payment scenarios (Paid/Partial/Credit)
- Approve/Reject functionality

---

## EXECUTION SEQUENCE

### DAY 1: Environment Setup
**Execute:** Sections "DAY 1: ENVIRONMENT SETUP" from deployment guide

**Key Tasks:**
1. Install Odoo 18 CE
2. Create PostgreSQL user
3. Create two databases:
   - `grest_staging` (with demo data)
   - `grest_production` (no demo data)
4. Start Odoo service

**Success Check:**
- Can access http://localhost:8069
- Both databases visible
- Can login to grest_staging

---

### DAY 2: Product Master
**Execute:** Section "DAY 2: PRODUCT MASTER SETUP"

**Key Tasks:**
1. Create product categories (Mobile, Tab, Laptop, Watch, Airpods)
2. Create product attributes (Brand, RAM, ROM)
3. Import ~100 device models from `/mnt/project/Procurement_Sample_Sheet.xlsx`

**Success Check:**
- Navigate to Sales → Products
- See imported products (iPhone 11, iPad, etc.)
- Products have Brand, RAM, ROM filled

---

### DAY 3-4: Build Procurement Module
**Execute:** Section "DAY 3-4: BUILD PROCUREMENT MODULE"

**Key Tasks:**
1. Create module directory structure
2. Copy ALL files from deployment guide:
   - __manifest__.py
   - models/procurement.py (500+ lines)
   - views/procurement_views.xml
   - views/procurement_menu.xml
   - security files
3. Install module in Odoo

**Success Check:**
- Module appears in Apps
- Can navigate to Procurement → Device Purchases
- Form view shows all fields
- Can create a test entry

---

### DAY 5: Build Accounts Module
**Execute:** Section "DAY 5: BUILD ACCOUNTS APPROVAL MODULE"

**Key Tasks:**
1. Create accounts_approval module structure
2. Copy ALL files from deployment guide:
   - __manifest__.py
   - models/accounts_approval.py
   - views (kanban, form, tree, menu)
   - security files
3. Install module in Odoo

**Success Check:**
- Module installed
- Navigate to Accounts → Dashboard
- Kanban view shows columns (Pending/Approved/Rejected)

---

### DAY 6: Integration Testing
**Execute:** Section "DAY 6: TESTING"

**Run ALL 4 tests:**
1. Test 1: Create Procurement → Verify GSN generation
2. Test 2: Accounts Approval → Verify workflow
3. Test 3: Check Status Update → Verify connection
4. Test 4: Rejection Flow → Verify rejection

**Success Check:**
- All 4 tests PASS
- GSN generates correctly
- Approval updates procurement status
- Rejection works

---

### DAY 7: User Setup & Training
**Execute:** Section "DAY 7: USER TRAINING"

**Key Tasks:**
1. Create 3 test users with different access levels
2. Test as each user
3. Document any issues
4. Prepare training materials

**Success Check:**
- Procurement user can create entries
- Accounts manager can approve/reject
- Regular user cannot approve

---

## CRITICAL REQUIREMENTS

### DO NOT SKIP:
1. ✅ **Database Creation:** MUST have both staging and production
2. ✅ **Product Import:** MUST import models before creating procurement
3. ✅ **Module Order:** MUST build procurement BEFORE accounts
4. ✅ **Testing:** MUST test each module before proceeding

### CODE INTEGRITY:
1. ✅ **Copy Python code EXACTLY** - No modifications
2. ✅ **Copy XML code EXACTLY** - No changes to structure
3. ✅ **Preserve indentation** - Python is indentation-sensitive
4. ✅ **Use provided field names** - Do NOT rename

### GSN FORMULA:
The GSN formula in `procurement.py` is TEMPORARY and marked with TODO.
When warehouse provides actual formula, update ONE function: `_compute_gsn()`

---

## REFERENCE FILES

Located in `/mnt/project/`:

**Primary Data Source:**
- `Procurement_Sample_Sheet.xlsx` - Extract unique models from Column G

**Business Context:**
- `Procurement_Meeting_Transcript.md` - Requirements discussion
- `nikhil.txt` - Accounts workflow requirements

**DO NOT modify these files.** Read-only reference.

---

## SUCCESS CRITERIA - PHASE 1 COMPLETE

Before declaring Phase 1 done, verify ALL of these:

### Functional Tests:
- [ ] Procurement module installed
- [ ] Accounts approval module installed
- [ ] Can create procurement entry
- [ ] GSN auto-generates on save
- [ ] Commission auto-calculates
- [ ] Invoice uploads successfully
- [ ] Approval auto-creates on procurement create
- [ ] Accounts can see pending approvals
- [ ] Can approve procurement
- [ ] Procurement status updates to "Approved"
- [ ] Can reject procurement
- [ ] Rejection reason required

### Data Validation:
- [ ] IMEI must be unique (constraint works)
- [ ] GSN must be unique (constraint works)
- [ ] Required fields enforced (cannot save without)
- [ ] Commission rates correct (Unicorn=12%, Cashify B2B=0%)
- [ ] Month auto-fills from dates

### UI/UX:
- [ ] Forms are readable and organized
- [ ] Kanban dashboard shows 3 columns
- [ ] Can filter by status
- [ ] Can search by GSN/IMEI
- [ ] Approve/Reject buttons visible

### Security:
- [ ] Procurement user can create/edit own entries
- [ ] Procurement manager can see all entries
- [ ] Accounts user can view approvals
- [ ] Accounts manager can approve/reject
- [ ] Regular user has no access

---

## IF YOU ENCOUNTER ERRORS

### Python Errors:
1. Check indentation (Python is strict)
2. Verify all imports at top of file
3. Check field names match exactly
4. Look for typos in model names

### XML Errors:
1. Check all tags are closed properly
2. Verify field names match Python model
3. Ensure proper XML structure (no missing `</>`)

### Module Won't Install:
1. Check `/var/log/odoo/odoo.log` for errors
2. Verify manifest.py syntax
3. Ensure depends modules are installed
4. Try: Apps → Update Apps List

### GSN Not Generating:
1. Verify all required fields filled:
   - source_name
   - imei (at least 5 chars)
   - technician_id
   - serial_number
   - purchase_month
2. Check `_compute_gsn()` function has no syntax errors

---

## IMPORTANT NOTES

### About GSN Formula:
The current formula is TEMPORARY:
```
GRG + Source(3) + IMEI(last5) + Tech(4) + Serial(2) + Month(1)
```

Warehouse team will provide actual formula later.
When they do, update ONLY the `_compute_gsn()` function in `procurement.py`.

Mark location with comment:
```python
# TODO: Replace with actual warehouse formula when provided
```

### About Commission Rates:
Current rates in `_compute_pricing()`:
- Cashify B2B: 0%
- Cashify Trading: 0%
- Unicorn: 12%
- Sangeeta: 12%
- Other: 12%

These can be adjusted in `COMMISSION_RATES` dictionary.

### About Payment Scenarios:
Three scenarios implemented:
1. **Paid** - Immediate payment
2. **Partial** - Pay some now, rest later
3. **Credit** - Supplier gives 15-20 days credit

All three require accounts approval before proceeding.

---

## WORKFLOW VALIDATION

**End-to-End Test:**

```
1. Procurement creates entry (PROC-1)
   → Status: Pending Accounts Approval
   
2. System auto-creates approval (APPR-PROC-1)
   → State: Pending
   
3. Accounts reviews and approves
   → State: Approved
   → Approval date/user logged
   
4. Procurement status updates
   → Status: Approved
   
5. Ready for Phase 2 (Warehouse)
```

If this flow works from start to finish → **Phase 1 SUCCESS** ✅

---

## WHAT HAPPENS AFTER PHASE 1

Once Phase 1 is complete and tested:

**Phase 2:** Build Warehouse module (4 weeks)
- Receive devices from procurement
- Verify IMEI
- Print GSN barcode
- Track locations
- Handover to TRC

**Phase 3:** Build TRC & P&L (4 weeks)
**Phase 4:** Build Sales & Integration (4 weeks)

**DO NOT start Phase 2 until Phase 1 is 100% complete and tested.**

---

## COMMUNICATION

### Report Progress:
After each day, report:
- ✅ Tasks completed
- ⏸️ Any blockers
- 📊 Test results
- ⏭️ Next day plan

### Ask for Help:
If stuck for more than 1 hour:
- Share error message
- Share code that's failing
- Share what you've tried

**Contact:** Sammy, Nikhil, or Astra

---

## FINAL CHECKLIST

Before declaring Phase 1 complete:

**Code:**
- [ ] All files created in correct locations
- [ ] No syntax errors in Python
- [ ] No syntax errors in XML
- [ ] Imports are correct
- [ ] Indentation is correct

**Functionality:**
- [ ] All 12 success criteria tests pass
- [ ] End-to-end workflow tested
- [ ] Security rules working
- [ ] Constraints enforced

**Documentation:**
- [ ] Code comments added where needed
- [ ] TODO markers for future updates
- [ ] Test results documented

**Deployment:**
- [ ] Works in grest_staging
- [ ] Ready to deploy to grest_production
- [ ] Can export modules
- [ ] Can import to new database

---

## START NOW

1. Open `GREST_ERP_COMPLETE_DEPLOYMENT_GUIDE.md`
2. Read sections carefully
3. Execute DAY 1 tasks
4. Report progress
5. Continue to DAY 2

**Good luck! You've got this.** 🚀

---

**END OF ANTI-GRAVITY PROMPT**
