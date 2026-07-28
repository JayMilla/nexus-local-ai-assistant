import ast
import operator
import re
from file_tools import FileReaderTool, FileListerTool, FileSearchTool


class ToolRegistry:
    def __init__(self, files_root="workspace"):
        self.calculator = Calculator()
        self.file_reader = FileReaderTool(files_root)
        self.file_lister = FileListerTool(files_root)
        self.file_search = FileSearchTool(files_root)

    def execute(self, tool_name, argument):
        if not tool_name:
            return "Invalid tool name."

        if not argument:
            return "Tool argument was empty."

        tool_name = tool_name.lower().strip()

        if tool_name == "calculator":
            return self.calculator.calculate(argument)

        if tool_name in ("read_file", "file_read"):
            return self.file_reader.read_file(argument)

        if tool_name in ("list_files", "list_dir", "ls"):
            return self.file_lister.list_files(argument)

        if tool_name in ("search_file", "file_search", "grep"):
            return self.file_search.search_file(argument)

        return f"Unknown tool: {tool_name}"



class Calculator:
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

    def calculate(self, expression):
        try:
            if not expression:
                return "Invalid mathematical expression."

            expression = expression.strip()
            expression = expression.replace("×", "*")
            expression = expression.replace("x", "*")
            expression = expression.replace("X", "*")
            expression = expression.rstrip("?.!,;:")
            expression = expression.replace(" ", "")

            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)

            return result

        except Exception:
            return "Invalid mathematical expression."

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant.")

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -self._evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return self._evaluate(node.operand)

            raise ValueError("Unsupported unary operator.")

        if isinstance(node, ast.BinOp):
            operator_function = self.operators.get(type(node.op))

            if operator_function is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operator_function(left, right)

        raise ValueError("Unsupported expression.")