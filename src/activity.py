import os
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# ========= Helpers ========= #
def append_to_file(filename: str, content: str) -> str:
    try:
        os.makedirs("activity_logs", exist_ok=True)
        filepath = os.path.join("activity_logs", filename)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {content}\n")
        
        return f"Updated {filename} with entry: {content}"
    except Exception as e:
        return f"Error writing to {filename}: {str(e)}"

def read_from_file(filename: str, n: int = None) -> str:
    """Reads last n lines or full file."""
    filepath = os.path.join("activity_logs", filename)
    if not os.path.exists(filepath):
        return f"No logs found in {filename}"
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if not lines:
        return f"{filename} is empty."
    
    if n and n > 0:
        lines = lines[-n:]
    
    return "".join(lines)

# ========= Activity Tools ========= #
def update_route_detail(text: str) -> str:
    return append_to_file("route.txt", text)

def update_task_detail(text: str) -> str:
    return append_to_file("task.txt", text)

def update_learning_detail(text: str) -> str:
    return append_to_file("learning.txt", text)

# ========= Search Tool ========= #
def search_logs(query: str) -> str:
    """
    Example inputs:
      'search route: last 5'
      'search task: all'
      'search learning: last 3'
    """
    try:
        parts = query.lower().split(":")
        if len(parts) != 2:
            return "Error: Input must be in format 'search <type>: <last N/all>'"
        
        log_type = parts[0].replace("search", "").strip()
        command = parts[1].strip()

        filename_map = {
            "route": "route.txt",
            "task": "task.txt",
            "learning": "learning.txt"
        }

        if log_type not in filename_map:
            return "Error: log type must be one of route, task, learning"

        filename = filename_map[log_type]

        if command.startswith("last"):
            try:
                n = int(command.split()[1])
                return read_from_file(filename, n)
            except Exception:
                return "Error: Use format 'last N' where N is a number"
        elif command == "all":
            return read_from_file(filename, None)
        else:
            return "Error: Command must be 'last N' or 'all'"
    except Exception as e:
        return f"Error searching logs: {str(e)}"

# ========= Define Tools ========= #
tools = [
    Tool(name="Update Route Detail", func=update_route_detail,
         description="Log route details (e.g., 'I took marthalli route today')."),
    Tool(name="Update Task Detail", func=update_task_detail,
         description="Log completed tasks (e.g., 'I completed sales ppt creation')."),
    Tool(name="Update Learning Detail", func=update_learning_detail,
         description="Log learning activities (e.g., 'I learned about AI agents')."),
    Tool(name="Search Logs", func=search_logs,
         description="Search activity logs. Example: 'search route: last 5' or 'search task: all'.")
]

# ========= Prompt ========= #
prompt_template = """You are a helpful assistant who uses tools to log activities, search logs, and perform tasks.
You have access to these tools:
{tools}

The available tools are: {tool_names}

Follow this reasoning format:

Question: the user's input
Thought: reasoning about what tool to use
Action: the tool to use, should be one of [{tool_names}]
Action Input: the input to the tool
Observation: result from the tool
Thought: reflect on observation
Final Answer: provide the user with the result

Question: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)

# ========= LLM & Agent ========= #
llm = ChatGroq(
    api_key=None, # replace with your Groq API key or set via environment variable
    model="llama-3.3-70b-versatile",
    temperature=0
)

agent = create_react_agent(llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# ========= Run Tests ========= #
test_inputs = [
    "I took marthalli route today",
    "I completed task of sales ppt creation",
    "I learned about reinforcement learning",
    "search route: last 1",
    "search task: all",
    "search learning: last 2",
]

for q in test_inputs:
    print(f"User Input: {q}")
    response = agent_executor.invoke({"input": q})
    print(f"Agent Response: {response}\n")
    print("-" * 50)
