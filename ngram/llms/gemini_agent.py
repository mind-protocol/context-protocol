"""
Gemini LLM agent subprocess for the ngram CLI.

DOCS: docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md
"""

import argparse
import json
import os
import sys
from google import genai
from dotenv import dotenv_values


"""
Gemini LLM agent subprocess for the ngram CLI.

DOCS: docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess # Added for run_shell_command
import sys
import urllib.parse
import urllib.request
from pathlib import Path # Added for read_file
from google import genai
from dotenv import dotenv_values


def main():
    parser = argparse.ArgumentParser(description="Gemini LLM agent for ngram CLI.")
    parser.add_argument("-p", "--prompt", required=True, help="User prompt.")
    parser.add_argument("--system-prompt", default="", help="System prompt.")
    parser.add_argument("--output-format", default="stream-json", help="Output format (stream-json or text).")
    parser.add_argument("--allowed-tools", help="Comma-separated list of allowed tools.")
    parser.add_argument("--api-key", help="Gemini API key.")

    args = parser.parse_args()

    # Load from .env file first
    config = dotenv_values()

    # Get API key
    api_key = args.api_key or config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        print(json.dumps({"error": "GEMINI_API_KEY not found. Please set it in a .env file, as an environment variable, or pass it with --api-key."}), flush=True)
        sys.exit(1)

    # Create the genai client with API key
    client = genai.Client(api_key=api_key)

    # --- Start Debugging: List available models ---
    try:
        print("Available Gemini models:", file=sys.stderr)
        for m in client.models.list():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name} (supports generateContent)", file=sys.stderr)
            else:
                print(f"- {m.name}", file=sys.stderr)
    except Exception as e:
        print(f"Error listing models: {e}", file=sys.stderr)
    # --- End Debugging ---

    # --- Tool Definitions ---
    # Python functions to be exposed to the Gemini model
    def run_shell_command_tool(command: str, description: str = ""):
        try:
            print(json.dumps({"type": "tool_code", "name": "run_shell_command", "args": {"command": command, "description": description}}), flush=True)
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return {"stdout": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"error": e.stderr if e.stderr else e.stdout, "exit_code": e.returncode}
        except Exception as e:
            return {"error": str(e)}

    def read_file_tool(file_path: str):
        try:
            print(json.dumps({"type": "tool_code", "name": "read_file", "args": {"file_path": file_path}}), flush=True)
            content = Path(file_path).read_text()
            return {"content": content}
        except FileNotFoundError:
            return {"error": f"File not found: {file_path}"}
        except Exception as e:
            return {"error": str(e)}

    # Placeholder for other tools from the ngram CLI
    # These will need actual implementations later
    def list_directory_tool(dir_path: str):
        print(json.dumps({"type": "tool_code", "name": "list_directory", "args": {"dir_path": dir_path}}), flush=True)
        try:
            base_path = Path(dir_path)
            if not base_path.exists():
                return {"error": f"Directory not found: {dir_path}"}
            if not base_path.is_dir():
                return {"error": f"Not a directory: {dir_path}"}
            entries = []
            for entry in sorted(base_path.iterdir(), key=lambda p: p.name.lower()):
                entry_type = "dir" if entry.is_dir() else "file"
                entries.append({"name": entry.name, "path": str(entry), "type": entry_type})
            return {"entries": entries, "count": len(entries)}
        except Exception as e:
            return {"error": str(e)}

    def search_file_content_tool(pattern: str, dir_path: str = "."):
        print(json.dumps({"type": "tool_code", "name": "search_file_content", "args": {"pattern": pattern, "dir_path": dir_path}}), flush=True)
        try:
            regex = re.compile(pattern)
        except re.error as e:
            return {"error": f"Invalid regex pattern: {e}"}
        matches = []
        files_scanned = 0
        max_matches = 200
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
            for filename in files:
                file_path = Path(root) / filename
                files_scanned += 1
                try:
                    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                        for line_number, line in enumerate(handle, start=1):
                            if regex.search(line):
                                matches.append({
                                    "path": str(file_path),
                                    "line": line_number,
                                    "text": line.rstrip("\n"),
                                })
                                if len(matches) >= max_matches:
                                    return {
                                        "matches": matches,
                                        "count": len(matches),
                                        "files_scanned": files_scanned,
                                        "truncated": True,
                                    }
                except Exception:
                    continue
        return {
            "matches": matches,
            "count": len(matches),
            "files_scanned": files_scanned,
            "truncated": False,
        }

    def glob_tool(pattern: str, dir_path: str = "."):
        print(json.dumps({"type": "tool_code", "name": "glob", "args": {"pattern": pattern, "dir_path": dir_path}}), flush=True)
        try:
            if os.path.isabs(pattern):
                search_pattern = pattern
            else:
                search_pattern = str(Path(dir_path) / pattern)
            matches = sorted(glob.glob(search_pattern, recursive=True))
            return {"matches": matches, "count": len(matches)}
        except Exception as e:
            return {"error": str(e)}

    def replace_tool(file_path: str, old_string: str, new_string: str, instruction: str = ""):
        print(json.dumps({"type": "tool_code", "name": "replace", "args": {"file_path": file_path, "old_string": old_string, "new_string": new_string, "instruction": instruction}}), flush=True)
        if old_string == "":
            return {"error": "old_string cannot be empty"}
        try:
            target_path = Path(file_path)
            if not target_path.exists():
                return {"error": f"File not found: {file_path}"}
            content = target_path.read_text(encoding="utf-8")
            count = content.count(old_string)
            if count == 0:
                return {"error": f"String not found in {file_path}"}
            updated = content.replace(old_string, new_string)
            target_path.write_text(updated, encoding="utf-8")
            return {"path": str(target_path), "replacements": count}
        except Exception as e:
            return {"error": str(e)}

    def write_file_tool(file_path: str, content: str):
        print(json.dumps({"type": "tool_code", "name": "write_file", "args": {"file_path": file_path, "content": content}}), flush=True)
        try:
            target_path = Path(file_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")
            return {"path": str(target_path), "bytes_written": len(content.encode("utf-8"))}
        except Exception as e:
            return {"error": str(e)}
    
    def google_web_search_tool(query: str):
        print(json.dumps({"type": "tool_code", "name": "google_web_search", "args": {"query": query}}), flush=True)
        if not query or not query.strip():
            return {"error": "Query cannot be empty"}
        try:
            url = "https://www.google.com/search?" + urllib.parse.urlencode({"q": query})
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read(200000).decode("utf-8", "ignore")
            results = []
            seen = set()
            for match in re.findall(r'href="/url\\?q=([^&"]+)', body):
                link = urllib.parse.unquote(match)
                if link.startswith("http") and link not in seen:
                    seen.add(link)
                    results.append({"url": link})
                if len(results) >= 5:
                    break
            return {"query": query, "results": results, "count": len(results)}
        except Exception as e:
            return {"error": str(e)}
    
    def web_fetch_tool(prompt: str):
        print(json.dumps({"type": "tool_code", "name": "web_fetch", "args": {"prompt": prompt}}), flush=True)
        try:
            match = re.search(r"https?://\\S+", prompt)
            url = match.group(0) if match else prompt.strip()
            if not url:
                return {"error": "No URL provided"}
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                content_type = response.headers.get("Content-Type", "")
                raw = response.read(200000)
            text = raw.decode("utf-8", "ignore")
            truncated = len(raw) >= 200000
            return {
                "url": url,
                "content_type": content_type,
                "content": text,
                "truncated": truncated,
            }
        except Exception as e:
            return {"error": str(e)}

    def write_todos_tool(todos: list):
        print(json.dumps({"type": "tool_code", "name": "write_todos", "args": {"todos": todos}}), flush=True)
        if not isinstance(todos, list):
            return {"error": "todos must be a list"}
        try:
            todo_path = Path(".ngram/state/agent_todos.json")
            existing = []
            if todo_path.exists():
                try:
                    existing_data = json.loads(todo_path.read_text(encoding="utf-8"))
                    if isinstance(existing_data, list):
                        existing = existing_data
                    elif isinstance(existing_data, dict) and isinstance(existing_data.get("todos"), list):
                        existing = existing_data["todos"]
                except Exception:
                    existing = []
            updated = existing + todos
            todo_path.parent.mkdir(parents=True, exist_ok=True)
            todo_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
            return {"path": str(todo_path), "count": len(updated)}
        except Exception as e:
            return {"error": str(e)}
    
    def save_memory_tool(fact: str):
        print(json.dumps({"type": "tool_code", "name": "save_memory", "args": {"fact": fact}}), flush=True)
        if not fact or not str(fact).strip():
            return {"error": "fact cannot be empty"}
        try:
            memory_path = Path(".ngram/state/agent_memory.jsonl")
            memory_path.parent.mkdir(parents=True, exist_ok=True)
            record = {"fact": str(fact).strip()}
            with memory_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record) + "\n")
            return {"path": str(memory_path)}
        except Exception as e:
            return {"error": str(e)}

    def codebase_investigator_tool(objective: str):
        print(json.dumps({"type": "tool_code", "name": "codebase_investigator", "args": {"objective": objective}}), flush=True)
        if not objective or not objective.strip():
            return {"error": "objective cannot be empty"}
        try:
            query = objective.strip()
            if shutil.which("rg"):
                result = subprocess.run(
                    ["rg", "-n", query, "."],
                    capture_output=True,
                    text=True,
                )
                if result.returncode not in (0, 1):
                    return {"error": result.stderr.strip() or "rg failed"}
                lines = result.stdout.splitlines()
                matches = []
                for line in lines[:50]:
                    parts = line.split(":", 2)
                    if len(parts) == 3:
                        path, line_number, text = parts
                        matches.append({
                            "path": path,
                            "line": int(line_number),
                            "text": text,
                        })
                return {
                    "matches": matches,
                    "count": len(matches),
                    "truncated": len(lines) > 50,
                }
            matches = []
            files_scanned = 0
            max_matches = 50
            for root, dirs, files in os.walk("."):
                dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
                for filename in files:
                    file_path = Path(root) / filename
                    files_scanned += 1
                    try:
                        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                            for line_number, line in enumerate(handle, start=1):
                                if query in line:
                                    matches.append({
                                        "path": str(file_path),
                                        "line": line_number,
                                        "text": line.rstrip("\n"),
                                    })
                                    if len(matches) >= max_matches:
                                        return {
                                            "matches": matches,
                                            "count": len(matches),
                                            "files_scanned": files_scanned,
                                            "truncated": True,
                                        }
                    except Exception:
                        continue
            return {
                "matches": matches,
                "count": len(matches),
                "files_scanned": files_scanned,
                "truncated": False,
            }
        except Exception as e:
            return {"error": str(e)}


    # Create the GenerativeModel with tools
    # Use gemini-2.5-flash as the default model
    model = client.models.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[
            run_shell_command_tool, read_file_tool, list_directory_tool,
            search_file_content_tool, glob_tool, replace_tool, write_file_tool,
            google_web_search_tool, web_fetch_tool, write_todos_tool,
            save_memory_tool, codebase_investigator_tool
        ]
    )

    # Build contents for chat
    contents = []
    if args.system_prompt:
        contents.append({'role': 'user', 'parts': [args.system_prompt]})
        contents.append({'role': 'model', 'parts': ['ok']}) # Gemini expects a reply from model if user starts with system prompt
    
    # Initial user prompt
    contents.append({'role': 'user', 'parts': [args.prompt]})

    try:
        # Start chat session
        chat_session = model.start_chat(history=[])

        # Send the first message
        response_stream = chat_session.send_message(contents[0]['parts'][0], stream=True)

        for chunk in response_stream:
            # Process text output
            if chunk.text:
                print(json.dumps({
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": chunk.text}
                        ]
                    }
                }), flush=True)
            
            # Process tool calls
            if chunk.tool_calls:
                for tool_call in chunk.tool_calls:
                    tool_name = tool_call.name
                    tool_args = tool_call.args
                    
                    # Output tool call JSON
                    print(json.dumps({"type": "tool_code", "name": tool_name, "args": tool_args}), flush=True)
                    
                    # --- Execute tool based on its name ---
                    tool_result = None
                    if tool_name == "run_shell_command_tool":
                        tool_result = run_shell_command_tool(**tool_args)
                    elif tool_name == "read_file_tool":
                        tool_result = read_file_tool(**tool_args)
                    elif tool_name == "list_directory_tool":
                        tool_result = list_directory_tool(**tool_args)
                    elif tool_name == "search_file_content_tool":
                        tool_result = search_file_content_tool(**tool_args)
                    elif tool_name == "glob_tool":
                        tool_result = glob_tool(**tool_args)
                    elif tool_name == "replace_tool":
                        tool_result = replace_tool(**tool_args)
                    elif tool_name == "write_file_tool":
                        tool_result = write_file_tool(**tool_args)
                    elif tool_name == "google_web_search_tool":
                        tool_result = google_web_search_tool(**tool_args)
                    elif tool_name == "web_fetch_tool":
                        tool_result = web_fetch_tool(**tool_args)
                    elif tool_name == "write_todos_tool":
                        tool_result = write_todos_tool(**tool_args)
                    elif tool_name == "save_memory_tool":
                        tool_result = save_memory_tool(**tool_args)
                    elif tool_name == "codebase_investigator_tool":
                        tool_result = codebase_investigator_tool(**tool_args)
                    else:
                        tool_result = {"error": f"Unknown tool: {tool_name}"}

                    # Output tool result
                    print(json.dumps({"type": "tool_result", "name": tool_name, "result": tool_result}), flush=True)

                    # Send tool output back to the model
                    response_from_tool_stream = chat_session.send_message(
                        genai.tool_code(tool_result), stream=True # Correctly use genai.tool_code with the result
                    )
                    
                    # Process response from tool output
                    for tool_response_chunk in response_from_tool_stream:
                        if tool_response_chunk.text:
                            print(json.dumps({
                                "type": "assistant",
                                "message": {
                                    "content": [
                                        {"type": "text", "text": tool_response_chunk.text}
                                    ]
                                }
                            }), flush=True)

        # Indicate successful completion
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
