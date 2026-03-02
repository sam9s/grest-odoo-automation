# Questions for Nikhil — GREST ERP Meeting
**Date:** 2 March 2026  
**Prepared by:** Antigravity (Developer)  
**For:** Nikhil (Technical / Warehouse Lead)

---

> These are the **blocking questions** that affect the Odoo build. Cannot finalize Phase 1 or plan Phase 2 without these answers.

---

## 🔴 CRITICAL — GSN Barcode Formula

**Current (temporary) formula:**
```
GRG + Source(3-char) + IMEI(last 4 digits) + Tech(first 4 chars) + Serial(2-digit) + Month(first char)
Example: GRGUNI6245MITC01M
```

**Real example from your sheet:**
```
GRGAmp00976Aman71J
GRGUni5TA7MSaur4N
GRGUniDDKNYSaur1N
```

Looking at these examples:
- `GRG` = fixed prefix ✅
- `Amp` / `Uni` = source code (3 chars) ✅ 
- `00976` = looks like **5 digits**, not 4 — or is this a serial/record number?
- `Aman` / `Saur` = technician code (4 chars) ✅
- `71` / `4` / `1` = serial number (variable digits, not zero-padded?)
- `J` / `N` = month first char ✅

**Questions:**
1. What exactly is the middle number? (`00976`, `5TA7M`, `DDKNY`) — is it IMEI digits, a device-specific ID, or something else?
2. Is the serial number zero-padded to 2 digits or just the raw number?
3. Who generates the GSN — Odoo auto-generates it, or does the warehouse team stamp it manually?
4. Will the formula change for different categories (Mobile vs Laptop vs Tab)?

---

## 🔴 CRITICAL — "Status" Column (C25) Meaning

**Sheet values:** `Downgrade`, `Upgrade`, `Same Grade`

This looks like a **comparison between the device's condition grade and what was expected/advertised**.

**Questions:**
1. Is `Status` comparing the advertised grade vs actual received grade? (e.g., sold as Grade A but arrived as Grade B = "Downgrade")
2. Who fills this — the warehouse/TRC team after inspection?
3. Does this affect payment (e.g., if "Downgrade", do you pay less)?
4. Should this be in the **Procurement module** (Phase 1) or the **Warehouse/TRC module** (Phase 2)?

---

## 🟡 IMPORTANT — "Receiving and Pickup date" (C18) — One Column or Two?

**Current sheet:** Single column called "Receiving and Pickup date"

**Question:**
1. Are "Receiving" (device arrives at GREST) and "Pickup" (someone picks it from the source) the **same event** or **two separate events**?
2. If two events: should they have separate date fields in Odoo?
3. Example from data: Purchase date = 11 Nov, Receiving date = 17 Nov — is the 17th the day it arrived at GREST warehouse, or the day the technician picked it up from the store?

---

## 🟡 IMPORTANT — Commission Logic Confirmation

**Current implementation:**
| Source | Commission Rate |
|---|---|
| Unicorn | 12% |
| Sangeetha | 12% |
| Cashify | 0% |
| Ample | 12% |
| Bhagwati | 12% |
| Reliance Digital | 12% |
| Others | 12% |
| Trade-In | 10% |

**Questions:**
1. Are these rates correct?
2. Does commission apply to ALL sources or only some?
3. For Cashify — is it always 0% or is it variable (the sheet has no commission data for Cashify rows)?
4. Is commission calculated on `price_offered` only, or `price_offered + extra_amount`?

---

## 🟡 IMPORTANT — Phase 2 Warehouse Scope

**Questions to kick off Phase 2 planning:**
1. After accounts approves a procurement, what happens next in the warehouse? Walk me through the physical steps.
2. What is TRC (Technical Report Card)? What fields does it need?
3. Who assigns the device to a technician for repair?
4. How does **grading** work? Is Grade (A/B/C/D/E) assigned by the technician after inspection?
5. What is **ELS grade** vs regular **Grade**? Are they set by different people?
6. At what point is the device considered "ready for sale"?

---

## 🟢 NICE TO HAVE

1. Should store names be fixed (our current list of 20), or do new stores get added regularly? If they can change, should it be a separate master table (Odoo Many2one) rather than a hardcoded dropdown?
2. Same question for **Technicians** — currently a dropdown from `res.users` (Odoo user accounts). Should all 24 technicians have Odoo login accounts, or should it be a separate "Technicians" master table?
3. Is "Pencil" in the Category referring to Apple Pencil? Should it be renamed?
4. What does "iMac" in Category mean — are you procuring iMacs too?
