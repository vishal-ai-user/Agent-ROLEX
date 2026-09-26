
import os
import datetime
import subprocess
import sys
from memory import mem_clean
from ddgs import DDGS 

#==============================================================
#                     Tool Functions
#==============================================================

# 1. Get the Current Time
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d & %H:%M:%S")


# 2. Clear the Chat memory
def clear_chat_mem():
    mem_clean()
    return "Current Conversation history was cleared."


# 3. Websearch (Live Web Search)
def web_search(query):
    results = []
    for r in DDGS().text(query, max_results=3):
        results.append({
            "title": r.get("title"),
            "url": r.get("href"),
            "snippet": r.get("body")
        })
    return results


# 4. File Reader
def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


# 5. File Writer/Creater
def write_file(filepath, content):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created/written to {filepath}"
    except Exception as e:
        return f"Error writting file: {str(e)}"


# 6. List files in the folder
def list_files(directory="."):
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error listing directory: {str(e)}"


# 7. Python code runner
def run_python_code(code):
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout
        error = result.stdout

        if error:
            return f"output:\n{output}\nError:\n{error}"
        return output if output else "Code executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (limit: 10 seconds)."
    except Exception as e:
        return f"Error executing code: {str(e)}"

#==============================================================
#                     Available Tools
#==============================================================

available_tools={
    "get_current_time":get_current_time,
    "clear_chat_mem": clear_chat_mem,
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "run_python_code": run_python_code,

}

#==============================================================
#                Tools Description for LLM
#==============================================================

tools=[
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Use this tool only to get the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clear_chat_mem",
            "description": "Call the tool only to clear the current conversation history. Don't use this tool when the user say 'cls'.",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Use the tool to get the current information from the internet. Also use the tool to get the information if you don't know.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Give the question to search the internet."}
                },
                "required": ["query"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Use this tool only to Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file to read"},
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Use this tool only to create or write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "path to the file to create/write."},
                    "content": {"type": "string", "description": "Text content to write inside the file."},
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_file",
            "description": "Use the tool only to List all the files in a directory. ",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory path (default is current folder '.')"}
                },
                "required": [],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Use this tool only to Execute python code and return output or errors. Use this tool for mathematical calculations, logic checks, or data processing ",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Valid executable python code string (e.g., 'print(5 * 25)')"
                    }
                },
                "required": ["code"]
            }
        }
    }
]