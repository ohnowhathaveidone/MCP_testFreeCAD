import os
import json
from openai import OpenAI
import freecad_core

async def run_cad_analysis(session, config) -> tuple[str, list[dict]]:
    """
    Connects via MCP session, fetches tree & standards,
    and asks the LLM for a structured JSON proposal + Markdown report.
    """
    client = OpenAI(
        api_key=config.get("api_key", "dummy-key"),
        base_url=config.get("base_url")
    )
    model_name = config.get("model_name", "llama3")

    # 1. Fetch resources and tools via MCP
    standards_resource = await session.read_resource("standards://company-dictionary")
    company_rules = standards_resource.contents[0].text if standards_resource.contents else "{}"

    tree_result = await session.call_tool("get_model_tree", arguments={})
    model_data = tree_result.content[0].text

    # 2. Construct a prompt enforcing structured JSON output + Markdown report
    system_prompt = f"""
    You are an expert CAD Data Management Assistant. Audit this FreeCAD model tree against company standards.

    Company Standards:
    {company_rules}

    You MUST output your response in two clearly separated sections:
    1. MARKDOWN_REPORT: A professional markdown audit report summarizing your findings.
    2. JSON_PROPOSALS: A strict JSON array of objects representing proposed renames, formatted exactly like this:
    [
      {{"old_name": "Pad001", "new_name": "SidePanel_Left", "reasoning": "Matches outer vertical support dimensions"}}
    ]

    Separate the two sections using the exact tag: ===JSON_START===
    """

    user_prompt = f"FreeCAD Model Tree:\n{model_data}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    full_output = response.choices[0].message.content

    # 3. Parse the output into Markdown text and JSON proposals list
    if "===JSON_START===" in full_output:
        report_part, json_part = full_output.split("===JSON_START===", 1)
        try:
            proposals = json.loads(json_part.strip())
        except json.JSONDecodeError:
            proposals = []
    else:
        report_part = full_output
        proposals = []

    return report_part.strip(), proposals
