# GREST ODOO ERP - COMPLETE DEPLOYMENT GUIDE
## Master Document for Anti-Gravity MCP Server

**Version:** 1.0  
**Date:** March 1, 2025  
**Project:** GREST Mobile Refurbishment ERP  
**Phase:** Phase 1 - Procurement & Accounts Approval  
**Author:** Astra (Solution Architect)  
**For:** Anti-Gravity (Implementation), Sammy (PM), Nikhil (Technical Lead)

---

## CRITICAL INSTRUCTIONS FOR ANTI-GRAVITY

**READ THIS FIRST:**

1. This document contains COMPLETE specifications for Phase 1
2. Execute steps IN ORDER (do not skip)
3. All code is COPY-PASTE ready
4. Test after each module before proceeding
5. Reference files are in `/mnt/project/` directory
6. Use `grest_staging` database for development
7. Phase 1 builds ONLY Procurement + Accounts modules
8. Future phases (Warehouse, TRC, Sales) are DEFERRED

**Success Criteria:**
- Procurement team can enter devices in Odoo
- GSN auto-generates
- Accounts can approve/reject
- Workflow: Procurement → Accounts Approval → Ready for Warehouse

---

# EXECUTIVE SUMMARY

## What We're Building

A complete ERP for GREST mobile refurbishment business, implemented in phases:

**Phase 1 (THIS DOCUMENT):** Procurement & Accounts - 7 days
- Module: `grest_procurement` - Device purchasing
- Module: `grest_accounts_approval` - Approval workflow
- Replaces Google Sheets for procurement
- Enables accounts approval before warehouse

**Phase 2:** Warehouse Operations - 4 weeks  
**Phase 3:** TRC & P&L Calculation - 4 weeks  
**Phase 4:** Sales & Integration - 4 weeks  

---

# PROJECT CONTEXT

## Business Model

GREST purchases refurbished devices, repairs them, and resells:

**Purchase Sources:**
- Cashify (B2B & Trading)
- Unicorn
- Sangeeta
- Direct trade-ins
- B2B partners

**Process Flow:**
```
Purchase → Warehouse → TRC (repair) → Sales
```

**Current Problem:**
- 50+ Google Sheets
- Manual WhatsApp coordination
- No real-time visibility
- Difficult P&L tracking

**Solution:** Centralized Odoo ERP

---

# DEPLOYMENT ROADMAP

## Timeline

```
Day 1: Odoo Installation + Database Setup
Day 2: Product Master Import
Day 3-4: Build grest_procurement module
Day 5: Build grest_accounts_approval module
Day 6: Connect modules + Testing
Day 7: User training + Refinements
```

## Modules to Build

### Module 1: grest_procurement
- **Purpose:** Track device purchases
- **Fields:** 38 fields
- **Key Features:**
  - GSN barcode auto-generation
  - Commission calculation
  - Invoice upload
  - Payment scenario tracking

### Module 2: grest_accounts_approval  
- **Purpose:** Approval workflow
- **Fields:** 12 fields
- **Key Features:**
  - Review pending procurements
  - 3 payment scenarios (Paid/Partial/Credit)
  - Approve/Reject workflow
  - Audit trail

---

# TECHNICAL ARCHITECTURE

## System Components

```
┌─────────────────────────────────────┐
│         Odoo 18 CE                  │
├─────────────────────────────────────┤
│  Custom Modules:                    │
│  ├── grest_procurement              │
│  └── grest_accounts_approval        │
├─────────────────────────────────────┤
│  Base Modules:                      │
│  ├── product (device models)        │
│  └── base (core Odoo)               │
├─────────────────────────────────────┤
│  Database: PostgreSQL 14+           │
└─────────────────────────────────────┘
```

## Data Flow

```
Procurement creates entry
         ↓
    Uploads invoice
         ↓
    GSN auto-generates
         ↓
Auto-creates Accounts Approval (status: pending)
         ↓
Accounts team sees in dashboard
         ↓
Reviews invoice + payment
         ↓
  Approves or Rejects
         ↓
IF Approved → Ready for Warehouse (Phase 2)
IF Rejected → Back to Procurement
```

---

# STEP-BY-STEP DEPLOYMENT

