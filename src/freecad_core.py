import os
import sys

FREECADPATH = '/home/ann1/Downloads/soft/freeCADunpacked/freecad114_decompressed/usr/lib';
sys.path.append(FREECADPATH);

try:
    import FreeCAD
    import Part
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    sys.exit('FREECAD NOT FOUND!');

def _extract_object_node(obj) -> dict:
    """Helper to extract metadata from a single FreeCAD object."""
    node = {
        "name": obj.Name,
        "label": obj.Label,
        "type": obj.TypeId,
        "children": []
    }

    # Extract dimensions/bounding box if available
    if hasattr(obj, "Shape") and not obj.Shape.isNull():
        bb = obj.Shape.BoundBox
        node["bounding_box"] = {
            "XLength": round(bb.XLength, 2),
            "YLength": round(bb.YLength, 2),
            "ZLength": round(bb.ZLength, 2)
        }

    return node

def get_document_tree(file_path: str) -> dict:
    """
    Extracts a hierarchical tree from a FreeCAD document,
    supporting both single bodies and complex assemblies.
    """
    if not FREECAD_AVAILABLE:
        # Mock data representing a multi-part assembly (e.g., a Cabinet Assembly)
        return {
            "document": os.path.basename(file_path),
            "structure_type": "Assembly",
            "components": [
                {
                    "name": "Cabinet_Carcass_Part",
                    "type": "App::Part",
                    "children": [
                        {"name": "Pad_SidePanel_L", "type": "Part::Pad", "children": [
                            {"name": "Pocket_Dado", "type": "Part::Pocket", "depth": 10.0}
                        ]}
                    ]
                }
            ]
        }

    doc = FreeCAD.open(file_path)
    document_tree = {
        "document": doc.Name,
        "structure_type": "Multi-Object" if len(doc.Objects) > 1 else "Single-Object",
        "root_objects": []
    }

    # Find top-level objects (objects that don't have an InGroup parent)
    for obj in doc.Objects:
        # If it's a top-level part container or root feature
        if not hasattr(obj, "InList") or not obj.InList:
            node = _extract_object_node(obj)

            # If the object contains children (like an App::Part or Group)
            if hasattr(obj, "Group"):
                for child in obj.Group:
                    node["children"].append(_extract_object_node(child))

            document_tree["root_objects"].append(node)

    return document_tree

def rename_cad_object(file_path: str, old_name: str, new_name: str) -> bool:
    """Renames an object label inside the FreeCAD document."""
    if not FREECAD_AVAILABLE:
        print(f"[MOCK] Renamed {old_name} to {new_name} in {file_path}")
        return True

    doc = FreeCAD.open(file_path)
    obj = doc.getObject(old_name)
    if obj:
        obj.Label = new_name
        doc.save()
        return True
    return False
