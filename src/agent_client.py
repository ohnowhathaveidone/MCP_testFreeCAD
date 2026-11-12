import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI  # Or Anthropic, depending on your preferred LLM

# Initialize LLM client (e.g., OpenAI or compatible local endpoint like Ollama)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def run_cad_audit_agent():
    # Define parameters to launch our MCP Server locally via stdio
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp_server.py"],
        env=None
    )

    print("[Agent] Connecting to FreeCAD MCP Server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # 1. Discover available tools from the server
            tools_response = await session.list_tools()
            print(f"[Agent] Discovered Tools: {[t.name for t in tools_response.tools]}")

            # 2. Read the company standards resource
            standards_resource = await session.read_resource("standards://company-dictionary")
            company_rules = standards_resource.contents[0].text if standards_resource.contents else "{}"

            # 3. Fetch the model tree using the MCP tool
            tree_result = await session.call_tool("get_model_tree", arguments={})
            model_data = tree_result.content[0].text

            # 4. Construct the prompt for the LLM
            system_prompt = f"""
            You are an expert CAD Data Management and Wood Technology Quality Assurance Assistant.
            Your job is to audit FreeCAD model trees against company naming standards.

            Here are the company design standards:
            {company_rules}

            Analyze the provided FreeCAD model tree data and check for anonymous or poorly named features (like Pad001, Pocket002).
            For each poorly named feature, propose a standardized name based on its dimensions, type, and position.
            Output a clear Markdown audit report summarizing your findings and recommended renames.
            """

            user_prompt = f"Here is the current FreeCAD model tree data:\n{model_data}"

            print("[Agent] Analyzing CAD model against company standards using LLM...")

            # Call the LLM
            response = client.chat.completions.create(
                model="gpt-4o",  # Or a local model like llama3 via Ollama
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
