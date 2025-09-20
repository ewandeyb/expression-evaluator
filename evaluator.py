from enum import Enum


class NodeType(Enum):
    BINARY_OP = "binary_op"
    ASSIGNMENT = "assignment"
    NUMBER = "number"
    VARIABLE = "variable"


class Evaluator:
    """
    To evaluate an AST, first call `.evaluate` to populate the stack and then
    you can either:

    - `.execute()` to add the value to the symbol_table.
    - call `str()` to return a string representation of the stack.
    """

    def __init__(self, ast, symbol_table) -> None:
        self.ast = ast
        self.stack = []
        self.symbol_table = symbol_table

    def _walk(self, node):
        node_type = node[0]

        if node_type == NodeType.ASSIGNMENT:
            _, identifier, expr = node
            self.stack.append(identifier)
            self._walk(expr)
            self.stack.append("=")

        elif node_type == NodeType.BINARY_OP:
            _, operator, left, right = node
            self._walk(left)
            self._walk(right)
            self.stack.append(operator)

        elif node_type == NodeType.NUMBER:
            _, value = node
            self.stack.append(value)

        elif node_type == NodeType.VARIABLE:
            _, name = node
            self.stack.append(name)

        else:
            raise ValueError(f"Unknown AST node: {node_type}")

    def evaluate(self):
        self._walk(self.ast)

    def execute(self):
        pass

    def __str__(self) -> str:
        pass