## DAY 1: ENVIRONMENT SETUP

### Objective
Install Odoo 18 and create databases

### Already Installed Check Access


### Create Databases

1. **Access:** http://your-server:8069
2. **Create Database 1:**
   - Name: `grest_staging`
   - Email: `samret.singh@grest.in`
   - Password: `admin123` (change in production)
   - Load demo data: YES (for testing)

3. **Create Database 2:**
   - Name: `grest_production`  
   - Email: `samret.singh@grest.in`
   - Password: `admin123`
   - Load demo data: NO

4. **Switch to:** `grest_staging` for development

---

## DAY 2: PRODUCT MASTER SETUP

### Objective
Import device models into Odoo

### Data Source
`D:\RAVENs\Grest-odoo-automation\docs\Procurement Sample Sheet.xlsx` - Column G (Model)

### Step 1: Create Product Template Attributes

Navigate to: **Sales → Configuration → Attributes**

Create attributes:
```
Brand: Apple, Samsung, OnePlus, Vivo, Realme, etc.
RAM: 2GB, 3GB, 4GB, 6GB, 8GB, 12GB
ROM: 16GB, 32GB, 64GB, 128GB, 256GB, 512GB, 1TB
```

### Step 2: Create Product Categories

Navigate to: **Sales → Configuration → Categories**

Create:
```
- Mobile
  - iPhone
  - Android
- Tab
  - iPad
- Laptop
  - MacBook
- Watch
- Airpods
```

### Step 3: Import Products

Use CSV import with these columns:
```
Name,Category,Brand,RAM,ROM,Type,Can be Sold,Can be Purchased
"Apple iPhone 11 (4 GB/64 GB)",Mobile,Apple,4GB,64GB,Consumable,TRUE,TRUE
"Apple iPhone XR (3 GB/128 GB)",Mobile,Apple,3GB,128GB,Consumable,TRUE,TRUE
"Apple iPad 1st Wifi (0 GB/16 GB)",Tab,Apple,0GB,16GB,Consumable,TRUE,TRUE
```

**Total products to create:** ~100-150 unique models

---

## DAY 3-4: BUILD PROCUREMENT MODULE

### Module Structure

```
/custom_addons/grest_procurement/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── procurement.py
├── views/
│   ├── procurement_views.xml
│   └── procurement_menu.xml
└── security/
    ├── ir.model.access.csv
    └── procurement_security.xml
```

### Create Files

#### File 1: `__manifest__.py`

