# FreeCAD Model Tree Naming Audit

**Document:** `mount_trispector_to_kuka`  
**Structure type:** Multi-Object  
**Audit basis:** Company dictionary file was not found.  
**Audit status:** **Provisional generic CAD naming audit** — cannot validate against official company naming standards.

---

## 1. Executive Summary

The model contains **1 root object** and **20 child features**.

### Major findings

| Finding | Count | Severity |
|---|---:|---|
| Auto-generated / anonymous internal names | 20 child features + root `Body` | High |
| Labels requiring normalization | 20 child features | Medium |
| Missing feature-type prefix in labels | Most pockets, mirror, chamfer | Medium |
| Inconsistent casing: lowercase, camelCase, ALL CAPS | Multiple | Medium |
| Abbreviations or ambiguous terms: `mirr`, `Trispec`, `2` | Multiple | Medium |
| Missing dimensions or position descriptors | Most features | Medium |
| Document name casing inconsistent with component names | 1 | Low |

### Overall assessment

The model is **not compliant** with a strict standardized naming convention because most internal names are anonymous and most labels lack consistent feature-type, function, position, and dimension information.

Because the company dictionary is unavailable, the proposed names below are **provisional** and should be reviewed against the official company standard when available.

---

## 2. Audit Limitations

The following limitations apply:

1. **Company dictionary unavailable**  
   The official company naming dictionary could not be loaded, so exact compliance cannot be confirmed.

2. **Exact XY position not provided**  
   The tree provides bounding-box lengths, but not exact feature coordinates. Position descriptors such as `Center`, `Outer`, `Base`, and `Washer` are inferred from labels and feature extents.

3. **Pocket bounding boxes may reflect full body extents**  
   Several pockets report a bounding box of `220 x 100 x 30`, which appears to be the full body extent. For naming purposes, the associated sketch footprint is used where available.

4. **Feature depth not explicitly provided**  
   Through-hole status is inferred only where the label explicitly says `throughholes`.

---

## 3. Proposed Provisional Naming Convention

Because no company dictionary is available, the following generic convention is proposed:

```text
<FeatureType>_<Function>_<Position>_<Size>
```

### Examples

```text
Sketch_BasePlate_220x100
Pad_BasePlate_220x100x30
Pocket_KukaMountThroughHoles_160x90
Pocket_KukaMountWasherSink_168x98
Mirror_ReliefOuter_220x20
Chamfer_PrintBase_220x100
```

### Recommended rules

| Rule | Recommendation |
|---|---|
| Feature type prefix | Use `Sketch`, `Pad`, `Pocket`, `Mirror`, `Chamfer`, `Body` |
| Function | Use clear function names: `BasePlate`, `KukaMount`, `TrispectorMount`, `MassRelief`, `Cutaway` |
| Position | Use `Center`, `Outer`, `Base`, `Washer`, `Through` where applicable |
| Dimensions | Use `LxW` for sketches and `LxWxH` for solids |
| Casing | Use PascalCase words separated by underscores |
| Abbreviations | Avoid `mirr`, `Trispec`, `2`; use `Mirror`, `Trispector`, `to` |
| Internal names | Use lowercase snake_case if internal names must be machine-safe |

---

## 4. Document and Root Object Audit

| Item | Current name / label | Type | Extents | Issue | Proposed standardized label | Proposed internal name |
|---|---|---|---:|---|---|---|
| Document | `mount_trispector_to_kuka` | FreeCAD Document | N/A | Lowercase; inconsistent casing for `KUKA` and `Trispector` | `Mount_Trispector_to_KUKA` | `mount_trispector_to_kuka` |
| Root object | `Body` / `Body` | `PartDesign::Body` | `220 x 100 x 30` | Generic default name; lacks function and dimensions | `Body_Mount_Trispector_to_KUKA_220x100x30` | `body_mount_trispector_to_kuka` |

### Structural note

