from nexus_app import NexusApp

from commands.exit_command import ExitCommand
from commands.clear_command import ClearCommand
from commands.remember_command import RememberCommand

from tools.calculator import CalculatorTool

def main():
    
    app = NexusApp()

    app.initialize()
   
    app.register_command(ExitCommand())
    app.register_command(ClearCommand())
    app.register_command(RememberCommand())

    app.register_tool(CalculatorTool())



    print("NEXUS v0.1")
    print("Type 'exit' to quit.")
    print("Type 'clear' to clear the screen.\n")

    while True:
        user_input = input("You: ")

        handled = app.command_registry.execute(
            user_input,
            app.conversation,
            app.memory
        )

        if handled:
            continue

        app.process_user_input(user_input)
   

if __name__ == "__main__":
    main()