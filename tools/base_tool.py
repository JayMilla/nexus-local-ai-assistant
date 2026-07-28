class BaseTool:
    """
    Base class for every tool.
    """

    name = ""

    description = ""

    def execute(self, argument):
        raise NotImplementedError