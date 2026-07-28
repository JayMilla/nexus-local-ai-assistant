class Conversation:
    def __init__(self, system_prompt, max_messages=20, max_memories=8):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self.max_memories = max_memories
        self.messages = []
        self.memories = []

    def load_memories(self, memories):
        self.memories = []

        for memory in memories:
            if isinstance(memory, tuple) and memory:
                self.memories.append(str(memory[0]))
            elif isinstance(memory, dict) and memory.get("memory"):
                self.memories.append(str(memory["memory"]))
            elif memory:
                self.memories.append(str(memory))

    def load_messages(self, messages):
        self.messages = []

        for message in messages:
            if isinstance(message, tuple) and len(message) >= 2:
                role, content = message[0], message[1]
            elif isinstance(message, dict):
                role = message.get("role")
                content = message.get("content")
            else:
                continue

            if role is not None and content is not None:
                self.messages.append(
                    {
                        "role": str(role),
                        "content": str(content)
                    }
                )

    def add_message(self, role, content):
        if role is None or content is None:
            return

        self.messages.append(
            {
                "role": str(role),
                "content": str(content)
            }
        )

    def add_user_message(self, message):
        self.add_message("user", message)

    def add_assistant_message(self, message):
        self.add_message("assistant", message)

    def add_tool_message(self, tool_name, result):
        self.add_message(
            "tool",
            f"{tool_name} returned: {result}"
        )

    def clear_messages(self):
        self.messages = []

    def clear_memories(self):
        self.memories = []

    def build_prompt(self):
        prompt = self.system_prompt.strip() + "\n\n"

        if self.memories:
            prompt += "Important information about the user:\n"
            for memory in self.memories[-self.max_memories:]:
                prompt += f"- {memory}\n"
            prompt += "\n"

        prompt += "Conversation:\n"

        recent_messages = self.messages[-self.max_messages:]
        for message in recent_messages:
            role = message["role"].strip().lower()
            content = message["content"].strip()
            prompt += f"{role}: {content}\n"

        prompt += "assistant:"
        return prompt