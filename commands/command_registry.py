class Command:
    """
    Base class for every command.
    """

    name = ""

    def matches(self, user_input):
        raise NotImplementedError

    def execute(self, user_input, conversation, memory):
        raise NotImplementedError


class CommandRegistry:
    def __init__(self):
        self.commands = []

    def register(self, command):
        self.commands.append(command)

    def execute(self, user_input, conversation, memory):
        for command in self.commands:

            if command.matches(user_input):

                return command.execute(
                    user_input,
                    conversation,
                    memory
                )

        return False