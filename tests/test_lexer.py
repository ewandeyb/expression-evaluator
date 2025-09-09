import pytest
from lexer import Lexer, Token, TokenType

@pytest.mark.parametrize("input_string, expected_tokens", [
    ("1 + 2", [
        Token(TokenType.INTEGER, "1"),
        Token(TokenType.PRED1, "+"),
        Token(TokenType.INTEGER, "2"),
        Token(TokenType.EOF, "")
    ]),
    ("var_name", [
        Token(TokenType.VAR, "var_name"),
        Token(TokenType.EOF, "")
    ]),
    ("3 * (4 - 5)", [
        Token(TokenType.INTEGER, "3"),
        Token(TokenType.PRED2, "*"),
        Token(TokenType.PRED3, "("),
        Token(TokenType.INTEGER, "4"),
        Token(TokenType.PRED1, "-"),
        Token(TokenType.INTEGER, "5"),
        Token(TokenType.PRED3, ")"),
        Token(TokenType.EOF, "")
    ])
])
def test_lexer(input_string, expected_tokens):
    lexer = Lexer(input_string)
    tokens = lexer.tokenize()
    assert tokens == expected_tokens