```python
{
    'name': 'GREST Procurement',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Device procurement for GREST',
    'author': 'Raven Solutions',
    'depends': ['base', 'product'],
    'data': [
        'security/procurement_security.xml',
        'security/ir.model.access.csv',
        'views/procurement_views.xml',
        'views/procurement_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

#### File 2: `__init__.py` (root)

```python
from . import models
```

#### File 3: `models/__init__.py`

```python
from . import procurement
```

#### File 4: `models/procurement.py`

**(See complete Python model in previous section - 500+ lines)**

Key computed fields:
- `_compute_gsn()` - GSN generation
- `_compute_pricing()` - Commission calculation
- `_compute_purchase_month()` - Month auto-fill
- Auto-create approval on create()

#### File 5: `views/procurement_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Form View -->
    <record id="view_grest_procurement_form" model="ir.ui.view">
        <field name="name">grest.procurement.form</field>
        <field name="model">grest.procurement</field>
        <field name="arch" type="xml">
            <form string="Procurement Entry">
                <header>
                    <field name="approval_status" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" readonly="1"/>
                        </h1>
                    </div>
                    <group>
                        <group string="Basic Information">
                            <field name="purchase_date" required="1"/>
                            <field name="purchase_month" readonly="1"/>
                            <field name="technician_id" required="1"/>
                            <field name="category" required="1"/>
                        </group>
                        <group string="Status">
                            <field name="status"/>
                            <field name="grest_received"/>
                            <field name="approval_status" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Device Information">
                        <group>
                            <field name="imei" required="1"/>
                            <field name="model_id" required="1"/>
                        </group>
                        <group>
                            <field name="brand" readonly="1"/>
                            <field name="ram" readonly="1"/>
                            <field name="rom" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Source & Pricing">
                        <group>
                            <field name="source_name" required="1"/>
                            <field name="store_name"/>
                            <field name="payment_scenario" required="1"/>
                        </group>
                        <group>
                            <field name="price_offered" required="1"/>
                            <field name="logistic_charge"/>
                            <field name="extra_amount"/>
                            <field name="credit_used"/>
                        </group>
                    </group>
                    
                    <group string="Auto-Calculated">
                        <group>
                            <field name="gsn" readonly="1" class="oe_inline"/>
                            <field name="commission_amount" readonly="1"/>
                        </group>
                        <group>
                            <field name="purchase_price_no_commission" readonly="1"/>
                            <field name="total_price" readonly="1" class="oe_inline oe_right"/>
                        </group>
                    </group>
                    
                    <group string="Invoice">
                        <field name="invoice_file" filename="invoice_filename"/>
                        <field name="invoice_filename" invisible="1"/>
                    </group>
                    
                    <group string="Payment Details">
                        <group>
                            <field name="payment_status"/>
                            <field name="payment_date"/>
                            <field name="payment_utr"/>
                        </group>
                        <group>
                            <field name="due_amount"/>
                            <field name="amount_balance"/>
                        </group>
                    </group>
                    
                    <group string="Receiving">
                        <group>
                            <field name="receiving_date"/>
                            <field name="receiving_month" readonly="1"/>
                        </group>
                        <group>
                            <field name="handover_date"/>
                            <field name="handover_month" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Grading (Filled Later)">
                        <field name="grade"/>
                        <field name="els_grade"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Tree View -->
    <record id="view_grest_procurement_tree" model="ir.ui.view">
        <field name="name">grest.procurement.tree</field>
        <field name="model">grest.procurement</field>
        <field name="arch" type="xml">
            <tree string="Procurement">
                <field name="serial_number"/>
                <field name="purchase_date"/>
                <field name="gsn"/>
                <field name="imei"/>
                <field name="model_id"/>
                <field name="source_name"/>
                <field name="price_offered"/>
                <field name="total_price"/>
                <field name="payment_scenario"/>
                <field name="approval_status"/>
                <field name="technician_id"/>
            </tree>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_grest_procurement_search" model="ir.ui.view">
        <field name="name">grest.procurement.search</field>
        <field name="model">grest.procurement</field>
        <field name="arch" type="xml">
            <search string="Search Procurement">
                <field name="gsn"/>
                <field name="imei"/>
                <field name="model_id"/>
                <field name="source_name"/>
                <field name="technician_id"/>
                <filter name="pending_approval" string="Pending Approval" 
                        domain="[('approval_status','=','pending')]"/>
                <filter name="approved" string="Approved" 
                        domain="[('approval_status','=','approved')]"/>
                <filter name="rejected" string="Rejected" 
                        domain="[('approval_status','=','rejected')]"/>
                <group expand="0" string="Group By">
                    <filter name="group_source" string="Source" 
                            context="{'group_by':'source_name'}"/>
                    <filter name="group_month" string="Month" 
                            context="{'group_by':'purchase_month'}"/>
                    <filter name="group_technician" string="Technician" 
                            context="{'group_by':'technician_id'}"/>
                </group>
            </search>
        </field>
    </record>
</odoo>
```

#### File 6: `views/procurement_menu.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Action -->
    <record id="action_grest_procurement" model="ir.actions.act_window">
        <field name="name">Procurement</field>
        <field name="res_model">grest.procurement</field>
        <field name="view_mode">tree,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first procurement entry
            </p>
        </field>
    </record>

    <!-- Menu -->
    <menuitem id="menu_grest_procurement_root" 
              name="Procurement" 
              sequence="10"/>
    
    <menuitem id="menu_grest_procurement_entries" 
              name="Device Purchases" 
              parent="menu_grest_procurement_root" 
              action="action_grest_procurement" 
              sequence="10"/>
