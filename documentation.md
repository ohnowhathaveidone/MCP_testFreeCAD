# Project API Reference

---


## `src/agent_engine.py`

### Function: `run_cad_analysis(session, config) -> tuple[str, list[dict]]`


Connects via MCP session, fetches tree & standards,
and asks the LLM for a structured JSON proposal + Markdown report.


---


## `src/approval_controller.py`

### Function: `request_user_approval(proposals: list[dict]) -> bool`


Displays proposed changes in the terminal and asks the user for confirmation.
Future-proof: Can be replaced later with a GUI modal dialog returning True/False.


---


## `src/config_loader.py`

### Function: `load_config()`


Loads LLM connection settings from the data folder.


---


## `src/freecad_core.py`

### Function: `check_version_control(file_path: str) -> dict`


Stub hook for checking if the FreeCAD file is versioned
using the History Workbench or a Git repository.
(Not yet strictly enforced).


---

### Function: `get_document_tree(file_path: str) -> dict`


Extracts a hierarchical tree from a FreeCAD document,
supporting both single bodies and complex assemblies.


---

### Function: `rename_cad_object(file_path: str, old_name: str, new_name: str) -> bool`


Renames an object label inside the FreeCAD document, matching by Name or Label.


---


## `src/main.py`

### Function: `main()`


_No description provided._


---


## `src/mcp_server.py`

### Function: `get_model_tree() -> str`


Inspects the active FreeCAD model and returns its tree hierarchy and object properties.


---

### Function: `rename_object(old_name: str, new_name: str) -> str`


Renames an object in the CAD model to match company standard terminology.


---

### Function: `get_company_standards() -> str`


Exposes the company's official feature naming dictionary and geometric rule set.


---
