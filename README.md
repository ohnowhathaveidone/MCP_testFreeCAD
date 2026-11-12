# MCP_testFreeCAD
exploring the idea of a model hierarchy sanitizer for freeCAD

## preparation  
if no venv has been yet cerated  
uv venv --python 3.11.14  
NOTE: .venv is in .gitignore  

activate venv  
source .venv/bin/activate  

pull in dependencies  
uv pip install -r requirements.txt  

## configuration  
set up config  
cp data/dummyConfig.json data/config.json  
-> adapt config  
NOTE: config.json is in .gitignore  
for local ollama deployments (not yet tested):  
{  
  "base_url": "http://localhost:11434/v1",  
  "api_key": "ollama",  
  "model_name": "llama3"  
  "freecad_path: "/path/to/freecad/bin/or/lib"  
}  

## run (in venv)  
python ./src/agent_client.py  

## TODO  
- let user load freeCAD file  
- let user work on folder?  
- **TEST** load assembly  
- let agent execute changes  
- integration w/ history WB?  

