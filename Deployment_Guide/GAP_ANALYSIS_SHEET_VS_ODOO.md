# GREST Procurement — Sheet vs Odoo Gap Analysis
**Author:** Antigravity (Developer)  
**Date:** 2 March 2026  
**Based on:** `Procurement Sample Sheet.xlsx` — Sheet1, 43 columns, 4,650 records

---

## The Short Answer First

The Excel sheet has **43 columns**. Our current Odoo model has **38 fields**.  
After analysis: we are **missing 2 fields, have 3 type mismatches, and have 3 fields that need renaming** to match the sheet.  
Everything else is already there.

---

## Full Column-by-Column Comparison

| # | Excel Column | In Odoo? | Field Name | Issues / Notes |
|---|---|---|---|---|
| C1 | S.no | ✅ | `serial_number` | Auto-generated. ✅ |
| C2 | Purchase Month | ✅ | `purchase_month` | Auto-derived from date. ✅ |
| C3 | Purchase Date | ✅ | `purchase_date` | ✅ |
| C4 | Technicians | ✅ | `technician_id` | Many2one to `res.users`. ✅ |
| C5 | Category (Mobile, Tab, Laptop, Watch) | ✅ | `category` | Selection. Missing `Airpods` in header label but we have it in code. ✅ |
| C6 | IMEI No | ✅ | `imei` | ✅ |
| C7 | Model | ✅ | `model_id` | Many2one to `product.product`. ✅ |
| C8 | Store name | ✅ | `store_name` | ⚠️ **Currently a free-text field. Should be dropdown.** See Section 3. |
| C9 | Price Offered to Customer | ✅ | `price_offered` | ✅ |
| C10 | Ave Price | ✅ | `ave_price` | Free-text manual entry. ✅ |
| C11 | GREST RECEIVED | ✅ | `grest_received` | Boolean (Yes/No). ✅ |
| C12 | Grest Unique Code / GSN | ✅ | `gsn` + `grest_unique_code` | ⚠️ **GSN formula is TEMPORARY** — Nikhil to confirm. Current: `GRGUniDDKNYSaur1N`. Sheet example. |
| C13 | Source Name | ✅ | `source_name` | Selection dropdown. ✅ |
| C14 | Payment status | ✅ | `payment_status` | ⚠️ **Currently a free-text field.** Sheet values seen: `'Paid'`. Should be a Selection (Paid/Partial/Pending). |
| C15 | Payment date | ✅ | `payment_date` | ✅ |
| C16 | Payment Month | ✅ | `payment_month` | Auto-derived. ✅ |
| C17 | Store payment UTR number | ✅ | `payment_utr` | Free-text. ✅ (UTRs are free-form strings, correct to keep as text.) |
| C18 | **Receiving and Pickup date** | ⚠️ | `receiving_date` | **ONE column in sheet = TWO different events.** We have only `receiving_date`. Need to rename to `receiving_pickup_date` OR add a separate `pickup_date`. Discuss with Nikhil. |
| C19 | RECEIVING Month | ✅ | `receiving_month` | Auto-derived. ✅ |
| C20 | Total price | ✅ | `total_price` | Auto-computed. ✅ |
| C21 | Due Amount | ✅ | `due_amount` | ✅ |
| C22 | Logistic Charge | ✅ | `logistic_charge` | ✅ |
| C23 | Grade | ✅ | `grade` | ⚠️ **Free-text. Sheet values: A, B, C, D, E. Should be Selection.** |
| C24 | ELS grade | ✅ | `els_grade` | ⚠️ **Free-text. Sheet values: B, C, C+, D, E. Should be Selection.** |
| C25 | Status | ✅ | `status` | ⚠️ **Mismatch!** Our values: `pending/received/handed_over`. Sheet values: `'Downgrade'`, `'Upgrade'`, `'Completed'` etc. — these look like **device condition/TRC status**, NOT procurement status. Need Nikhil to clarify what this column means. |
| C26 | Amount balance | ✅ | `amount_balance` | ✅ |
| C27 | Handover date | ✅ | `handover_date` | ✅ |
| C28 | Handover Month | ✅ | `handover_month` | Auto-derived. ✅ |
| C29 | Commission Payment status | ✅ | `commission_payment_status` | ⚠️ **Free-text.** Should be Selection (Paid/Pending/NA). |
| C30 | Commission UTR number | ✅ | `commission_utr` | Free-text. ✅ |
| C31 | Paid on (commission date) | ✅ | `commission_paid_date` | ✅ (named differently but same field) |
| C32 | PURCHASE PRICE WITHOUT COMMISSION | ✅ | `purchase_price_no_commission` | Auto-computed. ✅ |
| C33 | EXTRA AMOUNT GIVEN TO CUSTOMER | ✅ | `extra_amount` | ✅ |
| C34 | CREDIT USED | ✅ | `credit_used` | ✅ |
| C35 | COMMISSION AMOUNT | ✅ | `commission_amount` | Auto-computed. ✅ |
| C36 | Price With Spare | ✅ | `price_with_spare` | Present as Phase 3 stub. ✅ |
| C37 | Final Price | ✅ | `final_price` | Present as Phase 3 stub. ✅ |
| C38 | Sales Price | ✅ | `sales_price` | Present as Phase 3 stub. ✅ |
| C39 | P&L | ✅ | `p_and_l` | Present as Phase 3 stub. ✅ |
| C40 | Brand | ✅ | `brand` | Auto-filled from product. ✅ |
| C41 | Model (split from C7) | ✅ | Part of `model_id` display | The sheet splits C7 (full name) and C41 (model only). In Odoo this is one field `model_id`. Fine. |
| C42 | RAM | ✅ | `ram` | ⚠️ **Free-text. Should be Selection.** Sheet values: `'4'`, `'0'`, `'#N/A'`. See Section 3. |
| C43 | ROM | ✅ | `rom` | ⚠️ **Free-text. Should be Selection.** Sheet values: `'16'`, `'128'`, `'#N/A'`. See Section 3. |

