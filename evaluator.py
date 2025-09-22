from enum import Enum


class NodeType(Enum):
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
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
        self.postfix = []
        self.symbol_table = symbol_table

    def _walk(self, node):
        node_type = node[0]

        if node_type == NodeType.ASSIGNMENT:
            _, identifier, expr = node
            self.postfix.append(identifier)
            self._walk(expr)
            self.postfix.append("=")

        elif node_type == NodeType.BINARY_OP:
            _, operator, left, right = node
            self._walk(left)
            self._walk(right)
            self.postfix.append(operator)

        elif node_type == NodeType.UNARY_OP:
            _, operator, operand = node
            self._walk(operand)
            self.postfix.append(f"u{operator}")  # prefix with 'u' for unary

        elif node_type == NodeType.NUMBER:
            _, value = node
            self.postfix.append(value)

        elif node_type == NodeType.VARIABLE:
            _, name = node
            self.postfix.append(name)

        else:
            raise ValueError(f"Unknown AST node: {node_type}")

    def evaluate(self):
        self._walk(self.ast)

    def execute(self):
        """
        Assigns the expression value to a variable in the symbol table.

        Returns the name of the variable assigned to.
        """

        var_name = self.postfix[0]

        stack = []

        # ignore first and last symbol
        for i in range(1, len(self.postfix) - 1):
            node = self.postfix[i]

            if type(node) in (int, float):
                stack.append(node)

            elif isinstance(node, str) and node.startswith('u'):
                # Handle unary operations (e.g., 'u-' for unary minus)
                operator = node[1:]  # Remove 'u' prefix
                operand = stack.pop()
                if operator == '-':
                    stack.append(-operand)
                elif operator == '+':
                    stack.append(operand)
                else:
                    raise ValueError(f"Unknown unary operator: {operator}")

            elif node not in "+/*%-":
                if node not in self.symbol_table:
                    raise NameError(f"Variable `{node}` is not defined.")

                stack.append(self.symbol_table[node])

            else:
                b, a = stack.pop(), stack.pop()
                stack.append(eval(f"{a}{node}{b}"))

        self.symbol_table[var_name] = stack[0]
        return var_name

    def __str__(self) -> str:
        return " ".join(str(e) for e in self.postfix)
