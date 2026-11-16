## MARKDOWN_REPORT

# FreeCAD Model Audit — `bearing_13x3x5`

## Executive Summary
The model appears to represent a simple bearing-like part with:
- Outer diameter: **13 mm**
- Bore diameter: **3 mm**
- Width / thickness: **5 mm**

The geometry is internally consistent, but the model tree violates the company naming standard because most objects retain default generic names such as `Body`, `Sketch`, `Pad`, `Sketch001`, and `Pocket`.

Feature-specific standards for dowel holes, dado grooves, and shelf pin holes are **not applicable** to this model.

---

## Naming Compliance Findings

| Object | Type | Current Name / Label | Issue | Proposed Name | Standard Basis |
|---|---:|---|---|---|---|
| `Body` | `PartDesign::Body` | `Body` | Generic container name. | `ASM_Bearing` | Container / part objects should use `ASM_` prefix. |
| `Sketch` | `Sketcher::SketchObject` | `Sketch` | Generic sketch name. | `SK_BearingOuterProfile` | Sketches must use `SK_` prefix and descriptive PascalCase name. |
| `Pad` | `PartDesign::Pad` | `Pad` | Generic pad name. | `PD_BearingBody` | Pads must use `PD_` prefix and descriptive PascalCase name. |
| `Sketch001` | `Sketcher::SketchObject` | `Sketch001` | Generic sketch name. | `SK_BearingBoreProfile` | Sketches must use `SK_` prefix and descriptive PascalCase name. |
| `Pocket` | `PartDesign::Pocket` | `Pocket` | Generic pocket name. | `PK_BearingBore` | Pockets must use `PK_` prefix and descriptive PascalCase name. |
| `Local_CS` | `PartDesign::CoordinateSystem` | `Local_CS` / `center1` | Generic coordinate system name. | `CS_Center1` | No explicit company prefix is defined for coordinate systems; `CS_` is proposed as a descriptive prefix. |
| `Local_CS001` | `PartDesign::CoordinateSystem` | `Local_CS001` / `center2` | Generic coordinate system name. | `CS_Center2` | No explicit company prefix is defined for coordinate systems; `CS_` is proposed as a descriptive prefix. |

---

## Geometry Interpretation

### Outer Body
- `Sketch` bounding box: **13.0 × 13.0 × 0.0**
- `Pad` bounding box: **13.0 × 13.0 × 5.0**

This indicates the first sketch defines the outer circular profile, and the pad extrudes it to a **5 mm** thickness.

### Inner Bore
- `Sketch001` bounding box: **3.0 × 3.0 × 0.0**
- `Pocket` bounding box: **13.0 × 13.0 × 5.0**

This indicates the second sketch defines a **3 mm** bore profile, and the pocket subtracts the bore through the bearing body.

### Coordinate Systems
- `Local_CS` and `Local_CS001` appear to be center reference coordinate systems.
- Their bounding boxes are extremely large, which is typical for coordinate system objects.

---

## Feature-Specific Standards Review

| Standard | Applicability | Finding |
|---|---|---|
| Dowel hole | Not applicable | No dowel hole detected. The bore is approximately **3 mm** diameter and **5 mm** deep, not matching the dowel hole standard of **15 mm** depth. |
| Dado groove | Not applicable | No shelf housing groove detected. The pocket is a bore, not a dado groove. |
| Shelf pin hole | Not applicable | No shelf pin hole detected. The bore is approximately **3 mm** diameter and **5 mm** deep, not matching the shelf pin hole standard of **5 mm** diameter and **10 mm** depth. |
| Chamfer | Not applicable | No chamfer objects detected. |
| Fillet | Not applicable | No fillet objects detected. |

---

## Recommendations
1. Rename all generic feature objects using the proposed names.
2. Ensure all new names use PascalCase after the required prefix.
3. If coordinate systems are to be governed by naming standards, formally add a prefix such as `CS_` to the company standard.
4. Consider adopting a document naming standard if not already defined; the current document name `bearing_13x3x5` is descriptive but uses lowercase.

## Execution Status
Status: **Approved & Applied** (7 objects renamed).
