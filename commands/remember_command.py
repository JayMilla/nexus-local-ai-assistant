class RememberCommand:

    def matches(self, user_input):

        return user_input.lower().startswith(
            "/remember "
        )

    def execute(
        self,
        user_input,
        conversation,
        memory
    ):

        text = user_input[10:].strip()

        if not text:

            print("NEXUS: Nothing to remember.\n")

            return True

        memory.save_memory(text)

        conversation.memories.append(text)

        print("NEXUS: I'll remember that.\n")

        return True