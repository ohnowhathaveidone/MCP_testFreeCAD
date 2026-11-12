import json
from fastmcp import FastMCP
from freecad_core import get_document_tree, rename_cad_object

# Initialize the MCP server container
mcp = FastMCP(name="WoodCAD Inspector Server")

# Define path to the sample CAD file and company standards
CAD_FILE_PATH = "data/sample_cabinet.FCStd"
DICT_FILE_PATH = "data/company_feature_dict.json"

# --- MCP TOOLS (Actions the Agent Can Call) ---

@mcp.tool()
def get_model_tree() -> str:
    """Inspects the active FreeCAD model and returns its tree hierarchy and object properties."""
    tree_data = get_document_tree(CAD_FILE_PATH)
    return json.dumps(tree_data, indent=2)

@mcp.tool()
def rename_object(old_name: str, new_name: str) -> str:
    """Renames an object in the CAD model to match company standard terminology."""
    success = rename_cad_object(CAD_FILE_PATH, old_name, new_name)
    if success:
        return f"Successfully renamed '{old_name}' to '{new_name}'."
    return f"Error: Object '{old_name}' could not be found."


# --- MCP RESOURCES (Read-only data endpoints for the LLM) ---

@mcp.resource("standards://company-dictionary")
def get_company_standards() -> str:
    """Exposes the company's official feature naming dictionary and geometric rule set."""
    try:
        with open(DICT_FILE_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return json.dumps({"error": "Company dictionary file not found."})


if __name__ == "__main__":
    # Runs the server using standard input/output (STDIO) for local agent communication
    mcp.run()
