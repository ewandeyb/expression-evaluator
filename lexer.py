import re
from dataclasses import dataclass
from enum import Enum
from typing import Self


class TokenType(Enum):
    INTEGER = "INTEGER"
    VAR = "VAR"
    PRED1 = "PRED1"
    PRED2 = "PRED2"
    PRED3 = "PRED3"
    ASSIGNMENT = "ASSIGNMENT"


@dataclass
class Token:
    type: TokenType
    value: str | None


class Lexer:
    NUMBER = r"\d+\.?\d*"
    VARIABLE = r"[a-zA-Z]+[0-9a-zA-Z]*"
    OPERATOR = r"[=+-/*%]"
    PAREN = r"[()]"

    def __init__(self, text: str):
        self.text = text
        self.token_list = None

    @classmethod
    def helper(cls, token):
        if re.fullmatch(cls.NUMBER, token):
            return Token(TokenType.INTEGER, token)
        elif re.fullmatch(cls.VARIABLE, token):
            return Token(TokenType.VAR, token)
        elif re.fullmatch(cls.OPERATOR, token):
            if token in "+-":
                return Token(TokenType.PRED1, token)
            elif token in "*/%":
                return Token(TokenType.PRED2, token)
            else:
                return Token(TokenType.ASSIGNMENT, None)

        elif re.fullmatch(cls.PAREN, token):
            return Token(TokenType.PRED3, token)
        else:
            raise ValueError(f"Invalid character: {token}")

    def tokenize(self) -> Self:
        # Set valid definitions for different token types
        definitions = "|".join(
            [
                self.NUMBER,
                self.VARIABLE,
                self.OPERATOR,
                self.PAREN,
                r"\S",
            ]
        )
        pattern = re.compile(definitions)

        # Find all tokens in the input text
        tokens = re.findall(pattern, self.text)

        # Map tokens to their respective types
        self.token_list = (self.helper(token) for token in tokens)

        return self

    def next(self) -> Token:
        """
        Wrapper for advancing the generator.
        """
        return next(self.token_list)