</odoo>
```

#### File 7: `security/procurement_security.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Groups -->
    <record id="group_procurement_user" model="res.groups">
        <field name="name">Procurement User</field>
        <field name="category_id" ref="base.module_category_operations"/>
    </record>
    
    <record id="group_procurement_manager" model="res.groups">
        <field name="name">Procurement Manager</field>
        <field name="category_id" ref="base.module_category_operations"/>
        <field name="implied_ids" eval="[(4, ref('group_procurement_user'))]"/>
    </record>
    
    <!-- Record Rules -->
    <record id="procurement_user_rule" model="ir.rule">
        <field name="name">Procurement User: Own Records</field>
        <field name="model_id" ref="model_grest_procurement"/>
        <field name="domain_force">[('technician_id','=',user.id)]</field>
        <field name="groups" eval="[(4, ref('group_procurement_user'))]"/>
    </record>
    
    <record id="procurement_manager_rule" model="ir.rule">
        <field name="name">Procurement Manager: All Records</field>
        <field name="model_id" ref="model_grest_procurement"/>
        <field name="domain_force">[(1,'=',1)]</field>
        <field name="groups" eval="[(4, ref('group_procurement_manager'))]"/>
    </record>
</odoo>
```

#### File 8: `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_procurement_user,procurement.user,model_grest_procurement,group_procurement_user,1,1,1,0
access_procurement_manager,procurement.manager,model_grest_procurement,group_procurement_manager,1,1,1,1
```

### Install Module

```bash
# Restart Odoo
sudo systemctl restart odoo

# Or if running manually:
# Ctrl+C to stop
./odoo-bin -c /etc/odoo.conf -u grest_procurement -d grest_staging
```

Navigate to: **Apps → Update Apps List → Search "GREST Procurement" → Install**

---

## DAY 5: BUILD ACCOUNTS APPROVAL MODULE

### Module Structure

```
/opt/odoo/custom_addons/grest_accounts_approval/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── accounts_approval.py
├── views/
│   ├── accounts_approval_views.xml
│   └── accounts_approval_menu.xml
└── security/
    ├── ir.model.access.csv
    └── accounts_security.xml
