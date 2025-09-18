from typing import List

from lexer import Token, TokenType


class ParseError(Exception):
    """Exception raised for parsing errors."""

    pass


class Parser:
    """
    Recursive descent parser for the grammar:

    program    → statement*
    statement  → IDENTIFIER '=' expression
    expression → term (( '+' | '-' ) term)*
    term       → factor (( '*' | '/' | '%' ) factor)*
    factor     → NUMBER | IDENTIFIER | '(' expression ')'

    Note: All statements are assignment statements.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token:
        """Return the current token without consuming it."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return Token(TokenType.EOF, None)

    def advance(self) -> Token:
        """Consume and return the current token."""
        token = self.peek()
        if self.current < len(self.tokens):
            self.current += 1
        return token

    def match(self, token_type: TokenType) -> bool:
        """Check if current token matches the given type."""
        return self.peek().type == token_type

    def consume(
        self,
        token_type: TokenType,
        message: str | None = None,
    ) -> Token:
        """Consume a token of the expected type or raise an error."""
        if self.match(token_type):
            return self.advance()

        current_token = self.peek()
        if message is None:
            message = f"Expected {token_type.value}, \
                        got {current_token.type.value}"

        raise ParseError(message)

    def parse_statement(self):
        """
        statement → IDENTIFIER '=' expression
        Returns: ('assignment', identifier, expression)
        """
        # Must start with an identifier
        if not self.match(TokenType.VAR):
            current_token = self.peek()
            raise ParseError(
                f"Expected variable name,\
                              got {current_token.type.value}"
            )

        identifier = self.advance()

        # Must be followed by assignment operator
        if not self.match(TokenType.ASSIGNMENT):
            current_token = self.peek()
            raise ParseError(
                f"Expected '=' after variable name, \
                    got {current_token.type.value}"
            )

        self.advance()  # consume '='

        expr = self.parse_expression()

        return ("assignment", identifier.value, expr)

    def parse_expression(self):
        """
        expression → term (( '+' | '-' ) term)*
        Returns: ('binary_op', operator, left, right) or term
        """
        left = self.parse_term()

        while self.match(TokenType.PRED1):  # + or -
            operator = self.advance()
            right = self.parse_term()
            left = ("binary_op", operator.value, left, right)

        return left

    def parse_term(self):
        """
        term → factor (( '*' | '/' | '%' ) factor)*
        Returns: ('binary_op', operator, left, right) or factor
        """
        left = self.parse_factor()

        while self.match(TokenType.PRED2):  # *, /, %
            operator = self.advance()
            right = self.parse_factor()
            left = ("binary_op", operator.value, left, right)

        return left

    def parse_factor(self):
        """
        factor → NUMBER | IDENTIFIER | '(' expression ')'
        Returns: ('number', value) | ('variable', name) | expression
        """
        if self.match(TokenType.NUMBER):
            token = self.advance()
            # Convert to appropriate numeric type
            if "." in token.value:
                value = float(token.value)
            else:
                value = int(token.value)
            return ("number", value)

        elif self.match(TokenType.VAR):
            token = self.advance()
            return ("variable", token.value)

        elif self.match(TokenType.PRED3) and self.peek().value == "(":
            self.advance()  # consume '('
            expr = self.parse_expression()

            # Consume closing paren
            if not (self.match(TokenType.PRED3) and self.peek().value == ")"):
                raise ParseError("Expected closing parenthesis ')'")
            self.advance()

            return expr

        else:
            current_token = self.peek()
            raise ParseError(
                f"Unexpected token: {current_token.type.value} \
                    with value '{current_token.value}'"
            )

    def parse(self):
        """
        Parse a single statement and ensure we consume all tokens except EOF.
        Returns the parsed AST or None for empty input.
        """
        if self.match(TokenType.EOF):
            return None  # Empty input is valid

        ast = self.parse_statement()

        # Ensure we've consumed everything except EOF
        if not self.match(TokenType.EOF):
            current_token = self.peek()
            raise ParseError(
                f"Unexpected token after statement: {current_token.type.value}"
            )

        return ast
