from parser import ParseError, Parser, Token, TokenType

import pytest


class TestParser:
    """Test cases for the Parser class."""

    def test_parse_simple_assignment(self):
        """Test parsing simple assignment with number."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "42"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "x", ("number", 42))

    def test_parse_variable_assignment(self):
        """Test parsing assignment with variable."""
        tokens = [
            Token(TokenType.VAR, "y"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.VAR, "x"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "y", ("variable", "x"))

    def test_parse_addition_assignment(self):
        """Test parsing assignment with addition expression."""
        tokens = [
            Token(TokenType.VAR, "result"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == (
            "assignment",
            "result",
            ("binary_op", "+", ("number", 1), ("number", 2)),
        )

    def test_parse_multiplication_precedence(self):
        """Test that multiplication has higher precedence than addition."""
        tokens = [
            Token(TokenType.VAR, "result"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.PRED2, "*"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "result",
            (
                "binary_op",
                "+",
                ("number", 1),
                ("binary_op", "*", ("number", 2), ("number", 3)),
            ),
        )
        assert ast == expected

    def test_parse_left_associativity(self):
        """Test left associativity of operators."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "x",
            (
                "binary_op",
                "+",
                ("binary_op", "+", ("number", 1), ("number", 2)),
                ("number", 3),
            ),
        )
        assert ast == expected

    def test_parse_parentheses_override_precedence(self):
        tokens = [
            Token(TokenType.VAR, "result"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.PRED3, "("),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.PRED2, "*"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "result",
            (
                "binary_op",
                "*",
                ("binary_op", "+", ("number", 1), ("number", 2)),
                ("number", 3),
            ),
        )
        assert ast == expected

    def test_parse_nested_parentheses(self):
        """Test parsing nested parentheses."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.PRED3, "("),
            Token(TokenType.PRED3, "("),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "x",
            (
                "binary_op",
                "+",
                ("number", 1),
                ("number", 2),
            ),
        )
        assert ast == expected

    def test_parse_complex_assignment(self):
        """Test parsing complex assignment expressions."""
        tokens = [
            Token(TokenType.VAR, "result"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.VAR, "a"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.VAR, "b"),
            Token(TokenType.PRED2, "*"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "result",
            (
                "binary_op",
                "+",
                ("variable", "a"),
                ("binary_op", "*", ("variable", "b"), ("number", 2)),
            ),
        )
        assert ast == expected

    @pytest.mark.parametrize(
        "number_str,expected_value",
        [("42", 42), ("3.14", 3.14), ("0", 0), (".5", 0.5), ("100", 100)],
    )
    def test_parse_number_types(self, number_str, expected_value):
        """Test parsing different number formats."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, number_str),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "x", ("number", expected_value))

    @pytest.mark.parametrize(
        "token_type,operator",
        [
            (TokenType.PRED1, "+"),
            (TokenType.PRED1, "-"),
            (TokenType.PRED2, "*"),
            (TokenType.PRED2, "/"),
            (TokenType.PRED2, "%"),
        ],
    )
    def test_parse_all_operators(self, token_type, operator):
        """Test parsing all supported operators."""
        tokens = [
            Token(TokenType.VAR, "result"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(token_type, operator),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "result",
            ("binary_op", operator, ("number", 1), ("number", 2)),
        )
        assert ast == expected

    @pytest.mark.parametrize(
        "var_name",
        [
            "x",
            "variable",
            "var123",
            "longVariableName",
            "a1b2c3",
        ],
    )
    def test_parse_variable_names(self, var_name):
        """Test parsing various valid variable names."""
        tokens = [
            Token(TokenType.VAR, var_name),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", var_name, ("number", 5))

    def test_parse_empty_input(self):
        """Test that empty input returns None."""
        tokens = [Token(TokenType.EOF, None)]
        parser = Parser(tokens)
        result = parser.parse()
        assert result is None


class TestParserPrecedenceAndAssociativity:
    """Test cases for operator precedence and associativity."""

    @pytest.mark.parametrize(
        "expression_tokens,expected_ast",
        [
            # Test: 1 + 2 * 3 should be 1 + (2 * 3)
            (
                [
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED2, "*"),
                    Token(TokenType.NUMBER, "3"),
                ],
                (
                    "binary_op",
                    "+",
                    ("number", 1),
                    ("binary_op", "*", ("number", 2), ("number", 3)),
                ),
            ),
            # Test: 1 * 2 + 3 should be (1 * 2) + 3
            (
                [
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED2, "*"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "3"),
                ],
                (
                    "binary_op",
                    "+",
                    ("binary_op", "*", ("number", 1), ("number", 2)),
                    ("number", 3),
                ),
            ),
            # Test: 1 - 2 - 3 should be (1 - 2) - 3 (left associative)
            (
                [
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED1, "-"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED1, "-"),
                    Token(TokenType.NUMBER, "3"),
                ],
                (
                    "binary_op",
                    "-",
                    ("binary_op", "-", ("number", 1), ("number", 2)),
                    ("number", 3),
                ),
            ),
            # Test: 1 / 2 / 3 should be (1 / 2) / 3 (left associative)
            (
                [
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED2, "/"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED2, "/"),
                    Token(TokenType.NUMBER, "3"),
                ],
                (
                    "binary_op",
                    "/",
                    ("binary_op", "/", ("number", 1), ("number", 2)),
                    ("number", 3),
                ),
            ),
        ],
    )
    def test_operator_precedence_and_associativity(
        self, expression_tokens, expected_ast
    ):
        """Test operator precedence and associativity rules."""
        tokens = (
            [
                Token(TokenType.VAR, "result"),
                Token(TokenType.ASSIGNMENT, "="),
            ]
            + expression_tokens
            + [Token(TokenType.EOF, None)]
        )

        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "result", expected_ast)

    @pytest.mark.parametrize(
        "expression_tokens,expected_ast",
        [
            # Test: (1 + 2) * 3
            (
                [
                    Token(TokenType.PRED3, "("),
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED3, ")"),
                    Token(TokenType.PRED2, "*"),
                    Token(TokenType.NUMBER, "3"),
                ],
                (
                    "binary_op",
                    "*",
                    ("binary_op", "+", ("number", 1), ("number", 2)),
                    ("number", 3),
                ),
            ),
            # Test: 1 * (2 + 3)
            (
                [
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED2, "*"),
                    Token(TokenType.PRED3, "("),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "3"),
                    Token(TokenType.PRED3, ")"),
                ],
                (
                    "binary_op",
                    "*",
                    ("number", 1),
                    ("binary_op", "+", ("number", 2), ("number", 3)),
                ),
            ),
            # Test: (1 + 2) * (3 + 4)
            (
                [
                    Token(TokenType.PRED3, "("),
                    Token(TokenType.NUMBER, "1"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "2"),
                    Token(TokenType.PRED3, ")"),
                    Token(TokenType.PRED2, "*"),
                    Token(TokenType.PRED3, "("),
                    Token(TokenType.NUMBER, "3"),
                    Token(TokenType.PRED1, "+"),
                    Token(TokenType.NUMBER, "4"),
                    Token(TokenType.PRED3, ")"),
                ],
                (
                    "binary_op",
                    "*",
                    ("binary_op", "+", ("number", 1), ("number", 2)),
                    ("binary_op", "+", ("number", 3), ("number", 4)),
                ),
            ),
        ],
    )
    def test_parentheses_precedence_override(
        self,
        expression_tokens,
        expected_ast,
    ):
        """Test that parentheses correctly override operator precedence."""
        tokens = (
            [
                Token(TokenType.VAR, "result"),
                Token(TokenType.ASSIGNMENT, "="),
            ]
            + expression_tokens
            + [Token(TokenType.EOF, None)]
        )

        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "result", expected_ast)