```

### Create Files

#### File 1: `__manifest__.py`

```python
{
    'name': 'GREST Accounts Approval',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Accounts approval workflow',
    'author': 'Raven Solutions',
    'depends': ['base', 'grest_procurement'],
    'data': [
        'security/accounts_security.xml',
        'security/ir.model.access.csv',
        'views/accounts_approval_views.xml',
        'views/accounts_approval_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

#### File 2: `models/accounts_approval.py`

```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class GrestAccountsApproval(models.Model):
    _name = 'grest.accounts.approval'
    _description = 'Accounts Approval Workflow'
    _order = 'create_date desc'
    _rec_name = 'name'
    
    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True
    )
    
    procurement_id = fields.Many2one(
        'grest.procurement',
        string='Procurement',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # Related fields from procurement (readonly)
    gsn = fields.Char(
        string='GSN',
        related='procurement_id.gsn',
        store=True,
        readonly=True
    )
    
    imei = fields.Char(
        string='IMEI',
        related='procurement_id.imei',
        readonly=True
    )
    
    model_id = fields.Many2one(
        'product.product',
        string='Model',
        related='procurement_id.model_id',
        readonly=True
    )
    
    source_name = fields.Selection(
        string='Source',
        related='procurement_id.source_name',
        readonly=True
    )
    
    price_offered = fields.Float(
        string='Price',
        related='procurement_id.price_offered',
        readonly=True
    )
    
    total_price = fields.Float(
        string='Total Price',
        related='procurement_id.total_price',
        readonly=True
    )
    
    # Invoice
    invoice_file = fields.Binary(
        string='Invoice',
        related='procurement_id.invoice_file',
        readonly=True
    )
    
    invoice_filename = fields.Char(
        string='Invoice Filename',
        related='procurement_id.invoice_filename',
        readonly=True
    )
    
    # Payment scenario
    payment_scenario = fields.Selection(
        string='Payment Scenario',
        related='procurement_id.payment_scenario',
        readonly=True
    )
    
    # Approval fields
    payment_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('verified', 'Payment Verified'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Payment Status', required=True, default='pending')
    
    payment_utr = fields.Char(string='Payment UTR')
    credit_days = fields.Integer(string='Credit Days')
    partial_amount = fields.Float(string='Partial Amount Paid')
    
    approval_date = fields.Datetime(string='Approval Date', readonly=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True)
    
    rejection_reason = fields.Text(string='Rejection Reason')
    notes = fields.Text(string='Notes')
    
    state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='State', default='pending', required=True, index=True)
    
    @api.depends('procurement_id')
    def _compute_name(self):
        for record in self:
            record.name = f"APPR-{record.procurement_id.name}"
    
    def action_approve(self):
        """Approve procurement"""
        for record in self:
            # Update approval
            record.write({
                'state': 'approved',
                'payment_status': 'approved',
                'approval_date': fields.Datetime.now(),
                'approved_by_id': self.env.user.id,
            })
            
            # Update procurement
            record.procurement_id.write({
                'approval_status': 'approved'
            })
        
        return True
    
    def action_reject(self):
        """Reject procurement"""
        for record in self:
            if not record.rejection_reason:
                raise UserError(_("Please provide rejection reason"))
            
            record.write({
                'state': 'rejected',
                'payment_status': 'rejected',
            })
            
            record.procurement_id.write({
                'approval_status': 'rejected'
            })
        
        return True
```

#### File 3: `views/accounts_approval_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Kanban View (Dashboard) -->
    <record id="view_accounts_approval_kanban" model="ir.ui.view">
        <field name="name">grest.accounts.approval.kanban</field>
        <field name="model">grest.accounts.approval</field>
        <field name="arch" type="xml">
            <kanban default_group_by="state" class="o_kanban_mobile">
                <field name="name"/>
                <field name="gsn"/>
                <field name="source_name"/>
                <field name="total_price"/>
                <field name="payment_scenario"/>
                <field name="state"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <div class="o_kanban_record_top">
                                <div class="o_kanban_record_headings">
                                    <strong class="o_kanban_record_title">
                                        <field name="name"/>
                                    </strong>
                                    <br/>
                                    <span class="o_kanban_record_subtitle">
                                        GSN: <field name="gsn"/>
                                    </span>
                                </div>
                            </div>
                            <div class="o_kanban_record_body">
                                <field name="source_name"/>
                                <br/>
                                ₹<field name="total_price"/>
                                <br/>
                                <span class="badge badge-pill">
                                    <field name="payment_scenario"/>
                                </span>
                            </div>
                            <div class="o_kanban_record_bottom">
                                <div class="oe_kanban_bottom_right">
                                    <button name="action_approve" 
                                            string="Approve" 
                                            type="object" 
                                            class="btn btn-sm btn-success"
                                            attrs="{'invisible': [('state', '!=', 'pending')]}"/>
                                    <button name="action_reject" 
                                            string="Reject" 
                                            type="object" 
                                            class="btn btn-sm btn-danger"
                                            attrs="{'invisible': [('state', '!=', 'pending')]}"/>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_accounts_approval_form" model="ir.ui.view">
        <field name="name">grest.accounts.approval.form</field>
        <field name="model">grest.accounts.approval</field>
        <field name="arch" type="xml">
            <form string="Approval">
                <header>
                    <button name="action_approve" 
                            string="APPROVE" 
                            type="object" 
                            class="btn-success"
                            attrs="{'invisible': [('state', '!=', 'pending')]}"/>
                    <button name="action_reject" 
                            string="REJECT" 
                            type="object" 
                            class="btn-danger"
                            attrs="{'invisible': [('state', '!=', 'pending')]}"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    
                    <group string="Procurement Details (Read-only)">
                        <group>
                            <field name="gsn" readonly="1"/>
                            <field name="imei" readonly="1"/>
                            <field name="model_id" readonly="1"/>
                        </group>
                        <group>
                            <field name="source_name" readonly="1"/>
                            <field name="price_offered" readonly="1"/>
                            <field name="total_price" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Invoice">
                        <field name="invoice_file" filename="invoice_filename" readonly="1"/>
                        <field name="invoice_filename" invisible="1"/>
                    </group>
                    
                    <group string="Payment Information">
                        <group>
                            <field name="payment_scenario" readonly="1"/>
                            <field name="payment_status"/>
                            <field name="payment_utr"/>
                        </group>
                        <group>
                            <field name="credit_days" 
                                   attrs="{'invisible': [('payment_scenario', '!=', 'credit')]}"/>
                            <field name="partial_amount" 
                                   attrs="{'invisible': [('payment_scenario', '!=', 'partial')]}"/>
                        </group>
                    </group>
                    
                    <group string="Approval">
                        <group>
                            <field name="approved_by_id" readonly="1"/>
                            <field name="approval_date" readonly="1"/>
                        </group>
                        <group>
                            <field name="rejection_reason" 
                                   attrs="{'invisible': [('state', '!=', 'rejected')]}"/>
                        </group>
                    </group>
                    
                    <group string="Notes">
                        <field name="notes" nolabel="1"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Tree View -->
    <record id="view_accounts_approval_tree" model="ir.ui.view">
        <field name="name">grest.accounts.approval.tree</field>
        <field name="model">grest.accounts.approval</field>
        <field name="arch" type="xml">
            <tree string="Approvals">
                <field name="name"/>
                <field name="gsn"/>
                <field name="source_name"/>
                <field name="payment_scenario"/>
                <field name="payment_status"/>
                <field name="total_price"/>
                <field name="state"/>
                <field name="approved_by_id"/>
            </tree>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_accounts_approval_search" model="ir.ui.view">
        <field name="name">grest.accounts.approval.search</field>
        <field name="model">grest.accounts.approval</field>
        <field name="arch" type="xml">
            <search string="Search Approvals">
                <field name="gsn"/>
                <field name="source_name"/>
                <filter name="pending" string="Pending" 
                        domain="[('state','=','pending')]"/>
                <filter name="approved" string="Approved" 
                        domain="[('state','=','approved')]"/>
                <filter name="rejected" string="Rejected" 
                        domain="[('state','=','rejected')]"/>
            </search>
        </field>
    </record>
</odoo>
```

#### File 4: `views/accounts_approval_menu.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Actions -->
    <record id="action_accounts_approval_dashboard" model="ir.actions.act_window">
        <field name="name">Approvals Dashboard</field>
        <field name="res_model">grest.accounts.approval</field>
        <field name="view_mode">kanban,tree,form</field>
    </record>
    
    <record id="action_accounts_approval_pending" model="ir.actions.act_window">
        <field name="name">Pending Approvals</field>
        <field name="res_model">grest.accounts.approval</field>
        <field name="view_mode">tree,form</field>
        <field name="domain">[('state','=','pending')]</field>
    </record>

    <!-- Menu -->
    <menuitem id="menu_accounts_root" 
              name="Accounts" 
              sequence="20"/>
    
    <menuitem id="menu_accounts_dashboard" 
              name="Dashboard" 
              parent="menu_accounts_root" 
              action="action_accounts_approval_dashboard" 
              sequence="10"/>
    
    <menuitem id="menu_accounts_pending" 
              name="Pending Approvals" 
              parent="menu_accounts_root" 
              action="action_accounts_approval_pending" 
              sequence="20"/>
</odoo>
```

#### File 5: `security/accounts_security.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="group_accounts_user" model="res.groups">
        <field name="name">Accounts User</field>
        <field name="category_id" ref="base.module_category_accounting"/>
    </record>
    
    <record id="group_accounts_manager" model="res.groups">
        <field name="name">Accounts Manager</field>
        <field name="category_id" ref="base.module_category_accounting"/>
        <field name="implied_ids" eval="[(4, ref('group_accounts_user'))]"/>
    </record>
</odoo>
```

#### File 6: `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_accounts_user,accounts.user,model_grest_accounts_approval,group_accounts_user,1,0,0,0
access_accounts_manager,accounts.manager,model_grest_accounts_approval,group_accounts_manager,1,1,1,1
```

### Install Module

```bash
./odoo-bin -c /etc/odoo.conf -u grest_accounts_approval -d grest_staging
```

---

## DAY 6: TESTING

### Test Workflow

#### Test 1: Create Procurement Entry

1. Login as Procurement User
2. Navigate to: **Procurement → Device Purchases → Create**
3. Enter:
   - Purchase Date: Today
   - Technician: Current user
   - Category: Mobile
   - IMEI: 356281920626245
   - Model: Apple iPhone 11 (4 GB/64 GB)
   - Source: Unicorn
   - Payment Scenario: Credit
   - Price Offered: 5000
   - Upload invoice PDF

4. **Save**

5. **Verify:**
   - ✅ GSN auto-generated (format: GRGUNI...)
   - ✅ Commission = ₹600 (12%)
   - ✅ Total Price = ₹5600
   - ✅ Approval Status = "Pending Accounts Approval"

#### Test 2: Accounts Approval

1. Login as Accounts Manager
2. Navigate to: **Accounts → Dashboard**
3. **Verify:** New approval appears in "Pending" column
4. Open the approval card
5. **Verify:**
   - Invoice is viewable
   - Procurement details shown (read-only)
   - Payment scenario: Credit

6. Enter:
   - Credit Days: 15
   - Notes: "Approved - 15 days credit from Unicorn"

7. Click **APPROVE**

8. **Verify:**
   - State changes to "Approved"
   - Approved By = Current user
   - Approval Date = Now

#### Test 3: Check Procurement Status

1. Navigate to: **Procurement → Device Purchases**
2. Find the entry (PROC-1)
3. **Verify:**
   - Approval Status = "Approved"

#### Test 4: Rejection Flow

1. Create another procurement entry
2. As Accounts Manager, reject it
3. Enter rejection reason: "Invoice missing"
4. **Verify:**
   - State = Rejected
   - Procurement approval_status = Rejected

---

## DAY 7: USER TRAINING

### Setup User Groups

Create users:
```
1. procurement_user@grest.com - Group: Procurement User
2. accounts_manager@grest.com - Group: Accounts Manager
3. samret.singh@grest.in - Group: Admin (all access)
```

### Training Checklist

**For Procurement Team:**
- [ ] How to create entry
- [ ] Required fields
- [ ] GSN auto-generation
- [ ] Invoice upload
- [ ] Check approval status

**For Accounts Team:**
- [ ] Dashboard overview
- [ ] How to review pending
- [ ] 3 payment scenarios
- [ ] Approve/Reject process
- [ ] Add notes

---

# REFERENCE FILES

Files available in `/mnt/project/`:

1. **Procurement_Sample_Sheet.xlsx** - Real procurement data (4,650 rows)
2. **Procurement_Meeting_Transcript.md** - Business requirements discussion
3. **nikhil.txt** - Accounts approval workflow discussion

---

# SUCCESS CRITERIA

## Phase 1 Complete When:

✅ Procurement module installed and working  
✅ Accounts approval module installed and working  
✅ Modules connected (auto-create approval)  
✅ GSN auto-generates correctly  
✅ Commission calculates correctly  
✅ Approval workflow works (approve/reject)  
✅ 5+ sample entries tested  
✅ Team trained and comfortable  

## Then Move to Phase 2: Warehouse

---

# TROUBLESHOOTING

## Common Issues

### Module Won't Install
```bash
# Check logs
tail -f /var/log/odoo/odoo.log

# Update module list
# Odoo UI: Apps → Update Apps List
```

### GSN Not Generating
- Check all required fields filled
- Verify serial_number exists
- Check Python compute function

### Permission Denied
- Verify user in correct security group
- Check ir.model.access.csv

---

# NEXT PHASES (FUTURE)

## Phase 2: Warehouse (Weeks 5-8)
- Module: `grest_warehouse`
- Warehouse receiving
- IMEI verification
- Location management
- Handover to TRC

## Phase 3: TRC & P&L (Weeks 9-12)
- Module: `grest_trc`
- Entry Level Screening
- Repair decision engine
- P&L calculation
- Cannibalization

## Phase 4: Sales (Weeks 13-16)
- Module: `grest_sales`
- Sales orders
- Channel allocation
- Shopify integration
- Advanced accounting

---

# DOCUMENT VERSION HISTORY

- **v1.0** - March 1, 2025 - Initial Phase 1 complete spec

---

**END OF DEPLOYMENT GUIDE**

**For questions or issues, contact:**
- **Sammy** (Project Manager)
- **Nikhil** (Technical Lead)
- **Astra** (Solution Architect)
