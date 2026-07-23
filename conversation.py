class Conversation:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = []

    def add_user_message(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_assistant_message(self, message):
        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def build_prompt(self):
        prompt = self.system_prompt + "\n"

        for message in self.messages:
            prompt += f"{message['role']}: {message['content']}\n"

        prompt += "assistant:"

        return prompt