---

## Summary: What We're Missing or Wrong

### 🔴 Missing Fields (need to add)
| Field | Issue |
|---|---|
| None critically missing | All 43 sheet columns exist in Odoo already |

> The good news: **everything from the sheet is already in the model.** The issues are with field *types* and *values*, not missing fields.

---

### 🟡 Field Type Issues (should be fixed soon)

| Field | Current | Should Be | Sheet Values Seen |
|---|---|---|---|
| `store_name` | Free text | **Selection dropdown** | `UNI_CYB`, `UNI_CBE`, `SAN_HYD` etc. (~25 stores) |
| `payment_status` | Free text | **Selection** | `Paid`, `Partial`, `Pending` |
| `grade` | Free text | **Selection** | `A`, `B`, `C`, `D`, `E` |
| `els_grade` | Free text | **Selection** | `A`, `B`, `C`, `C+`, `D`, `E` |
| `commission_payment_status` | Free text | **Selection** | `Paid`, `Pending`, `NA` |
| `ram` | Free text | **Selection** | `0`, `2`, `4`, `6`, `8`, `12`, `16`, `NA` |
| `rom` | Free text | **Selection** | `16`, `32`, `64`, `128`, `256`, `512`, `NA` |

---

### 🟡 Needs Nikhil's Clarification

| # | Question | Why It Matters |
|---|---|---|
| 1 | **C18: "Receiving and Pickup date"** — are Receiving and Pickup the same event or two separate dates? | If two events: we need to add a `pickup_date` field. If one: current `receiving_date` is correct. |
| 2 | **C25: "Status"** column — Values like `'Downgrade'`, `'Upgrade'`, `'Completed'` don't match procurement status. Is this TRC/grading status? | Our current `status` field has `pending/received/handed_over`. If the sheet's `status` is TRC-related, it belongs in Phase 2 warehouse module. |
| 3 | **GSN Formula** — Sheet example: `GRGUniDDKNYSaur1N`. Our formula: `GRGUNI{imei_last4}{tech4}{serial2}{month1}`. The sheet seems to use IMEI *last 5 chars* and serial without zero-padding. Exact spec needed. | **Critical** — spine of the whole system. |

---

## Who Enters What: Data Entry vs Auto-Calculated

This is the procurement team's workflow — what they type vs what the system computes:

### 📝 Procurement Team Fills In (manual entry):
| Field | Notes |
|---|---|
| Purchase Date | |
| Technician | Defaults to logged-in user |
| Category | Dropdown |
| IMEI | |
| Model | Product lookup |
| Store Name | Dropdown (once fixed) |
| Source Name | Dropdown |
| Price Offered | The key input for all pricing |
| Ave Price | Optional — from source |
| Logistic Charge | Optional |
| Extra Amount | Optional |
| Credit Used | Optional |
| Payment Scenario | Paid / Partial / Credit |
| Payment Date | |
| Payment UTR | |
| GREST Received | Checkbox |
| Receiving Date | When device arrived |
| Handover Date | When handed to warehouse |
| Invoice File | Upload PDF |

### 🤖 Auto-Calculated (no data entry needed):
| Field | Formula |
|---|---|
| Serial Number | Sequential, auto-incremented |
| Reference (PROC-N) | From serial number |
| GSN / Grest Unique Code | `GRG + Source + IMEI_last4 + Tech + Serial + Month` |
| Purchase Month | From purchase_date |
| Payment Month | From payment_date |
| Receiving Month | From receiving_date |
| Handover Month | From handover_date |
| Brand | From product (product_template.brand) |
| RAM | From product (product_template.ram) |
| ROM | From product (product_template.rom) |
| Commission Amount | `price_offered × rate` (12% Unicorn, 10% Trade-In, 0% Cashify) |
| Purchase Price (No Commission) | `price_offered + extra_amount` |
| Total Price | `(price_offered + extra_amount) × (1 + rate) + logistic_charge` |
| Approval Status | Always starts as `pending` |

### 🏭 Filled Later by Other Teams (Phase 2+):
| Field | Who | When |
|---|---|---|
| Grade | Warehouse / TRC team | After device inspection |
| ELS Grade | Warehouse / TRC team | After device inspection |
| Status | Warehouse | After TRC |
| Price With Spare | TRC | During repair costing |
| Final Price | TRC/Accounts | After grading |
| Sales Price | Sales team | At listing |
| P&L | Computed | After sale |
| Commission Payment Status | Accounts | After paying source |
| Commission UTR | Accounts | After paying source |

---

## Recommended Changes (prioritized)

| Priority | Change | Effort |
|---|---|---|
| 🔴 **P1** | Get GSN formula from Nikhil — update `_compute_gsn()` | 30 min once spec received |
| 🟡 **P2** | Convert `store_name` from free text → Selection with ~25 store codes | 1 hour |
| 🟡 **P2** | Convert `payment_status` → Selection: `paid`, `partial`, `pending` | 30 min |
| 🟡 **P2** | Convert `grade` and `els_grade` → Selection: A/B/C/C+/D/E | 30 min |
| 🟡 **P2** | Convert `ram` → Selection, `rom` → Selection | 30 min |
| 🟢 **P3** | Clarify `receiving_date` vs `pickup_date` (Nikhil) | Depends on answer |
| 🟢 **P3** | Clarify `status` column meaning (Nikhil) | Depends on answer |
| 🟢 **P3** | Import `store_names` list from actual sheet data | 1 hour |
| 🟢 **P4** | Import `sample_products.csv` (already prepared) | 30 min |
