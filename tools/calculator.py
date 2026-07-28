from .base_tool import BaseTool

import ast
import operator


class CalculatorTool(BaseTool):

    name = "calculator"

    description = "Evaluate mathematical expressions."

    def __init__(self):

        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

    def execute(self, expression):

        try:

            if not expression:
                return "Invalid mathematical expression."

            expression = expression.strip()

            expression = expression.replace("×", "*")
            expression = expression.replace("x", "*")
            expression = expression.replace("X", "*")

            expression = expression.rstrip("?.!,;:")

            expression = expression.replace(" ", "")

            tree = ast.parse(
                expression,
                mode="eval"
            )

            return self._evaluate(tree.body)

        except Exception:

            return "Invalid mathematical expression."

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError()

        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):
                return -self._evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return self._evaluate(node.operand)

        if isinstance(node, ast.BinOp):

            func = self.operators.get(type(node.op))

            if func is None:
                raise ValueError()

            return func(
                self._evaluate(node.left),
                self._evaluate(node.right)
            )

        raise ValueError()