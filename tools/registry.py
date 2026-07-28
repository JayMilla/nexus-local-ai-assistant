class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, tool):
        self.tools[tool.name.lower()] = tool

    def execute(self, tool_name, argument):
        tool = self.tools.get(tool_name.lower().strip())
        if tool is None:
            return f"Unknown tool: {tool_name}"
        return tool.execute(argument)

    def list_tools(self):

        return list(self.tools.keys())