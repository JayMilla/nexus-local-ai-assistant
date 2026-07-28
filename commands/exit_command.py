class ExitCommand:

    def matches(self, user_input):
        return user_input.lower() in (
            "exit",
            "quit"
        )

    def execute(self, user_input, conversation, memory):

        print("Goodbye!")

        memory.close()

        raise SystemExit