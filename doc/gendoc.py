import ast
from pathlib import Path


def get_function_signature(node: ast.FunctionDef) -> str:
  """Extracts parameters and type hints cleanly from a function node."""
  args = []
  # Process standard arguments
  all_args = (
      node.args.posonlyargs + node.args.args
  )  # handles positional-only and normal args
  defaults = node.args.defaults

  # Map defaults to the end of the argument list
  offset = len(all_args) - len(defaults)
  for i, arg in enumerate(all_args):
    arg_str = arg.arg
    if arg.annotation:
      arg_str += f": {ast.unparse(arg.annotation)}"
    # Check if there is a default value
    if i >= offset:
      default_val = ast.unparse(defaults[i - offset])
      arg_str += f" = {default_val}"
    args.append(arg_str)

  # Handle *args and **kwargs if present
  if node.args.vararg:
    vararg_str = f"*{node.args.vararg.arg}"
    if node.args.vararg.annotation:
      vararg_str += f": {ast.unparse(node.args.vararg.annotation)}"
    args.append(vararg_str)

  if node.args.kwarg:
    kwarg_str = f"**{node.args.kwarg.arg}"
    if node.args.kwarg.annotation:
      kwarg_str += f": {ast.unparse(node.args.kwarg.annotation)}"
    args.append(kwarg_str)

  sig = ", ".join(args)

  # Extract return type hint if available
  returns = ""
  if node.returns:
    returns = f" -> {ast.unparse(node.returns)}"

  return f"({sig}){returns}"


def generate_advanced_doc(source_dir=".", output_file="documentation.md"):
  md_content = ["# Project API Reference\n", "---\n"]

  source_path = Path(source_dir)
  for path in sorted(source_path.rglob("*.py")):
    if any(
        p.startswith(".") or p in ("venv", "env", "__pycache__", "build")
        for p in path.parts
    ):
      continue

    try:
      tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
      continue

    file_header_added = False

    for node in ast.walk(tree):
      if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        if node.name.startswith("_") and node.name != "__init__":
          continue

        if not file_header_added:
          md_content.append(f"\n## `{path}`\n")
          file_header_added = True

        docstring = ast.get_docstring(node) or "_No description provided._"

        if isinstance(node, ast.ClassDef):
          md_content.append(f"### Class: `{node.name}`\n")
        else:
          sig = get_function_signature(node)
          md_content.append(f"### Function: `{node.name}{sig}`\n")

        md_content.append(f"\n{docstring}\n")
        md_content.append("\n---\n")

  Path(output_file).write_text("\n".join(md_content), encoding="utf-8")
  print(f"Single-file documentation generated at: {output_file}")


if __name__ == "__main__":
  generate_advanced_doc(source_dir="./src/", output_file="documentation.md")