The structure is reported as **Multi-Object**, but only one root object is present: `Body`. If this is intended to be a multi-body assembly or multi-component model, verify whether additional bodies or components are missing.

---

## 5. Anonymous Internal Name Summary

All child features currently use auto-generated internal names.

| Feature type | Count | Examples |
|---|---:|---|
| Sketches | 9 | `Sketch`, `Sketch001`, `Sketch002` |
| Pockets | 8 | `Pocket`, `Pocket001`, `Pocket002` |
| Pad | 1 | `Pad` |
| Mirror | 1 | `Mirrored` |
| Chamfer | 1 | `Chamfer` |
| **Total child features** | **20** | — |

The root object `Body` also uses a generic default internal name.

---

## 6. Child Feature Audit and Proposed Standardized Names

| # | Current name / label | Type | Footprint / extents | Issue | Proposed standardized label | Proposed internal name |
|---:|---|---|---:|---|---|---|
| 1 | `Sketch` / `Sketch` | Sketch | `220 x 100` | Anonymous internal name; label lacks function and dimensions | `Sketch_BasePlate_220x100` | `sketch_base_plate_220x100` |
| 2 | `Pad` / `BASE` | Pad | `220 x 100 x 30` | Auto-generated internal name; ALL CAPS label; lacks feature-type prefix and dimensions | `Pad_BasePlate_220x100x30` | `pad_base_plate_220x100x30` |
| 3 | `Sketch001` / `sketch_mount2KUKA` | Sketch | `160 x 90` | Auto-numbered; lowercase; uses `2` instead of `to`; lacks dimensions | `Sketch_KukaMountPattern_160x90` | `sketch_kuka_mount_pattern_160x90` |
| 4 | `Pocket` / `mount2KUKA_throughholes` | Pocket | `160 x 90 through` | Auto-generated internal name; no feature-type prefix; inconsistent casing; lacks dimensions | `Pocket_KukaMountThroughHoles_160x90` | `pocket_kuka_mount_through_holes_160x90` |
| 5 | `Sketch002` / `sketch_mount2KUKA_washers` | Sketch | `168 x 98` | Auto-numbered; lowercase; uses `2`; lacks dimensions | `Sketch_KukaMountWasherPattern_168x98` | `sketch_kuka_mount_washer_pattern_168x98` |
| 6 | `Pocket001` / `mount2KUKA_washersSink` | Pocket | `168 x 98 sink` | Auto-numbered; no feature-type prefix; inconsistent casing; lacks dimensions | `Pocket_KukaMountWasherSink_168x98` | `pocket_kuka_mount_washer_sink_168x98` |
| 7 | `Sketch003` / `sketch_mount2trispector` | Sketch | `101 x 52` | Auto-numbered; lowercase; uses `2`; lacks dimensions | `Sketch_TrispectorMountPattern_101x52` | `sketch_trispector_mount_pattern_101x52` |
| 8 | `Pocket002` / `mount2Trispector` | Pocket | `101 x 52` | Auto-numbered; no feature-type prefix; inconsistent casing; lacks dimensions | `Pocket_TrispectorMount_101x52` | `pocket_trispector_mount_101x52` |
| 9 | `Sketch004` / `sketch_mount2Trispector_washers` | Sketch | `105 x 56` | Auto-numbered; lowercase; uses `2`; lacks dimensions | `Sketch_TrispectorMountWasherPattern_105x56` | `sketch_trispector_mount_washer_pattern_105x56` |
| 10 | `Pocket003` / `mount2Trispector_washers` | Pocket | `105 x 56 sink` | Auto-numbered; no feature-type prefix; inconsistent casing; lacks dimensions | `Pocket_TrispectorMountWasherSink_105x56` | `pocket_trispector_mount_washer_sink_105x56` |
| 11 | `Sketch005` / `sketch_reliefTrispector` | Sketch | `220 x 30` | Auto-numbered; camelCase; unclear function; lacks dimensions | `Sketch_ReliefCenter_220x30` | `sketch_relief_center_220x30` |
| 12 | `Pocket004` / `relief_center` | Pocket | `220 x 30` | Auto-numbered; no feature-type prefix; lacks dimensions | `Pocket_ReliefCenter_220x30` | `pocket_relief_center_220x30` |
| 13 | `Sketch006` / `sketch_relief_outer` | Sketch | `220 x 20` | Auto-numbered; lowercase; lacks dimensions | `Sketch_ReliefOuter_220x20` | `sketch_relief_outer_220x20` |
| 14 | `Pocket005` / `relief_outer_base` | Pocket | `220 x 20` | Auto-numbered; no feature-type prefix; lacks dimensions | `Pocket_ReliefOuterBase_220x20` | `pocket_relief_outer_base_220x20` |
| 15 | `Mirrored` / `relief_outer_mirr` | Mirror | `220 x 20 mirrored` | Abbreviation `mirr`; no feature-type prefix; lacks dimensions | `Mirror_ReliefOuter_220x20` | `mirror_relief_outer_220x20` |
| 16 | `Sketch007` / `sketch_massRelief` | Sketch | `190 x 65` | Auto-numbered; camelCase; lacks dimensions | `Sketch_MassRelief_190x65` | `sketch_mass_relief_190x65` |
| 17 | `Pocket006` / `massRelief` | Pocket | `190 x 65` | Auto-numbered; no feature-type prefix; lacks dimensions | `Pocket_MassRelief_190x65` | `pocket_mass_relief_190x65` |
| 18 | `Sketch008` / `sketch_cutAway_TrispecMount` | Sketch | `190 x 60` | Auto-numbered; inconsistent casing; abbreviation `Trispec`; lacks dimensions | `Sketch_Cutaway_TrispectorMount_190x60` | `sketch_cutaway_trispector_mount_190x60` |
| 19 | `Pocket007` / `cutAway_trispecMount` | Pocket | `190 x 60` | Auto-numbered; no feature-type prefix; abbreviation `Trispec`; lacks dimensions | `Pocket_Cutaway_TrispectorMount_190x60` | `pocket_cutaway_trispector_mount_190x60` |
| 20 | `Chamfer` / `printBaseChamfer` | Chamfer | `220 x 100 base edges` | Auto-generated internal name; camelCase; no feature-type prefix; lacks dimensions | `Chamfer_PrintBase_220x100` | `chamfer_print_base_220x100` |

