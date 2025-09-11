import pytest

from lexer import Lexer, Token, TokenType


@pytest.mark.parametrize(
    "input_string, expected_tokens",
    [
        (
            "1 + 2",
            [
                Token(TokenType.INTEGER, "1"),
                Token(TokenType.PRED1, "+"),
                Token(TokenType.INTEGER, "2"),
                Token(TokenType.EOF, None),
            ],
        ),
        (
            "var_name",
            [
                Token(TokenType.VAR, "var_name"),
                Token(TokenType.EOF, None),
            ],
        ),
        (
            "var_name = 3",
            [
                Token(TokenType.VAR, "var_name"),
                Token(TokenType.ASSIGNMENT, None),
                Token(TokenType.INTEGER, "3"),
                Token(TokenType.EOF, None),
            ],
        ),
        (
            "3 * (4 - 5)",
            [
                Token(TokenType.INTEGER, "3"),
                Token(TokenType.PRED2, "*"),
                Token(TokenType.PRED3, "("),
                Token(TokenType.INTEGER, "4"),
                Token(TokenType.PRED1, "-"),
                Token(TokenType.INTEGER, "5"),
                Token(TokenType.PRED3, ")"),
                Token(TokenType.EOF, None),
            ],
        ),
    ],
)
def test_lexer(input_string, expected_tokens):
    lexer = Lexer(input_string)
    tokens = lexer.tokenize()
    assert tokens == expected_tokens


def test_lexer_invalid_character():
    lexer = Lexer("?")

    with pytest.raises(ValueError) as excinfo:
        lexer.tokenize()
    assert "Invalid character: ?" in str(excinfo.value)
