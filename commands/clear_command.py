import os


class ClearCommand:

    def matches(self, user_input):
        return user_input.lower() == "clear"

    def execute(self, user_input, conversation, memory):

        os.system("cls")

        return True