---

## 7. Poorly Named Label Categories

### 7.1 Anonymous or auto-numbered internal names

These internal names provide no engineering meaning:

```text
Sketch
Pad
Sketch001
Pocket
Sketch002
Pocket001
Sketch003
Pocket002
Sketch004
Pocket003
Sketch005
Pocket004
Sketch006
Pocket005
Mirrored
Sketch007
Pocket006
Sketch008
Pocket007
Chamfer
```

### 7.2 Inconsistent casing

Examples:

```text
BASE
sketch_mount2KUKA
mount2KUKA_throughholes
sketch_mount2trispector
mount2Trispector
sketch_massRelief
massRelief
sketch_cutAway_TrispecMount
cutAway_trispecMount
printBaseChamfer
```

### 7.3 Abbreviations and ambiguous terms

| Current term | Recommended replacement |
|---|---|
| `mirr` | `Mirror` |
| `Trispec` | `Trispector` |
| `2` | `to` |
| `BASE` | `BasePlate` |
| `massRelief` | `MassRelief` |
| `cutAway` | `Cutaway` |

### 7.4 Missing feature-type prefixes

Examples:

```text
mount2KUKA_throughholes
mount2KUKA_washersSink
mount2Trispector
mount2Trispector_washers
relief_center
relief_outer_base
massRelief
cutAway_trispecMount
printBaseChamfer
```

These should begin with the feature type, for example:

