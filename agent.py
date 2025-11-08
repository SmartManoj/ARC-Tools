print('Starting')
import os
from openhands.sdk import LLM, Conversation, Agent
from openhands.sdk.tool import Tool, register_tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.preset.default import get_default_condenser
# Configure LLM
is_cloud=1
if is_cloud:
    base_url=None
    model="vertex_ai/gemini-2.5-pro"
    max_input_tokens=None
    max_output_tokens=None
else:
    model = 'hosted_vllm//kaggle/input/qwen3-coder/transformers/30b-a3b-instruct/1'
    base_url = 'http://localhost:8000/v1/'
    max_input_tokens=48_000
    max_output_tokens=16_000
llm = LLM(model=model, base_url=base_url, max_input_tokens=max_input_tokens, max_output_tokens=max_output_tokens, seed=42, log_completions=1)

# Register tools
register_tool("TerminalTool", TerminalTool)
register_tool("FileEditorTool", FileEditorTool)
register_tool("TaskTrackerTool", TaskTrackerTool)

# Create agent with custom bash tool configuration
agent = Agent(
    llm=llm,
    tools=[
        Tool(name="TerminalTool"),
        Tool(name="FileEditorTool"),
        Tool(name="TaskTrackerTool"),
    ],
    condenser=get_default_condenser(
            llm=llm.model_copy(update={"usage_id": "condenser"})
        ),
)

# Start a conversation
conversation = Conversation(agent=agent, workspace=".", persistence_dir=".conversations")
conversation.send_message(open('prompt.txt').read())
conversation.run()