class ToolParser:
    def parse(self, response):
        if not response:
            return None

        response = response.strip()

        if not response:
            return None

        pattern = (
            r"TOOL_CALL:\s*"
            r"([A-Za-z_][A-Za-z0-9_]*)"
            r"\s*\n"
            r"(.+)"
        )

        match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)

        if not match:
            return None

        tool_name = match.group(1).strip().lower()
        argument = match.group(2).strip()
        argument = argument.splitlines()[0].strip()
        argument = argument.rstrip("?.!,;:")

        if not tool_name or not argument:
            return None

        return tool_name, argument