```text
Pocket_KukaMountThroughHoles_160x90
Pocket_KukaMountWasherSink_168x98
Pocket_TrispectorMount_101x52
Pocket_TrispectorMountWasherSink_105x56
Pocket_ReliefCenter_220x30
Pocket_ReliefOuterBase_220x20
Pocket_MassRelief_190x65
Pocket_Cutaway_TrispectorMount_190x60
Chamfer_PrintBase_220x100
```

---

## 8. Recommended Remediation Plan

### Priority 1: Rename labels

Rename all feature labels to the proposed standardized labels. This improves readability without necessarily changing internal object names.

### Priority 2: Rename internal names if safe

If no expressions, external links, scripts, or downstream references depend on the current internal names, rename internal names to the proposed lowercase snake_case names.

### Priority 3: Standardize document name

Rename the document label from:

```text
mount_trispector_to_kuka
```

to:

```text
Mount_Trispector_to_KUKA
```

### Priority 4: Add company dictionary

Once the company dictionary is available, re-run this audit and adjust the proposed names to match official prefixes, suffixes, dimension rules, and abbreviation rules.

---

## 9. Optional FreeCAD Label Rename Script

The following script renames **labels only**, which is generally safer than renaming internal object names.

> **Warning:** Always save a backup before running rename scripts.

```python
import FreeCAD

doc = FreeCAD.getDocument("mount_trispector_to_kuka")

# Rename document label
doc.Label = "Mount_Trispector_to_KUKA"

# Rename object labels
renames = {
    "Body": "Body_Mount_Trispector_to_KUKA_220x100x30",
    "Sketch": "Sketch_BasePlate_220x100",
    "BASE": "Pad_BasePlate_220x100x30",
    "sketch_mount2KUKA": "Sketch_KukaMountPattern_160x90",
    "mount2KUKA_throughholes": "Pocket_KukaMountThroughHoles_160x90",
    "sketch_mount2KUKA_washers": "Sketch_KukaMountWasherPattern_168x98",
    "mount2KUKA_washersSink": "Pocket_KukaMountWasherSink_168x98",
    "sketch_mount2trispector": "Sketch_TrispectorMountPattern_101x52",
    "mount2Trispector": "Pocket_TrispectorMount_101x52",
    "sketch_mount2Trispector_washers": "Sketch_TrispectorMountWasherPattern_105x56",
    "mount2Trispector_washers": "Pocket_TrispectorMountWasherSink_105x56",
    "sketch_reliefTrispector": "Sketch_ReliefCenter_220x30",
    "relief_center": "Pocket_ReliefCenter_220x30",
    "sketch_relief_outer": "Sketch_ReliefOuter_220x20",
    "relief_outer_base": "Pocket_ReliefOuterBase_220x20",
    "relief_outer_mirr": "Mirror_ReliefOuter_220x20",
    "sketch_massRelief": "Sketch_MassRelief_190x65",
    "massRelief": "Pocket_MassRelief_190x65",
    "sketch_cutAway_TrispecMount": "Sketch_Cutaway_TrispectorMount_190x60",
    "cutAway_trispecMount": "Pocket_Cutaway_TrispectorMount_190x60",
    "printBaseChamfer": "Chamfer_PrintBase_220x100",
}

for obj in doc.Objects:
    if obj.Label in renames:
        obj.Label = renames[obj.Label]

doc.recompute()
```

---

## 10. Final Audit Conclusion

The model is functionally organized, but its naming is not standardized.

### Required actions

1. Replace anonymous internal names with meaningful names where safe.
2. Normalize all labels to include feature type, function, position, and dimensions.
3. Remove inconsistent casing and abbreviations.
4. Standardize the document name.
5. Re-audit once the official company dictionary is available.

### Provisional compliance status

```text
Company dictionary unavailable: audit is provisional.
Generic naming compliance: NOT COMPLIANT.
Recommended action: apply proposed standardized names after review.
```