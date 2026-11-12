import os
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from agent_engine import run_cad_analysis
from approval_controller import request_user_approval

from freecad_core import check_version_control

def load_config() -> dict:
    """Loads LLM connection settings from the data folder."""
    config_path = "data/config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}. Please create one.")

    with open(config_path, "r") as f:
        return json.load(f)

async def main():
    config = load_config()

    # Define parameters to launch our MCP Server locally using FreeCAD's Python
    server_params = StdioServerParameters(
        #command="./squashfs-root/usr/bin/python",
        #args=["src/mcp_server.py"],
        command=".venv/bin/python3.11",
        args=["src/mcp_server.py"],
        env=None
    )
    # --- History Workbench Check Hook (Non-blocking warning) ---
    # We import or call the core check function to see status

    vc_status = check_version_control("data/mount_trispector_to_kuka.FCStd")
    print(f"[Check] {vc_status['message']}")
    if not vc_status["is_versioned"]:
        print("[Warning] Best Practice: Consider tracking this model with History Workbench before making automated changes.")

    print("[Main] Connecting to FreeCAD MCP Server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # --- Future Hook Location for History Workbench check ---
            # check_version_control(session)

            # Phase 1 & 2: Run Agent Analysis & Get Proposals
            print("[Main] Analyzing CAD model and generating proposals...")
            markdown_report, proposals = await run_cad_analysis(session, config)

            # Phase 3: Ask User for Approval
            changes_approved = request_user_approval(proposals)

            # Phase 4: Conditional Execution
            execution_log = "\n\n## Execution Status\n"
            if changes_approved:
                print("[Main] User approved changes. Applying updates via MCP...")
                applied_count = 0
                for p in proposals:
                    old = p.get("old_name")
                    new = p.get("new_name")

                    # Call MCP tool to rename object in FreeCAD
                    result = await session.call_tool("rename_object", arguments={"old_name": old, "new_name": new})
                    print(f"  - {result.content[0].text}")
                    applied_count += 1

                execution_log += f"Status: **Approved & Applied** ({applied_count} objects renamed)."
            else:
                print("[Main] Changes declined by user. No modifications made.")
                execution_log += "Status: **Declined by User**. No changes were written to the CAD file."

            # Save final comprehensive report
            final_report = markdown_report + execution_log
            os.makedirs("outputs", exist_ok=True)
            with open("outputs/audit_report.md", "w") as f:
                f.write(final_report)

            print("[Main] Complete! Audit report saved to outputs/audit_report.md")

if __name__ == "__main__":
    asyncio.run(main())
