import os
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

def load_config() -> dict:
    """Loads LLM connection settings from the data folder."""
    config_path = "data/config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}. Please create one.")

    with open(config_path, "r") as f:
        return json.load(f)

async def run_cad_audit_agent():
    # Load configuration
    config = load_config()

    # Initialize OpenAI client with custom base_url (works for school server or Ollama)
    client = OpenAI(
        api_key=config.get("api_key", "dummy-key"),
        base_url=config.get("base_url")
    )
    model_name = config.get("model_name", "qwen3.8-flash-next")

    # Define parameters to launch our MCP Server locally using FreeCAD's Python
    server_params = StdioServerParameters(
        #command="./squashfs-root/usr/bin/python",
        #args=["src/mcp_server.py"],
        command="python",
        args=["src/mcp_server.py"],
        env=None
    )

    print(f"[Agent] Connecting to FreeCAD MCP Server using model: {model_name}...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Read company standards resource
            standards_resource = await session.read_resource("standards://company-dictionary")
            company_rules = standards_resource.contents[0].text if standards_resource.contents else "{}"

            # 2. Fetch the model tree via MCP tool
            tree_result = await session.call_tool("get_model_tree", arguments={})
            model_data = tree_result.content[0].text

            # 3. Construct prompt
            system_prompt = f"""
            You are an expert CAD Data Management and Wood Technology Quality Assurance Assistant.
            Your job is to audit FreeCAD model trees against company naming standards.

            Here are the company design standards:
            {company_rules}

            Analyze the provided FreeCAD model tree data and check for anonymous or poorly named features.
            Propose standardized names based on dimensions, type, and position.
            Output a clear Markdown audit report.
            """

            user_prompt = f"Here is the current FreeCAD model tree data:\n{model_data}"

            print("[Agent] Querying LLM endpoint...")

            # Call the LLM (School infrastructure or local Ollama)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )

            audit_report = response.choices[0].message.content

            # Save output report
            os.makedirs("outputs", exist_ok=True)
            with open("outputs/audit_report.md", "w") as f:
                f.write(audit_report)

            print("[Agent] Audit complete! Report saved to outputs/audit_report.md")

if __name__ == "__main__":
    asyncio.run(run_cad_audit_agent())
