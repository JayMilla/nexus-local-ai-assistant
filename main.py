import os
from config import MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT
from conversation import Conversation
from ollama_client import OllamaClient


def main():
    conversation = Conversation(SYSTEM_PROMPT)

    ollama = OllamaClient(
        MODEL_NAME,
        OLLAMA_URL
    )

    print("NEXUS v0.1")
    print("Type 'exit' to quit.")
    print("Type 'clear' to clear the screen.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            os.system("cls")
            continue

        conversation.add_user_message(user_input)

        prompt = conversation.build_prompt()

        print("NEXUS: ", end="", flush=True)

        assistant_response = ollama.generate_response(prompt)

        if assistant_response is not None:
            conversation.add_assistant_message(assistant_response)

        print("\n")


if __name__ == "__main__":
    main()