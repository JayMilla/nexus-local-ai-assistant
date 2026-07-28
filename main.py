import os
from config import MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT
from conversation import Conversation
from ollama_client import OllamaClient
from memory import Memory
from tools import ToolRegistry, ToolParser
from pathlib import Path
from commands.command_registry import CommandRegistry
from commands.exit_command import ExitCommand
from commands.clear_command import ClearCommand
from commands.remember_command import RememberCommand
from tools.registry import ToolRegistry

from tools.calculator import CalculatorTool

def main():
    Path("workspace").mkdir(exist_ok=True)
    
    conversation = Conversation(SYSTEM_PROMPT)

    memory = Memory()

    previous_messages = memory.load_messages(limit=30)
    conversation.load_messages(previous_messages)

    stored_memories = memory.load_memories(limit=8)
    conversation.load_memories(stored_memories)

    tool_registry = ToolRegistry()
    tool_parser = ToolParser()
    tool_registry.register(
        CalculatorTool()
    )

    tool_registry.register(
        FileReaderTool()
    )

    tool_registry.register(
        FileListerTool()
    )

    tool_registry.register(
        FileSearchTool()
    )


    command_registry = CommandRegistry()

    command_registry.register(
        ExitCommand()
    )

    command_registry.register(
        ClearCommand()
    )

    command_registry.register(
        RememberCommand()
    )

    ollama = OllamaClient(
        MODEL_NAME,
        OLLAMA_URL
    )

    print("NEXUS v0.1")
    print("Type 'exit' to quit.")
    print("Type 'clear' to clear the screen.\n")

    while True:
        user_input = input("You: ")

        handled = command_registry.execute(
            user_input,
            conversation,
            memory
        )

        if handled:
            continue

        conversation.add_user_message(user_input)
        memory.save_message("user", user_input)

        prompt = conversation.build_prompt()





        assistant_response = ollama.generate_response(prompt)

        if assistant_response is None:
            continue

        tool_request = tool_parser.parse(assistant_response)

        if tool_request is None:
            print(f"NEXUS: {assistant_response}\n")
            conversation.add_assistant_message(assistant_response)
            memory.save_message("assistant", assistant_response)
            continue

        tool_name, argument = tool_request

        # Save the tool request in conversation history before executing it.
        conversation.add_assistant_message(assistant_response)
        memory.save_message("assistant", assistant_response)

        tool_result = tool_registry.execute(tool_name, argument)

        print(f"[Tool Result: {tool_result}]")

        conversation.add_tool_message(tool_name, tool_result)
        memory.save_message("tool", f"{tool_name}: {tool_result}")

        prompt = conversation.build_prompt()
        final_answer = ollama.generate_response(prompt)

        if final_answer is None:
            continue

        print(f"NEXUS: {final_answer}\n")
        conversation.add_assistant_message(final_answer)
        memory.save_message("assistant", final_answer)
   

if __name__ == "__main__":
    main()