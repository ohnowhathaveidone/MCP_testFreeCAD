# 🔍 FreeCAD Model Tree – Naming Standards Audit Report

**Document:** `sample_cabinet.FCStd`
**Structure Type:** Assembly
**Audit Date:** 2025-07-14
**Auditor:** CAD Data Management / Wood Technology QA

---

## ⚠️ Preliminary Note

> **Company dictionary file not found.** This audit is conducted against **general wood-technology CAD naming best practices** (ISO 10303 / internal conventions). Once the company dictionary is restored, re-run this audit for full compliance verification.

---

## 1. Summary of Findings

| Severity | Count | Description |
|----------|-------|-------------|
| 🔴 Critical | 2 | Operation-type prefixes leak into component names |
| 🟡 Warning | 3 | Missing positional / dimensional identifiers |
| 🔵 Info | 1 | Document-level naming inconsistency |

**Overall Compliance Score: 3 / 10**

---

## 2. Node-by-Node Audit

### 2.1 Document Name
| Field | Current | Issue | Proposed |
|-------|---------|-------|----------|
| File | `sample_cabinet.FCStd` | Lowercase; no project/customer code; no revision | `PRJ-2025-001_Cabinet-Carcass_R01.FCStd` |

### 2.2 `Cabinet_Carcass_Part` *(App::Part)*
| Field | Current | Issue | Proposed |
|-------|---------|-------|----------|
| Name | `Cabinet_Carcass_Part` | No part number, no dimensions, no material tag | `CARCASS-001_Cabinet-Carcass_600x450x720_MDF18` |

### 2.3 `Pad_SidePanel_L` *(Part::Pad)* 🔴
| Field | Current | Issue | Proposed |
|-------|---------|-------|----------|
| Name | `Pad_SidePanel_L` | **"Pad_" is a CAD operation, not a component identity.** The body should be named by its *function*, not the extrude command used to create it. | `SP-L_01_SidePanel-Left_18x450x720` |

> **Rule violated:** *Component names must reflect the physical part (function + position + dimensions), never the modelling operation (Pad, Pocket, Fillet, etc.).*

### 2.4 `Pocket_Dado` *(Part::Pocket)* 🔴
| Field | Current | Issue | Proposed |
|-------|---------|-------|----------|
| Name | `Pocket_Dado` | **"Pocket_" is an operation prefix.** Also missing: which panel it belongs to, which dado (top/bottom/back), depth reference, and position along the panel. | `DADO-01_BackDado-10mm-SP-L` |

> **Rule violated:** *Feature names must include: feature-type code → sequence → functional description → parent component reference.*

---

## 3. Proposed Corrected Tree

```
PRJ-2025-001_Cabinet-Carcass_R01.FCStd          ← Assembly
│
└── CARCASS-001_Cabinet-Carcass_600x450x720_MDF18   ← App::Part
    │
    └── SP-L_01_SidePanel-Left_18x450x720            ← Part::Body (was "Pad_SidePanel_L")
        │
        └── DADO-01_BackDado-10mm-SP-L               ← Part::Pocket (was "Pocket_Dado")
```

### Naming Convention Applied
```
<FUNCTION-CODE>_<SEQ>_<Description>_<Dimensions>_<ParentRef>
```
| Token | Meaning | Example |
|-------|---------|---------|
| `SP-L` | Side Panel – Left | Positional code |
| `01` | Sequence / instance number | Distinguishes duplicates |
| `SidePanel-Left` | Human-readable function | Clarity for shop floor |
| `18x450x720` | Thickness × Width × Height (mm) | Stock / cut-list link |
| `MDF18` | Material + thickness | BOM / CNC toolpath |

---

## 4. Recommended Actions

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | **Restore company dictionary file** and re-run audit for full compliance | CAD Admin | 🔴 High |
| 2 | Rename all nodes per §3 above; update linked BOM / cut-list | Designer | 🔴 High |
| 3 | Add a **FreeCAD macro / script** that auto-prefixes new Bodies with `BODY_` and features with `FEAT_` to prevent operation-name leakage | CAD Admin | 🟡 Med |
| 4 | Add **dimension parameters** (Length, Width, Thickness) as spreadsheet-driven properties so names can be auto-generated | Designer | 🟡 Med |
| 5 | Add **material & finish** properties to every `App::Part` for downstream CNC / ERP integration | Designer | 🔵 Low |

---

## 5. Verdict

> **FAIL – 2 critical naming violations detected.**
> The model tree currently embeds **CAD operation names** (`Pad_`, `Pocket_`) into component and feature identifiers, which breaks traceability between the 3D model, the cut-list, and the shop-floor work order. Rename per §3 and re-submit for a **pass** audit.

---
*End of Report – CAD Data Management / Wood Technology QA*