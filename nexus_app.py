from pathlib import Path

from config import MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT

from conversation import Conversation
from memory import Memory
from ollama_client import OllamaClient

from commands.command_registry import CommandRegistry

from tools.registry import ToolRegistry
from tools.parser import ToolParser


class NexusApp:

    def __init__(self):

        Path("workspace").mkdir(exist_ok=True)

        self.conversation = Conversation(SYSTEM_PROMPT)

        self.memory = Memory()

        self.ollama = OllamaClient(
            MODEL_NAME,
            OLLAMA_URL
        )

        self.command_registry = CommandRegistry()

        self.tool_registry = ToolRegistry()

        self.tool_parser = ToolParser()

    def initialize(self):

        previous_messages = self.memory.load_messages(limit=30)

        self.conversation.load_messages(
            previous_messages
        )

        memories = self.memory.load_memories(limit=8)

        self.conversation.load_memories(
            memories
        )

    def register_command(self, command):

        self.command_registry.register(command)


    def register_tool(self, tool):

        self.tool_registry.register(tool)

    def build_prompt(self):
        return self.conversation.build_prompt()

    
    def ask_model(self):

        prompt = self.build_prompt()

        return self.ollama.generate_response(
            prompt
        )

    def parse_tool_call(
        self,
        assistant_response
    ):

        return self.tool_parser.parse(
            assistant_response
        )

    def execute_tool(
        self,
        tool_name,
        argument
    ):

        return self.tool_registry.execute(
            tool_name,
            argument
        )

    def add_user_message(
        self,
        message
    ):

        self.conversation.add_user_message(
            message
        )

        self.memory.save_message(
            "user",
            message
        )


    def add_assistant_message(
        self,
        message
    ):

        self.conversation.add_assistant_message(
            message
        )

        self.memory.save_message(
            "assistant",
            message
        )


    def add_tool_result(
        self,
        tool_name,
        result
    ):

        self.conversation.add_tool_message(
            tool_name,
            result
        )

        self.memory.save_message(
            "tool",
            f"{tool_name}: {result}"
        )


    def process_user_input(self, user_input):

        # Save the user's message
        self.add_user_message(user_input)

        # Ask the model
        assistant_response = self.ask_model()

        if assistant_response is None:
            return

        # Check for a tool call
        tool_request = self.parse_tool_call(
            assistant_response
        )

        # No tool? Just answer.
        if tool_request is None:

            print(f"NEXUS: {assistant_response}\n")

            self.add_assistant_message(
                assistant_response
            )

            return

        # Execute tool
        tool_name, argument = tool_request

        tool_result = self.execute_tool(
            tool_name,
            argument
        )

        print(f"[Tool Result: {tool_result}]")

        self.add_tool_result(
            tool_name,
            tool_result
        )

        # Ask the model again
        final_answer = self.ask_model()

        if final_answer is None:
            return

        print(f"NEXUS: {final_answer}\n")

        self.add_assistant_message(
            final_answer
        )

    