class TestParserErrors:
    """Test cases for parser error handling."""

    def test_missing_variable_name_error(self):
        """Test error when statement doesn't start with variable name."""
        tokens = [
            Token(TokenType.NUMBER, "42"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        with pytest.raises(ParseError, match="Expected variable name"):
            parser.parse()

    def test_missing_assignment_operator_error(self):
        """Test error when assignment operator is missing."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        with pytest.raises(
            ParseError,
            match="Expected '=' after variable name",
        ):
            parser.parse()

    def test_missing_closing_parenthesis_error(self):
        """Test error on missing closing parenthesis."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.PRED3, "("),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        with pytest.raises(ParseError, match="Expected closing parenthesis"):
            parser.parse()

    def test_unexpected_token_in_expression_error(self):
        """Test error on unexpected token in expression."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        with pytest.raises(ParseError, match="Unexpected token"):
            parser.parse()

    def test_unexpected_token_after_statement(self):
        """
        Test error when there are extra tokens after a complete statement.
        """
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED3, ")"),  # Extra closing paren
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        with pytest.raises(
            ParseError,
            match="Unexpected token after statement",
        ):
            parser.parse()

    def test_missing_operand_error(self):
        """Test error when operand is missing."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.EOF, None),  # Missing right operand
        ]
        parser = Parser(tokens)
        with pytest.raises(ParseError):
            parser.parse()

    @pytest.mark.parametrize(
        "invalid_tokens",
        [
            # Missing expression after assignment
            [
                Token(TokenType.VAR, "x"),
                Token(TokenType.ASSIGNMENT, "="),
                Token(TokenType.EOF, None),
            ],
            # Missing right operand
            [
                Token(TokenType.VAR, "x"),
                Token(TokenType.ASSIGNMENT, "="),
                Token(TokenType.NUMBER, "1"),
                Token(TokenType.PRED1, "+"),
                Token(TokenType.EOF, None),
            ],
            # Missing left operand (operator at start)
            [
                Token(TokenType.VAR, "x"),
                Token(TokenType.ASSIGNMENT, "="),
                Token(TokenType.PRED2, "*"),
                Token(TokenType.NUMBER, "1"),
                Token(TokenType.EOF, None),
            ],
            # Unmatched opening parenthesis
            [
                Token(TokenType.VAR, "x"),
                Token(TokenType.ASSIGNMENT, "="),
                Token(TokenType.PRED3, "("),
                Token(TokenType.NUMBER, "1"),
                Token(TokenType.EOF, None),
            ],
            # Empty parentheses
            [
                Token(TokenType.VAR, "x"),
                Token(TokenType.ASSIGNMENT, "="),
                Token(TokenType.PRED3, "("),
                Token(TokenType.PRED3, ")"),
                Token(TokenType.EOF, None),
            ],
        ],
    )
    def test_various_syntax_errors(self, invalid_tokens):
        """Test various syntax error scenarios."""
        parser = Parser(invalid_tokens)
        with pytest.raises(ParseError):
            parser.parse()


class TestParserEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_deeply_nested_parentheses(self):
        """Test deeply nested parentheses."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.PRED3, "("),
            Token(TokenType.PRED3, "("),
            Token(TokenType.PRED3, "("),
            Token(TokenType.NUMBER, "1"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.PRED3, ")"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected = (
            "assignment",
            "x",
            (
                "binary_op",
                "+",
                ("number", 1),
                ("number", 2),
            ),
        )
        assert ast == expected

    def test_complex_mixed_operators(self):
        """Test complex expression with mixed operators."""
        # x = a + b * c - d / e % f
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.VAR, "a"),
            Token(TokenType.PRED1, "+"),
            Token(TokenType.VAR, "b"),
            Token(TokenType.PRED2, "*"),
            Token(TokenType.VAR, "c"),
            Token(TokenType.PRED1, "-"),
            Token(TokenType.VAR, "d"),
            Token(TokenType.PRED2, "/"),
            Token(TokenType.VAR, "e"),
            Token(TokenType.PRED2, "%"),
            Token(TokenType.VAR, "f"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        # Expected: a + (b * c) - ((d / e) % f)
        expected = (
            "assignment",
            "x",
            (
                "binary_op",
                "-",
                (
                    "binary_op",
                    "+",
                    ("variable", "a"),
                    ("binary_op", "*", ("variable", "b"), ("variable", "c")),
                ),
                (
                    "binary_op",
                    "%",
                    ("binary_op", "/", ("variable", "d"), ("variable", "e")),
                    ("variable", "f"),
                ),
            ),
        )
        assert ast == expected

    def test_single_variable_assignment(self):
        """Test assignment of single variable to another."""
        tokens = [
            Token(TokenType.VAR, "y"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.VAR, "x"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "y", ("variable", "x"))

    def test_single_number_assignment(self):
        """Test assignment of single number."""
        tokens = [
            Token(TokenType.VAR, "x"),
            Token(TokenType.ASSIGNMENT, "="),
            Token(TokenType.NUMBER, "42"),
            Token(TokenType.EOF, None),
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast == ("assignment", "x", ("number", 42))
